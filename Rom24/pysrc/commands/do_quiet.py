import logging


logger = logging.getLogger()

import merc
import interp
import state_checks

# RT quiet blocks out all communication
def do_quiet(ch, argument):
    if ch.comm.is_set(merc.COMM_QUIET):
        ch.send("Quiet mode removed.\n")
        ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_QUIET)
    else:
        ch.send("From now on, you will only hear says and emotes.\n")
        ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_QUIET)


interp.register_command(interp.cmd_type('quiet', do_quiet, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
