import logging

logger = logging.getLogger()

import game_utils
import handler_item
import merc
import interp

def do_wear(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Wear, wield, or hold what?\n")
        return
    if arg == "all":
        for item_id in ch.contents[:]:
            item = merc.items[item_id]
            if item.wear_loc == merc.WEAR_NONE and ch.can_see_item(item):
                handler_item.wear_item(ch, item, False)
        return
    else:
        item = ch.get_item_carry(arg, ch)
        if not item:
            ch.send("You do not have that item.\n")
            return
        handler_item.wear_item(ch, item, True)
    return


interp.register_command(interp.cmd_type('wield', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('hold', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('wear', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
