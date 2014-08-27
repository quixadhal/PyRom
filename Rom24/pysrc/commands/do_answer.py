import logging

logger = logging.getLogger()

import handler_ch
import merc
import interp
import nanny
import handler_game


# RT answer channel - uses same line as questions
def do_answer(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOQUESTION):
            ch.send("Q/A channel is now ON.\n")
            ch.comm.rem_bit(merc.COMM_NOQUESTION)
        else:
            ch.send("Q/A channel is now OFF.\n")
            ch.comm.set_bit(merc.COMM_NOQUESTION)
    else:  # answer sent, turn Q/A on if it isn't already */
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.comm.rem_bit(merc.COMM_NOQUESTION)
        ch.send("You answer '%s'\n" % argument )
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not victim.comm.is_set(merc.COMM_NOQUESTION) and not victim.comm.is_set(merc.COMM_QUIET):
                handler_game.act("$n answers '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('answer', do_answer, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
