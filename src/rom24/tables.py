from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger(__name__)

clan_type = namedtuple("clan_type", "name, who_name, hall, independent")
clan_table: dict = OrderedDict()

position_type = namedtuple("position_type", "name, short_name")
position_table: dict = OrderedDict()

sex_table: dict = OrderedDict()

# for sizes */
size_table: list = []

# various flag tables */
flag_type = namedtuple("flag_type", "name, bit, settable")
act_flags: dict = OrderedDict()
plr_flags: dict = OrderedDict()
affect_flags: dict = OrderedDict()
off_flags: dict = OrderedDict()
imm_flags: dict = OrderedDict()
form_flags: dict = OrderedDict()
part_flags: dict = OrderedDict()
comm_flags: dict = OrderedDict()
exit_flags: dict = OrderedDict()
vuln_flags: dict = OrderedDict()
