import merc
import interp
import nanny


def do_shout(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_SHOUTSOFF):
            ch.send("You can hear shouts again.\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_SHOUTSOFF)
        else:
            ch.send("You will no longer hear shouts.\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_SHOUTSOFF)
        return
    if merc.IS_SET(ch.comm, merc.COMM_NOSHOUT):
        ch.send("You can't shout.\n")
        return
    ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_SHOUTSOFF)
    merc.WAIT_STATE(ch, 12)
    merc.act("You shout '$T'", ch, None, argument, merc.TO_CHAR)
    for d in merc.descriptor_list:
        victim = merc.CH(d)
        if d.is_connected(nanny.con_playing) and d.character != ch \
        and not merc.IS_SET(victim.comm, merc.COMM_SHOUTSOFF) and not merc.IS_SET(victim.comm, merc.COMM_QUIET):
            merc.act("$n shouts '$t'", ch, argument, d.character, merc.TO_VICT)

interp.cmd_table['shout'] = interp.cmd_type('shout', do_shout, merc.POS_RESTING, 3, merc.LOG_NORMAL, 1)