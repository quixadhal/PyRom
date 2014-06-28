from merc import dice, DAM_ACID, saves_spell, TAR_CHAR_OFFENSIVE, POS_FIGHTING
from const import register_spell, skill_type, SLOT
from fight import damage


def spell_acid_blast(sn, level, ch, victim, target):
    dam = dice(level, 12)
    if saves_spell(level, victim, DAM_ACID):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_ACID, True)


register_spell(skill_type("acid blast",
                          {'mage': 28, 'cleric': 53, 'thief': 35, 'warrior': 32},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_acid_blast, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(70), 20, 12, "acid blast", "!Acid Blast!", ""))