import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp


def do_hide(ch, argument):
    ch.send("You attempt to hide.\n")

    if ch.is_affected(merc.AFF_HIDE):
        ch.affected_by.rem_bit(merc.AFF_HIDE)

    if random.randint(1, 99) < ch.get_skill("hide"):
        ch.affected_by.set_bit(merc.AFF_HIDE)
        if ch.is_pc:
            ch.check_improve("hide", True, 3)
    else:
        if ch.is_pc:
            ch.check_improve("hide", False, 3)
    return


interp.register_command(
    interp.cmd_type("hide", do_hide, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
