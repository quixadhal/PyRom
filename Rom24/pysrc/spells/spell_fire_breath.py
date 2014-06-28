import random

from const import SLOT, skill_type, register_spell
from effects import fire_effect
from fight import damage, is_safe_spell
from merc import act, TO_NOTVICT, TO_VICT, TO_CHAR, dice, TARGET_ROOM, IS_NPC, saves_spell, DAM_FIRE, TARGET_CHAR, \
    POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_fire_breath(sn, level, ch, victim, target):
    act("$n breathes forth a cone of fire.", ch, None, victim, TO_NOTVICT)
    act("$n breathes a cone of hot fire over you! ", ch, None, victim, TO_VICT)
    act("You breath forth a cone of fire.", ch, None, None, TO_CHAR)

    hpch = max(10, ch.hit)
    hp_dam = random.randint(hpch // 9 + 1, hpch // 5)
    dice_dam = dice(level, 20)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    fire_effect(victim.in_room, level, dam // 2, TARGET_ROOM)

    for vch in victim.in_room.people[:]:
        if is_safe_spell(ch, vch, True) or (IS_NPC(vch) and IS_NPC(ch) and (ch.fighting != vch or vch.fighting != ch)):
            continue

        if vch == victim:  # full damage */
            if saves_spell(level, vch, DAM_FIRE):
                fire_effect(vch, level // 2, dam // 4, TARGET_CHAR)
                damage(ch, vch, dam // 2, sn, DAM_FIRE, True)
            else:
                fire_effect(vch, level, dam, TARGET_CHAR)
                damage(ch, vch, dam, sn, DAM_FIRE, True)
        else:  # partial damage */
            if saves_spell(level - 2, vch, DAM_FIRE):
                fire_effect(vch, level // 4, dam // 8, TARGET_CHAR)
                damage(ch, vch, dam // 4, sn, DAM_FIRE, True)
            else:
                fire_effect(vch, level // 2, dam // 4, TARGET_CHAR)
                damage(ch, vch, dam // 2, sn, DAM_FIRE, True)


register_spell(skill_type("fire breath",
                          {'mage': 40, 'cleric': 45, 'thief': 50, 'warrior': 51},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fire_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(201), 200, 24, "blast of flame", "The smoke leaves your eyes.", ""))