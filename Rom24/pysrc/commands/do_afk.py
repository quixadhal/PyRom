import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


# afk command
def do_afk(ch, argument):
    if state_checks.IS_SET(ch.comm, merc.COMM_AFK):
        ch.send("AFK mode removed. Type 'replay' to see tells.\n")
        state_checks.REMOVE_BIT(ch.comm, merc.COMM_AFK)
    else:
        ch.send("You are now in AFK mode.\n")
        state_checks.SET_BIT(ch.comm, merc.COMM_AFK)


interp.register_command(interp.cmd_type('afk', do_afk, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
