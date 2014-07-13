import random
import const
import fight
import handler_magic
import merc


def spell_magic_missile(sn, level, ch, victim, target):
    dam_each = [0,
                3, 3, 4, 4, 5, 6, 6, 6, 6, 6,
                7, 7, 7, 7, 7, 8, 8, 8, 8, 8,
                9, 9, 9, 9, 9, 10, 10, 10, 10, 10,
                11, 11, 11, 11, 11, 12, 12, 12, 12, 12,
                13, 13, 13, 13, 13, 14, 14, 14, 14, 14]

    level = min(level, len(dam_each) - 1)
    level = max(0, level)
    dam = random.randint(dam_each[level] // 2, dam_each[level] * 2)
    if handler_magic.saves_spell(level, victim, merc.DAM_ENERGY):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_ENERGY, True)


const.register_spell(const.skill_type("magic missile",
                          {'mage': 1, 'cleric': 53, 'thief': 2, 'warrior': 2},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_magic_missile, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(32), 15, 12, "magic missile", "!Magic Missile!", ""))
