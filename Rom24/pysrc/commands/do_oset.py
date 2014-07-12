import logging

logger = logging.getLogger()

import merc
import interp
import game_utils

def do_oset(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    arg3 = argument

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set obj <object> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    value0 value1 value2 value3 value4 (v1-v4)\n")
        ch.send("    extra wear level weight cost timer\n")
        return
    obj = ch.get_item_world(arg1)
    if not obj:
        ch.send("Nothing like that in heaven or earth.\n")
        return
    # Snarf the value (which need not be numeric).
    value = int(arg3) if arg3.isdigit else -1
    if value == -1:
        ch.do_oset("")
    # Set something.
    if arg2 == "value0" or arg2 == "v0":
        obj.value[0] = min(50, value)
        return
    if arg2 == "value1" or arg2 == "v1":
        obj.value[1] = value
        return
    if arg2 == "value2" or arg2 == "v2":
        obj.value[2] = value
        return
    if arg2 == "value3" or arg2 == "v3":
        obj.value[3] = value
        return
    if arg2 == "value4" or arg2 == "v4":
        obj.value[4] = value
        return
    if "extra".startswith(arg2):
        obj.extra_flags = value
        return
    if "wear".startswith(arg2):
        obj.wear_flags = value
        return
    if "level".startswith(arg2):
        obj.level = value
        return
    if "weight".startswith(arg2):
        obj.weight = value
        return
    if "cost".startswith(arg2):
        obj.cost = value
        return
    if "timer".startswith(arg2):
        obj.timer = value
        return

    # Generate usage message.
    ch.do_oset("")
    return


interp.register_command(interp.cmd_type('oset', do_oset, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1))
