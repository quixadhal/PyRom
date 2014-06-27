import random

from interp import cmd_type
from merc import IS_AFFECTED, AFF_SNEAK, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, POS_STANDING, LOG_NORMAL
from skills import check_improve


def do_sneak(ch, argument):
    ch.send("You attempt to move silently.\n")
    ch.affect_strip("sneak")

    if IS_AFFECTED(ch, AFF_SNEAK):
        return

    if random.randint(1, 99) < ch.get_skill("sneak"):
        check_improve(ch, "sneak", True, 3)
        af = AFFECT_DATA()
        af.where = TO_AFFECTS
        af.type = "sneak"
        af.level = ch.level
        af.duration = ch.level
        af.location = APPLY_NONE
        af.modifier = 0
        af.bitvector = AFF_SNEAK
        ch.affect_add(af)
    else:
        check_improve(ch, "sneak", False, 3)
    return


cmd_type('sneak', do_sneak, POS_STANDING, 0, LOG_NORMAL, 1)
