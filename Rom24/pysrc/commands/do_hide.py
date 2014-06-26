import random
from interp import cmd_type
from merc import IS_AFFECTED, AFF_HIDE, REMOVE_BIT, SET_BIT, POS_RESTING, LOG_NORMAL
from skills import check_improve


def do_hide(ch, argument):
    ch.send("You attempt to hide.\n")

    if IS_AFFECTED(ch, AFF_HIDE):
        REMOVE_BIT(ch.affected_by, AFF_HIDE)

    if random.randint(1, 99) < ch.get_skill("hide"):
        SET_BIT(ch.affected_by, AFF_HIDE)
        check_improve(ch, "hide", True, 3)
    else:
        check_improve(ch, "hide", False, 3)
    return


cmd_type('hide', do_hide, POS_RESTING, 0, LOG_NORMAL, 1)
