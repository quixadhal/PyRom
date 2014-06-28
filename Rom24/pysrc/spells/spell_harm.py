import const
import fight
import game_utils
import handler_magic
import merc


def spell_harm(sn, level, ch, victim, target):
    dam = max(20, victim.hit - game_utils.dice(1, 4))
    if handler_magic.saves_spell(level, victim, merc.DAM_HARM):
        dam = min(50, dam // 2)
    dam = min(100, dam)
    fight.damage(ch, victim, dam, sn, merc.DAM_HARM, True)


const.register_spell(const.skill_type("harm",
                          {'mage': 53, 'cleric': 23, 'thief': 53, 'warrior': 28},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_harm, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(27), 35, 12, "harm spell", "!Harm!", ""))
