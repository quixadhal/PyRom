import const
import fight
import game_utils
import merc


def spell_cure_serious(sn, level, ch, victim, target):
    heal = game_utils.dice(2, 8) + level // 2
    victim.hit = min(victim.hit + heal, victim.max_hit)
    fight.update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("cure serious",
                          {'mage': 53, 'cleric': 7, 'thief': 53, 'warrior': 10},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_serious, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(61), 15, 12, "", "!Cure Serious!", ""))
