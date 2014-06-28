from const import SLOT, skill_type, register_spell
from merc import IS_OBJ_STAT, ITEM_BURN_PROOF, act, TO_CHAR, AFFECT_DATA, TO_OBJECT, number_fuzzy, APPLY_NONE, TO_ROOM, \
    POS_STANDING, TAR_OBJ_INV


def spell_fireproof(sn, level, ch, victim, target):
    if IS_OBJ_STAT(obj, ITEM_BURN_PROOF):
        act("$p is already protected from burning.", ch, obj, None, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_OBJECT
    af.type = sn
    af.level = level
    af.duration = number_fuzzy(level // 4)
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = ITEM_BURN_PROOF

    obj.affect_add(af)

    act("You protect $p from fire.", ch, obj, None, TO_CHAR)
    act("$p is surrounded by a protective aura.", ch, obj, None, TO_ROOM)


register_spell(skill_type("fireproof",
                          {'mage': 13, 'cleric': 12, 'thief': 19, 'warrior': 18},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fireproof, TAR_OBJ_INV, POS_STANDING, None,
                          SLOT(523), 10, 12, "", "", "$p's protective aura fades."))