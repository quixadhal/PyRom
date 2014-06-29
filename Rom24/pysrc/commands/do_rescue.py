import logging

logger = logging.getLogger()

import random

import merc
import const
import skills
import fight
import interp
import game_utils
import handler_game
import state_checks


def do_rescue(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Rescue whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim == ch:
        ch.send("What about fleeing instead?\n")
        return
    if not ch.is_npc() and victim.is_npc():
        ch.send("Doesn't need your help!\n")
        return
    if ch.fighting == victim:
        ch.send("Too late.\n")
        return
    fch = victim.fighting
    if not fch:
        ch.send("That person is not fighting right now.\n")
        return
    if state_checks.IS_NPC(fch) and not ch.is_same_group(victim):
        ch.send("Kill stealing is not permitted.\n")
        return
    state_checks.WAIT_STATE(ch, const.skill_table['rescue'].beats)
    if random.randint(1, 99) > ch.get_skill('rescue'):
        ch.send("You fail the rescue.\n")
        skills.check_improve(ch, 'rescue', False, 1)
        return
    handler_game.act("You rescue $N!", ch, None, victim, merc.TO_CHAR)
    handler_game.act("$n rescues you!", ch, None, victim, merc.TO_VICT)
    handler_game.act("$n rescues $N!", ch, None, victim, merc.TO_NOTVICT)
    skills.check_improve(ch, 'rescue', True, 1)

    fight.stop_fighting(fch, False)
    fight.stop_fighting(victim, False)

    fight.check_killer(ch, fch)
    fight.set_fighting(ch, fch)
    fight.set_fighting(fch, ch)
    return


interp.register_command(interp.cmd_type('rescue', do_rescue, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0))
