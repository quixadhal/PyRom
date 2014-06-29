import logging
import skills

logger = logging.getLogger()

import random

import merc
import state_checks
import interp


def do_hide(ch, argument):
    ch.send("You attempt to hide.\n")

    if ch.is_affected(merc.AFF_HIDE):
        state_checks.REMOVE_BIT(ch.affected_by, merc.AFF_HIDE)

    if random.randint(1, 99) < ch.get_skill("hide"):
        state_checks.SET_BIT(ch.affected_by, merc.AFF_HIDE)
        skills.check_improve(ch, "hide", True, 3)
    else:
        skills.check_improve(ch, "hide", False, 3)
    return


interp.register_command(interp.cmd_type('hide', do_hide, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))

