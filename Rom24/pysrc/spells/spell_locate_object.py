import random
import const
import game_utils
import handler_magic
import merc
import state_checks


def spell_locate_object(sn, level, ch, victim, target):
    found = False
    number = 0
    max_found = 200 if state_checks.IS_IMMORTAL(ch) else 2 * level

    for obj in merc.object_list:
        if not ch.can_see_obj(obj) or not game_utils.is_name(handler_magic.target_name, obj.name) \
                or state_checks.IS_OBJ_STAT(obj, merc.ITEM_NOLOCATE) or random.randint(1, 99) > 2 * level \
                or ch.level < obj.level:
            continue

        found = True
        number = number + 1
        in_obj = obj
        while in_obj.in_obj:
            in_obj = in_obj.in_obj

        if in_obj.carried_by and ch.can_see(in_obj.carried_by):
            ch.send("one is carried by %s\n" % state_checks.PERS(in_obj.carried_by, ch))
        else:
            if state_checks.IS_IMMORTAL(ch) and in_obj.in_room != None:
                ch.send("one is in %s [Room %d]\n" % (in_obj.in_room.name, in_obj.in_room.vnum))
            else:
                ch.send("one is in %s\n" % ( "somewhere" if in_obj.in_room == None else in_obj.in_room.name ))

        if number >= max_found:
            break

    if not found:
        ch.send("Nothing like that in heaven or earth.\n")


const.register_spell(const.skill_type("locate object",
                          {'mage': 9, 'cleric': 15, 'thief': 11, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_locate_object, merc.TAR_IGNORE, merc.POS_STANDING, None,
                          const.SLOT(31), 20, 18, "", "!Locate Object!", ""))
