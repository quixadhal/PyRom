import const
import fight
import game_utils
import merc


def spell_cause_critical(sn, level, ch, victim, target):
    fight.damage(ch, victim, game_utils.dice(3, 8) + level - 6, sn, merc.DAM_HARM, True)
    return


const.register_spell(const.skill_type("cause critical",
                          {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 19},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cause_critical, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(63), 20, 12, "spell", "!Cause Critical!", ""))
