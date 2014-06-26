import merc
import interp


def do_sla(ch, argument):
    ch.send("If you want to SLAY, spell it out.\n\r")
    return

interp.cmd_table['sla'] = interp.cmd_type('sla', do_sla, merc.POS_DEAD, merc.L3, merc.LOG_NORMAL, 0)