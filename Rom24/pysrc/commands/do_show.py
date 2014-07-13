import logging

logger = logging.getLogger()

import merc
import interp


def do_show(ch, argument):
    if ch.comm.is_set(merc.COMM_SHOW_AFFECTS):
        ch.send("Affects will no longer be shown in score.\n")
        ch.comm.rem_bit(merc.COMM_SHOW_AFFECTS)
    else:
        ch.send("Affects will now be shown in score.\n")
        ch.comm.set_bit(merc.COMM_SHOW_AFFECTS)


interp.register_command(interp.cmd_type('show', do_show, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
