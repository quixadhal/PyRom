import merc
import interp


def do_log(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Log whom?\n")
        return
    if arg == "all" :
        if merc.fLogAll:
            merc.fLogAll = False
            ch.send("Log ALL off.\n")
        else:
            merc.fLogAll = True
            ch.send("Log ALL on.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if merc.IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    # * No level check, gods can log anyone.
    if merc.IS_SET(victim.act, merc.PLR_LOG):
        victim.act = merc.REMOVE_BIT(victim.act, merc.PLR_LOG)
        ch.send("LOG removed.\n")
    else:
        victim.act = merc.SET_BIT(victim.act, merc.PLR_LOG)
        ch.send("LOG set.\n")
    return

interp.cmd_type('log', do_log, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1)