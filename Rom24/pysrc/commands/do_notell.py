import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


def do_notell(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Notell whom?")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.trust >= ch.trust:
        ch.send("You failed.\n")
        return
    if victim.comm.is_set(merc.COMM_NOTELL):
        victim.comm = state_checks.REMOVE_BIT(victim.comm, merc.COMM_NOTELL)
        victim.send("You can tell again.\n")
        ch.send("NOTELL removed.\n")
        handler_game.wiznet("$N restores tells to %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        victim.comm = state_checks.SET_BIT(victim.comm, merc.COMM_NOTELL)
        victim.send("You can't tell!\n")
        ch.send("NOTELL set.\n")
        handler_game.wiznet("$N revokes %s's tells." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    return


interp.register_command(interp.cmd_type('notell', do_notell, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
