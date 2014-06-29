import logging

logger = logging.getLogger()

import handler_game
import merc
import interp
import nanny
import handler_ch
import state_checks


def do_auction(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOAUCTION):
            ch.send("Auction channel is now ON.\n")
            ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOAUCTION)
        else:
            ch.send("Auction channel is now OFF.\n")
            ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_NOAUCTION)
    else:  # auction message sent, turn auction on if it is off */
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return

        ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOAUCTION)
        ch.send("You auction '%s'\n" % argument )
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not state_checks.IS_SET(victim.comm, merc.COMM_NOAUCTION) \
            and not state_checks.IS_SET(victim.comm, merc.COMM_QUIET):
                handler_game.act("$n auctions '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)


interp.register_command(interp.cmd_type('auction', do_auction, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
