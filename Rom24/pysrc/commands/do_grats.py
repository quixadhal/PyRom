import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game
import state_checks


def do_grats(ch, argument):
    if not argument:
        if state_checks.IS_SET(ch.comm, merc.COMM_NOGRATS):
            ch.send("Grats channel is now ON.\n")
            ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOGRATS)
        else:
            ch.send("Grats channel is now OFF.\n")
            ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_NOGRATS)
    else:  # grats message sent, turn grats on if it isn't already
        if state_checks.IS_SET(ch.comm, merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if state_checks.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOGRATS)
        ch.send("You grats '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) \
                    and d.character != ch \
                    and not state_checks.IS_SET(victim.comm, merc.COMM_NOGRATS)\
                    and not state_checks.IS_SET(victim.comm, merc.COMM_QUIET):
                handler_game.act("$n grats '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)


interp.register_command(interp.cmd_type('grats', do_grats, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
