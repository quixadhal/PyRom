import logging

logger = logging.getLogger()

import merc
import interp


def do_autosac(ch, argument):
    if ch.is_npc():
        return
    if ch.act.is_set(merc.PLR_AUTOSAC):
        ch.send("Autosacrificing removed.\n")
        ch.act.rem_bit(merc.PLR_AUTOSAC)
    else:
        ch.send("Automatic corpse sacrificing set.\n")
        ch.act.set_bit(merc.PLR_AUTOSAC)


interp.register_command(interp.cmd_type('autosac', do_autosac, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
