import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_obj


def do_remove(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Remove what?\n")
        return
    obj = ch.get_obj_wear(arg)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    handler_obj.remove_obj(ch, obj.wear_loc, True)
    return


interp.register_command(interp.cmd_type('remove', do_remove, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
