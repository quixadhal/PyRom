from handler_room import move_char
from interp import cmd_type
from merc import DIR_SOUTH, LOG_NEVER, POS_STANDING


def do_south(ch, argument):
    move_char(ch, DIR_SOUTH, False)
    return


cmd_type('south', do_south, POS_STANDING, 0, LOG_NEVER, 0)
