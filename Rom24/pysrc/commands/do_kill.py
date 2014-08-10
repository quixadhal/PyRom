import logging

logger = logging.getLogger()

import merc
import fight
import interp
import game_utils
import state_checks
import handler_game


def do_kill(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Kill whom?\n")
        return
    victim = ch.get_char_room(arg)
    if victim is None:
        ch.send("They aren't here.\n")
        return
    # Allow player killing
    # if not IS_NPC(victim) and not IS_SET(victim.act, PLR_KILLER) and not IS_SET(victim.act, PLR_THIEF):
    #     ch.send("You must MURDER a player.\n")
    #     return

    if victim == ch:
        ch.send("You hit yourself.  Ouch!\n")
        fight.multi_hit(ch, ch, merc.TYPE_UNDEFINED)
        return
    if fight.is_safe(ch, victim):
        return
    if victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n")
        return
    if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
        handler_game.act("$N is your beloved master.", ch, None, victim, merc.TO_CHAR)
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("You do the best you can!\n")
        return

    state_checks.WAIT_STATE(ch, 1 * merc.PULSE_VIOLENCE)
    fight.check_killer(ch, victim)
    fight.multi_hit(ch, victim, merc.TYPE_UNDEFINED)
    return


interp.register_command(interp.cmd_type('hit', do_kill, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0))
interp.register_command(interp.cmd_type('kill', do_kill, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1))
