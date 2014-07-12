import logging


logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks

def do_owhere(ch, argument):
    found = False
    number = 0
    max_found = 200

    if not argument:
        ch.send("Find what?\n")
        return
    for obj in merc.object_list:
        if not ch.can_see_item(obj) or not game_utils.is_name(argument, obj.name) or ch.level < obj.level:
            continue
        found = True
        number += 1
        in_item = obj.in_item
        while in_item.in_item:
            in_item = in_item.in_item

        if in_item.carried_by and ch.can_see(in_item.carried_by) and in_item.carried_by.in_room:
            ch.send("%3d) %s is carried by %s [Room %d]\n" % (
                number, obj.short_descr, state_checks.PERS(in_item.carried_by, ch), in_item.carried_by.in_room.vnum ))
        elif in_item.in_room and ch.can_see_room(in_item.in_room):
            ch.send("%3d) %s is in %s [Room %d]\n" % (
                number, obj.short_descr, in_item.in_room.name, in_item.in_room.vnum))
        else:
            ch.send("%3d) %s is somewhere\n" % (number, obj.short_descr))

        if number >= max_found:
            break
    if not found:
        ch.send("Nothing like that in heaven or earth.\n")


interp.register_command(interp.cmd_type('owhere', do_owhere, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
