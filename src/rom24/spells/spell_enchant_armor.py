import random

from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_enchant_armor(sn, level, ch, victim, target):
    obj = victim
    if obj.item_type != merc.ITEM_ARMOR:
        ch.send("That isn't an armor.\n")
        return

    if not obj.equips_to:
        ch.send("The item must be carried to be enchanted.\n")
        return

    # this means they have no bonus */
    ac_bonus = 0
    ac_found = False
    fail = 25  # base 25% chance of failure */
    affected = obj.affected
    # find the bonuses */
    if not obj.enchanted:
        affected = obj.affected

    for paf in affected:
        if paf.location == merc.APPLY_AC:
            ac_bonus = paf.modifier
            ac_found = True
            fail += 5 * (ac_bonus * ac_bonus)

        else:  # things get a little harder */
            fail += 20

    # apply other modifiers */
    fail -= level

    if obj.flags.bless:
        fail -= 15
    if obj.flags.glow:
        fail -= 5

    fail = max(5, min(fail, 85))

    result = random.randint(1, 99)

    # the moment of truth */
    if result < (fail // 5):  # item destroyed */
        handler_game.act(
            "$p flares blindingly... and evaporates! ", ch, obj, None, merc.TO_CHAR
        )
        handler_game.act(
            "$p flares blindingly... and evaporates! ", ch, obj, None, merc.TO_ROOM
        )
        obj.extract()

    if result < (fail // 3):  # item disenchanted */
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

    if result <= (90 - level // 5):  # success!  */
        handler_game.act("$p shimmers with a gold aura.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$p shimmers with a gold aura.", ch, obj, None, merc.TO_ROOM)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_MAGIC)
        added = -1
    else:  # exceptional enchant */
        handler_game.act("$p glows a brillant gold! ", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$p glows a brillant gold! ", ch, obj, None, merc.TO_ROOM)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_MAGIC)
        state_checks.SET_BIT(obj.extra_flags, merc.ITEM_GLOW)
        added = -2

    # now add the enchantments */
    if obj.level < merc.LEVEL_HERO:
        obj.level = min(merc.LEVEL_HERO - 1, obj.level + 1)

    if ac_found:
        for paf in obj.affected:
            if paf.location == merc.APPLY_AC:
                paf.type = sn
                paf.modifier += added
                paf.level = max(paf.level, level)
    else:  # add a new affect */
        paf = handler_game.AFFECT_DATA()

        paf.where = merc.TO_OBJECT
        paf.type = sn
        paf.level = level
        paf.duration = -1
        paf.location = merc.APPLY_AC
        paf.modifier = added
        paf.bitvector = 0
        obj.affected.append(paf)


const.register_spell(
    const.skill_type(
        "enchant armor",
        {"mage": 16, "cleric": 53, "thief": 53, "warrior": 53},
        {"mage": 2, "cleric": 2, "thief": 4, "warrior": 4},
        spell_enchant_armor,
        merc.TAR_OBJ_INV,
        merc.POS_STANDING,
        None,
        const.SLOT(510),
        100,
        24,
        "",
        "!Enchant Armor!",
        "",
    )
)
