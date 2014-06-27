import logging

logger = logging.getLogger()

import merc
import interp


def do_nofollow(ch, argument):
    if merc.IS_NPC(ch):
        return
    if merc.IS_SET(ch.act, merc.PLR_NOFOLLOW):
        ch.send("You now accept followers.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_NOFOLLOW)
    else:
        ch.send("You no longer accept followers.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_NOFOLLOW)
        merc.die_follower(ch)


interp.register_command(interp.cmd_type('nofollow', do_nofollow, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
