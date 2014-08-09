import logging


logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game
import state_checks

# RT question channel
def do_question(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOQUESTION):
            ch.send("Q/A channel is now ON.\n")
            ch.comm.rem_bit(merc.COMM_NOQUESTION)
        else:
            ch.send("Q/A channel is now OFF.\n")
            ch.comm.set_bit(merc.COMM_NOQUESTION)
    else:  # question sent, turn Q/A on if it isn't already
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel privileges.\n")
            return
        ch.comm.rem_bit(merc.COMM_NOQUESTION)

        ch.send("You question '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
                    and not victim.comm.is_set(merc.COMM_NOQUESTION) and not state_checks.IS_SET(victim.comm,
                                                                                                               merc.COMM_QUIET):
                handler_game.act("$n questions '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('question', do_question, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
