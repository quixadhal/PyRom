import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import fight
from rom24 import interp
from rom24 import state_checks
from rom24 import instance


def do_peace(ch, argument):
    for rch_id in ch.in_room.people[:]:
        rch = instance.characters[rch_id]
        if rch.fighting:
            fight.stop_fighting(rch, True)
        if rch.is_npc() and rch.act.is_set(merc.ACT_AGGRESSIVE):
            rch.act = state_checks.REMOVE_BIT(rch.act, merc.ACT_AGGRESSIVE)
    ch.send("Ok.\n")
    return


interp.register_command(
    interp.cmd_type("peace", do_peace, merc.POS_DEAD, merc.L5, merc.LOG_NORMAL, 1)
)
