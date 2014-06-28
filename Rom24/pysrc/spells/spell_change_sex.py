import random

from const import SLOT, skill_type, register_spell
from merc import is_affected, act, TO_CHAR, saves_spell, DAM_OTHER, AFFECT_DATA, TO_AFFECTS, APPLY_SEX, TO_ROOM, \
    TAR_CHAR_DEFENSIVE, POS_FIGHTING


def spell_change_sex(sn, level, ch, victim, target):
    if is_affected(victim, sn):
        if victim == ch:
            ch.send("You've already been changed.\n")
        else:
            act("$N has already had $s(?) sex changed.", ch, None, victim, TO_CHAR)
        return

    if saves_spell(level, victim, DAM_OTHER):
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = APPLY_SEX

    while af.modifier == 0:
        af.modifier = random.randint(0, 2) - victim.sex

    af.bitvector = 0
    victim.affect_add(af)
    victim.send("You feel different.\n")
    act("$n doesn't look like $mself anymore...", victim, None, None, TO_ROOM)


register_spell(skill_type("change sex",
                          {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_change_sex, TAR_CHAR_DEFENSIVE, POS_FIGHTING,
                          None, SLOT(82), 15, 12, "", "Your body feels familiar again.", ""))