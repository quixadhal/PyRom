import logging

logger = logging.getLogger()

import random
import merc
import interp
import skills
import const


def do_brandish(ch, argument):
    staff = ch.get_eq(merc.WEAR_HOLD)
    if not staff:
        ch.send("You hold nothing in your hand.\n")
        return
    if staff.item_type != merc.ITEM_STAFF:
        ch.send("You can brandish only with a staff.\n")
        return
    sn = staff.value[3]
    if sn < 0 or not const.skill_table[sn].spell_fun:
        logger.error("BUG: Do_brandish: bad sn %s.", sn)
        return
    merc.WAIT_STATE(ch, 2 * merc.PULSE_VIOLENCE)
    if staff.value[2] > 0:
        merc.act("$n brandishes $p.", ch, staff, None, merc.TO_ROOM)
        merc.act("You brandish $p.", ch, staff, None, merc.TO_CHAR)
        if ch.level < staff.level or random.randint(1, 99) >= 20 + ch.get_skill("staves") * 4 / 5:
            merc.act("You fail to invoke $p.", ch, staff, None, merc.TO_CHAR)
            merc.act("...and nothing happens.", ch, None, None, merc.TO_ROOM)
            ch.check_improve( "staves", False, 2)
        else:
            for vch in ch.in_room.people[:]:
                target = const.skill_table[sn].target
                if target == merc.TAR_IGNORE:
                    if vch != ch:
                        continue
                elif target == merc.TAR_CHAR_OFFENSIVE:
                    if merc.IS_NPC(vch) if merc.IS_NPC(ch) else not merc.IS_NPC(vch):
                        continue
                elif target == merc.TAR_CHAR_DEFENSIVE:
                    if not merc.IS_NPC(vch) if merc.IS_NPC(ch) else merc.IS_NPC(vch):
                        continue
                elif target == merc.TAR_CHAR_SELF:
                    if vch != ch:
                        continue
                else:
                    logger.error("BUG: Do_brandish: bad target for sn %s.", sn)
                    return
                merc.obj_cast_spell(staff.value[3], staff.value[0], ch, vch, None)
                ch.check_improve( "staves", True, 2)
    staff.value[2] -= 1
    if staff.value[2] <= 0:
        merc.act("$n's $p blazes bright and is gone.", ch, staff, None, merc.TO_ROOM)
        merc.act("Your $p blazes bright and is gone.", ch, staff, None, merc.TO_CHAR)
        staff.extract()


interp.register_command(interp.cmd_type('brandish', do_brandish, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
