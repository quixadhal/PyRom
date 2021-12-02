from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import object_creator
from rom24 import state_checks


def spell_continual_light(sn, level, ch, victim, target):
    if victim:  # do a glow on some object */
        light = ch.get_item_carry(victim, ch)

        if not light:
            ch.send("You don't see that here.\n")
            return

        if item.flags.glow:
            handler_game.act("$p is already glowing.", ch, light, None, merc.TO_CHAR)
            return

        item.flags.glow = True
        handler_game.act("$p glows with a white light.", ch, light, None, merc.TO_ALL)
        return

    light = object_creator.create_object(
        instance.item_templates[merc.OBJ_VNUM_LIGHT_BALL], 0
    )
    ch.in_room.put(light)
    handler_game.act(
        "$n twiddles $s thumbs and $p appears.", ch, light, None, merc.TO_ROOM
    )
    handler_game.act(
        "You twiddle your thumbs and $p appears.", ch, light, None, merc.TO_CHAR
    )


const.register_spell(
    const.skill_type(
        "continual light",
        {"mage": 6, "cleric": 4, "thief": 6, "warrior": 9},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_continual_light,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(57),
        7,
        12,
        "",
        "!Continual Light!",
        "",
    )
)
