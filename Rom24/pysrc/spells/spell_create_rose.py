from const import SLOT, skill_type
from db import create_object
from merc import obj_index_hash, OBJ_VNUM_ROSE, act, TO_ROOM, POS_STANDING, TAR_IGNORE


def spell_create_rose(sn, level, ch, victim, target):
    rose = create_object(obj_index_hash[OBJ_VNUM_ROSE], 0)
    act("$n has created a beautiful red rose.", ch, rose, None, TO_ROOM)
    ch.send("You create a beautiful red rose.\n")
    rose.to_char(ch)


skill_type("create rose",
           {'mage': 16, 'cleric': 11, 'thief': 10, 'warrior': 24},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_create_rose, TAR_IGNORE, POS_STANDING, None,
           SLOT(511), 30, 12, "", "!Create Rose!", "")