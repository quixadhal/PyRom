import const
import fight
import merc


def spell_heal(sn, level, ch, victim, target):
    victim.hit = min(victim.hit + 100, victim.max_hit)
    fight.update_pos(victim)
    victim.send("A warm feeling fills your body.\n")
    if ch != victim:
        ch.send("Ok.\n")
    return


const.register_spell(const.skill_type("heal",
                          {'mage': 53, 'cleric': 21, 'thief': 33, 'warrior': 30},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_heal, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(28), 50, 12, "", "!Heal!", ""))
