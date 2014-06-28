from const import SLOT, skill_type, register_spell
from merc import is_affected, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_AC, TO_ROOM, POS_STANDING, TAR_CHAR_DEFENSIVE


def spell_shield(sn, level, ch, victim, target):
    if is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already shielded from harm.\n")
        else:
            act("$N is already protected by a shield.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 8 + level
    af.location = APPLY_AC
    af.modifier = -20
    af.bitvector = 0
    victim.affect_add(af)
    act("$n is surrounded by a force shield.", victim, None, None, TO_ROOM)
    victim.send("You are surrounded by a force shield.\n")
    return


register_spell(skill_type("shield",
                          {'mage': 20, 'cleric': 35, 'thief': 35, 'warrior': 40},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_shield, TAR_CHAR_DEFENSIVE, POS_STANDING, None,
                          SLOT(67), 12, 18, "", "Your force shield shimmers then fades away.", ""))