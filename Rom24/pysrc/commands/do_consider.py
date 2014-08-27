import logging

logger = logging.getLogger()

import game_utils
import merc
import interp
import fight
import handler_game


def do_consider(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Consider killing whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They're not here.\n")
        return
    if fight.is_safe(ch, victim):
        ch.send("Don't even think about it.\n")
        return
    diff = victim.level - ch.level
    if diff <= -10:
        msg = "You can kill $N naked and weaponless."
    elif diff <= -5:
        msg = "$N is no match for you."
    elif diff <= -2:
        msg = "$N looks like an easy kill."
    elif diff <= 1:
        msg = "The perfect match!"
    elif diff <= 4:
        msg = "$N says 'Do you feel lucky, punk?'."
    elif diff <= 9:
        msg = "$N laughs at you mercilessly."
    else:
        msg = "Death will thank you for your gift."
    handler_game.act(msg, ch, None, victim, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('consider', do_consider, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
