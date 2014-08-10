import logging

logger = logging.getLogger()

import merc
import interp
import nanny
import state_checks


# clan channels
def do_clantalk(ch, argument):
    if not ch.is_clan() or ch.clan.independent:
        ch.send("You aren't in a clan.\n")
        return
    if not argument:
        if state_checks.IS_SET(ch.comm, merc.COMM_NOCLAN):
            ch.send("Clan channel is now ON\n")
            ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOCLAN)
        else:
            ch.send("Clan channel is now OFF\n")
            ch.comm = state_checks.SET_BIT(ch.comm, merc.COMM_NOCLAN)
        return
    if state_checks.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
        ch.send("The gods have revoked your channel priviliges.\n")
        return
    ch.comm = state_checks.REMOVE_BIT(ch.comm, merc.COMM_NOCLAN)

    ch.send("You clan '%s'\n" % argument)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) and d.character != ch and ch.is_same_clan(d.character) \
                and not state_checks.IS_SET(d.character.comm, merc.COMM_NOCLAN) and not state_checks.IS_SET(d.character.comm,
                                                                                            merc.COMM_QUIET):
            merc.act("$n clans '$t'", ch, argument, d.character, merc.TO_VICT, merc.POS_DEAD)


interp.register_command(interp.cmd_type('clan', do_clantalk, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))