import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game
import state_checks


# RT music channel
def do_music(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOMUSIC):
            ch.send("Music channel is now ON.\n")
            ch.comm.rem_bit(merc.COMM_NOMUSIC)
        else:
            ch.send("Music channel is now OFF.\n")
            ch.comm.set_bit(merc.COMM_NOMUSIC)
    else:  # music sent, turn music on if it isn't already
        if ch.comm.is_set(merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if ch.comm.is_set(merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.comm.rem_bit(merc.COMM_NOMUSIC)
        ch.send("You MUSIC: '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
                    and not victim.comm.is_set(merc.COMM_NOMUSIC) and not state_checks.IS_SET(victim.comm,
                                                                                                            merc.COMM_QUIET):
                handler_game.act("$n MUSIC: '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('music', do_music, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
