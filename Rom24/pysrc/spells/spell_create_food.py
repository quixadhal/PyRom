import const
import handler_game
import merc


def spell_create_food(sn, level, ch, victim, target):
    mushroom = instancer.create_object(merc.itemTemplate[merc.OBJ_VNUM_MUSHROOM], 0)
    mushroom.value[0] = level // 2
    mushroom.value[1] = level
    mushroom.to_environment(ch.in_room)
    handler_game.act("$p suddenly appears.", ch, mushroom, None, merc.TO_ROOM)
    handler_game.act("$p suddenly appears.", ch, mushroom, None, merc.TO_CHAR)
    return


const.register_spell(const.skill_type("create food",
                          {'mage': 10, 'cleric': 5, 'thief': 11, 'warrior': 12},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_create_food, merc.TAR_IGNORE, merc.POS_STANDING, None,
                          const.SLOT(12), 5, 12, "", "!Create Food!", ""))
