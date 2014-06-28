from const import skill_type, SLOT
from fight import damage
from merc import dice, DAM_HARM, TAR_CHAR_OFFENSIVE, POS_FIGHTING


def spell_cause_critical(sn, level, ch, victim, target):
    damage(ch, victim, dice(3, 8) + level - 6, sn, DAM_HARM, True)
    return


skill_type("cause critical",
           {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 19},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cause_critical, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(63), 20, 12, "spell", "!Cause Critical!", "")