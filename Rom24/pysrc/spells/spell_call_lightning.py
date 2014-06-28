from merc import (weather_info, SKY_RAINING, dice, act, TO_ROOM, char_list, IS_NPC,
                  saves_spell, DAM_LIGHTNING, IS_OUTSIDE, IS_AWAKE, TAR_IGNORE, POS_FIGHTING)
from const import skill_type, SLOT


def spell_call_lightning(sn, level, ch, victim, target):
    if not IS_OUTSIDE(ch):
        ch.send("You must be out of doors.\n")
        return

    if weather_info.sky < SKY_RAINING:
        ch.send("You need bad weather.\n")
        return

    dam = dice(level // 2, 8)

    ch.send("Mota's lightning strikes your foes! \n")
    act("$n calls Mota's lightning to strike $s foes! ", ch, None, None, TO_ROOM)

    for vch in char_list[:]:
        if vch.in_room == None:
            continue
        if vch.in_room == ch.in_room:
            if vch is not ch and ( not IS_NPC(vch) if IS_NPC(ch) else IS_NPC(vch) ):
                damage(ch, vch, dam // 2 if saves_spell(level, vch, DAM_LIGHTNING) else dam, sn, DAM_LIGHTNING, True)
            continue

        if vch.in_room.area == ch.in_room.area and IS_OUTSIDE(vch) and IS_AWAKE(vch):
            vch.send("Lightning flashes in the sky.\n")


skill_type("call lightning",
           {'mage': 26, 'cleric': 18, 'thief': 31, 'warrior': 22},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_call_lightning, TAR_IGNORE, POS_FIGHTING, None,
           SLOT(6), 15, 12, "lightning bolt", "!Call Lightning!", "")