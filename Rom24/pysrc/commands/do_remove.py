import merc
import interp


def do_remove(self, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Remove what?\n")
        return
    obj = ch.get_obj_wear(arg)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    merc.remove_obj(ch, obj.wear_loc, True)
    return

interp.cmd_table['remove'] = interp.cmd_type('remove', do_remove, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)