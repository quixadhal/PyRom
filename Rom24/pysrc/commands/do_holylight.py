import logging

logger = logging.getLogger()

import merc
import interp


def do_holylight(ch, argument):
    if merc.IS_NPC(ch):
        return
    if merc.IS_SET(ch.act, merc.PLR_HOLYLIGHT):
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode off.\n")
    else:
        ch.act = merc.SET_BIT(ch.act, merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode on.\n")
    return


interp.register_command(interp.cmd_type('holylight', do_holylight, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
