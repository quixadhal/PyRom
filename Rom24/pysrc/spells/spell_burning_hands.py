import random

from merc import DAM_FIRE, saves_spell, TAR_CHAR_OFFENSIVE, POS_FIGHTING
from fight import damage
from const import register_spell, skill_type, SLOT


def spell_burning_hands(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 14, 17, 20, 23, 26, 29,
                29, 29, 30, 30, 31, 31, 32, 32, 33, 33,
                34, 34, 35, 35, 36, 36, 37, 37, 38, 38,
                39, 39, 40, 40, 41, 41, 42, 42, 43, 43,
                44, 44, 45, 45, 46, 46, 47, 47, 48, 48]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if saves_spell(level, victim, DAM_FIRE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_FIRE, True)


register_spell(skill_type("burning hands",
                          {'mage': 7, 'cleric': 53, 'thief': 10, 'warrior': 9},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_burning_hands, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(5), 15, 12, "burning hands", "!Burning Hands!", ""))