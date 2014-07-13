import logging

logger = logging.getLogger()

import merc
import interp


# RT deaf blocks out all shouts
def do_deaf(ch, argument):
    if ch.comm.is_set(merc.COMM_DEAF):
        ch.send("You can now hear tells again.\n")
        ch.comm.rem_bit( merc.COMM_DEAF)
    else:
        ch.send("From now on, you won't hear tells.\n")
        ch.comm.set_bit( merc.COMM_DEAF)


interp.register_command(interp.cmd_type('deaf', do_deaf, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
