import logging

logger = logging.getLogger()

import game_utils
import merc
import interp
import handler_game
import state_checks


def do_wake(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.do_stand("")
        return

    if not ch.is_awake():
        ch.send("You are asleep yourself!\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if state_checks.IS_AWAKE(victim):
        handler_game.act("$N is already awake.", ch, None, victim, merc.TO_CHAR)
        return
    if victim.is_affected( merc.AFF_SLEEP):
        handler_game.act("You can't wake $M!", ch, None, victim, merc.TO_CHAR)
        return
    handler_game.act("$n wakes you.", ch, None, victim, merc.TO_VICT, merc.POS_SLEEPING)
    victim.do_stand("")
    return


interp.register_command(interp.cmd_type('wake', do_wake, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
