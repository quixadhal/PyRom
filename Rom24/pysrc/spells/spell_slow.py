from const import SLOT, skill_type
import const
from merc import is_affected, IS_AFFECTED, AFF_SLOW, act, TO_CHAR, saves_spell, DAM_OTHER, IS_SET, IMM_MAGIC, AFF_HASTE, \
    check_dispel, TO_ROOM, AFFECT_DATA, TO_AFFECTS, APPLY_DEX, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_slow(sn, level, ch, victim, target):
    if is_affected(victim, sn) or IS_AFFECTED(victim, AFF_SLOW):
        if victim == ch:
            ch.send("You can't move any slower! \n")
        else:
            act("$N can't get any slower than that.", ch, None, victim, TO_CHAR)
        return

    if saves_spell(level, victim, DAM_OTHER) or IS_SET(victim.imm_flags, IMM_MAGIC):
        if victim != ch:
            ch.send("Nothing seemed to happen.\n")
        victim.send("You feel momentarily lethargic.\n")
        return

    if IS_AFFECTED(victim, AFF_HASTE):
        if not check_dispel(level, victim, const.skill_table['haste']):
            if victim != ch:
                ch.send("Spell failed.\n")
            victim.send("You feel momentarily slower.\n")
            return
        act("$n is moving less quickly.", victim, None, None, TO_ROOM)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 2
    af.location = APPLY_DEX
    af.modifier = -1 - (level >= 18) - (level >= 25) - (level >= 32)
    af.bitvector = AFF_SLOW
    victim.affect_add(af)
    victim.send("You feel yourself slowing d o w n...\n")
    act("$n starts to move in slow motion.", victim, None, None, TO_ROOM)


skill_type("slow",
           { 'mage':23, 'cleric':30, 'thief':29, 'warrior':32 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_slow, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
           SLOT(515), 30, 12, "", "You feel yourself speed up.", "")