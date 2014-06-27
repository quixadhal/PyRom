import logging

logger = logging.getLogger()

import random
import merc
import interp
import skills


def do_zap(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg and not ch.fighting:
        ch.send("Zap whom or what?\n")
        return
    wand = ch.get_eq(merc.WEAR_HOLD)
    if not wand:
        ch.send("You hold nothing in your hand.\n")
        return
    if wand.item_type != merc.ITEM_WAND:
        ch.send("You can zap only with a wand.\n")
        return
    obj = None
    victim = None
    if not arg:
        if ch.fighting:
            victim = ch.fighting
        else:
            ch.send("Zap whom or what?\n")
            return
    else:
        victim = ch.get_char_room(arg)
        obj = ch.get_obj_here(arg)
        if not victim or not obj:
            ch.send("You can't find it.\n")
            return
        merc.WAIT_STATE(ch, 2 * merc.PULSE_VIOLENCE)

    if wand.value[2] > 0:
        if victim:
            merc.act("$n zaps $N with $p.", ch, wand, victim, merc.TO_NOTVICT)
            merc.act("You zap $N with $p.", ch, wand, victim, merc.TO_CHAR)
            merc.act("$n zaps you with $p.", ch, wand, victim, merc.TO_VICT)
        else:
            merc.act("$n zaps $P with $p.", ch, wand, obj, merc.TO_ROOM)
            merc.act("You zap $P with $p.", ch, wand, obj, merc.TO_CHAR)
        if ch.level < wand.level \
                or random.randint(1, 99) >= 20 + ch.get_skill("wands") * 4 // 5:
            merc.act("Your efforts with $p produce only smoke and sparks.", ch, wand, None, merc.TO_CHAR)
            merc.act("$n's efforts with $p produce only smoke and sparks.", ch, wand, None, merc.TO_ROOM)
            skills.check_improve(ch, "wands", False, 2)
        else:
            merc.obj_cast_spell(wand.value[3], wand.value[0], ch, victim, obj)
            skills.check_improve(ch, "wands", True, 2)
    wand.value[2] -= 1
    if wand.value[2] <= 0:
        merc.act("$n's $p explodes into fragments.", ch, wand, None, merc.TO_ROOM)
        merc.act("Your $p explodes into fragments.", ch, wand, None, merc.TO_CHAR)
        wand.extract()


interp.register_command(interp.cmd_type('zap', do_zap, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
