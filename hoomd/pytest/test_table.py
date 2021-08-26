from io import StringIO
from math import isclose
import pytest

from hoomd.conftest import operation_pickling_check
import hoomd
import hoomd.write

try:
    from mpi4py import MPI
    skip_mpi = False
except ImportError:
    skip_mpi = True

skip_mpi = pytest.mark.skipif(skip_mpi, reason="MPI4py is not importable.")


class Identity:

    def __init__(self, x):
        self.x = x

    def __call__(self):
        return self.x

    def __eq__(self, other):
        return self.x == other.x


@pytest.fixture
def logger():
    logger = hoomd.logging.Logger(categories=['scalar'])
    logger[('dummy', 'loggable', 'int')] = (Identity(42000000), 'scalar')
    logger[('dummy', 'loggable', 'float')] = (Identity(3.1415), 'scalar')
    logger[('dummy', 'loggable', 'string')] = (Identity("foobarbaz"), 'string')
    return logger


@pytest.fixture
def expected_values():
    return {
        'dummy.loggable.int': 42000000,
        'dummy.loggable.float': 3.1415,
        'dummy.loggable.string': "foobarbaz"
    }


def test_invalid_attrs(logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output)
    with pytest.raises(AttributeError):
        table_writer.action
    with pytest.raises(AttributeError):
        table_writer.detach
    with pytest.raises(AttributeError):
        table_writer.attach


@pytest.mark.serial
def test_header_generation(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output)
    table_writer._comm = device.communicator
    for i in range(10):
        table_writer.write()
    output_str = output.getvalue()
    lines = output_str.split('\n')
    headers = lines[0].split()
    expected_headers = [
        'dummy.loggable.int', 'dummy.loggable.float', 'dummy.loggable.string'
    ]
    assert all(hdr in headers for hdr in expected_headers)
    for i in range(1, 10):
        values = lines[i].split()
        assert not any(v in expected_headers for v in values)
    table_writer.logger[('new', 'quantity')] = (lambda: 53, 'scalar')
    table_writer.write()
    output_str = output.getvalue()
    lines = output_str.split('\n')
    headers = lines[-3].split()
    expected_headers.append('new.quantity')
    assert all(hdr in headers for hdr in expected_headers)


@pytest.mark.serial
def test_values(device, logger, expected_values):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output)
    table_writer._comm = device.communicator
    for i in range(10):
        table_writer.write()
    lines = output.getvalue().split('\n')
    headers = lines[0].split()

    def test_equality(expected, given):
        """Used to test the accuracy and ordering of Table rows."""
        type_ = expected.__class__
        try:
            if issubclass(type_, (int, float)):
                # the float conversion is necessary for scientific notation
                # conversion to int
                return isclose(expected, type_(float(given)))
            else:
                return expected == type_(given)
        except Exception:
            return False

    for row in lines[1:]:
        values = row.split()
        assert all(
            test_equality(expected_values[hdr], v)
            for hdr, v in zip(headers, values))


@skip_mpi
def test_mpi_write_only(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output)
    table_writer._comm = device.communicator
    table_writer.write()

    comm = MPI.COMM_WORLD
    if comm.rank == 0:
        assert output.getvalue() != ''
    else:
        assert output.getvalue() == ''


@pytest.mark.serial
def test_header_attributes(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1,
                                     logger,
                                     output,
                                     header_sep='-',
                                     max_header_len=13)
    table_writer._comm = device.communicator
    table_writer.write()
    lines = output.getvalue().split('\n')
    headers = lines[0].split()
    expected_headers = ['loggable-int', 'loggable-float', 'string']
    assert all(hdr in headers for hdr in expected_headers)


@pytest.mark.serial
def test_delimiter(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output, delimiter=',')
    table_writer._comm = device.communicator
    table_writer.write()
    lines = output.getvalue().split('\n')
    assert all(len(row.split(',')) == 3 for row in lines[:-1])


@pytest.mark.serial
def test_max_precision(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1,
                                     logger,
                                     output,
                                     pretty=False,
                                     max_precision=5)
    table_writer._comm = device.communicator
    for i in range(10):
        table_writer.write()

    smaller_lines = output.getvalue().split('\n')

    output = StringIO("")
    table_writer = hoomd.write.Table(1,
                                     logger,
                                     output,
                                     pretty=False,
                                     max_precision=15)
    table_writer._comm = device.communicator
    for i in range(10):
        table_writer.write()

    longer_lines = output.getvalue().split('\n')

    for long_row, short_row in zip(longer_lines[1:-1], smaller_lines[1:-1]):
        assert all(
            len(long_) >= len(short)
            for long_, short in zip(long_row.split(), short_row.split()))

        assert any(
            len(long_) > len(short)
            for long_, short in zip(long_row.split(), short_row.split()))


def test_only_string_and_scalar_quantities(device):
    logger = hoomd.logging.Logger()
    output = StringIO("")
    with pytest.raises(ValueError):
        hoomd.write.Table(1, logger, output)
    logger = hoomd.logging.Logger(categories=['sequence'])
    with pytest.raises(ValueError):
        hoomd.write.Table(1, logger, output)


def test_eq(device, logger):
    output = StringIO("")
    table_writer = hoomd.write.Table(1, logger, output)
    table_writer_copy = hoomd.write.Table(1, logger, output)
    assert table_writer == table_writer_copy
    # Test that _comm doesn't matter for __eq__
    table_writer._comm = device.communicator
    assert table_writer == table_writer_copy
    # Test that trigger does matter
    table_writer_copy.trigger = 10
    assert table_writer != table_writer_copy
    # Test that output does matter
    new_output = StringIO("")
    table_writer_copy = hoomd.write.Table(1, logger, new_output)
    assert table_writer != table_writer_copy
    # Test that logger matters for equality
    table_writer_copy = hoomd.write.Table(1, hoomd.logging.Logger(["scalar"]),
                                          output)
    assert table_writer != table_writer_copy


def test_pickling(simulation_factory, two_particle_snapshot_factory, logger):
    sim = simulation_factory(two_particle_snapshot_factory())
    table = hoomd.write.Table(1, logger)
    operation_pickling_check(table, sim)
