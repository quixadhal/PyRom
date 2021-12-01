import const
import fight
import game_utils
import merc


def spell_cure_light(sn, level, ch, victim, target):
    heal = game_utils.dice(1, 8) + level // 3
    victim.hit = min(victim.hit + heal, victim.max_hit)
    fight.update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")
    return


const.register_spell(const.skill_type("cure light",
                          {'mage': 53, 'cleric': 1, 'thief': 53, 'warrior': 3},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_light, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(16), 10, 12, "", "!Cure Light!", ""))
