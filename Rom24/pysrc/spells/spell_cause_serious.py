import const
import fight
import game_utils
import merc


def spell_cause_serious(sn, level, ch, victim, target):
    fight.damage(ch, victim, game_utils.dice(2, 8) + level // 2, sn, merc.DAM_HARM, True)
    return


const.register_spell(const.skill_type("cause serious",
                          {'mage': 53, 'cleric': 7, 'thief': 53, 'warrior': 10},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cause_serious, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(64), 17, 12, "spell", "!Cause Serious!", "")

)
