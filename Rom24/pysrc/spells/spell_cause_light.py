from merc import dice, DAM_HARM, TAR_CHAR_OFFENSIVE, POS_FIGHTING
from const import register_spell, skill_type, SLOT
from fight import damage


def spell_cause_light(sn, level, ch, victim, target):
    damage(ch, victim, dice(1, 8) + level // 3, sn, DAM_HARM, True)
    check_killer
    return


register_spell(skill_type("cause light",
                          {'mage': 53, 'cleric': 1, 'thief': 53, 'warrior': 3},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cause_light, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(62), 15, 12, "spell", "!Cause Light!", ""))