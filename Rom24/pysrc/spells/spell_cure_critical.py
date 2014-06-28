import const
import fight
import game_utils
import merc


def spell_cure_critical(sn, level, ch, victim, target):
    heal = game_utils.dice(3, 8) + level - 6
    victim.hit = min(victim.hit + heal, victim.max_hit)
    fight.update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("cure critical",
                          {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 19},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_critical, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(15), 20, 12, "", "!Cure Critical!", ""))
