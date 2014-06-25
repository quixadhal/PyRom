import merc
import interp
import nanny


# RT music channel */
def do_music(ch, argument):
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOMUSIC):
            ch.send("Music channel is now ON.\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOMUSIC)
        else:
            ch.send("Music channel is now OFF.\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOMUSIC)
    else:  # music sent, turn music on if it isn't already */
        if merc.IS_SET(ch.comm, merc.COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if merc.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOMUSIC)
        ch.send("You MUSIC: '%s'\n" % argument)
        for d in merc.descriptor_list:
            victim = merc.CH(d)
            if d.is_connected(nanny.con_playing) and d.character != ch \
            and not merc.IS_SET(victim.comm, merc.COMM_NOMUSIC) and not merc.IS_SET(victim.comm, merc.COMM_QUIET):
                merc.act("$n MUSIC: '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_SLEEPING)

interp.cmd_table['music'] = interp.cmd_type('music', do_music, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)