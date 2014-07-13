import logging

logger = logging.getLogger()

import merc
import interp


# afk command
def do_afk(ch, argument):
    if ch.comm.is_set(merc.COMM_AFK):
        ch.send("AFK mode removed. Type 'replay' to see tells.\n")
        ch.comm.rem_bit(merc.COMM_AFK)
    else:
        ch.send("You are now in AFK mode.\n")
        ch.comm.set_bit(merc.COMM_AFK)


interp.register_command(interp.cmd_type('afk', do_afk, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
