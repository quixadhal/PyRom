import const
import handler_game
import handler_magic
import handler_room
import merc
import state_checks


def spell_teleport(sn, level, ch, victim, target):
    if victim.in_room == None \
            or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_NO_RECALL) \
            or ( victim != ch and victim.imm_flags.is_set(merc.IMM_SUMMON)) \
            or ( not ch.is_npc() and victim.fighting is not None ) \
            or ( victim != ch \
                         and ( handler_magic.saves_spell(level - 5, victim, merc.DAM_OTHER))):
        ch.send("You failed.\n")
        return

    random_room = handler_room.get_random_room(victim)

    if victim != ch:
        victim.send("You have been teleported! \n")

    handler_game.act("$n vanishes! ", victim, None, None, merc.TO_ROOM)
    victim.in_room.get(victim)
    random_room.put(victim)
    handler_game.act("$n slowly fades into existence.", victim, None, None, merc.TO_ROOM)
    victim.do_look("auto")


const.register_spell(const.skill_type("teleport",
                          {'mage': 13, 'cleric': 22, 'thief': 25, 'warrior': 36},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_teleport, merc.TAR_CHAR_SELF, merc.POS_FIGHTING, None,
                          const.SLOT(2), 35, 12, "", "!Teleport!", ""))
