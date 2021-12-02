from rom24 import const
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import object_creator
from rom24 import state_checks


def spell_nexus(sn, level, ch, victim, target):
    from_room = ch.in_room
    victim = ch.get_char_world(handler_magic.target_name)
    to_room = victim.in_room

    if (
        not victim
        or victim == ch
        or not to_room
        or not ch.can_see_room(to_room.instance_id)
        or not ch.can_see_room(from_room.instance_id)
        or state_checks.IS_SET(to_room.room_flags, merc.ROOM_SAFE)
        or state_checks.IS_SET(from_room.room_flags, merc.ROOM_SAFE)
        or state_checks.IS_SET(to_room.room_flags, merc.ROOM_PRIVATE)
        or state_checks.IS_SET(to_room.room_flags, merc.ROOM_SOLITARY)
        or state_checks.IS_SET(to_room.room_flags, merc.ROOM_NO_RECALL)
        or state_checks.IS_SET(from_room.room_flags, merc.ROOM_NO_RECALL)
        or victim.level >= level + 3
        or (not victim.is_npc() and victim.level >= merc.LEVEL_HERO)
        or (victim.is_npc() and state_checks.IS_SET(victim.imm_flags, merc.IMM_SUMMON))
        or (victim.is_npc() and handler_magic.saves_spell(level, victim, merc.DAM_NONE))
        or (victim.is_clan() and not ch.is_same_clan(victim))
    ):
        ch.send("You failed.\n")
        return

    stone = ch.slots.held
    if not ch.is_immortal() and (
        stone is None or stone.item_type != merc.ITEM_WARP_STONE
    ):
        ch.send("You lack the proper component for this spell.\n")
        return

    if stone and stone.item_type == merc.ITEM_WARP_STONE:
        handler_game.act(
            "You draw upon the power of $p.", ch, stone, None, merc.TO_CHAR
        )
        handler_game.act(
            "It flares brightly and vanishes! ", ch, stone, None, merc.TO_CHAR
        )
        ch.unequip(stone.equipped_to)
        ch.get(stone)
        stone.extract()

    # portal one */
    portal = object_creator.create_item(
        instance.item_templates[merc.OBJ_VNUM_PORTAL], 0
    )
    portal.timer = 1 + level // 10
    portal.value[3] = to_room.instance_id

    from_room.put(portal)

    handler_game.act("$p rises up from the ground.", ch, portal, None, merc.TO_ROOM)
    handler_game.act("$p rises up before you.", ch, portal, None, merc.TO_CHAR)

    # no second portal if rooms are the same */
    if to_room == from_room:
        return

    # portal two */
    portal = object_creator.create_item(
        instance.item_templates[merc.OBJ_VNUM_PORTAL], 0
    )
    portal.timer = 1 + level // 10
    portal.value[3] = from_room.instance_id

    to_room.put(portal)

    if to_room.people:
        vch = instance.characters[to_room.people[0]]
        handler_game.act(
            "$p rises up from the ground.", vch, portal, None, merc.TO_ROOM
        )
        handler_game.act(
            "$p rises up from the ground.", vch, portal, None, merc.TO_CHAR
        )


const.register_spell(
    const.skill_type(
        "nexus",
        {"mage": 40, "cleric": 35, "thief": 50, "warrior": 45},
        {"mage": 2, "cleric": 2, "thief": 4, "warrior": 4},
        spell_nexus,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(520),
        150,
        36,
        "",
        "!Nexus!",
        "",
    )
)
