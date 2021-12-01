import const
import fight
import game_utils
import merc


def spell_cause_light(sn, level, ch, victim, target):
    fight.damage(ch, victim, game_utils.dice(1, 8) + level // 3, sn, merc.DAM_HARM, True)
    fight.check_killer
    return


const.register_spell(const.skill_type("cause light",
                          {'mage': 53, 'cleric': 1, 'thief': 53, 'warrior': 3},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cause_light, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(62), 15, 12, "spell", "!Cause Light!", ""))
