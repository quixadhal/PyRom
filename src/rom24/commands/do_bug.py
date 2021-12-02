import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import game_utils
from rom24 import interp
from rom24 import settings


def do_bug(ch, argument):
    game_utils.append_file(ch, settings.BUG_FILE, argument)
    ch.send("Bug logged.\n")
    return


interp.register_command(
    interp.cmd_type("bug", do_bug, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
)
