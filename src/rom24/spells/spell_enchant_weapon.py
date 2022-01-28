import random

from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_enchant_weapon(sn, level, ch, victim, target):
    obj = victim

    if obj.item_type != merc.ITEM_WEAPON:
        ch.send("That isn't a weapon.\n")
        return

    if obj.wear_loc != -1:
        ch.send("The item must be carried to be enchanted.\n")
        return

    # this means they have no bonus */
    hit_bonus = 0
    dam_bonus = 0
    fail = 25  # base 25% chance of failure */
    dam_found = False
    hit_found = False
    # find the bonuses */
    affected = obj.affected
    if not obj.enchanted:
        affected = obj.pIndexData.affected

    for paf in affected:
        if paf.location == merc.APPLY_HITROLL:
            hit_bonus = paf.modifier
            hit_found = True
            fail += 2 * (hit_bonus * hit_bonus)
        elif paf.location == merc.APPLY_DAMROLL:
            dam_bonus = paf.modifier
            dam_found = True
            fail += 2 * (dam_bonus * dam_bonus)
        else:  # things get a little harder */
            fail += 25

    # apply other modifiers */
    fail -= 3 * level // 2

    if obj.flags.bless:
        fail -= 15
    if obj.flags.glow:
        fail -= 5

    fail = max(5, min(fail, 95))

    result = random.randint(1, 99)

    # the moment of truth */
    if result < (fail // 5):  # item destroyed */
        handler_game.act(
            "$p shivers violently and explodes! ", ch, obj, None, merc.TO_CHAR
        )
        handler_game.act(
            "$p shivers violently and explodeds! ", ch, obj, None, merc.TO_ROOM
        )
        obj.extract()
        return

    if result < (fail // 2):  # item disenchanted */
        handler_game.act(
            "$p glows brightly, then fades...oops.", ch, obj, None, merc.TO_CHAR
        )
        handler_game.act("$p glows brightly, then fades.", ch, obj, None, merc.TO_ROOM)
        obj.enchanted = True
        # remove all affects */
        obj.affected[:] = []

        # clear all flags */
        obj.extra_flags = 0
        return

    if result <= fail:  # failed, no bad result */
        ch.send("Nothing seemed to happen.\n")
        return

    # okay, move all the old flags into new vectors if we have to */
    if not obj.enchanted:
        obj.enchanted = True
        for paf in obj.pIndexData.affected:
            af_new = handler_game.AFFECT_DATA()
            af_new.where = paf.where
            af_new.type = max(0, paf.type)
            af_new.level = paf.level
            af_new.duration = paf.duration
            af_new.location = paf.location
            af_new.modifier = paf.modifier
            af_new.bitvector = paf.bitvector
            obj.affected.append(af_new)
    if result <= (100 - level // 5):  # success!  */
        handler_game.act("$p glows blue.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$p glows blue.", ch, obj, None, merc.TO_ROOM)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_MAGIC)
        added = 1
    else:  # exceptional enchant */
        handler_game.act("$p glows a brillant blue! ", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$p glows a brillant blue! ", ch, obj, None, merc.TO_ROOM)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_MAGIC)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_GLOW)
        added = 2

    # now add the enchantments */
    if obj.level < merc.LEVEL_HERO - 1:
        obj.level = min(merc.LEVEL_HERO - 1, obj.level + 1)

    if dam_found:
        for paf in obj.affected:
            if paf.location == merc.APPLY_DAMROLL:
                paf.type = sn
                paf.modifier += added
                paf.level = max(paf.level, level)
                if paf.modifier > 4:
                    state_checks.SET_BIT(obj.extra_flags, merc.ITEM_HUM)
    else:  # add a new affect */
        paf = handler_game.AFFECT_DATA()

        paf.where = merc.TO_OBJECT
        paf.type = sn
        paf.level = level
        paf.duration = -1
        paf.location = merc.APPLY_DAMROLL
        paf.modifier = added
        paf.bitvector = 0
        obj.affected.append(paf)

    if hit_found:
        for paf in obj.affected:
            if paf.location == merc.APPLY_HITROLL:
                paf.type = sn
                paf.modifier += added
                paf.level = max(paf.level, level)
                if paf.modifier > 4:
                    state_checks.SET_BIT(obj.extra_flags, merc.ITEM_HUM)
    else:  # add a new affect */
        paf = handler_game.AFFECT_DATA()

        paf.type = sn
        paf.level = level
        paf.duration = -1
        paf.location = merc.APPLY_HITROLL
        paf.modifier = added
        paf.bitvector = 0
        obj.affected.append(paf)


const.register_spell(
    const.skill_type(
        "enchant weapon",
        {"mage": 17, "cleric": 53, "thief": 53, "warrior": 53},
        {"mage": 2, "cleric": 2, "thief": 4, "warrior": 4},
        spell_enchant_weapon,
        merc.TAR_OBJ_INV,
        merc.POS_STANDING,
        None,
        const.SLOT(24),
        100,
        24,
        "",
        "!Enchant Weapon!",
        "",
    )
)
