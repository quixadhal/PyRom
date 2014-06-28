from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_FAERIE_FIRE, AFFECT_DATA, TO_AFFECTS, APPLY_AC, act, TO_ROOM, POS_FIGHTING, \
    TAR_CHAR_OFFENSIVE


def spell_faerie_fire(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_FAERIE_FIRE):
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = APPLY_AC
    af.modifier = 2 * level
    af.bitvector = AFF_FAERIE_FIRE
    victim.affect_add(af)
    victim.send("You are surrounded by a pink outline.\n")
    act("$n is surrounded by a pink outline.", victim, None, None, TO_ROOM)

skill_type("faerie fire",
           { 'mage':6, 'cleric':3, 'thief':5, 'warrior':8 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_faerie_fire, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(72), 5, 12, "faerie fire", "The pink aura around you fades away.", "")