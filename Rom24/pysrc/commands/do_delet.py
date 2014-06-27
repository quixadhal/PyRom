import merc
import interp


def do_delet(ch, argument):
    ch.send("You must type the full command to delete yourself.\n")

interp.cmd_type('delet', do_delet, merc.POS_DEAD, 0, merc.LOG_ALWAYS, 0)