import merc
import interp


def do_qui(ch, argument):
    ch.send("If you want to QUIT, you have to spell it out.\n")
    return

interp.cmd_type('qui', do_qui, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0)