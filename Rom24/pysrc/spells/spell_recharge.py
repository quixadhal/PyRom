import random
from const import SLOT, skill_type

from merc import ITEM_WAND, ITEM_STAFF, act, TO_CHAR, TO_ROOM, POS_STANDING, TAR_OBJ_INV


def spell_recharge(sn, level, ch, victim, target):
    obj = victim
    if obj.item_type != ITEM_WAND and obj.item_type != ITEM_STAFF:
        ch.send("That item does not carry charges.\n")
        return

    if obj.value[3] >= 3 * level // 2:
        ch.send("Your skills are not great enough for that.\n")
        return
    if obj.value[1] == 0:
        ch.send("That item has already been recharged once.\n")
        return

    chance = 40 + 2 * level

    chance -= obj.value[3]  # harder to do high-level spells */
    chance -= (obj.value[1] - obj.value[2]) * (obj.value[1] - obj.value[2])

    chance = max(level // 2, chance)

    percent = random.randint(1, 99)

    if percent < chance // 2:
        act("$p glows softly.", ch, obj, None, TO_CHAR)
        act("$p glows softly.", ch, obj, None, TO_ROOM)
        obj.value[2] = max(obj.value[1], obj.value[2])
        obj.value[1] = 0
        return
    elif percent <= chance:
        act("$p glows softly.", ch, obj, None, TO_CHAR)
        act("$p glows softly.", ch, obj, None, TO_CHAR)

        chargemax = obj.value[1] - obj.value[2]
        chargeback = 0
        if chargemax > 0:
            chargeback = max(1, chargemax * percent // 100)
        obj.value[2] += chargeback
        obj.value[1] = 0
        return
    elif percent <= min(95, 3 * chance // 2):
        ch.send("Nothing seems to happen.\n")
        if obj.value[1] > 1:
            obj.value[1] -= 1
        return
    else:  # whoops!  */
        act("$p glows brightly and explodes! ", ch, obj, None, TO_CHAR)
        act("$p glows brightly and explodes! ", ch, obj, None, TO_ROOM)
        obj.extract()

skill_type("recharge",
           { 'mage':9, 'cleric':53, 'thief':53, 'warrior':53 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_recharge, TAR_OBJ_INV, POS_STANDING, None,
           SLOT(517), 60, 24, "", "!Recharge!", "")