from const import SLOT, skill_type
from db import create_object
from merc import obj_index_hash, OBJ_VNUM_SPRING, act, TO_ROOM, TO_CHAR, POS_STANDING, TAR_IGNORE


def spell_create_spring(sn, level, ch, victim, target):
    spring = create_object(obj_index_hash[OBJ_VNUM_SPRING], 0)
    spring.timer = level
    spring.to_room(ch.in_room)
    act("$p flows from the ground.", ch, spring, None, TO_ROOM)
    act("$p flows from the ground.", ch, spring, None, TO_CHAR)


skill_type("create spring",
           {'mage': 14, 'cleric': 17, 'thief': 23, 'warrior': 20},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_create_spring, TAR_IGNORE, POS_STANDING, None,
           SLOT(80), 20, 12, "", "!Create Spring!", "")