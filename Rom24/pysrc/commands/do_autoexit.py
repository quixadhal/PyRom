import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_autoexit(ch, argument):
    if ch.is_npc():
        return

    if ch.act.is_set(merc.PLR_AUTOEXIT):
        ch.send("Exits will no longer be displayed.\n")
        ch.act.rem_bit(merc.PLR_AUTOEXIT)
    else:
        ch.send("Exits will now be displayed.\n")
        ch.act.set_bit(merc.PLR_AUTOEXIT)


interp.register_command(interp.cmd_type('autoexit', do_autoexit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
