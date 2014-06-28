import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_show(ch, argument):
    if state_checks.IS_SET(ch.comm, merc.COMM_SHOW_AFFECTS):
        ch.send("Affects will no longer be shown in score.\n")
        ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_SHOW_AFFECTS)
    else:
        ch.send("Affects will now be shown in score.\n")
        ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_SHOW_AFFECTS)


interp.register_command(interp.cmd_type('show', do_show, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
