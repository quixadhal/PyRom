import logging

logger = logging.getLogger(__name__)

import merc
import interp
import handler_ch


def do_nofollow(ch, argument):
    if ch.is_npc():
        return
    if ch.act.is_set(merc.PLR_NOFOLLOW):
        ch.send("You now accept followers.\n")
        ch.act.rem_bit(merc.PLR_NOFOLLOW)
    else:
        ch.send("You no longer accept followers.\n")
        ch.act.set_bit(merc.PLR_NOFOLLOW)
        handler_ch.die_follower(ch)


interp.register_command(interp.cmd_type('nofollow', do_nofollow, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
