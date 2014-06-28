import random

from const import register_spell, skill_type, SLOT, skill_table
from fight import damage
from merc import saves_spell, DAM_LIGHT, TARGET_CHAR, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_colour_spray(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                30, 35, 40, 45, 50, 55, 55, 55, 56, 57,
                58, 58, 59, 60, 61, 61, 62, 63, 64, 64,
                65, 66, 67, 67, 68, 69, 70, 70, 71, 72,
                73, 73, 74, 75, 76, 76, 77, 78, 79, 79]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if saves_spell(level, victim, DAM_LIGHT):
        dam //= 2
    else:
        skill_table["blindness"].spell_fun('blindness', level // 2, ch, victim, TARGET_CHAR)

    damage(ch, victim, dam, sn, DAM_LIGHT, True)


register_spell(skill_type('colour spray',
                          {'mage': 16, 'cleric': 53, 'thief': 22, 'warrior': 20},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_colour_spray, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(10), 15, 12, "colour spray", "!Colour Spray!", ""))