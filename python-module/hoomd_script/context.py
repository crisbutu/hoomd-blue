# -- start license --
# Highly Optimized Object-oriented Many-particle Dynamics -- Blue Edition
# (HOOMD-blue) Open Source Software License Copyright 2009-2014 The Regents of
# the University of Michigan All rights reserved.

# HOOMD-blue may contain modifications ("Contributions") provided, and to which
# copyright is held, by various Contributors who have granted The Regents of the
# University of Michigan the right to modify and/or distribute such Contributions.

# You may redistribute, use, and create derivate works of HOOMD-blue, in source
# and binary forms, provided you abide by the following conditions:

# * Redistributions of source code must retain the above copyright notice, this
# list of conditions, and the following disclaimer both in the code and
# prominently in any materials provided with the distribution.

# * Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions, and the following disclaimer in the documentation and/or
# other materials provided with the distribution.

# * All publications and presentations based on HOOMD-blue, including any reports
# or published results obtained, in whole or in part, with HOOMD-blue, will
# acknowledge its use according to the terms posted at the time of submission on:
# http://codeblue.umich.edu/hoomd-blue/citations.html

# * Any electronic documents citing HOOMD-Blue will link to the HOOMD-Blue website:
# http://codeblue.umich.edu/hoomd-blue/

# * Apart from the above required attributions, neither the name of the copyright
# holder nor the names of HOOMD-blue's contributors may be used to endorse or
# promote products derived from this software without specific prior written
# permission.

# Disclaimer

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND/OR ANY
# WARRANTIES THAT THIS SOFTWARE IS FREE OF INFRINGEMENT ARE DISCLAIMED.

# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -- end license --

# Maintainer: csadorf / All Developers are free to add commands for new features

## \package hoomd_script.context
# \brief Gather information about the execution context
#
# As much data from the environment is gathered as possible.

import hoomd;
from hoomd_script import meta;

## \internal
# \brief Gather context from the environment
class ExecutionContext(meta._metadata):
    ## \internal
    # \brief Constructs the context object
    def __init__(self):
        meta._metadata.__init__(self)
        self.metadata_fields = [
            'hostname', 'num_cpu', 'gpu', 'num_ranks',
            'hoomd_version', 'git_hash', 'username']

    ## \internal
    # \brief Return the execution configuration if initialized or raise exception.
    def _get_exec_conf(self):
        from hoomd_script import globals
        if globals.exec_conf is None:
            raise RuntimeError("Not initialized.")
        else:
            return globals.exec_conf

    # \brief Return the network hostname.
    @property
    def hostname(self):
        import socket
        return socket.gethostname()

    # \brief Return the number of CPUs used.
    @property
    def num_cpu(self):
        return self._get_exec_conf().n_cpu

    # \brief Return the name of the GPU used in GPU mode.
    @property
    def gpu(self):
        return self._get_exec_conf().getGPUName()

    # \brief Return the number of ranks.
    @property
    def num_ranks(self):
        return self._get_exec_conf().getNRanks()

    # \brief Return the hoomd version.
    @property
    def hoomd_version(self):
        from hoomd_script import get_hoomd_script_version
        return get_hoomd_script_version()

    # \brief Return the git hash value of the current working directory.
    #
    # The hash value is only obtained if the git executable is found and
    # the commit stage is clean, that means no unstaged changes to the
    # working directory and no uncommited, but staged changes.
    @property
    def git_hash(self):
        from . import git_tools
        try:
            return git_tools.sha1_if_clean_stage()
        except git_tools.StageDirtyWarning:
            # Do not keep track of sha1 if stage is not clean, 
            # because it is misleading.
            return None
        except OSError:
            # git was not found
            return None

    # \brief Return the username.
    @property
    def username(self):
        import getpass
        return getpass.getuser()
