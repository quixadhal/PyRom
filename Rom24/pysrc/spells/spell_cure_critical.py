from const import register_spell, skill_type, SLOT
from fight import update_pos
from merc import dice, TAR_CHAR_DEFENSIVE, POS_FIGHTING


def spell_cure_critical(sn, level, ch, victim, target):
    heal = dice(3, 8) + level - 6
    victim.hit = min(victim.hit + heal, victim.max_hit)
    update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")


register_spell(skill_type("cure critical",
                          {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 19},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_critical, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None,
                          SLOT(15), 20, 12, "", "!Cure Critical!", ""))