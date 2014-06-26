from handler_room import move_char
from interp import cmd_table, cmd_type
from merc import DIR_WEST, POS_STANDING, LOG_NEVER


def do_west(ch, argument):
    move_char(ch, DIR_WEST, False)
    return


cmd_table['west'] = cmd_type('west', do_west, POS_STANDING, 0, LOG_NEVER, 0)
