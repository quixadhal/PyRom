from handler_room import move_char
import interp
from merc import DIR_NORTH, POS_STANDING, LOG_NEVER


def do_north(ch, argument):
    move_char(ch, DIR_NORTH, False)
    return


interp.cmd_table['north'] = interp.cmd_type('north', do_north, POS_STANDING, 0, LOG_NEVER, 0)
