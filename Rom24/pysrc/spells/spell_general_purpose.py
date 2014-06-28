import random
import const
import fight
import handler_magic
import merc


def spell_general_purpose(sn, level, ch, victim, target):
    dam = random.randint(25, 100)
    if handler_magic.saves_spell(level, victim, merc.DAM_PIERCE):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_PIERCE, True)
    return


const.register_spell(const.skill_type("general purpose",
                          {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 53},
                          {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 0},
                          spell_general_purpose, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(401), 0, 12, "general purpose ammo", "!General Purpose Ammo!", ""))
