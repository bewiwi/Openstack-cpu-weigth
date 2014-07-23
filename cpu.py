# Copyright (c) 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
CPU Weigher.  Weigh hosts by their CPU usage.

The default is to spread instances across all hosts evenly.  If you prefer
stacking, you can set the 'ram_weight_multiplier' option to a negative
number and the weighing has the opposite effect of the default.
"""

from oslo.config import cfg

from nova.scheduler import weights
from nova.openstack.common import log as logging

cpu_weight_opts = [
        cfg.FloatOpt('cpu_weight_multiplier',
                     default=1.0,
                     help='Multiplier used for weighing cpu.  Negative '
                          'numbers mean to stack vs spread.'),
]

CONF = cfg.CONF
CONF.register_opts(cpu_weight_opts)
LOG = logging.getLogger(__name__)

class CPUWeigher(weights.BaseHostWeigher):
    minval = 0

    def weight_multiplier(self):
        """Override the weight multiplier."""
        return CONF.cpu_weight_multiplier

    def _weigh_object(self, host_state, weight_properties):
        """Higher weights win.  We want spreading to be the default."""
        LOG.debug('vCPU avaible %s' % (host_state.vcpus_total - host_state.vcpus_used))
        return host_state.vcpus_total - host_state.vcpus_used
