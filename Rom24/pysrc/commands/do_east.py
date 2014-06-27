import logging

logger = logging.getLogger()

from handler_room import move_char
from interp import cmd_type, register_command
from merc import DIR_EAST, POS_STANDING, LOG_NEVER


def do_east(ch, argument):
    move_char(ch, DIR_EAST, False)
    return


register_command(cmd_type('east', do_east, POS_STANDING, 0, LOG_NEVER, 0))
