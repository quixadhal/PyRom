import logging

logger = logging.getLogger()

import merc
import interp


def do_noshout(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Noshout whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if merc.IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if victim.get_trust() >= ch.get_trust():
        ch.send("You failed.\n")
        return
    if merc.IS_SET(victim.comm, merc.COMM_NOSHOUT):
        victim.comm = merc.REMOVE_BIT(victim.comm, merc.COMM_NOSHOUT)
        victim.send("You can shout again.\n")
        ch.send("NOSHOUT removed.\n")
        merc.wiznet("$N restores shouts to %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        victim.comm = merc.SET_BIT(victim.comm, merc.COMM_NOSHOUT)
        victim.send("You can't shout!\n")
        ch.send("NOSHOUT set.\n")
        merc.wiznet("$N revokes %s's shouts." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    return


interp.register_command(interp.cmd_type('noshout', do_noshout, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
