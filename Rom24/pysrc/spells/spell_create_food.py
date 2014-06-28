from const import SLOT, skill_type, register_spell
from db import create_object
from merc import obj_index_hash, OBJ_VNUM_MUSHROOM, act, TO_ROOM, TO_CHAR, POS_STANDING, TAR_IGNORE


def spell_create_food(sn, level, ch, victim, target):
    mushroom = create_object(obj_index_hash[OBJ_VNUM_MUSHROOM], 0)
    mushroom.value[0] = level // 2
    mushroom.value[1] = level
    mushroom.to_room(ch.in_room)
    act("$p suddenly appears.", ch, mushroom, None, TO_ROOM)
    act("$p suddenly appears.", ch, mushroom, None, TO_CHAR)
    return


register_spell(skill_type("create food",
                          {'mage': 10, 'cleric': 5, 'thief': 11, 'warrior': 12},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_create_food, TAR_IGNORE, POS_STANDING, None,
                          SLOT(12), 5, 12, "", "!Create Food!", ""))