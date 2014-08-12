import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_remove(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Remove what?\n")
        return
    if arg == "all":
        for loc, item_id in ch.equipped.items():
            if item_id:
                ch.unequip(loc, True)
        return
    else:
        item = ch.get_item_wear(arg)
        if not item:
            ch.send("You are not wearing %s.\n" % arg)
            return
        ch.unequip(item.equipped_to, True)
        return


interp.register_command(interp.cmd_type('remove', do_remove, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
