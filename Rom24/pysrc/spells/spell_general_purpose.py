import random
from const import SLOT, skill_type
from fight import damage

from merc import saves_spell, DAM_PIERCE, TAR_CHAR_OFFENSIVE, POS_FIGHTING


def spell_general_purpose(sn, level, ch, victim, target):
    dam = random.randint(25, 100)
    if saves_spell(level, victim, DAM_PIERCE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_PIERCE, True)
    return

skill_type("general purpose",
           { 'mage':53, 'cleric':53, 'thief':53, 'warrior':53 },
           { 'mage':0, 'cleric':0, 'thief':0, 'warrior':0 },
           spell_general_purpose, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(401), 0, 12, "general purpose ammo", "!General Purpose Ammo!", "")