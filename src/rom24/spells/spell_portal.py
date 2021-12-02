from rom24 import const
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import object_creator
from rom24 import state_checks


def spell_portal(sn, level, ch, victim, target):
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
        or (not victim.is_npc() and victim.level >= merc.LEVEL_HERO)
        or (victim.is_npc() and victim.imm_flags.is_set(merc.IMM_SUMMON))
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

    portal = object_creator.create_item(
        instance.item_templates[merc.OBJ_VNUM_PORTAL], 0
    )
    portal.timer = 2 + level // 25
    portal.value[3] = victim.in_room.instance_id

    ch.in_room.put(portal)

    handler_game.act("$p rises up from the ground.", ch, portal, None, merc.TO_ROOM)
    handler_game.act("$p rises up before you.", ch, portal, None, merc.TO_CHAR)


const.register_spell(
    const.skill_type(
        "portal",
        {"mage": 35, "cleric": 30, "thief": 45, "warrior": 40},
        {"mage": 2, "cleric": 2, "thief": 4, "warrior": 4},
        spell_portal,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(519),
        100,
        24,
        "",
        "!Portal!",
        "",
    )
)
