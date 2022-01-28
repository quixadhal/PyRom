from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import object_creator


def spell_create_food(sn, level, ch, victim, target):
    mushroom = object_creator.create_item(
        instance.item_templates[merc.OBJ_VNUM_MUSHROOM], 0
    )
    mushroom.value[0] = level // 2
    mushroom.value[1] = level
    ch.in_room.put(mushroom)
    handler_game.act("$p suddenly appears.", ch, mushroom, None, merc.TO_ROOM)
    handler_game.act("$p suddenly appears.", ch, mushroom, None, merc.TO_CHAR)
    return


const.register_spell(
    const.skill_type(
        "create food",
        {"mage": 10, "cleric": 5, "thief": 11, "warrior": 12},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_create_food,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(12),
        5,
        12,
        "",
        "!Create Food!",
        "",
    )
)
