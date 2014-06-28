from const import SLOT, skill_type, skill_table
from merc import is_affected, IS_AFFECTED, AFF_HASTE, IS_SET, OFF_FAST, act, TO_CHAR, AFF_SLOW, check_dispel, TO_ROOM, \
    TO_AFFECTS, APPLY_DEX, POS_FIGHTING, TAR_CHAR_DEFENSIVE


def spell_haste(sn, level, ch, victim, target):
    # RT haste spell */
    if is_affected(victim, sn) or IS_AFFECTED(victim, AFF_HASTE) or IS_SET(victim.off_flags, OFF_FAST):
        if victim == ch:
            ch.send("You can't move any faster! \n")
        else:
            act("$N is already moving as fast as $E can.", ch, None, victim, TO_CHAR)
        return
    if IS_AFFECTED(victim, AFF_SLOW):
        if not check_dispel(level, victim, skill_table["slow"]):
            if victim != ch:
                ch.send("Spell failed.\n")
            victim.send("You feel momentarily faster.\n")
            return
        act("$n is moving less slowly.", victim, None, None, TO_ROOM)
        return

    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    if victim == ch:
        af.duration = level // 2
    else:
        af.duration = level // 4
    af.location = APPLY_DEX
    af.modifier = 1 + (level >= 18) + (level >= 25) + (level >= 32)
    af.bitvector = AFF_HASTE
    victim.affect_add(af)
    victim.send("You feel yourself moving more quickly.\n")
    act("$n is moving more quickly.", victim, None, None, TO_ROOM)
    if ch != victim:
        ch.send("Ok.\n")

skill_type("haste",
           { 'mage':21, 'cleric':53, 'thief':26, 'warrior':29 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_haste, TAR_CHAR_DEFENSIVE, POS_FIGHTING,
           None, SLOT(502), 30, 12, "", "You feel yourself slow down.", "")