import random

import merc
import const
import interp
import fight
import skills


def do_rescue(ch, argument):
    argument, arg = merc.read_word(argument)

    if not arg:
        ch.send("Rescue whom?\n\r")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if victim == ch:
        ch.send("What about fleeing instead?\n\r")
        return
    if not merc.IS_NPC(ch) and merc.IS_NPC(victim):
        ch.send("Doesn't need your help!\n\r")
        return
    if ch.fighting == victim:
        ch.send("Too late.\n\r")
        return
    fch = victim.fighting
    if not fch:
        ch.send("That person is not fighting right now.\n\r")
        return
    if merc.IS_NPC(fch) and not ch.is_same_group(victim):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    merc.WAIT_STATE(ch, const.skill_table['rescue'].beats)
    if random.randint(1,99) > ch.get_skill('rescue'):
        ch.send("You fail the rescue.\n\r")
        merc.check_improve(ch, 'rescue', False, 1)
        return
    merc.act("You rescue $N!", ch, None, victim, merc.TO_CHAR)
    merc.act("$n rescues you!", ch, None, victim, merc.TO_VICT)
    merc.act("$n rescues $N!", ch, None, victim, merc.TO_NOTVICT)
    skills.check_improve(ch, 'rescue', True, 1)

    fight.stop_fighting(fch, False)
    fight.stop_fighting(victim, False)

    fight.check_killer(ch, fch)
    fight.set_fighting(ch, fch)
    fight.set_fighting(fch, ch)
    return

interp.cmd_type('rescue', do_rescue, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0)
