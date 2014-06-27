import merc
import interp


def do_pardon(ch, argument):
    argument, arg1 = merc.read_word(argument)
    argument, arg2 = merc.read_word(argument)
    if not arg1 or not arg2:
        ch.send("Syntax: pardon <character> <killer|thief>.\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if merc.IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if arg2 == "killer" :
        if merc.IS_SET(victim.act, merc.PLR_KILLER):
            victim.act = merc.REMOVE_BIT(victim.act, merc.PLR_KILLER)
            ch.send("Killer flag removed.\n")
            victim.send("You are no longer a KILLER.\n")
        return
    if arg2 == "thief" :
        if merc.IS_SET(victim.act, merc.PLR_THIEF):
            victim.act = merc.REMOVE_BIT(victim.act, merc.PLR_THIEF)
            ch.send("Thief flag removed.\n")
            victim.send("You are no longer a THIEF.\n")
        return
    ch.send("Syntax: pardon <character> <killer|thief>.\n")
    return

interp.cmd_type('pardon', do_pardon, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1)