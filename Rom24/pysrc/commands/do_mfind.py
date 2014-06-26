import merc
import interp


def do_mfind(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Find whom?\n")
        return
    fAll  = False # !str_cmp( arg, "all" ) */
    found = False
    nMatch  = 0
     #* Yeah, so iterating over all vnum's takes 10,000 loops.
     #* Get_mob_index is fast, and I don't feel like threading another link.
     #* Do you?
     # -- Furey
    for pMobIndex in merc.mob_index_hash.values():
        if fAll or merc.is_name(arg, pMobIndex.player_name):
            found = True
            ch.send("[%5d] %s\n" % (pMobIndex.vnum, pMobIndex.short_descr))
    if not found:
        ch.send("No mobiles by that name.\n")
    return

interp.cmd_table['mfind'] = interp.cmd_type('mfind', do_mfind, merc.POS_DEAD, merc.L4, merc.LOG_NORMAL, 1)