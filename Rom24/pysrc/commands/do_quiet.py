import merc
import interp


# RT quiet blocks out all communication */
def do_quiet(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_QUIET):
        ch.send("Quiet mode removed.\n")
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_QUIET)
    else:
        ch.send("From now on, you will only hear says and emotes.\n")
        ch.comm = merc.SET_BIT(ch.comm, merc.COMM_QUIET)

interp.cmd_type('quiet', do_quiet, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)