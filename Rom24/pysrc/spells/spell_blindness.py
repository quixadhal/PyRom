from merc import (IS_AFFECTED, saves_spell, DAM_OTHER, AFFECT_DATA,
                  TO_AFFECTS, APPLY_HITROLL, AFF_BLIND, act, TO_ROOM, TAR_CHAR_OFFENSIVE,
                  POS_FIGHTING)
from const import skill_type, SLOT


def spell_blindness(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_BLIND) or saves_spell(level, victim, DAM_OTHER):
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.location = APPLY_HITROLL
    af.modifier = -4
    af.duration = 1 + level
    af.bitvector = AFF_BLIND
    victim.affect_add(af)
    victim.send("You are blinded! \n")
    act("$n appears to be blinded.", victim, target=TO_ROOM)


skill_type("blindness",
           {'mage': 12, 'cleric': 8, 'thief': 17, 'warrior': 15},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_blindness, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(4), 5, 12, "", "You can see again.", "")