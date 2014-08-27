import logging

logger = logging.getLogger()

import interp
import merc


# Contributed by Alander.
def do_visible(ch, argument):
    ch.affect_strip("invisibility")
    ch.affect_strip("mass invis")
    ch.affect_strip("sneak")
    ch.affected_by.rem_bit(merc.AFF_HIDE)
    ch.affected_by.rem_bit(merc.AFF_INVISIBLE)
    ch.affected_by.rem_bit(merc.AFF_SNEAK)
    ch.send("Ok.\n")


interp.register_command(interp.cmd_type('visible', do_visible, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
