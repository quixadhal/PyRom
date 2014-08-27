import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import instance


def do_ofind(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Find what?\n")
        return

    if arg.isdigit():
        item_id = instance.instances_by_item[arg][argument]
    fAll = False  # !str_cmp( arg, "all" )
    found = False
    nMatch = 0

    # Yeah, so iterating over all vnum's takes 10,000 loops.
    # Get_obj_index is fast, and I don't feel like threading another link.
    # Do you?
    # -- Furey
    for objTemplate in instance.item_templates.values():
        if fAll or game_utils.is_name(arg, objTemplate.name):
            found = True
            ch.send("[[%5d]] %s(%s)\n" % (objTemplate.vnum, objTemplate.short_descr, objTemplate.name))
    if not found:
        ch.send("No objects by that name.\n")
    return


interp.register_command(interp.cmd_type('ofind', do_ofind, merc.POS_DEAD, merc.L4, merc.LOG_NORMAL, 1))
