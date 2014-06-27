import logging

logger = logging.getLogger()

from interp import cmd_type, register_command
from merc import REMOVE_BIT, AFF_HIDE, AFF_INVISIBLE, AFF_SNEAK, POS_SLEEPING, LOG_NORMAL


# Contributed by Alander.
def do_visible(ch, argument):
    ch.affect_strip("invis")
    ch.affect_strip("mass invis")
    ch.affect_strip("sneak")
    REMOVE_BIT(ch.affected_by, AFF_HIDE)
    REMOVE_BIT(ch.affected_by, AFF_INVISIBLE)
    REMOVE_BIT(ch.affected_by, AFF_SNEAK)
    ch.send("Ok.\n")


register_command(cmd_type('visible', do_visible, POS_SLEEPING, 0, LOG_NORMAL, 1))
