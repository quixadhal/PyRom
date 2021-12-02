import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp

# TODO: Known broken
def do_dump(ch, argument):
    pass


interp.register_command(
    interp.cmd_type("dump", do_dump, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 0)
)
