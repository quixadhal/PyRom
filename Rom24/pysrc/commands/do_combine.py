import logging

logger = logging.getLogger()

import merc
import interp


def do_combine(ch, argument):
    if ch.comm.is_set(merc.COMM_COMBINE):
        ch.send("Long inventory selected.\n")
        ch.comm.rem_bit(merc.COMM_COMBINE)
    else:
        ch.send("Combined inventory selected.\n")
        ch.comm.set_bit(merc.COMM_COMBINE)


interp.register_command(interp.cmd_type('combine', do_combine, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
