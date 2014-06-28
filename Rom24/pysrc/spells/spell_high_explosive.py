import random
from const import SLOT, skill_type
from fight import damage

from merc import saves_spell, DAM_PIERCE, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_high_explosive(sn, level, ch, victim, target):
    dam = random.randint(30, 120)
    if saves_spell(level, victim, DAM_PIERCE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_PIERCE, True)

skill_type("high explosive",
           { 'mage':53, 'cleric':53, 'thief':53, 'warrior':53 },
           { 'mage':0, 'cleric':0, 'thief':0, 'warrior':0 },
           spell_high_explosive, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(402), 0, 12, "high explosive ammo", "!High Explosive Ammo!", "") # combat and weapons skills */