import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_autoassist(ch, argument):
    if ch.is_npc():
        return

    if state_checks.IS_SET(ch.act, merc.PLR_AUTOASSIST):
        ch.send("Autoassist removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOASSIST)
    else:
        ch.send("You will now assist when needed.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOASSIST)


interp.register_command(interp.cmd_type('autoassist', do_autoassist, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
