import logging

logger = logging.getLogger(__name__)

from rom24 import handler_ch
from rom24 import interp
from rom24 import merc


def do_down(ch, argument):
    handler_ch.move_char(ch, merc.DIR_DOWN, False)
    return


interp.register_command(
    interp.cmd_type("down", do_down, merc.POS_STANDING, 0, merc.LOG_NEVER, 0)
)
