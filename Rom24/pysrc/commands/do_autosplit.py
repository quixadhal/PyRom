import logging

logger = logging.getLogger()

import merc
import interp


def do_autosplit(ch, argument):
    if ch.is_npc():
        return

    if ch.act.is_set(merc.PLR_AUTOSPLIT):
        ch.send("Autosplitting removed.\n")
        ch.act.rem_bit(merc.PLR_AUTOSPLIT)
    else:
        ch.send("Automatic gold splitting set.\n")
        ch.act.set_bit(merc.PLR_AUTOSPLIT)


interp.register_command(interp.cmd_type('autosplit', do_autosplit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
