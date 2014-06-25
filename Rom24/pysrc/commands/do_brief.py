import merc
import interp


def do_brief(ch, argument):
    if merc.IS_SET(ch.comm, COMM_BRIEF):
        ch.send("Full descriptions activated.\n")
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_BRIEF)
    else:
        ch.send("Short descriptions activated.\n")
        ch.comm = merc.SET_BIT(ch.comm, merc.COMM_BRIEF)

interp.cmd_table['brief'] = interp.cmd_type('brief', do_brief, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)