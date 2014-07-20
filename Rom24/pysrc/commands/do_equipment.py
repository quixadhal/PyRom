import logging

logger = logging.getLogger()

import merc
import interp
import handler_item


def do_equipment(ch, argument):
    ch.send("You are using:\n")
    found = False
    for iWear in range(merc.MAX_WEAR):
        item = ch.get_eq(iWear)
        if not item:
            continue

        ch.send(merc.where_name[iWear])
        if ch.can_see_item(item):
            ch.send(handler_item.format_item_to_char(item, ch, True) + "\n")
        else:
            ch.send("something.\n")
        found = True
    if not found:
        ch.send("Nothing.\n")


interp.register_command(interp.cmd_type('equipment', do_equipment, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
