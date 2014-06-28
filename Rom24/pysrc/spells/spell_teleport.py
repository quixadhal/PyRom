from const import SLOT, skill_type, register_spell
from merc import IS_SET, ROOM_NO_RECALL, IMM_SUMMON, IS_NPC, saves_spell, DAM_OTHER, get_random_room, act, TO_ROOM, \
    POS_FIGHTING, TAR_CHAR_SELF


def spell_teleport(sn, level, ch, victim, target):
    if victim.in_room == None \
            or IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL) \
            or ( victim != ch and IS_SET(victim.imm_flags, IMM_SUMMON)) \
            or ( not IS_NPC(ch) and victim.fighting != None ) \
            or ( victim != ch \
                         and ( saves_spell(level - 5, victim, DAM_OTHER))):
        ch.send("You failed.\n")
        return

    pRoomIndex = get_random_room(victim)

    if victim != ch:
        victim.send("You have been teleported! \n")

    act("$n vanishes! ", victim, None, None, TO_ROOM)
    victim.from_room()
    victim.to_room(pRoomIndex)
    act("$n slowly fades into existence.", victim, None, None, TO_ROOM)
    victim.do_look("auto")


register_spell(skill_type("teleport",
                          {'mage': 13, 'cleric': 22, 'thief': 25, 'warrior': 36},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_teleport, TAR_CHAR_SELF, POS_FIGHTING, None,
                          SLOT(2), 35, 12, "", "!Teleport!", ""))