from const import SLOT, skill_type
from merc import POS_STANDING, TAR_CHAR_DEFENSIVE


def spell_refresh(sn, level, ch, victim, target):
    victim.move = min(victim.move + level, victim.max_move)
    if victim.max_move == victim.move:
        victim.send("You feel fully refreshed! \n")
    else:
        victim.send("You feel less tired.\n")
    if ch != victim:
        ch.send("Ok.\n")
    return

skill_type("refresh",
           { 'mage':8, 'cleric':5, 'thief':12, 'warrior':9 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_refresh, TAR_CHAR_DEFENSIVE, POS_STANDING,
           None, SLOT(81), 12, 18, "refresh", "!Refresh!", "")