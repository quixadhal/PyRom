# RT calm spell stops all fighting in the room */
import random
from rom24 import const
from rom24 import fight
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_calm(sn, level, ch, victim, target):
    # get sum of all mobile levels in the room */
    count = 0
    mlevel = 0
    high_level = 0
    for vch_id in ch.in_room.people:
        vch = instance.characters[vch_id]
        if vch.position == merc.POS_FIGHTING:
            count = count + 1
        if vch.is_npc():
            mlevel += vch.level
        else:
            mlevel += vch.level // 2
        high_level = max(high_level, vch.level)

    # compute chance of stopping combat */
    chance = 4 * level - high_level + 2 * count

    if ch.is_immortal():  # always works */
        mlevel = 0

    if random.randint(0, chance) >= mlevel:  # hard to stop large fights */
        for vch_id in ch.in_room.people:
            vch = instance.characters[vch_id]
            if vch.is_npc() and (
                vch.imm_flags.is_set(merc.IMM_MAGIC) or vch.act.is_set(merc.ACT_UNDEAD)
            ):
                return

            if (
                vch.is_affected(merc.AFF_CALM)
                or vch.is_affected(merc.AFF_BERSERK)
                or vch.is_affected("frenzy")
            ):
                return

            vch.send("A wave of calm passes over you.\n")

            if vch.fighting or vch.position == merc.POS_FIGHTING:
                fight.stop_fighting(vch, False)
            af = handler_game.AFFECT_DATA()
            af.where = merc.TO_AFFECTS
            af.type = sn
            af.level = level
            af.duration = level // 4
            af.location = merc.APPLY_HITROLL
            if not vch.is_npc():
                af.modifier = -5
            else:
                af.modifier = -2
            af.bitvector = merc.AFF_CALM
            vch.affect_add(af)

            af.location = merc.APPLY_DAMROLL
            vch.affect_add(af)


const.register_spell(
    const.skill_type(
        "calm",
        {"mage": 48, "cleric": 16, "thief": 50, "warrior": 20},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_calm,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(509),
        30,
        12,
        "",
        "You have lost your peace of mind.",
        "",
    )
)
