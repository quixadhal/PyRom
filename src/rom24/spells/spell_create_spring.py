from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import object_creator


def spell_create_spring(sn, level, ch, victim, target):
    spring = object_creator.create_item(
        instance.item_templates[merc.OBJ_VNUM_SPRING], 0
    )
    spring.timer = level
    ch.in_room.put(spring)
    handler_game.act("$p flows from the ground.", ch, spring, None, merc.TO_ROOM)
    handler_game.act("$p flows from the ground.", ch, spring, None, merc.TO_CHAR)


const.register_spell(
    const.skill_type(
        "create spring",
        {"mage": 14, "cleric": 17, "thief": 23, "warrior": 20},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_create_spring,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(80),
        20,
        12,
        "",
        "!Create Spring!",
        "",
    )
)
