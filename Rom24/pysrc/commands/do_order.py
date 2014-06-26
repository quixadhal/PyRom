import merc
import interp


def do_order(ch, argument):
    argument, arg = merc.read_word(argument)
    remainder, arg2 = merc.read_word(argument)

    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    if not arg or not argument:
        ch.send("Order whom to do what?\n")
        return

    if merc.IS_AFFECTED(ch, merc.AFF_CHARM):
        ch.send("You feel like taking, not giving, orders.\n")
        return
    victim = None
    if  arg == "all":
        fAll   = True
        victim = None
    else:
        fAll   = False
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not merc.IS_AFFECTED(victim, merc.AFF_CHARM) or victim.master != ch  \
        or (merc.IS_IMMORTAL(victim) and victim.trust >= ch.trust):
            ch.send("Do it yourself!\n")
            return
    found = False
    for och in ch.in_room.people[:]:
        if merc.IS_AFFECTED(och, merc.AFF_CHARM) \
        and och.master == ch \
        and (fAll or och == victim):
            found = True
            act("$n orders you to '%s'." % argument, ch, None, och, merc.TO_VICT)
            interp.interpret(och, argument)

    if found:
        merc.WAIT_STATE(ch, merc.PULSE_VIOLENCE)
        ch.send("Ok.\n")
    else:
        ch.send("You have no followers here.\n")
    return

interp.cmd_type('order', do_order, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)