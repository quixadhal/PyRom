from const import SLOT, skill_type
from fight import stop_fighting
from merc import IS_NPC, ROOM_VNUM_TEMPLE, room_index_hash, IS_SET, ROOM_NO_RECALL, IS_AFFECTED, AFF_CURSE, act, TO_ROOM, \
    POS_RESTING, TAR_CHAR_SELF


def spell_word_of_recall(sn, level, ch, victim, target):
    # RT recall spell is back */
    if IS_NPC(victim):
        return

    if ROOM_VNUM_TEMPLE not in room_index_hash:
        victim.send("You are completely lost.\n")
        return
    location = room_index_hash[ROOM_VNUM_TEMPLE]

    if IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL) or IS_AFFECTED(victim, AFF_CURSE):
        victim.send("Spell failed.\n")
        return

    if victim.fighting:
        stop_fighting(victim, True)

    ch.move = move // 2
    act("$n disappears.", victim, None, None, TO_ROOM)
    victim.from_room()
    victim.to_room(location)
    act("$n appears in the room.", victim, None, None, TO_ROOM)
    victim.do_look("auto")

skill_type("word of recall",
           { 'mage':32, 'cleric':28, 'thief':40, 'warrior':30 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_word_of_recall, TAR_CHAR_SELF, POS_RESTING, None,
           SLOT(42), 5, 12, "", "!Word of Recall!", "") # * Dragon breath */