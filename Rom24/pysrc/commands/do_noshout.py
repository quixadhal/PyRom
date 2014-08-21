import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks

def do_noshout(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Noshout whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    if victim.trust >= ch.trust:
        ch.send("You failed.\n")
        return
    if victim.comm.is_set(merc.COMM_NOSHOUT):
        victim.comm = state_checks.REMOVE_BIT(victim.comm, merc.COMM_NOSHOUT)
        victim.send("You can shout again.\n")
        ch.send("NOSHOUT removed.\n")
        handler_game.wiznet("$N restores shouts to %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        victim.comm = state_checks.SET_BIT(victim.comm, merc.COMM_NOSHOUT)
        victim.send("You can't shout!\n")
        ch.send("NOSHOUT set.\n")
        handler_game.wiznet("$N revokes %s's shouts." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    return


interp.register_command(interp.cmd_type('noshout', do_noshout, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
