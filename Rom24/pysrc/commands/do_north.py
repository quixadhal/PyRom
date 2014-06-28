import logging

logger = logging.getLogger()

import handler_ch
import interp
import merc


def do_north(ch, argument):
    handler_ch.move_char(ch, merc.DIR_NORTH, False)
    return


interp.register_command(interp.cmd_type('north', do_north, merc.POS_STANDING, 0, merc.LOG_NEVER, 0))
