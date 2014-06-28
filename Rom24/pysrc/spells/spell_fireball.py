import random

from const import SLOT, skill_type, register_spell
from fight import damage
from merc import saves_spell, DAM_FIRE, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_fireball(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 30, 35, 40, 45, 50, 55,
                60, 65, 70, 75, 80, 82, 84, 86, 88, 90,
                92, 94, 96, 98, 100, 102, 104, 106, 108, 110,
                112, 114, 116, 118, 120, 122, 124, 126, 128, 130]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if saves_spell(level, victim, DAM_FIRE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_FIRE, True)


register_spell(skill_type("fireball",
                          {'mage': 22, 'cleric': 53, 'thief': 30, 'warrior': 26},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fireball, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
                          SLOT(26), 15, 12, "fireball", "!Fireball!", ""))