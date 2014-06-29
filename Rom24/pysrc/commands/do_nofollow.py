import logging

logger = logging.getLogger()

import merc
import interp
import handler_ch
import state_checks


def do_nofollow(ch, argument):
    if ch.is_npc():
        return
    if state_checks.IS_SET(ch.act, merc.PLR_NOFOLLOW):
        ch.send("You now accept followers.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_NOFOLLOW)
    else:
        ch.send("You no longer accept followers.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_NOFOLLOW)
        handler_ch.die_follower(ch)


interp.register_command(interp.cmd_type('nofollow', do_nofollow, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
