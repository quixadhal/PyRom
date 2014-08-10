import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_item


def do_remove(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Remove what?\n")
        return
    if arg == "all":
        for obj_id in ch.items:
            obj = merc.items.get(obj_id, None)
            if obj.wear_loc != merc.WEAR_NONE:
                ch.remove_item(obj.wear_loc, True)
        return
    else:
        obj = ch.get_item_wear(arg)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        ch.remove_item(obj.wear_loc, True)
        return


interp.register_command(interp.cmd_type('remove', do_remove, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
