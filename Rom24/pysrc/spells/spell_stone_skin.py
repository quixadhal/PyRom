from const import SLOT, skill_type
from merc import is_affected, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_AC, TO_ROOM, POS_STANDING, TAR_CHAR_SELF


def spell_stone_skin(sn, level, ch, victim, target):
    if is_affected(ch, sn):
        if victim == ch:
            ch.send("Your skin is already as hard as a rock.\n")
        else:
            act("$N is already as hard as can be.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = APPLY_AC
    af.modifier = -40
    af.bitvector = 0
    victim.affect_add(af)
    act("$n's skin turns to stone.", victim, None, None, TO_ROOM)
    victim.send("Your skin turns to stone.\n")

skill_type("stone skin",
           { 'mage':25, 'cleric':40, 'thief':40, 'warrior':45 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_stone_skin, TAR_CHAR_SELF, POS_STANDING, None,
           SLOT(66), 12, 18, "", "Your skin feels soft again.", "")