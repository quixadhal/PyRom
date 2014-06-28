from const import SLOT, skill_type
from merc import target_name, IS_SET, ROOM_SAFE, ROOM_PRIVATE, ROOM_SOLITARY, ROOM_NO_RECALL, IS_NPC, LEVEL_HERO, \
    IMM_SUMMON, saves_spell, DAM_OTHER, act, TO_ROOM, TAR_IGNORE, POS_FIGHTING


def spell_gate(sn, level, ch, victim, target):
    # RT ROM-style gate */
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
            or (victim.is_clan() and not ch.is_same_clan(victim)) \
            or (not IS_NPC(victim) and victim.level >= LEVEL_HERO) \
            or (IS_NPC(victim) and IS_SET(victim.imm_flags, IMM_SUMMON)) \
            or (IS_NPC(victim) and saves_spell(level, victim, DAM_OTHER) ):
        ch.send("You failed.\n")
        return

    if ch.pet and ch.in_room == ch.pet.in_room:
        gate_pet = True
    else:
        gate_pet = False

    act("$n steps through a gate and vanishes.", ch, None, None, TO_ROOM)
    ch.send("You step through a gate and vanish.\n")
    ch.from_room()
    ch.to_room(victim.in_room)

    act("$n has arrived through a gate.", ch, None, None, TO_ROOM)
    ch.do_look("auto")

    if gate_pet:
        act("$n steps through a gate and vanishes.", ch.pet, None, None, TO_ROOM)
        ch.pet.send("You step through a gate and vanish.\n")
        ch.pet.from_room()
        ch.pet.to_room(victim.in_room)
        act("$n has arrived through a gate.", ch.pet, None, None, TO_ROOM)
        ch.pet.do_look("auto")

skill_type("gate",
           { 'mage':27, 'cleric':17, 'thief':32, 'warrior':28 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_gate, TAR_IGNORE, POS_FIGHTING, None, SLOT(83),
           80, 12, "", "!Gate!", "")