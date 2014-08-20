import logging

logger = logging.getLogger()

import merc
import interp
import tables
import game_utils
import state_checks


def do_guild(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg2:
        ch.send("Syntax: guild <char> <cln name>\n")
        return

    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't playing.\n")
        return

    if "none".startswith(arg2):
        ch.send("They are now clanless.\n")
        victim.send("You are now a member of no clan!\n")
        victim.clan = 0
        return
    clan = state_checks.prefix_lookup(tables.clan_table, arg2)
    if not clan:
        ch.send("No such clan exists.\n")
        return
    if clan.independent:
        ch.send("They are now a %s.\n" % clan.name)
        victim.send("You are now a %s.\n" % clan.name)
    else:
        ch.send("They are now a member of clan %s.\n" % clan.name.capitalize())
        victim.send("You are now a member of clan %s.\n" % clan.name.capitalize())
    victim.clan = clan.name
    ch.send("dbeug")


interp.register_command(interp.cmd_type('guild', do_guild, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
