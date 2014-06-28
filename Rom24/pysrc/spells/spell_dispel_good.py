from const import SLOT, skill_type
from fight import damage
from merc import IS_NPC, IS_GOOD, IS_EVIL, act, TO_ROOM, IS_NEUTRAL, TO_CHAR, dice, saves_spell, DAM_NEGATIVE, \
    POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_dispel_good(sn, level, ch, victim, target):
    if not IS_NPC(ch) and IS_GOOD(ch):
        victim = ch

    if IS_EVIL(victim):
        act("$N is protected by $S evil.", ch, None, victim, TO_ROOM)
        return

    if IS_NEUTRAL(victim):
        act("$N does not seem to be affected.", ch, None, victim, TO_CHAR)
        return

    if victim.hit > (ch.level * 4):
        dam = dice(level, 4)
    else:
        dam = max(victim.hit, dice(level, 4))
    if saves_spell(level, victim, DAM_NEGATIVE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_NEGATIVE, True)

skill_type("dispel good",
           { 'mage':53, 'cleric':15, 'thief':53, 'warrior':21 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_dispel_good, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(512), 15, 12, "dispel good", "!Dispel Good!", "")