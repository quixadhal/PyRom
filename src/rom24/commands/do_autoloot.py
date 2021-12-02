import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp


def do_autoloot(ch, argument):
    if ch.is_npc():
        return

    if ch.act.is_set(merc.PLR_AUTOLOOT):
        ch.send("Autolooting removed.\n")
        ch.act.rem_bit(merc.PLR_AUTOLOOT)
    else:
        ch.send("Automatic corpse looting set.\n")
        ch.act.set_bit(merc.PLR_AUTOLOOT)


interp.register_command(
    interp.cmd_type("autoloot", do_autoloot, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
)
