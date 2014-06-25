import merc
import interp
import nanny


def do_immtalk(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOWIZ):
            ch.send("Immortal channel is now ON\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOWIZ)
        else:
            ch.send("Immortal channel is now OFF\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOWIZ)
        return

    ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOWIZ)
    act("$n: $t", ch, argument, None, merc.TO_CHAR, merc.POS_DEAD)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) and merc.IS_IMMORTAL(d.character) \
        and not merc.IS_SET(d.character.comm, merc.COMM_NOWIZ):
            merc.act("$n: $t", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)

interp.cmd_table['immtalk'] = interp.cmd_type('immtalk', do_immtalk, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)
interp.cmd_table[':'] = interp.cmd_type(':', do_immtalk, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 0)