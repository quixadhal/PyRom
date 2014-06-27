import merc
import interp


# afk command */
def do_afk(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_AFK):
        ch.send("AFK mode removed. Type 'replay' to see tells.\n")
        merc.REMOVE_BIT(ch.comm, merc.COMM_AFK)
    else:
        ch.send("You are now in AFK mode.\n")
        merc.SET_BIT(ch.comm, merc.COMM_AFK)

interp.cmd_type('afk', do_afk, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)