import merc
import interp


def do_pecho(ch, argument):
    argument, arg = merc.read_word(argument)
    if not argument or not arg:
        ch.send("Personal echo what?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("Target not found.\n")
        return
    if victim.get_trust() >= ch.get_trust() and ch.get_trust() != merc.MAX_LEVEL:
        victim.send("personal> ")

    victim.send(argument)
    victim.send("\n")
    ch.send("personal> ")
    ch.send(argument)
    ch.send("\n")

interp.cmd_type('pecho', do_pecho, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1)