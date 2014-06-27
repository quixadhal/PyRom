import logging

logger = logging.getLogger()

import merc
import interp


def do_noemote(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Noemote whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.get_trust() >= ch.get_trust():
        ch.send("You failed.\n")
        return
    if merc.IS_SET(victim.comm, merc.COMM_NOEMOTE):
        victim.comm = merc.REMOVE_BIT(victim.comm, merc.COMM_NOEMOTE)
        victim.send("You can emote again.\n")
        ch.send("NOEMOTE removed.\n")
        merc.wiznet("$N restores emotes to %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        victim.comm = merc.SET_BIT(victim.comm, merc.COMM_NOEMOTE)
        victim.send("You can't emote!\n")
        ch.send("NOEMOTE set.\n")
        merc.wiznet("$N revokes %s's emotes." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    return


interp.register_command(interp.cmd_type('noemote', do_noemote, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
