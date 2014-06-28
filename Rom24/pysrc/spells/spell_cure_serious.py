from const import register_spell, skill_type, SLOT
from fight import update_pos
from merc import dice, TAR_CHAR_DEFENSIVE, POS_FIGHTING


def spell_cure_serious(sn, level, ch, victim, target):
    heal = dice(2, 8) + level // 2
    victim.hit = min(victim.hit + heal, victim.max_hit)
    update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")


register_spell(skill_type("cure serious",
                          {'mage': 53, 'cleric': 7, 'thief': 53, 'warrior': 10},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_serious, TAR_CHAR_DEFENSIVE, POS_FIGHTING,
                          None, SLOT(61), 15, 12, "", "!Cure Serious!", ""))