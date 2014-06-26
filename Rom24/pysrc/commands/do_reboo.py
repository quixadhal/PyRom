import merc
import interp


def do_reboo(ch, argument):
    ch.send("If you want to REBOOT, spell it out.\n")
    return

interp.cmd_type('reboo', do_reboo, merc.POS_DEAD, merc.L1, merc.LOG_NORMAL, 0)
