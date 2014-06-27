import logging

logger = logging.getLogger()

import interp
import merc


def do_sla(ch, argument):
    ch.send("If you want to SLAY, spell it out.\n")
    return


interp.register_command(interp.cmd_type('sla', do_sla, merc.POS_DEAD, merc.L3, merc.LOG_NORMAL, 0))
