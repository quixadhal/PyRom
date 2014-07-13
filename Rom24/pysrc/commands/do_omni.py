import logging

logger = logging.getLogger()

import merc
import interp


def do_omni(ch, argument):
    if ch.act.is_set(merc.PLR_OMNI):
        ch.send("Omnimode removed\n")
        ch.act.rem_bit(merc.PLR_OMNI)
    else:
        ch.send("Omnimode enabled.\n")
        ch.act.set_bit(merc.PLR_OMNI)


interp.register_command(interp.cmd_type('omni', do_omni, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
