import logging

logger = logging.getLogger()

import merc
import interp


def do_shutdow(ch, argument):
    ch.send("If you want to SHUTDOWN, spell it out.\n")
    return


interp.register_command(interp.cmd_type('shutdow', do_shutdow, merc.POS_DEAD, merc.L1, merc.LOG_NORMAL, 0))
