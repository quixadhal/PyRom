import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks
import instance


def do_owhere(ch, argument):
    found = False
    number = 0
    max_found = 200

    if not argument:
        ch.send("Find what?\n")
        return
    for item in instance.items.values():
        if not ch.can_see_item(item) or not game_utils.is_name(argument, item.name) or ch.level < item.level:
            continue
        found = True
        number += 1
        content = item.in_item
        while content.in_item:
            content = content.in_item

        if content.in_living and ch.can_see(content.in_living) and content.in_living.in_room:
            ch.send("%3d) %s is carried by %s [[Room %d]]\n" % (
                number, item.short_descr, state_checks.PERS(content.in_living, ch), content.in_living.in_room.vnum ))
        elif content.in_room and ch.can_see_room(content.in_room):
            ch.send("%3d) %s is in %s [[Room %d]]\n" % (
                number, item.short_descr, content.in_room.name, content.in_room.vnum))
        else:
            ch.send("%3d) %s is somewhere\n" % (number, item.short_descr))

        if number >= max_found:
            break
    if not found:
        ch.send("Nothing like that in heaven or earth.\n")


interp.register_command(interp.cmd_type('owhere', do_owhere, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
