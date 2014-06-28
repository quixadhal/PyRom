from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_FLYING, act, TO_CHAR, TO_AFFECTS, TO_ROOM, POS_STANDING, TAR_CHAR_DEFENSIVE


def spell_fly(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_FLYING):
        if victim == ch:
            ch.send("You are already airborne.\n")
        else:
            act("$N doesn't need your help to fly.", ch, None, victim, TO_CHAR)
        return
    af = AFFECDT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level + 3
    af.location = 0
    af.modifier = 0
    af.bitvector = AFF_FLYING
    victim.affect_add(af)
    victim.send("Your feet rise off the ground.\n")
    act("$n's feet rise off the ground.", victim, None, None, TO_ROOM)
    return


register_spell(skill_type("fly",
                          {'mage': 10, 'cleric': 18, 'thief': 20, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fly, TAR_CHAR_DEFENSIVE, POS_STANDING, None,
                          SLOT(56), 10, 18, "", "You slowly float to the ground.", ""))