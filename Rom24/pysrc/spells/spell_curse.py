from const import SLOT, register_spell, skill_type
from merc import TARGET_OBJ, IS_OBJ_STAT, ITEM_EVIL, act, TO_CHAR, ITEM_BLESS, affect_find, saves_dispel, TO_ALL, \
    REMOVE_BIT, AFFECT_DATA, TO_OBJECT, APPLY_SAVES, WEAR_NONE, IS_AFFECTED, AFF_CURSE, saves_spell, DAM_NEGATIVE, \
    TO_AFFECTS, APPLY_HITROLL, APPLY_SAVING_SPELL, POS_FIGHTING, TAR_OBJ_CHAR_OFF


def spell_curse(sn, level, ch, victim, target):
    # deal with the object case first */
    if target == TARGET_OBJ:
        obj = victim
        if IS_OBJ_STAT(obj, ITEM_EVIL):
            act("$p is already filled with evil.", ch, obj, None, TO_CHAR)
            return

        if IS_OBJ_STAT(obj, ITEM_BLESS):
            paf = affect_find(obj.affected, skill_table["bless"])
            if not saves_dispel(level, paf.level if paf != None else obj.level, 0):
                if paf:
                    obj.affect_remove(paf)
                act("$p glows with a red aura.", ch, obj, None, TO_ALL)
                REMOVE_BIT(obj.extra_flags, ITEM_BLESS)
                return
            else:
                act("The holy aura of $p is too powerful for you to overcome.", ch, obj, None, TO_CHAR)
                return
        af = AFFECT_DATA()
        af.where = TO_OBJECT
        af.type = sn
        af.level = level
        af.duration = 2 * level
        af.location = APPLY_SAVES
        af.modifier = +1
        af.bitvector = ITEM_EVIL
        obj.affect_add(af)

        act("$p glows with a malevolent aura.", ch, obj, None, TO_ALL)

        if obj.wear_loc != WEAR_NONE:
            ch.saving_throw += 1
        return

    # character curses */
    if IS_AFFECTED(victim, AFF_CURSE) or saves_spell(level, victim, DAM_NEGATIVE):
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = APPLY_HITROLL
    af.modifier = -1 * (level // 8)
    af.bitvector = AFF_CURSE
    victim.affect_add(af)

    af.location = APPLY_SAVING_SPELL
    af.modifier = level // 8
    victim.affect_add(af)

    victim.send("You feel unclean.\n")
    if ch != victim:
        act("$N looks very uncomfortable.", ch, None, victim, TO_CHAR)


register_spell(skill_type("curse",
                          {'mage': 18, 'cleric': 18, 'thief': 26, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_curse, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None,
                          SLOT(17), 20, 12, "curse", "The curse wears off.", "$p is no longer impure."))