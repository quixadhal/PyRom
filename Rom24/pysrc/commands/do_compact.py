import logging

logger = logging.getLogger()

import merc
import interp


def do_compact(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_COMPACT):
        ch.send("Compact mode removed.\n")
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_COMPACT)
    else:
        ch.send("Compact mode set.\n")
        ch.comm = merc.SET_BIT(ch.comm, merc.COMM_COMPACT)


interp.register_command(interp.cmd_type('compact', do_compact, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
