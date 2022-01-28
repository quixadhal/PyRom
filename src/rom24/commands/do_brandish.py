import logging

logger = logging.getLogger(__name__)

import random
from rom24 import merc
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import interp
from rom24 import const
from rom24 import state_checks
from rom24 import instance


def do_brandish(ch, argument):
    staff = ch.get_eq("held")
    if not staff:
        ch.send("You hold nothing in your hand.\n")
        return
    if staff.item_type != merc.ITEM_STAFF:
        ch.send("You can brandish only with a staff.\n")
        return
    sn = staff.value[3]
    if not sn or not const.skill_table[sn].spell_fun:
        logger.error("BUG: Do_brandish: bad sn %s.", sn)
        return
    state_checks.WAIT_STATE(ch, 2 * merc.PULSE_VIOLENCE)
    if staff.value[2] > 0:
        handler_game.act("$n brandishes $p.", ch, staff, None, merc.TO_ROOM)
        handler_game.act("You brandish $p.", ch, staff, None, merc.TO_CHAR)
        if (
            ch.level < staff.level
            or random.randint(1, 99) >= 20 + ch.get_skill("staves") * 4 / 5
        ):
            handler_game.act("You fail to invoke $p.", ch, staff, None, merc.TO_CHAR)
            handler_game.act("...and nothing happens.", ch, None, None, merc.TO_ROOM)
            if ch.is_pc:
                ch.check_improve("staves", False, 2)
        else:
            for vch_id in ch.in_room.people[:]:
                vch = instance.characters[vch_id]
                target = const.skill_table[sn].target
                if target == merc.TAR_IGNORE:
                    if vch != ch:
                        continue
                elif target == merc.TAR_CHAR_OFFENSIVE:
                    if vch.is_npc() if ch.is_npc() else not vch.is_npc():
                        continue
                elif target == merc.TAR_CHAR_DEFENSIVE:
                    if not vch.is_npc() if ch.is_npc() else vch.is_npc():
                        continue
                elif target == merc.TAR_CHAR_SELF:
                    if vch != ch:
                        continue
                else:
                    logger.error("BUG: Do_brandish: bad target for sn %s.", sn)
                    return
                handler_magic.obj_cast_spell(
                    staff.value[3], staff.value[0], ch, vch, None
                )
                if ch.is_pc:
                    ch.check_improve("staves", True, 2)
    staff.value[2] -= 1
    if staff.value[2] <= 0:
        handler_game.act(
            "$n's $p blazes bright and is gone.", ch, staff, None, merc.TO_ROOM
        )
        handler_game.act(
            "Your $p blazes bright and is gone.", ch, staff, None, merc.TO_CHAR
        )
        staff.extract()


interp.register_command(
    interp.cmd_type("brandish", do_brandish, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
