import random
from const import SLOT, skill_type
from effects import poison_effect
from fight import damage, is_safe_spell

from merc import act, TO_ROOM, TO_CHAR, dice, TARGET_ROOM, IS_NPC, saves_spell, DAM_POISON, TARGET_CHAR, POS_FIGHTING, \
    TAR_IGNORE


def spell_gas_breath(sn, level, ch, victim, target):
    act("$n breathes out a cloud of poisonous gas! ", ch, None, None, TO_ROOM)
    act("You breath out a cloud of poisonous gas.", ch, None, None, TO_CHAR)

    hpch = max(16, ch.hit)
    hp_dam = random.randint(hpch // 15 + 1, 8)
    dice_dam = dice(level, 12)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    poison_effect(ch.in_room, level, dam, TARGET_ROOM)

    for vch in ch.in_room.people[:]:
        if is_safe_spell(ch, vch, True) or (IS_NPC(ch) and IS_NPC(vch) and (ch.fighting == vch or vch.fighting == ch)):
            continue

        if saves_spell(level, vch, DAM_POISON):
            poison_effect(vch, level // 2, dam // 4, TARGET_CHAR)
            damage(ch, vch, dam // 2, sn, DAM_POISON, True)
        else:
            poison_effect(vch, level, dam, TARGET_CHAR)
            damage(ch, vch, dam, sn, DAM_POISON, True)

skill_type("gas breath",
           { 'mage':39, 'cleric':43, 'thief':47, 'warrior':50 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_gas_breath, TAR_IGNORE, POS_FIGHTING, None,
           SLOT(203), 175, 24, "blast of gas", "!Gas Breath!", "")