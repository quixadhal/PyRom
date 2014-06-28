from const import SLOT, skill_type, register_spell
from merc import is_affected, saves_spell, DAM_OTHER, AFFECT_DATA, TO_AFFECTS, APPLY_STR, AFF_WEAKEN, act, TO_ROOM, \
    TAR_CHAR_OFFENSIVE, POS_FIGHTING


def spell_weaken(sn, level, ch, victim, target):
    if is_affected(victim, sn) or saves_spell(level, victim, DAM_OTHER):
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 2
    af.location = APPLY_STR
    af.modifier = -1 * (level // 5)
    af.bitvector = AFF_WEAKEN
    victim.affect_add(af)
    victim.send("You feel your strength slip away.\n")
    act("$n looks tired and weak.", victim, None, None, TO_ROOM)


register_spell(skill_type("weaken",
                          {'mage': 11, 'cleric': 14, 'thief': 16, 'warrior': 17},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_weaken, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
                          SLOT(68), 20, 12, "spell", "You feel stronger.", ""))