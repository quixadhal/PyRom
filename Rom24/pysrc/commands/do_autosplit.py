import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_autosplit(ch, argument):
    if state_checks.IS_NPC(ch):
        return

    if state_checks.IS_SET(ch.act, merc.PLR_AUTOSPLIT):
        ch.send("Autosplitting removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOSPLIT)
    else:
        ch.send("Automatic gold splitting set.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOSPLIT)


interp.register_command(interp.cmd_type('autosplit', do_autosplit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
