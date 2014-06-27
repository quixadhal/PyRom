import logging

logger = logging.getLogger()

from interp import cmd_type, register_command
from merc import read_word, IS_AWAKE, act, TO_CHAR, IS_AFFECTED, AFF_SLEEP, TO_VICT, POS_SLEEPING, LOG_NORMAL


def do_wake(ch, argument):
    argument, arg = read_word(argument)
    if not arg:
        ch.do_stand("")
        return

    if not IS_AWAKE(ch):
        ch.send("You are asleep yourself!\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_AWAKE(victim):
        act("$N is already awake.", ch, None, victim, TO_CHAR)
        return
    if IS_AFFECTED(victim, AFF_SLEEP):
        act("You can't wake $M!", ch, None, victim, TO_CHAR)
        return
    act("$n wakes you.", ch, None, victim, TO_VICT, POS_SLEEPING)
    victim.do_stand("")
    return


register_command(cmd_type('wake', do_wake, POS_SLEEPING, 0, LOG_NORMAL, 1))
