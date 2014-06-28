import random
import const
import fight
import handler_magic
import merc


def spell_high_explosive(sn, level, ch, victim, target):
    dam = random.randint(30, 120)
    if handler_magic.saves_spell(level, victim, merc.DAM_PIERCE):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_PIERCE, True)


const.register_spell(const.skill_type("high explosive",
                          {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 53},
                          {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 0},
                          spell_high_explosive, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(402), 0, 12, "high explosive ammo", "!High Explosive Ammo!",
                          ""))  # combat and weapons skills */)
