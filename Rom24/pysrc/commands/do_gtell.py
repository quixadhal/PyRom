import logging

logger = logging.getLogger()

import merc
import interp
import handler_game
import state_checks

def do_gtell(ch, argument):
    if not argument:
        ch.send("Tell your group what?\n")
        return
    if state_checks.IS_SET(ch.comm, merc.COMM_NOTELL):
        ch.send("Your message didn't get through!\n")
        return
    for gch in merc.char_list[:]:
        if gch.is_same_group(ch):
            handler_game.act("$n tells the group '$t'", ch, argument, gch, merc.TO_VICT, merc.POS_SLEEPING)
    return


interp.register_command(interp.cmd_type('gtell', do_gtell, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type(';', do_gtell, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0))
