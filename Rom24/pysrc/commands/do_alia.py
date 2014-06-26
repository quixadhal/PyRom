import merc
import interp


def do_alia(ch, argument):
    ch.send("I'm sorry, alias must be entered in full.\n\r")
    return

interp.cmd_table['alia'] = interp.cmd_type('alia', do_alia, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0)