from handler_room import move_char
from interp import cmd_type
from merc import DIR_DOWN, POS_STANDING, LOG_NEVER


def do_down(ch, argument):
    move_char(ch, DIR_DOWN, False)
    return


cmd_type('down', do_down, POS_STANDING, 0, LOG_NEVER, 0)
