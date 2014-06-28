from const import SLOT, skill_type, register_spell
from merc import is_affected, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_STR, TO_ROOM, POS_STANDING, \
    TAR_CHAR_DEFENSIVE


def spell_giant_strength(sn, level, ch, victim, target):
    if is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already as strong as you can get! \n")
        else:
            act("$N can't get any stronger.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = APPLY_STR
    af.modifier = 1 + (level >= 18) + (level >= 25) + (level >= 32)
    af.bitvector = 0
    victim.affect_add(af)
    victim.send("Your muscles surge with heightened power! \n")
    act("$n's muscles surge with heightened power.", victim, None, None, TO_ROOM)


register_spell(skill_type("giant strength",
                          {'mage': 11, 'cleric': 53, 'thief': 22, 'warrior': 20},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_giant_strength, TAR_CHAR_DEFENSIVE, POS_STANDING,
                          None, SLOT(39), 20, 12, "", "You feel weaker.", ""))