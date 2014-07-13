import logging

logger = logging.getLogger()

import merc
import interp


def do_holylight(ch, argument):
    if ch.is_npc():
        return
    if ch.act.is_set(merc.PLR_HOLYLIGHT):
        ch.act.rem_bit(merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode off.\n")
    else:
        ch.act.set_bit(merc.PLR_HOLYLIGHT)
        ch.send("Holy light mode on.\n")
    return


interp.register_command(interp.cmd_type('holylight', do_holylight, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
