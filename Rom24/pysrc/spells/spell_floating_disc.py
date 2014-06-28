import random
from const import SLOT, skill_type
from db import create_object

from merc import WEAR_FLOAT, IS_OBJ_STAT, ITEM_NOREMOVE, act, TO_CHAR, obj_index_hash, OBJ_VNUM_DISC, TO_ROOM, wear_obj, \
    POS_STANDING, TAR_IGNORE


def spell_floating_disc(sn, level, ch, victim, target):
    floating = ch.get_eq(WEAR_FLOAT)
    if floating and IS_OBJ_STAT(floating, ITEM_NOREMOVE):
        act("You can't remove $p.", ch, floating, None, TO_CHAR)
        return

    disc = create_object(obj_index_hash[OBJ_VNUM_DISC], 0)
    disc.value[0] = ch.level * 10  # 10 pounds per level capacity */
    disc.value[3] = ch.level * 5  # 5 pounds per level max per item */
    disc.timer = ch.level * 2 - random.randint(0, level // 2)

    act("$n has created a floating black disc.", ch, None, None, TO_ROOM)
    ch.send("You create a floating disc.\n")
    disc.to_char(ch)
    wear_obj(ch, disc, True)

skill_type("floating disc",
           { 'mage':4, 'cleric':10, 'thief':7, 'warrior':16 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_floating_disc, TAR_IGNORE, POS_STANDING, None,
           SLOT(522), 40, 24, "", "!Floating disc!", "")