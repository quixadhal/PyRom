import logging

logger = logging.getLogger()

import merc
import interp


def do_omni(ch, argument):
    if merc.IS_SET(ch.act, merc.PLR_OMNI):
        ch.send("Omnimode removed\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_OMNI)
    else:
        ch.send("Omnimode enabled.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_OMNI)


interp.register_command(interp.cmd_type('omni', do_omni, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
