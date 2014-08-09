import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import handler_game
import state_checks


def do_yell(ch, argument):
    if ch.comm.is_set(merc.COMM_NOSHOUT):
        ch.send("You can't yell.\n")
        return
    if not argument:
        ch.send("Yell what?\n")
        return
    handler_game.act("You yell '$t'", ch, argument, None, merc.TO_CHAR)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) \
                and d.character != ch \
                and d.character.in_room is not None \
                and d.character.in_room.area == ch.in_room.area \
                and not state_checks.IS_SET(d.character.comm, merc.COMM_QUIET):
            handler_game.act("$n yells '$t'", ch, argument, d.character, merc.TO_VICT)


interp.register_command(interp.cmd_type('yell', do_yell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
