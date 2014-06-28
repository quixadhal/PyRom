from const import SLOT, skill_type
from db import create_object
from merc import target_name, IS_SET, ROOM_SAFE, ROOM_PRIVATE, ROOM_SOLITARY, ROOM_NO_RECALL, IS_NPC, LEVEL_HERO, \
    IMM_SUMMON, saves_spell, DAM_NONE, WEAR_HOLD, IS_IMMORTAL, ITEM_WARP_STONE, act, TO_CHAR, obj_index_hash, \
    OBJ_VNUM_PORTAL, TO_ROOM, TAR_IGNORE, POS_STANDING


def spell_nexus(sn, level, ch, victim, target):
    from_room = ch.in_room
    victim = ch.get_char_world(target_name)
    to_room = victim.in_room

    if not victim \
            or victim == ch \
            or not to_room \
            or not ch.can_see_room(to_room) or not ch.can_see_room(from_room) \
            or IS_SET(to_room.room_flags, ROOM_SAFE) \
            or IS_SET(from_room.room_flags, ROOM_SAFE) \
            or IS_SET(to_room.room_flags, ROOM_PRIVATE) \
            or IS_SET(to_room.room_flags, ROOM_SOLITARY) \
            or IS_SET(to_room.room_flags, ROOM_NO_RECALL) \
            or IS_SET(from_room.room_flags, ROOM_NO_RECALL) \
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

    # portal one */
    portal = create_object(obj_index_hash[OBJ_VNUM_PORTAL], 0)
    portal.timer = 1 + level // 10
    portal.value[3] = to_room.vnum

    portal.to_room(from_room)

    act("$p rises up from the ground.", ch, portal, None, TO_ROOM)
    act("$p rises up before you.", ch, portal, None, TO_CHAR)

    # no second portal if rooms are the same */
    if to_room == from_room:
        return

    # portal two */
    portal = create_object(obj_index_hash[OBJ_VNUM_PORTAL], 0)
    portal.timer = 1 + level // 10
    portal.value[3] = from_room.vnum

    portal.to_room(to_room)

    if to_room.people:
        act("$p rises up from the ground.", to_room.people[0], portal, None, TO_ROOM)
        act("$p rises up from the ground.", to_room.people[0], portal, None, TO_CHAR)

skill_type("nexus",
           { 'mage':40, 'cleric':35, 'thief':50, 'warrior':45 },
           { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 },
           spell_nexus, TAR_IGNORE, POS_STANDING, None, SLOT(520),
           150, 36, "", "!Nexus!", "")