import logging

logger = logging.getLogger()

import merc
import fight
import interp


def do_peace(ch, argument):
    for rch in ch.in_room.people:
        if rch.fighting:
            fight.stop_fighting(rch, True)
        if merc.IS_NPC(rch) and merc.IS_SET(rch.act, merc.ACT_AGGRESSIVE):
            rch.act = merc.REMOVE_BIT(rch.act, merc.ACT_AGGRESSIVE)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('peace', do_peace, merc.POS_DEAD, merc.L5, merc.LOG_NORMAL, 1))
