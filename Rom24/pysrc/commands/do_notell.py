import merc
import interp


def do_notell(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Notell whom?")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.get_trust() >= ch.get_trust():
        ch.send("You failed.\n")
        return
    if IS_SET(victim.comm, COMM_NOTELL):
        victim.comm = merc.REMOVE_BIT(victim.comm, merc.COMM_NOTELL)
        victim.send("You can tell again.\n")
        ch.send("NOTELL removed.\n")
        merc.wiznet("$N restores tells to %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        victim.comm = merc.SET_BIT(victim.comm, merc.COMM_NOTELL)
        victim.send("You can't tell!\n")
        ch.send("NOTELL set.\n")
        merc.wiznet("$N revokes %s's tells." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    return

interp.cmd_table['notell'] = interp.cmd_type('notell', do_notell, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)