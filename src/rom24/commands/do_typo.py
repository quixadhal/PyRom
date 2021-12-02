import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import settings
from rom24 import game_utils


def do_typo(ch, argument):
    game_utils.append_file(ch, settings.TYPO_FILE, argument)
    ch.send("Typo logged.\n")
    return


interp.register_command(
    interp.cmd_type("typo", do_typo, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
)
