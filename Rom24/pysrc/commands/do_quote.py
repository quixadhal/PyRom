import merc
import interp
import nanny



def do_quote(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOQUOTE):
            ch.send("Quote channel is now ON.\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOQUOTE)
        else:
            ch.send("Quote channel is now OFF.\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOQUOTE)
    else:  # quote message sent, turn quote on if it isn't already */
        if merc.IS_SET(ch.comm, merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if merc.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.commm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOQUOTE)

        ch.send("You quote '%s'\n" % argument )
        for d in merc.descriptor_list:
            victim = merc.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not merc.IS_SET(victim.comm, merc.COMM_NOQUOTE) and not merc.IS_SET(victim.comm, merc.COMM_QUIET):
                merc.act("$n quotes '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)

interp.cmd_table['quote'] = interp.cmd_type('quote', do_quote, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)