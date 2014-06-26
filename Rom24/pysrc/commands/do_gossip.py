import merc
import interp
import nanny


# RT chat replaced with ROM gossip */
def do_gossip(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOGOSSIP):
            ch.send("Gossip channel is now ON.\n")
            ch.comm = merc.REMOVE_BIT(ch.comm,COMM_NOGOSSIP)
        else:
            ch.send("Gossip channel is now OFF.\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOGOSSIP)
    else:  # gossip message sent, turn gossip on if it isn't already */
        if merc.IS_SET(ch.comm, merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if merc.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOGOSSIP)
        ch.send("You gossip '%s'\n" % argument )
        for d in merc.descriptor_list:
            victim = merc.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not merc.IS_SET(victim.comm, merc.COMM_NOGOSSIP) and not merc.IS_SET(victim.comm, merc.COMM_QUIET):
                merc.act( "$n gossips '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)

interp.cmd_type('.', do_gossip, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 0)
interp.cmd_type('gossip', do_gossip, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)