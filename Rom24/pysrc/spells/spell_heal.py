from const import SLOT, skill_type
from fight import update_pos
from merc import POS_FIGHTING, TAR_CHAR_DEFENSIVE


def spell_heal(sn, level, ch, victim, target):
    victim.hit = min(victim.hit + 100, victim.max_hit)
    update_pos(victim)
    victim.send("A warm feeling fills your body.\n")
    if ch != victim:
        ch.send("Ok.\n")
    return

skill_type("heal",
           { 'mage':53, 'cleric':21, 'thief':33, 'warrior':30 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_heal, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None,
           SLOT(28), 50, 12, "", "!Heal!", "")