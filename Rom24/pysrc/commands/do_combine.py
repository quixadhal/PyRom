import merc
import interp


def do_combine(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_COMBINE):
        ch.send("Long inventory selected.\n")
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_COMBINE)
    else:
        ch.send("Combined inventory selected.\n")
        ch.comm = merc.SET_BIT(ch.comm, merc.COMM_COMBINE)

interp.cmd_table['combine'] = interp.cmd_type('combine', do_combine, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)