import logging


logger = logging.getLogger()

import random
import handler_game
import merc
import interp


def do_sneak(ch, argument):
    ch.send("You attempt to move silently.\n")
    ch.affect_strip("sneak")

    if ch.is_affected(merc.AFF_SNEAK):
        return

    if random.randint(1, 99) < ch.get_skill("sneak"):
        ch.check_improve( "sneak", True, 3)
        af = handler_game.AFFECT_DATA()
        af.where = merc.TO_AFFECTS
        af.type = "sneak"
        af.level = ch.level
        af.duration = ch.level
        af.location = merc.APPLY_NONE
        af.modifier = 0
        af.bitvector = merc.AFF_SNEAK
        ch.affect_add(af)
    else:
        ch.check_improve( "sneak", False, 3)
    return


interp.register_command(interp.cmd_type('sneak', do_sneak, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1))
