import const
import fight
import game_utils
import handler_magic
import merc


def spell_acid_blast(sn, level, ch, victim, target):
    dam = game_utils.dice(level, 12)
    if handler_magic.saves_spell(level, victim, merc.DAM_ACID):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_ACID, True)


const.register_spell(const.skill_type("acid blast",
                          {'mage': 28, 'cleric': 53, 'thief': 35, 'warrior': 32},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_acid_blast, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(70), 20, 12, "acid blast", "!Acid Blast!", ""))
