import logging

logger = logging.getLogger()

import merc
import interp


def do_compact(ch, argument):
    if ch.comm.is_set(merc.COMM_COMPACT):
        ch.send("Compact mode removed.\n")
        ch.comm.rem_bit(merc.COMM_COMPACT)
    else:
        ch.send("Compact mode set.\n")
        ch.comm.set_bit(merc.COMM_COMPACT)


interp.register_command(interp.cmd_type('compact', do_compact, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
