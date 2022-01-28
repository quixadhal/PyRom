import random

from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import object_creator
from rom24 import state_checks


def spell_floating_disc(sn, level, ch, victim, target):
    floating = ch.slots.float
    if floating and floating.flags.no_remove:
        handler_game.act("You can't remove $p.", ch, floating, None, merc.TO_CHAR)
        return

    disc = object_creator.create_item(instance.item_templates[merc.OBJ_VNUM_DISC], 0)
    disc.value[0] = ch.level * 10  # 10 pounds per level capacity */
    disc.value[3] = ch.level * 5  # 5 pounds per level max per item */
    disc.timer = ch.level * 2 - random.randint(0, level // 2)

    handler_game.act(
        "$n has created a floating black disc.", ch, None, None, merc.TO_ROOM
    )
    ch.send("You create a floating disc.\n")
    ch.put(disc)
    ch.equip(disc, True, True)


const.register_spell(
    const.skill_type(
        "floating disc",
        {"mage": 4, "cleric": 10, "thief": 7, "warrior": 16},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_floating_disc,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(522),
        40,
        24,
        "",
        "!Floating disc!",
        "",
    )
)
