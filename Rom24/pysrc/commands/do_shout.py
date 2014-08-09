import logging


logger = logging.getLogger()

import merc
import interp
import nanny
import handler_ch
import handler_game
import state_checks

def do_shout(ch, argument):
    if not argument:
        if ch.comm.is_set(merc.COMM_SHOUTSOFF):
            ch.send("You can hear shouts again.\n")
            ch.comm.rem_bit(merc.COMM_SHOUTSOFF)
        else:
            ch.send("You will no longer hear shouts.\n")
            ch.comm.set_bit(merc.COMM_SHOUTSOFF)
        return
    if ch.comm.is_set(merc.COMM_NOSHOUT):
        ch.send("You can't shout.\n")
        return
    ch.comm.rem_bit(merc.COMM_SHOUTSOFF)
    state_checks.WAIT_STATE(ch, 12)
    handler_game.act("You shout '$T'", ch, None, argument, merc.TO_CHAR)
    for d in merc.descriptor_list:
        victim = handler_ch.CH(d)
        if d.is_connected(nanny.con_playing) and d.character != ch \
                and not victim.comm.is_set(merc.COMM_SHOUTSOFF) and not state_checks.IS_SET(victim.comm,
                                                                                                          merc.COMM_QUIET):
            handler_game.act("$n shouts '$t'", ch, argument, d.character, merc.TO_VICT)


interp.register_command(interp.cmd_type('shout', do_shout, merc.POS_RESTING, 3, merc.LOG_NORMAL, 1))
