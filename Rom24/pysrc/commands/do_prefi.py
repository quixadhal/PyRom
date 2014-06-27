import logging

logger = logging.getLogger()

import merc
import interp


def do_prefi(ch, argument):
    ch.send("You cannot abbreviate the prefix command.\n")
    return


interp.register_command(interp.cmd_type('prefi', do_prefi, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 0))
