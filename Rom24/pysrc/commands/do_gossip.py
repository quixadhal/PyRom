import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game


# RT chat replaced with ROM gossip
def do_gossip(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOGOSSIP):
            ch.send("Gossip channel is now ON.\n")
            ch.comm.rem_bit(merc.COMM_NOGOSSIP)
        else:
            ch.send("Gossip channel is now OFF.\n")
            ch.comm.set_bit(merc.COMM_NOGOSSIP)
    else:  # gossip message sent, turn gossip on if it isn't already
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel privileges.\n")
            return
        ch.comm.rem_bit(merc.COMM_NOGOSSIP)
        ch.send("You gossip '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) \
                    and d.character != ch \
                    and not victim.comm.is_set(merc.COMM_NOGOSSIP) \
                    and not victim.comm.is_set(merc.COMM_QUIET):
                handler_game.act("$n gossips '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('.', do_gossip, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 0))
interp.register_command(interp.cmd_type('gossip', do_gossip, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
