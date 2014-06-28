from const import skill_type, SLOT
from db import create_object
from merc import IS_OBJ_STAT, ITEM_GLOW, act, TO_CHAR, SET_BIT, TO_ALL, obj_index_hash, OBJ_VNUM_LIGHT_BALL, TO_ROOM, \
    TAR_IGNORE, POS_STANDING


def spell_continual_light(sn, level, ch, victim, target):
    if victim:  # do a glow on some object */
        light = ch.get_obj_carry(victim, ch)

        if not light:
            ch.send("You don't see that here.\n")
            return

        if IS_OBJ_STAT(light, ITEM_GLOW):
            act("$p is already glowing.", ch, light, None, TO_CHAR)
            return

        SET_BIT(light.extra_flags, ITEM_GLOW)
        act("$p glows with a white light.", ch, light, None, TO_ALL)
        return

    light = create_object(obj_index_hash[OBJ_VNUM_LIGHT_BALL], 0)
    light.to_room(ch.in_room)
    act("$n twiddles $s thumbs and $p appears.", ch, light, None, TO_ROOM)
    act("You twiddle your thumbs and $p appears.", ch, light, None, TO_CHAR)


skill_type("continual light",
           {'mage': 6, 'cleric': 4, 'thief': 6, 'warrior': 9},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_continual_light, TAR_IGNORE, POS_STANDING, None,
           SLOT(57), 7, 12, "", "!Continual Light!", "")