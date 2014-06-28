from const import SLOT, skill_type
from merc import target_name, IS_SET, ROOM_SAFE, ROOM_PRIVATE, ROOM_SOLITARY, ROOM_NO_RECALL, IS_NPC, ACT_AGGRESSIVE, \
    LEVEL_IMMORTAL, IMM_SUMMON, PLR_NOSUMMON, saves_spell, DAM_OTHER, act, TO_ROOM, TO_VICT, POS_STANDING, TAR_IGNORE


def spell_summon(sn, level, ch, victim, target):
    victim = ch.get_char_world(target_name)
    if not victim \
            or victim == ch \
            or victim.in_room == None \
            or IS_SET(ch.in_room.room_flags, ROOM_SAFE) \
            or IS_SET(victim.in_room.room_flags, ROOM_SAFE) \
            or IS_SET(victim.in_room.room_flags, ROOM_PRIVATE) \
            or IS_SET(victim.in_room.room_flags, ROOM_SOLITARY) \
            or IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL) \
            or (IS_NPC(victim) and IS_SET(victim.act, ACT_AGGRESSIVE)) \
            or victim.level >= level + 3 \
            or (not IS_NPC(victim) and victim.level >= LEVEL_IMMORTAL) \
            or victim.fighting != None \
            or (IS_NPC(victim) and IS_SET(victim.imm_flags, IMM_SUMMON)) \
            or (IS_NPC(victim) and victim.pIndexData.pShop != None) \
            or (not IS_NPC(victim) and IS_SET(victim.act, PLR_NOSUMMON)) \
            or (IS_NPC(victim) and saves_spell(level, victim, DAM_OTHER)):
        ch.send("You failed.\n")
        return

    act("$n disappears suddenly.", victim, None, None, TO_ROOM)
    victim.from_room()
    victim.to_room(ch.in_room)
    act("$n arrives suddenly.", victim, None, None, TO_ROOM)
    act("$n has summoned you! ", ch, None, victim, TO_VICT)
    victim.do_look("auto")

skill_type("summon",
           { 'mage':24, 'cleric':12, 'thief':29, 'warrior':22 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_summon, TAR_IGNORE, POS_STANDING, None,
           SLOT(40), 50, 12, "", "!Summon!", "")