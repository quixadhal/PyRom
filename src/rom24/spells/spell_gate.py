from rom24 import const
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_gate(sn, level, ch, victim, target):
    # RT ROM-style gate */
    victim = ch.get_char_world(handler_magic.target_name)
    if (
        not victim
        or victim == ch
        or victim.in_room == None
        or not ch.can_see_room(victim.in_room.instance_id)
        or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_SAFE)
        or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_PRIVATE)
        or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_SOLITARY)
        or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_NO_RECALL)
        or state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_NO_RECALL)
        or victim.level >= level + 3
        or (victim.is_clan() and not ch.is_same_clan(victim))
        or (not victim.is_npc() and victim.level >= merc.LEVEL_HERO)
        or (victim.is_npc() and victim.imm_flags.is_set(merc.IMM_SUMMON))
        or (
            victim.is_npc() and handler_magic.saves_spell(level, victim, merc.DAM_OTHER)
        )
    ):
        ch.send("You failed.\n")
        return

    if ch.pet and ch.in_room == ch.pet.in_room:
        gate_pet = True
    else:
        gate_pet = False

    handler_game.act(
        "$n steps through a gate and vanishes.", ch, None, None, merc.TO_ROOM
    )
    ch.send("You step through a gate and vanish.\n")
    ch.in_room.get(ch)
    victim.in_room.put(ch)

    handler_game.act("$n has arrived through a gate.", ch, None, None, merc.TO_ROOM)
    ch.do_look("auto")

    if gate_pet:
        handler_game.act(
            "$n steps through a gate and vanishes.", ch.pet, None, None, merc.TO_ROOM
        )
        instance.characters[ch.pet].send("You step through a gate and vanish.\n")
        instance.characters[ch.pet].in_room.get(instance.characters[ch.pet])
        ch.in_room.put(instance.characters[ch.pet])
        handler_game.act(
            "$n has arrived through a gate.", ch.pet, None, None, merc.TO_ROOM
        )
        ch.pet.do_look("auto")


const.register_spell(
    const.skill_type(
        "gate",
        {"mage": 27, "cleric": 17, "thief": 32, "warrior": 28},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_gate,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(83),
        80,
        12,
        "",
        "!Gate!",
        "",
    )
)
