import logging

logger = logging.getLogger()

from handler_room import move_char
from interp import cmd_type, register_command
from merc import DIR_UP, POS_STANDING, LOG_NEVER


def do_up(ch, argument):
    move_char(ch, DIR_UP, False)
    return


register_command(cmd_type('up', do_up, POS_STANDING, 0, LOG_NEVER, 0))
