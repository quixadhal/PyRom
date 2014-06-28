import random
from const import SLOT, skill_type
from effects import cold_effect
from fight import damage, is_safe_spell

from merc import act, TO_NOTVICT, TO_VICT, TO_CHAR, dice, TARGET_ROOM, IS_NPC, saves_spell, DAM_COLD, TARGET_CHAR, \
    POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_frost_breath(sn, level, ch, victim, target):
    act("$n breathes out a freezing cone of frost! ", ch, None, victim, TO_NOTVICT)
    act("$n breathes a freezing cone of frost over you! ", ch, None, victim, TO_VICT)
    act("You breath out a cone of frost.", ch, None, None, TO_CHAR)

    hpch = max(12, ch.hit)
    hp_dam = random.randint(hpch // 11 + 1, hpch // 6)
    dice_dam = dice(level, 16)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    cold_effect(victim.in_room, level, dam // 2, TARGET_ROOM)

    for vch in victim.in_room.people[:]:
        if is_safe_spell(ch, vch, True) or (IS_NPC(vch) and IS_NPC(ch) and (ch.fighting != vch or vch.fighting != ch)):
            continue

        if vch == victim:  # full damage */
            if saves_spell(level, vch, DAM_COLD):
                cold_effect(vch, level // 2, dam // 4, TARGET_CHAR)
                damage(ch, vch, dam // 2, sn, DAM_COLD, True)
            else:
                cold_effect(vch, level, dam, TARGET_CHAR)
                damage(ch, vch, dam, sn, DAM_COLD, True)
        else:
            if saves_spell(level - 2, vch, DAM_COLD):
                cold_effect(vch, level // 4, dam // 8, TARGET_CHAR)
                damage(ch, vch, dam // 4, sn, DAM_COLD, True)
            else:
                cold_effect(vch, level // 2, dam // 4, TARGET_CHAR)
                damage(ch, vch, dam // 2, sn, DAM_COLD, True)

skill_type("frost breath",
           { 'mage':34, 'cleric':36, 'thief':38, 'warrior':40 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_frost_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(202), 125, 24, "blast of frost", "!Frost Breath!", "")