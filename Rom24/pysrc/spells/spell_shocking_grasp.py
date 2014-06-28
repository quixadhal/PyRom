import random
import const
import fight
import handler_magic
import merc


def spell_shocking_grasp(sn, level, ch, victim, target):
    dam_each = [0,
                0, 0, 0, 0, 0, 0, 20, 25, 29, 33,
                36, 39, 39, 39, 40, 40, 41, 41, 42, 42,
                43, 43, 44, 44, 45, 45, 46, 46, 47, 47,
                48, 48, 49, 49, 50, 50, 51, 51, 52, 52,
                53, 53, 54, 54, 55, 55, 56, 56, 57, 57]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if handler_magic.saves_spell(level, victim, merc.DAM_LIGHTNING):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_LIGHTNING, True)


const.register_spell(const.skill_type("shocking grasp",
                          {'mage': 10, 'cleric': 53, 'thief': 14, 'warrior': 13},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_shocking_grasp, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(53), 15, 12, "shocking grasp", "!Shocking Grasp!", ""))
