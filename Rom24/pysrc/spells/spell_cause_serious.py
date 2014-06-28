from const import skill_type, SLOT
from fight import damage
from merc import dice, DAM_HARM, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_cause_serious(sn, level, ch, victim, target):
    damage(ch, victim, dice(2, 8) + level // 2, sn, DAM_HARM, True)
    return


skill_type("cause serious",
           {'mage': 53, 'cleric': 7, 'thief': 53, 'warrior': 10},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cause_serious, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
           SLOT(64), 17, 12, "spell", "!Cause Serious!", "")

