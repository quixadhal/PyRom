import logging

logger = logging.getLogger()

import merc
import interp


def do_autosac(ch, argument):
    if merc.IS_NPC(ch):
        return
    if merc.IS_SET(ch.act, merc.PLR_AUTOSAC):
        ch.send("Autosacrificing removed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOSAC)
    else:
        ch.send("Automatic corpse sacrificing set.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOSAC)


interp.register_command(interp.cmd_type('autosac', do_autosac, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
