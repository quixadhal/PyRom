import random
from const import SLOT, skill_type

from merc import IS_IMMORTAL, object_list, is_name, target_name, IS_OBJ_STAT, ITEM_NOLOCATE, PERS, POS_STANDING, \
    TAR_IGNORE


def spell_locate_object(sn, level, ch, victim, target):
    found = False
    number = 0
    max_found = 200 if IS_IMMORTAL(ch) else 2 * level

    for obj in object_list:
        if not ch.can_see_obj(obj) or not is_name(target_name, obj.name) \
                or IS_OBJ_STAT(obj, ITEM_NOLOCATE) or random.randint(1, 99) > 2 * level \
                or ch.level < obj.level:
            continue

        found = True
        number = number + 1
        in_obj = obj
        while in_obj.in_obj:
            in_obj = in_obj.in_obj

        if in_obj.carried_by and ch.can_see(in_obj.carried_by):
            ch.send("one is carried by %s\n" % PERS(in_obj.carried_by, ch))
        else:
            if IS_IMMORTAL(ch) and in_obj.in_room != None:
                ch.send("one is in %s [Room %d]\n" % (in_obj.in_room.name, in_obj.in_room.vnum))
            else:
                ch.send("one is in %s\n" % ( "somewhere" if in_obj.in_room == None else in_obj.in_room.name ))

        if number >= max_found:
            break

    if not found:
        ch.send("Nothing like that in heaven or earth.\n")

skill_type("locate object",
           { 'mage':9, 'cleric':15, 'thief':11, 'warrior':53 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_locate_object, TAR_IGNORE, POS_STANDING, None,
           SLOT(31), 20, 18, "", "!Locate Object!", "")