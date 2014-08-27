import logging

logger = logging.getLogger()

import merc
import interp
import handler_game
import instance


def do_gtell(ch, argument):
    if not argument:
        ch.send("Tell your group what?\n")
        return
    if ch.comm.is_set(merc.COMM_NOTELL):
        ch.send("Your message didn't get through!\n")
        return
    found = False
    for gch in instance.characters.values():
        if gch.is_same_group(ch):
            handler_game.act("$n tells the group '$t'", ch, argument, gch, merc.TO_VICT, merc.POS_SLEEPING)
            found = True
    if found:
        handler_game.act("$n tells the group '$t'", ch, argument, ch, merc.TO_CHAR, merc.POS_SLEEPING)
    else:
        ch.send("You do not have a group.\n")
    return


interp.register_command(interp.cmd_type('gtell', do_gtell, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type(';', do_gtell, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0))
