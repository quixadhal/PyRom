from merc import (TARGET_OBJ, IS_OBJ_STAT, ITEM_EVIL, affect_find,
                  saves_dispel, REMOVE_BIT, act, TO_CHAR, AFFECT_DATA, TO_OBJECT,
                  APPLY_SAVES, ITEM_BLESS, TO_ALL, WEAR_NONE, POS_FIGHTING, APPLY_HITROLL,
                  APPLY_SAVING_SPELL, TAR_OBJ_CHAR_DEF, POS_STANDING)
from const import register_spell, skill_type, SLOT


def spell_bless(sn, level, ch, victim, target):
    # deal with the object case first */
    if target == TARGET_OBJ:
        obj = victim
        if IS_OBJ_STAT(obj, ITEM_BLESS):
            act("$p is already blessed.", ch, obj, target=TO_CHAR)
            return
        if IS_OBJ_STAT(obj, ITEM_EVIL):
            paf = affect_find(obj.affected, "curse")
            level = obj.level
            if paf:
                level = paf.level
            if not saves_dispel(level, level, 0):
                if paf:
                    obj.affect_remove(paf)
                    act("$p glows a pale blue.", ch, obj, None, TO_ALL)
                    obj.extra_bits = REMOVE_BIT(obj.extra_flags, ITEM_EVIL)
                    return
                else:
                    act("The evil of $p is too powerful for you to overcome.", ch, obj, target=TO_CHAR)
                    return
        af = AFFECT_DATA()
        af.where = TO_OBJECT
        af.type = sn
        af.level = level
        af.duration = 6 + level
        af.location = APPLY_SAVES
        af.modifier = -1
        af.bitvector = ITEM_BLESS
        obj.affect_add(af)
        act("$p glows with a holy aura.", ch, obj, target=TO_ALL)
        if obj.wear_loc != WEAR_NONE:
            ch.saving_throw = ch.saving_throw - 1
        return


    # character target */
    if victim.position == POS_FIGHTING or is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already blessed.\n")
        else:
            act("$N already has divine favor.", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 6 + level
    af.location = APPLY_HITROLL
    af.modifier = level // 8
    af.bitvector = 0
    victim.affect_add(af)

    af.location = APPLY_SAVING_SPELL
    af.modifier = 0 - level // 8
    victim.affect_add(af)
    victim.send("You feel righteous.\n")
    if ch is not victim:
        act("You grant $N the favor of your god.", ch, None, victim, TO_CHAR)


register_spell(skill_type("bless",
                          {'mage': 53, 'cleric': 7, 'thief': 53, 'warrior': 8},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_bless, TAR_OBJ_CHAR_DEF, POS_STANDING, None,
                          SLOT(3), 5, 12, "", "You feel less righteous.", "$p's holy aura fades."))