import logging


logger = logging.getLogger()

import merc
import interp

# RT quiet blocks out all communication
def do_quiet(ch, argument):
    if ch.comm.is_set(merc.COMM_QUIET):
        ch.send("Quiet mode removed.\n")
        ch.comm.rem_bit(merc.COMM_QUIET)
    else:
        ch.send("From now on, you will only hear says and emotes.\n")
        ch.comm.set_bit(merc.COMM_QUIET)


interp.register_command(interp.cmd_type('quiet', do_quiet, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
