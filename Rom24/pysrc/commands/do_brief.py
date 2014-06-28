import logging

logger = logging.getLogger()

import state_checks
import merc
import interp


def do_brief(ch, argument):
    if state_checks.IS_SET(ch.comm, merc.COMM_BRIEF):
        ch.send("Full descriptions activated.\n")
        ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_BRIEF)
    else:
        ch.send("Short descriptions activated.\n")
        ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_BRIEF)


interp.register_command(interp.cmd_type('brief', do_brief, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
