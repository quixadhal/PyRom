from const import SLOT, skill_type
from fight import damage
from merc import dice, saves_spell, DAM_FIRE, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_flamestrike(sn, level, ch, victim, target):
    dam = dice(6 + level // 2, 8)
    if saves_spell(level, victim, DAM_FIRE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_FIRE, True)

skill_type("flamestrike",
           { 'mage':53, 'cleric':20, 'thief':53, 'warrior':27 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_flamestrike, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(65), 20, 12, "flamestrike", "!Flamestrike!", "")