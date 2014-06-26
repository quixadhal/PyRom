import merc
import interp
import comm


def do_disconnect(ch, argument):
    argument, arg = merc.read_word( argument )
    if not arg:
        ch.send("Disconnect whom?\n")
        return
    if arg.isdigit():
        desc = int(arg)
        for d in merc.descriptor_list:
            if d.descriptor == desc:
                comm.close_socket(d)
                ch.send("Ok.\n")
                return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.desc == None:
        merc.act("$N doesn't have a descriptor.", ch, None, merc.victim, merc.TO_CHAR)
        return
    for d in merc.descriptor_list:
        if d == victim.desc:
            comm.close_socket(d)
            ch.send("Ok.\n")
            return
    print("BUG: Do_disconnect: desc not found.")
    ch.send("Descriptor not found!\n")
    return

interp.cmd_table['disconnect'] = interp.cmd_type('disconnect', do_disconnect, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1)