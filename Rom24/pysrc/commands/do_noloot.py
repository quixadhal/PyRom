import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_noloot(ch, argument):
    if ch.is_npc():
        return
    if state_checks.IS_SET(ch.act, merc.PLR_CANLOOT):
        ch.send("Your corpse is now safe from thieves.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_CANLOOT)
    else:
        ch.send("Your corpse may now be looted.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_CANLOOT)


interp.register_command(interp.cmd_type('noloot', do_noloot, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
