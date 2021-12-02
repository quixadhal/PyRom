from collections import OrderedDict
import logging
from typing import *

logger = logging.getLogger(__name__)

from rom24 import living


class cmd_type:
    def __init__(self, name, do_fun, position, level, log, show, default_arg=None):
        self.name = name
        self.do_fun = do_fun
        self.position = position
        self.level = level
        self.log = log
        self.show = show
        self.default_arg = default_arg
        setattr(living.Living, self.do_fun.__name__, self.do_fun)


# These commands don't need to be here but are, for order. These will always match first with prefixes.
cmd_table: Dict[str, Any] = OrderedDict()

cmd_table["north"] = None
cmd_table["east"] = None
cmd_table["south"] = None
cmd_table["west"] = None
cmd_table["up"] = None
cmd_table["down"] = None
cmd_table["doat"] = None
cmd_table["buy"] = None
cmd_table["cast"] = None
cmd_table["follow"] = None
cmd_table["goto"] = None
cmd_table["group"] = None
cmd_table["hit"] = None
cmd_table["inventory"] = None
cmd_table["kill"] = None
cmd_table["look"] = None
cmd_table["who"] = None
cmd_table["autolist"] = None


def register_command(entry: cmd_type):
    cmd_table[entry.name] = entry
    logger.debug("    %s registered in command table.", entry.name)
