import random
import const
import fight
import handler_magic
import merc


def spell_burning_hands(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 14, 17, 20, 23, 26, 29,
                29, 29, 30, 30, 31, 31, 32, 32, 33, 33,
                34, 34, 35, 35, 36, 36, 37, 37, 38, 38,
                39, 39, 40, 40, 41, 41, 42, 42, 43, 43,
                44, 44, 45, 45, 46, 46, 47, 47, 48, 48]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if handler_magic.saves_spell(level, victim, merc.DAM_FIRE):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_FIRE, True)


const.register_spell(const.skill_type("burning hands",
                          {'mage': 7, 'cleric': 53, 'thief': 10, 'warrior': 9},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_burning_hands, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(5), 15, 12, "burning hands", "!Burning Hands!", ""))
