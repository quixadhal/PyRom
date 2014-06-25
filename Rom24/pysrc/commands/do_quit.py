import merc
import interp
import save
import comm


def do_quit(ch, argument):
    if merc.IS_NPC(ch):
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("No way! You are fighting.\n")
        return
    if ch.position < merc.POS_STUNNED:
        ch.send("You're not DEAD yet.\n")
        return
    ch.send( "Alas, all good things must come to an end.\n")
    merc.act("$n has left the game.", ch, None, None, merc.TO_ROOM)
    print ("%s has quit." % ch.name)
    merc.wiznet("$N rejoins the real world.", ch, None, merc.WIZ_LOGINS, 0, ch.get_trust())
    #* After extract_char the ch is no longer valid!
    save.save_char_obj(ch)
    id = ch.id
    d = ch.desc
    ch.extract(True)
    if d != None:
        comm.close_socket(d)

    # toast evil cheating bastards */
    for d in merc.descriptor_list[:]:
        tch = merc.CH(d)
        if tch and tch.id == id:
            tch.extract(True)
            comm.close_socket(d)
    return

interp.cmd_table['quit'] = interp.cmd_type('quit', do_quit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)