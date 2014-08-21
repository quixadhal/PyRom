import logging

logger = logging.getLogger()

import merc
import interp
import fight
import game_utils
import handler_game


def do_slay(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Slay whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if ch == victim:
        ch.send("Suicide is a mortal sin.\n")
        return
    if not victim.is_npc() and victim.level >= ch.trust:
        ch.send("You failed.\n")
        return
    handler_game.act("You slay $M in cold blood!", ch, None, victim, merc.TO_CHAR)
    handler_game.act("$n slays you in cold blood!", ch, None, victim, merc.TO_VICT)
    handler_game.act("$n slays $N in cold blood!", ch, None, victim, merc.TO_NOTVICT)
    fight.raw_kill(victim)
    return


def do_sla(ch, argument):
    ch.send("If you want to SLAY, spell it out.\n")
    return


interp.register_command(interp.cmd_type('slay', do_slay, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1))
interp.register_command(interp.cmd_type('sla', do_sla, merc.POS_DEAD, merc.L3, merc.LOG_NORMAL, 0))
