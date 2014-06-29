import logging


logger = logging.getLogger()

import merc
import interp
import nanny
import handler_game
import state_checks


def do_immtalk(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_NOWIZ):
            ch.send("Immortal channel is now ON\n")
            ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOWIZ)
        else:
            ch.send("Immortal channel is now OFF\n")
            ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_NOWIZ)
        return

    ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOWIZ)
    handler_game.act("$n: $t", ch, argument, None, merc.TO_CHAR, merc.POS_DEAD)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) and state_checks.IS_IMMORTAL(d.character) \
                and not state_checks.IS_SET(d.character.comm, merc.COMM_NOWIZ):
            handler_game.act("$n: $t", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)


interp.register_command(interp.cmd_type('immtalk', do_immtalk, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type(':', do_immtalk, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 0))
