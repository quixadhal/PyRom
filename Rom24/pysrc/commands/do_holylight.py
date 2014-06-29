import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_holylight(ch, argument):
    if ch.is_npc():
        return
    if state_checks.IS_SET(ch.act, merc.PLR_HOLYLIGHT):
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode off.\n")
    else:
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode on.\n")
    return


interp.register_command(interp.cmd_type('holylight', do_holylight, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
