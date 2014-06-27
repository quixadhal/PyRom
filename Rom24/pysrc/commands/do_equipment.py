import logging

logger = logging.getLogger()

import merc
import interp


def do_equipment(ch, argument):
    ch.send("You are using:\n")
    found = False
    for iWear in range(merc.MAX_WEAR):
        obj = ch.get_eq(iWear)
        if not obj:
            continue

        ch.send(merc.where_name[iWear])
        if ch.can_see_obj(obj):
            ch.send(merc.format_obj_to_char(obj, ch, True) + "\n")
        else:
            ch.send("something.\n")
        found = True
    if not found:
        ch.send("Nothing.\n")


interp.register_command(interp.cmd_type('equipment', do_equipment, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
