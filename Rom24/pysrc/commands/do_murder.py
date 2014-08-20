import logging

logger = logging.getLogger()

import merc
import interp
import fight
import game_utils
import handler_game
import state_checks


def do_murder(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Murder whom?\n")
        return

    if ch.is_affected(merc.AFF_CHARM) \
            or (ch.is_npc()
                and ch.act.is_set(merc.ACT_PET)):
        return
    victim = ch.get_char_room(arg)
    if victim is None:
        ch.send("They aren't here.\n")
        return
    if victim == ch:
        ch.send("Suicide is a mortal sin.\n")
        return
    if fight.is_safe(ch, victim):
        return
    if victim.is_npc() and victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n")
        return
    if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
        handler_game.act("$N is your beloved master.", ch, None, victim, merc.TO_CHAR)
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("You do the best you can!\n")
        return

    state_checks.WAIT_STATE(ch, 1 * merc.PULSE_VIOLENCE)
    if ch.is_npc():
        buf = "Help! I am being attacked by %s!" % ch.short_descr
    else:
        buf = "Help!  I am being attacked by %s!" % ch.name
    victim.do_yell(buf)
    fight.check_killer(ch, victim)
    fight.multi_hit(ch, victim, merc.TYPE_UNDEFINED)
    return


def do_murde(ch, argument):
    ch.send("If you want to MURDER, spell it out.\n")
    return

interp.register_command(interp.cmd_type('murder', do_murder, merc.POS_FIGHTING, 5, merc.LOG_ALWAYS, 1))
interp.register_command(interp.cmd_type('murde', do_murde, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0))
