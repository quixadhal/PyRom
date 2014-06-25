import merc
import interp
import nanny


# clan channels */
def do_clantalk(ch, argument):
    if not ch.is_clan() or ch.clan.independent:
        ch.send("You aren't in a clan.\n")
        return
    if not argument:
        if merc.IS_SET(ch.comm, merc.COMM_NOCLAN):
            ch.send("Clan channel is now ON\n")
            ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOCLAN)
        else:
            ch.send("Clan channel is now OFF\n")
            ch.comm = merc.SET_BIT(ch.comm, merc.COMM_NOCLAN)
        return
    if merc.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
        ch.send("The gods have revoked your channel priviliges.\n")
        return
    ch.comm = merc.REMOVE_BIT(ch.comm, merc.COMM_NOCLAN)

    ch.send("You clan '%s'\n" % argument)
    for d in descriptor_list:
        if d.is_connected(nanny.con_playing) and d.character != ch and ch.is_same_clan(d.character) \
        and not merc.IS_SET(d.character.comm, merc.COMM_NOCLAN) and not merc.IS_SET(d.character.comm, merc.COMM_QUIET):
            merc.act("$n clans '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)

interp.cmd_table['clan'] = interp.cmd_type('clan', do_clantalk, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)