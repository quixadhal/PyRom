import logging

logger = logging.getLogger()

from handler_room import move_char
from interp import cmd_type, register_command
from merc import DIR_WEST, POS_STANDING, LOG_NEVER


def do_west(ch, argument):
    move_char(ch, DIR_WEST, False)
    return


register_command(cmd_type('west', do_west, POS_STANDING, 0, LOG_NEVER, 0))
