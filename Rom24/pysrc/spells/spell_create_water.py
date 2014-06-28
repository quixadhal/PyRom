import const
import handler_game
import merc


def spell_create_water(sn, level, ch, victim, target):
    obj = victim
    if obj.item_type != merc.ITEM_DRINK_CON:
        ch.send("It is unable to hold water.\n")
        return

    if obj.value[2] != LIQ_WATER and obj.value[1] != 0:
        ch.send("It contains some other liquid.\n")
        return

    water = min(level * (4 if handler_game.weather_info.sky >= merc.SKY_RAINING else 2), obj.value[0] - obj.value[1])

    if water > 0:
        obj.value[2] = LIQ_WATER
        obj.value[1] += water
        if "water" in obj.name.lower():
            obj.name = "%s water" % obj.name

        handler_game.act("$p is filled.", ch, obj, None, merc.TO_CHAR)


const.register_spell(const.skill_type("create water",
                          {'mage': 8, 'cleric': 3, 'thief': 12, 'warrior': 11},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_create_water, merc.TAR_OBJ_INV, merc.POS_STANDING, None,
                          const.SLOT(13), 5, 12, "", "!Create Water!", ""))
