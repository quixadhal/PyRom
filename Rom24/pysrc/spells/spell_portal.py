from const import SLOT, skill_type, register_spell
from db import create_object
from merc import target_name, IS_SET, ROOM_SAFE, ROOM_PRIVATE, ROOM_SOLITARY, ROOM_NO_RECALL, IS_NPC, LEVEL_HERO, \
    IMM_SUMMON, saves_spell, DAM_NONE, WEAR_HOLD, IS_IMMORTAL, ITEM_WARP_STONE, act, TO_CHAR, obj_index_hash, \
    OBJ_VNUM_PORTAL, TO_ROOM, POS_STANDING, TAR_IGNORE


def spell_portal(sn, level, ch, victim, target):
    victim = ch.get_char_world(target_name)

    if not victim \
            or victim == ch \
            or victim.in_room == None \
            or not ch.can_see_room(victim.in_room) \
            or IS_SET(victim.in_room.room_flags, ROOM_SAFE) \
            or IS_SET(victim.in_room.room_flags, ROOM_PRIVATE) \
            or IS_SET(victim.in_room.room_flags, ROOM_SOLITARY) \
            or IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL) \
            or IS_SET(ch.in_room.room_flags, ROOM_NO_RECALL) \
            or victim.level >= level + 3 \
            or (not IS_NPC(victim) and victim.level >= LEVEL_HERO) \
            or (IS_NPC(victim) and IS_SET(victim.imm_flags, IMM_SUMMON)) \
            or (IS_NPC(victim) and saves_spell(level, victim, DAM_NONE) ) \
            or (victim.is_clan() and not ch.is_same_clan(victim)):
        ch.send("You failed.\n")
        return

    stone = ch.get_eq(WEAR_HOLD)
    if not IS_IMMORTAL(ch) and (stone == None or stone.item_type != ITEM_WARP_STONE):
        ch.send("You lack the proper component for this spell.\n")
        return

    if stone and stone.item_type == ITEM_WARP_STONE:
        act("You draw upon the power of $p.", ch, stone, None, TO_CHAR)
        act("It flares brightly and vanishes! ", ch, stone, None, TO_CHAR)
        stone.extract()

    portal = create_object(obj_index_hash[OBJ_VNUM_PORTAL], 0)
    portal.timer = 2 + level // 25
    portal.value[3] = victim.in_room.vnum

    portal.to_room(ch.in_room)

    act("$p rises up from the ground.", ch, portal, None, TO_ROOM)
    act("$p rises up before you.", ch, portal, None, TO_CHAR)


register_spell(skill_type("portal",
                          {'mage': 35, 'cleric': 30, 'thief': 45, 'warrior': 40},
                          {'mage': 2, 'cleric': 2, 'thief': 4, 'warrior': 4},
                          spell_portal, TAR_IGNORE, POS_STANDING, None, SLOT(519),
                          100, 24, "", "!Portal!", ""))