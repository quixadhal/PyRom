import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import state_checks
from rom24 import instance


def do_owhere(ch, argument):
    found = False
    number = 0
    max_found = 200

    if not argument:
        ch.send("Find what?\n")
        return
    for item in instance.items.values():
        if (
            not ch.can_see_item(item)
            or not game_utils.is_name(argument, item.name)
            or ch.level < item.level
        ):
            continue
        found = True
        logger.info("owhere command found an item for %s: %s", argument, item)
        number += 1
        logger.debug("item: %s", item)
        content = item.in_item if item.in_item else item
        logger.debug("content: %s", content)
        logger.debug("content.in_room: %s", content.in_room)
        logger.debug("content.in_living: %s", content.in_living)

        # Check for our highest level of container to determine where it is in the world - this
        # logic goes through and if a mob had a sword in a bag, it would iterate from the bag to the mob
        # and then to the room around it to give a creature or a room.

        while content and content.in_item:
            content = content.in_item

        if (
            content.in_living
            and ch.can_see(content.in_living)
            and content.in_living.in_room
        ):
            ch.send(
                "%3d) %s (%s) is carried by %s [[Room %d]]\n"
                % (
                    number,
                    item.short_descr,
                    item.vnum,
                    state_checks.PERS(content.in_living, ch),
                    content.in_living.in_room.vnum,
                )
            )
        elif content.in_room and ch.can_see_room(content.in_room.instance_id):
            ch.send(
                "%3d) %s (%s) is in %s [[Room %d]]\n"
                % (
                    number,
                    item.short_descr,
                    item.vnum,
                    content.in_room.name,
                    content.in_room.vnum,
                )
            )
        else:
            ch.send(
                "%3d) %s (%s) is somewhere\n" % (number, item.short_descr, item.vnum)
            )

        if number >= max_found:
            break

    if not found:
        ch.send("Nothing like that in heaven or earth.\n")


interp.register_command(
    interp.cmd_type("owhere", do_owhere, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)
)
