from const import SLOT, skill_type
from fight import update_pos
from merc import dice, TAR_CHAR_DEFENSIVE, POS_FIGHTING


def spell_cure_light(sn, level, ch, victim, target):
    heal = dice(1, 8) + level // 3
    victim.hit = min(victim.hit + heal, victim.max_hit)
    update_pos(victim)
    victim.send("You feel better! \n")
    if ch != victim:
        ch.send("Ok.\n")
    return


skill_type("cure light",
           {'mage': 53, 'cleric': 1, 'thief': 53, 'warrior': 3},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cure_light, TAR_CHAR_DEFENSIVE, POS_FIGHTING,
           None, SLOT(16), 10, 12, "", "!Cure Light!", "")