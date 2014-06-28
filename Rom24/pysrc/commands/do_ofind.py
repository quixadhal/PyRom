import logging

logger = logging.getLogger()

import merc
import interp


def do_ofind(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Find what?\n")
        return

    fAll = False  # !str_cmp( arg, "all" )
    found = False
    nMatch = 0

    # Yeah, so iterating over all vnum's takes 10,000 loops.
    # Get_obj_index is fast, and I don't feel like threading another link.
    # Do you?
    # -- Furey
    for pObjIndex in merc.obj_index_hash.values():
        if fAll or merc.is_name(arg, pObjIndex.name):
            found = True
            ch.send("[%5d] %s(%s)\n" % (pObjIndex.vnum, pObjIndex.short_descr, pObjIndex.name))
    if not found:
        ch.send("No objects by that name.\n")
    return


interp.register_command(interp.cmd_type('ofind', do_ofind, merc.POS_DEAD, merc.L4, merc.LOG_NORMAL, 1))
