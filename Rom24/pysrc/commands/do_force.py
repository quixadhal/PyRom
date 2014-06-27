import merc
import interp


# * Thanks to Grodyn for pointing out bugs in this function.
def do_force(ch, argument):
    argument, arg  = merc.read_word(argument)

    if not arg or not argument:
        ch.send("Force whom to do what?\n")
        return
    temp, arg2 = merc.read_word(argument)
    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    buf = "$n forces you to '%s'." % argument
    if arg == "all":
        if ch.get_trust() < merc.MAX_LEVEL - 3:
            ch.send("Not at your level!\n")
            return
        for vch in merc.char_list[:]:
            if not merc.IS_NPC(vch) and vch.get_trust() < ch.get_trust():
                merc.act(buf, ch, None, vch, merc.TO_VICT)
                interp.interpret(vch, argument)
    elif arg == "players":
        if ch.get_trust() < merc.MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in merc.char_list[:]:
            if not merc.IS_NPC(vch) and vch.get_trust() < ch.get_trust() and vch.level < merc.LEVEL_HERO:
                merc.act( buf, ch, None, vch, merc.TO_VICT )
                interp.interpret(vch, argument)
    elif arg == "gods":
        if ch.get_trust() < merc.MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in merc.char_list[:]:
            if not merc.IS_NPC(vch) and vch.get_trust() < ch.get_trust() and vch.level >= merc.LEVEL_HERO:
                merc.act(buf, ch, None, vch, merc.TO_VICT)
                interp.interpret(vch, argument)
    else:
        victim = ch.get_char_world(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not ch.is_room_owner(victim.in_room) and  ch.in_room != victim.in_room \
        and victim.in_room.is_private() and not merc.IS_TRUSTED(ch, merc.IMPLEMENTOR):
            ch.send("That character is in a private room.\n")
            return
        if victim.get_trust() >= ch.get_trust():
            ch.send("Do it yourself!\n")
            return
        if not merc.IS_NPC(victim) and ch.get_trust() < merc.MAX_LEVEL -3:
            ch.send("Not at your level!\n")
            return
        merc.act(buf, ch, None, victim, merc.TO_VICT)
        interp.interpret(victim, argument)
    ch.send("Ok.\n")
    return

interp.cmd_type('force', do_force, merc.POS_DEAD, merc.L7, merc.LOG_ALWAYS, 1)