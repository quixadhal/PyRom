import logging

logger = logging.getLogger()

import merc
import interp


def do_autoassist(ch, argument):
    if ch.is_npc():
        return

    if ch.act.is_set(merc.PLR_AUTOASSIST):
        ch.send("Autoassist removed.\n")
        ch.act.rem_bit(merc.PLR_AUTOASSIST)
    else:
        ch.send("You will now assist when needed.\n")
        ch.act.set_bit(merc.PLR_AUTOASSIST)


interp.register_command(interp.cmd_type('autoassist', do_autoassist, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
