import logging

logger = logging.getLogger()

import merc
import interp


def do_brief(ch, argument):
    if ch.comm.is_set(merc.COMM_BRIEF):
        ch.send("Full descriptions activated.\n")
        ch.comm.rem_bit(merc.COMM_BRIEF)
    else:
        ch.send("Short descriptions activated.\n")
        ch.comm.set_bit(merc.COMM_BRIEF)


interp.register_command(interp.cmd_type('brief', do_brief, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
