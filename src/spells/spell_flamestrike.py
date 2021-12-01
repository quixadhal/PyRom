import const
import fight
import game_utils
import handler_magic
import merc


def spell_flamestrike(sn, level, ch, victim, target):
    dam = game_utils.dice(6 + level // 2, 8)
    if handler_magic.saves_spell(level, victim, merc.DAM_FIRE):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_FIRE, True)


const.register_spell(const.skill_type("flamestrike",
                          {'mage': 53, 'cleric': 20, 'thief': 53, 'warrior': 27},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_flamestrike, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(65), 20, 12, "flamestrike", "!Flamestrike!", ""))
