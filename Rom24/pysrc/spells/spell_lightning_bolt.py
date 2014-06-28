import random

from const import SLOT, skill_type, register_spell
from fight import damage
from merc import saves_spell, DAM_LIGHTNING, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_lightning_bolt(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 0, 0, 0, 0, 25, 28,
                31, 34, 37, 40, 40, 41, 42, 42, 43, 44,
                44, 45, 46, 46, 47, 48, 48, 49, 50, 50,
                51, 52, 52, 53, 54, 54, 55, 56, 56, 57,
                58, 58, 59, 60, 60, 61, 62, 62, 63, 64]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if saves_spell(level, victim, DAM_LIGHTNING):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_LIGHTNING, True)


register_spell(skill_type("lightning bolt",
                          {'mage': 13, 'cleric': 23, 'thief': 18, 'warrior': 16},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_lightning_bolt, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(30), 15, 12, "lightning bolt", "!Lightning Bolt!", ""))