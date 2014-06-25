import merc
import interp
import nanny

# RT auction rewritten in ROM style */
def do_auction(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOAUCTION):
            ch.send("Auction channel is now ON.\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOAUCTION)
        else:
            ch.send("Auction channel is now OFF.\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOAUCTION)
    else:  # auction message sent, turn auction on if it is off */
        if merc.IS_SET(ch.comm, merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if merc.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return

        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOAUCTION)
        ch.send("You auction '%s'\n" % argument )
        for d in merc.descriptor_list:
            victim = merc.CH(D)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not merc.IS_SET(victim.comm, merc.COMM_NOAUCTION) \
            and not merc.IS_SET(victim.comm, merc.COMM_QUIET):
                merc.act("$n auctions '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)

interp.cmd_table['auction'] = interp.cmd_type('auction', do_auction, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)