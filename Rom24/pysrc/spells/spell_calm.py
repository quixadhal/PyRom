import random

from merc import (IS_SET, IMM_MAGIC, ACT_UNDEAD, IS_AFFECTED,
                  AFF_CALM, AFF_BERSERK, is_affected, POS_FIGHTING, TO_AFFECTS,
                  APPLY_HITROLL, IS_NPC, APPLY_DAMROLL, TAR_IGNORE, IS_IMMORTAL)
from fight import stop_fighting
from const import register_spell, skill_type, skill_table, SLOT



# RT calm spell stops all fighting in the room */
def spell_calm(sn, level, ch, victim, target):
    # get sum of all mobile levels in the room */
    count = 0
    mlevel = 0
    high_level = 0
    for vch in ch.in_room.people:
        if vch.position == POS_FIGHTING:
            count = count + 1
        if IS_NPC(vch):
            mlevel += vch.level
        else:
            mlevel += vch.level // 2
        high_level = max(high_level, vch.level)

    # compute chance of stopping combat */
    chance = 4 * level - high_level + 2 * count

    if IS_IMMORTAL(ch):  # always works */
        mlevel = 0

    if random.randint(0, chance) >= mlevel:  # hard to stop large fights */
        for vch in ch.in_room.people:
            if IS_NPC(vch) and (IS_SET(vch.imm_flags, IMM_MAGIC) \
                                        or IS_SET(vch.act, ACT_UNDEAD)):
                return

            if IS_AFFECTED(vch, AFF_CALM) or IS_AFFECTED(vch, AFF_BERSERK) \
                    or is_affected(vch, skill_table['frenzy']):
                return

            vch.send("A wave of calm passes over you.\n")

            if vch.fighting or vch.position == POS_FIGHTING:
                stop_fighting(vch, False)

            af.where = TO_AFFECTS
            af.type = sn
            af.level = level
            af.duration = level // 4
            af.location = APPLY_HITROLL
            if not IS_NPC(vch):
                af.modifier = -5
            else:
                af.modifier = -2
            af.bitvector = AFF_CALM
            vch.affect_add(af)

            af.location = APPLY_DAMROLL
            vch.affect_add(af)


register_spell(skill_type("calm",
                          {'mage': 48, 'cleric': 16, 'thief': 50, 'warrior': 20},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_calm, TAR_IGNORE, POS_FIGHTING, None, SLOT(509),
                          30, 12, "", "You have lost your peace of mind.", ""))