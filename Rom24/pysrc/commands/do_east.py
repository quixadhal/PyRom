from handler_room import move_char
from interp import cmd_table, cmd_type
from merc import DIR_EAST, POS_STANDING, LOG_NEVER


def do_east(ch, argument):
    move_char(ch, DIR_EAST, False)
    return


cmd_table['east'] = cmd_type('east', do_east, POS_STANDING, 0, LOG_NEVER, 0)
