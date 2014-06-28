from const import SLOT, skill_type, register_spell
from merc import TARGET_OBJ, IS_OBJ_STAT, ITEM_INVIS, act, TO_CHAR, AFFECT_DATA, TO_OBJECT, APPLY_NONE, TO_ALL, \
    IS_AFFECTED, AFF_INVISIBLE, TO_ROOM, TO_AFFECTS, POS_STANDING, TAR_OBJ_CHAR_DEF


def spell_invis(sn, level, ch, victim, target):
    # object invisibility */
    if target == TARGET_OBJ:
        obj = victim
        if IS_OBJ_STAT(obj, ITEM_INVIS):
            act("$p is already invisible.", ch, obj, None, TO_CHAR)
            return

        af = AFFECT_DATA()
        af.where = TO_OBJECT
        af.type = sn
        af.level = level
        af.duration = level + 12
        af.location = APPLY_NONE
        af.modifier = 0
        af.bitvector = ITEM_INVIS
        obj.affect_add(af)
        act("$p fades out of sight.", ch, obj, None, TO_ALL)
        return
    # character invisibility */
    if IS_AFFECTED(victim, AFF_INVISIBLE):
        return

    act("$n fades out of existence.", victim, None, None, TO_ROOM)
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level + 12
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_INVISIBLE
    victim.affect_add(af)
    victim.send("You fade out of existence.\n")
    return


register_spell(skill_type("invisibility",
                          {'mage': 5, 'cleric': 53, 'thief': 9, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_invis, TAR_OBJ_CHAR_DEF, POS_STANDING, None,
                          SLOT(29), 5, 12, "", "You are no longer invisible.", "$p fades into view."))