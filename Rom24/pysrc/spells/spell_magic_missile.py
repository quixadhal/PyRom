import random

from const import SLOT, skill_type, register_spell
from fight import damage
from merc import saves_spell, DAM_ENERGY, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_magic_missile(sn, level, ch, victim, target):
    dam_each = [0,
                3, 3, 4, 4, 5, 6, 6, 6, 6, 6,
                7, 7, 7, 7, 7, 8, 8, 8, 8, 8,
                9, 9, 9, 9, 9, 10, 10, 10, 10, 10,
                11, 11, 11, 11, 11, 12, 12, 12, 12, 12,
                13, 13, 13, 13, 13, 14, 14, 14, 14, 14]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if saves_spell(level, victim, DAM_ENERGY):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_ENERGY, True)


register_spell(skill_type("magic missile",
                          {'mage': 1, 'cleric': 53, 'thief': 2, 'warrior': 2},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_magic_missile, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(32), 15, 12, "magic missile", "!Magic Missile!", ""))