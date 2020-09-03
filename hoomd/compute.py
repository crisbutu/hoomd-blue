# Copyright (c) 2009-2019 The Regents of the University of Michigan
# This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

# Maintainer: joaander / All Developers are free to add commands for new features

r""" Compute system properties

A compute calculates properties of the system on demand. Most computes are automatically generated by the command
that needs them (e.g. integrate.nvt creates a compute.thermo for temperature calculations). User-specified computes
can be used when more flexibility is needed. Properties calculated by specified computes (automatically, or by the
user) can be logged with analyze.log.
"""

from hoomd import _hoomd;
import hoomd;
import sys;

class _Thermo(_Compute):

    def __init__(self, group):
        self._group = group


class ThermoQuantites(_Thermo):
    R""" Compute thermodynamic properties of a group of particles.

    Args:
        group (``hoomd.group``): Group to compute thermodynamic properties for.

    :py:class:`hoomd.compute.thermo` acts on a given group of particles and calculates thermodynamic properties of those particles when
    requested. A default :py:class:`hoomd.compute.thermo` is created that operates on the group of all particles. Integration methods
    such as ``hoomd.md.integrate.nvt`` automatically create an internal :py:class:`hoomd.compute.thermo` for the group that they operate on.
    If thermodynamic properties are needed on additional groups, a user can specify additional :py:class:`hoomd.compute.thermo` commands.

    Whether they are automatically created or created by a user, all specified thermos are available for logging via
    the ``hoomd.analyze.log`` command. Each one provides a set of quantities for logging, suffixed with *_groupname*, so that
    values for different groups are differentiated in the log file. The default :py:class:`hoomd.compute.thermo` specified on the group
    of all particles has no suffix placed on its quantity names.

    The quantities provided are (where **groupname** is replaced with the name of the group):

    * **num_particles_groupname** - :math:`N` number of particles in the group
    * **ndof_groupname**  - :math:`N_{\mathrm{dof}}` number of degrees of freedom given to the group by
      integrate commands
    * **translational_ndof_groupname**  - :math:`N_{\mathrm{dof}}` number of translational degrees of
      freedom given to the group by integrate commands
    * **rotational_ndof_groupname**  - :math:`N_{\mathrm{dof}}` number of rotational degrees of
      freedom given to the group by integrate commands
    * **potential_energy_groupname** - :math:`U` potential energy that the group contributes to the entire
      system (in energy units)
    * **kinetic_energy_groupname** - :math:`K` total kinetic energy of all particles in the group (in energy units)
    * **translational_kinetic_energy_groupname** - :math:`K` translational kinetic energy of all particles in the group (in energy units)
    * **rotational_kinetic_energy_groupname** - :math:`K` rotational kinetic energy of all particles in the group (in energy units)
    * **temperature_groupname** - :math:`kT` instantaneous thermal energy of the group (in energy units). Calculated as

      .. math::

        kT = 2 \cdot \frac{K}{N_{\mathrm{dof}}}

    * **pressure_groupname** - :math:`P` instantaneous pressure of the group (in pressure units). Calculated as

      .. math::

          W = \frac{1}{2} \sum_{i}\sum_{j \ne i} \vec{F}_{ij} \cdot \vec{r_{ij}} + \sum_{k} \vec{F}_{k} \cdot \vec{r_{k}}

      where :math:`\vec{F}_{ij}` are pairwise forces between particles and :math:`\vec{F}_k` are forces due to explicit constraints, implicit rigid
      body constraints, external walls, and fields. In 2D simulations,
      :math:`P = (K + \frac{1}{2}\cdot W)/A` where :math:`A` is the area of the simulation box.
      of the simulation box.
    * **pressure_xx_groupname**, **pressure_xy_groupname**, **pressure_xz_groupname**,
      **pressure_yy_groupname**, **pressure_yz_groupname**, **pressure_zz_groupname** -
      instantaneous pressure tensor of the group (in pressure units).

      .. math::

          P_{ij} = \left[  \sum_{k\in[0..N)} m_k v_{k,i} v_{k,j} +
                           \sum_{k\in[0..N)} \sum_{l > k} \frac{1}{2} \left(\vec{r}_{kl,i} \vec{F}_{kl,j} + \vec{r}_{kl,j} \vec{F}_{kl, i} \right) \right]/V

    See Also:
        ``hoomd.analyze.log``.

    Examples::

        g = group.type(name='typeA', type='A')
        compute.thermo(group=g)
    """

    def __init__(self, group):
        super().__init__(group)

    def _attach(self):
        self._cpp_obj = _hoomd.ComputeThermo(
            self._simulation.state._cpp_sys_def,
            self._group,
            "")
        super()._attach()

    @log
    def temperature(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getTemperature()
        else:
            return None

    @log
    def pressure(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressure()
        else:
            return None

    @log
    def pressureXX(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureXX()
        else:
            return None

    @log
    def pressureXY(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureXY()
        else:
            return None

    @log
    def pressureXZ(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureXZ()
        else:
            return None

    @log
    def pressureYY(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureYY()
        else:
            return None

    @log
    def pressureYZ(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureYZ()
        else:
            return None

    @log
    def pressureZZ(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPressureZZ()
        else:
            return None

    @log
    def kineticEnergy(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getKineticEnergy()
        else:
            return None

    @log
    def translationalKineticEnergy(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getTranslationalKineticEnergy()
        else:
            return None

    @log
    def rotationalKineticEnergy(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getRotationalKineticEnergy()
        else:
            return None

    @log
    def potentialEnergy(self):
        if self._attached:
            self._cpp_obj.compute(self._simulation.timestep)
            return self._cpp_obj.getPotentialEnergy()
        else:
            return None

    @log
    def NDOF(self):
        if self._attached:
            return self._cpp_obj.getNDOF()
        else:
            return None

    @log
    def translationalDOF(self):
        if self._attached:
            return self._cpp_obj.getTranslationalDOF()
        else:
            return None

    @log
    def rotationalDOF(self):
        if self._attached:
            return self._cpp_obj.getRotationalDOF()
        else:
            return None

    @log
    def numParticles(self):
        if self._attached:
            return self._cpp_obj.getNumParticles()
        else:
            return None

class thermoHMA(_compute):
    R""" Compute HMA thermodynamic properties of a group of particles.

    Args:
        group (``hoomd.group``): Group to compute thermodynamic properties for.
        temperature (float): Temperature
        harmonicPressure (float): Harmonic contribution to the pressure.  If ommitted, the HMA pressure can still be
            computed, but will be similar in precision to the conventional pressure.

    :py:class:`hoomd.compute.thermoHMA` acts on a given group of particles and calculates HMA (harmonically mapped
    averaging) properties of those particles when requested.  HMA computes properties more precisely (with less
    variance) for atomic crystals in NVT simulations.  The presence of diffusion (vanacy hopping, etc.) will prevent
    HMA from providing improvement.  HMA tracks displacements from the lattice positions, which are saved when the
    :py:class:`hoomd.compute.thermoHMA` is instantiated.

    The specified properties are available for logging via the ``hoomd.analyze.log`` command. Each one provides
    a set of quantities for logging, suffixed with *_groupname*, so that values for different groups are differentiated
    in the log file. The default :py:class:`hoomd.compute.thermoHMA` specified on the group of all particles has no suffix
    placed on its quantity names.

    The quantities provided are (where **groupname** is replaced with the name of the group):

    * **potential_energyHMA_groupname** - :math:`U` HMA potential energy that the group contributes to the entire
      system (in energy units)
    * **pressureHMA_groupname** - :math:`P` HMA pressure that the group contributes to the entire
      system (in pressure units)

    See Also:
        ``hoomd.analyze.log``.

    Examples::

        g = group.all()
        compute.thermoHMA(group=g, temperature=1.0)
    """

    def __init__(self, group, temperature, harmonicPressure=0):

        # initialize base class
        _compute.__init__(self);

        suffix = '';
        if group.name != 'all':
            suffix = '_' + group.name;

        # create the c++ mirror class
        if not hoomd.context.current.device.cpp_exec_conf.isCUDAEnabled():
            self.cpp_compute = _hoomd.ComputeThermoHMA(hoomd.context.current.system_definition, group.cpp_group, temperature, harmonicPressure, suffix);
        else:
            self.cpp_compute = _hoomd.ComputeThermoHMAGPU(hoomd.context.current.system_definition, group.cpp_group, temperature, harmonicPressure, suffix);

        hoomd.context.current.system.addCompute(self.cpp_compute, self.compute_name);

        # save the group for later referencing
        self.group = group;

    def disable(self):
        R""" Disables the thermoHMA.

        Examples::

            my_thermo.disable()

        Executing the disable command will remove the thermoHMA compute from the system. Any ```hoomd.run``` command
        executed after disabling a thermoHMA compute will not be able to log computed values with ``hoomd.analyze.log``.

        A disabled thermoHMA compute can be re-enabled with :py:meth:`enable()`.
        """

        _compute.disable(self)

    def enable(self):
        R""" Enables the thermoHMA compute.

        Examples::

            my_thermo.enable()

        See ``disable``.
        """
        _compute.enable(self)

## \internal
# \brief Returns the previously created compute.thermo with the same group, if created. Otherwise, creates a new
# compute.thermo
def _get_unique_thermo(group):

    # first check the context for an existing compute.thermo
    for t in hoomd.context.current.thermos:
        # if we find a match, return it
        if t.group is group:
            return t;

    # if we get here, there were no matches: create a new one
    res = thermo(group);
    return res;
