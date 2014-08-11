import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_autogold(ch, argument):
    if ch.is_npc():
        return

    if state_checks.IS_SET(ch.act, merc.PLR_AUTOGOLD):
        ch.send("Autogold removed.\n")
        ch.act.rem_bit(merc.PLR_AUTOGOLD)
    else:
        ch.send("Automatic gold looting set.\n")
        ch.act.set_bit(merc.PLR_AUTOGOLD)


interp.register_command(interp.cmd_type('autogold', do_autogold, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
