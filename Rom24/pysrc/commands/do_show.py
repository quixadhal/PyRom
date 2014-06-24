import merc
import interp


def do_show(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_SHOW_AFFECTS):
        ch.send("Affects will no longer be shown in score.\n")
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_SHOW_AFFECTS)
    else:
        ch.send("Affects will now be shown in score.\n")
        ch.comm = merc.SET_BIT(ch.comm, merc.COMM_SHOW_AFFECTS)

interp.cmd_table['show'] = interp.cmd_type('show', do_show, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)