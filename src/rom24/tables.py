
from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger(__name__)

clan_type = namedtuple('clan_type', 'name, who_name, hall, independent')
clan_table = OrderedDict()

position_type = namedtuple('position_type', 'name, short_name')
position_table = OrderedDict()

sex_table = OrderedDict()

# for sizes */
size_table = []

# various flag tables */
flag_type = namedtuple('flag_type', 'name, bit, settable')
act_flags = OrderedDict()
plr_flags = OrderedDict()
affect_flags = OrderedDict()
off_flags = OrderedDict()
imm_flags = OrderedDict()
form_flags = OrderedDict()
part_flags = OrderedDict()
comm_flags = OrderedDict()
exit_flags = OrderedDict()
vuln_flags = OrderedDict()
