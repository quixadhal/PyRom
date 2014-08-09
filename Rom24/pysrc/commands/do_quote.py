import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game
import state_checks


def do_quote(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOQUOTE):
            ch.send("Quote channel is now ON.\n")
            ch.comm.rem_bit(merc.COMM_NOQUOTE)
        else:
            ch.send("Quote channel is now OFF.\n")
            ch.comm.set_bit(merc.COMM_NOQUOTE)
    else:  # quote message sent, turn quote on if it isn't already
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.commm = ch.comm.rem_bit( merc.COMM_NOQUOTE)

        ch.send("You quote '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
                    and not victim.comm.is_set(merc.COMM_NOQUOTE) and not state_checks.IS_SET(victim.comm,
                                                                                                            merc.COMM_QUIET):
                handler_game.act("$n quotes '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('quote', do_quote, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
