from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_PASS_DOOR, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, number_fuzzy, APPLY_NONE, TO_ROOM, \
    POS_STANDING, TAR_CHAR_SELF


def spell_pass_door(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_PASS_DOOR):
        if victim == ch:
            ch.send("You are already out of phase.\n")
        else:
            act("$N is already shifted out of phase.", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = number_fuzzy(level // 4)
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_PASS_DOOR
    victim.affect_add(af)
    act("$n turns translucent.", victim, None, None, TO_ROOM)
    victim.send("You turn translucent.\n")


register_spell(skill_type("pass door",
                          {'mage': 24, 'cleric': 32, 'thief': 25, 'warrior': 37},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_pass_door, TAR_CHAR_SELF, POS_STANDING, None,
                          SLOT(74), 20, 12, "", "You feel solid again.", ""))