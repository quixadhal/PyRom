import logging

logger = logging.getLogger()

import game_utils
import handler_obj
import merc
import interp

def do_wear(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Wear, wield, or hold what?\n")
        return
    if arg == "all":
        for obj in ch.carrying[:]:
            if obj.wear_loc == merc.WEAR_NONE and ch.can_see_obj(obj):
                handler_obj.wear_obj( ch, obj, False )
        return
    else:
        obj = ch.get_obj_carry(arg, ch)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        handler_obj.wear_obj( ch, obj, True )
    return


interp.register_command(interp.cmd_type('wield', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('hold', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('wear', do_wear, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
