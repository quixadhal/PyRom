from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_INVISIBLE, act, TO_ROOM, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, POS_STANDING, TAR_IGNORE


def spell_mass_invis(sn, level, ch, victim, target):
    for gch in ch.in_room.people:
        if not gch.is_same_group(ch) or IS_AFFECTED(gch, AFF_INVISIBLE):
            continue
        act("$n slowly fades out of existence.", gch, None, None, TO_ROOM)
        gch.send("You slowly fade out of existence.\n")
        af = AFFECT_DATA()
        af.where = TO_AFFECTS
        af.type = sn
        af.level = level // 2
        af.duration = 24
        af.location = APPLY_NONE
        af.modifier = 0
        af.bitvector = AFF_INVISIBLE
        gch.affect_add(af)
    ch.send("Ok.\n")

skill_type("mass invis",
           { 'mage':22, 'cleric':25, 'thief':31, 'warrior':53 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_mass_invis, TAR_IGNORE, POS_STANDING, None,
           SLOT(69), 20, 24, "", "You are no longer invisible.", "")