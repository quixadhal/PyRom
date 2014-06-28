from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_SANCTUARY, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, TO_ROOM, \
    TAR_CHAR_DEFENSIVE, POS_STANDING


def spell_sanctuary(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_SANCTUARY):
        if victim == ch:
            ch.send("You are already in sanctuary.\n")
        else:
            act("$N is already in sanctuary.", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 6
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_SANCTUARY
    victim.affect_add(af)
    act("$n is surrounded by a white aura.", victim, None, None, TO_ROOM)
    victim.send("You are surrounded by a white aura.\n")

skill_type("sanctuary",
           { 'mage':36, 'cleric':20, 'thief':42, 'warrior':30 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_sanctuary, TAR_CHAR_DEFENSIVE, POS_STANDING, None,
           SLOT(36), 75, 12, "", "The white aura around your body fades.", "")