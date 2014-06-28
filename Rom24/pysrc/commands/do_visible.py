import logging

logger = logging.getLogger()
import interp
import merc
import state_checks


# Contributed by Alander.
def do_visible(ch, argument):
    ch.affect_strip("invis")
    ch.affect_strip("mass invis")
    ch.affect_strip("sneak")
    state_checks.REMOVE_BIT(ch.affected_by, merc.AFF_HIDE)
    state_checks.REMOVE_BIT(ch.affected_by, merc.AFF_INVISIBLE)
    state_checks.REMOVE_BIT(ch.affected_by, merc.AFF_SNEAK)
    ch.send("Ok.\n")


interp.register_command(interp.cmd_type('visible', do_visible, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
