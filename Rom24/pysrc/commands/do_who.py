import logging

logger = logging.getLogger()

import game_utils
import merc
import const
import interp
import nanny
import tables
import handler_ch

# New 'who' command originally by Alander of Rivers of Mud.
def do_who(ch, argument):
    fClassRestrict = False
    fClanRestrict = False
    fClan = False
    fRaceRestrict = False
    fImmortalOnly = False
    # Set default arguments.
    iLevelLower = 0
    iLevelUpper = merc.MAX_LEVEL
    rgfClass = {k: False for k, g in const.guild_table.items()}
    rgfRace = {k: False for k, r in const.pc_race_table.items()}
    rgfClan = {k: False for k, r in tables.clan_table.items()}

    # Parse arguments.
    nNumber = 0
    while True:
        argument, arg = game_utils.read_word(argument)
        if not arg:
            break
        if arg.isdigit():
            nNumber += 1
            if nNumber == 1:
                iLevelLower = int(arg)
            elif nNumber == 2:
                iLevelUpper = int(arg)
            else:
                ch.send("Only two level numbers allowed.\n")
                return
        else:
            # Look for classes to turn on.
            if "immortals".startswith(arg):
                fImmortalOnly = True
            else:
                if arg not in const.guild_table:
                    if arg not in const.pc_race_table:
                        if "clan".startswith(arg):
                            fClan = True
                        else:
                            if arg in tables.clan_table:
                                fClanRestrict = True
                                rgfClan[arg] = tables.clan_table[arg]
                            else:
                                ch.send("That's not a valid race, class, or clan.\n")
                                return
                    else:
                        fRaceRestrict = True
                        rgfRace[arg] = const.pc_race_table[arg]
                else:
                    fClassRestrict = True
                    rgfClass[arg] = const.guild_table[arg]

    # Now show matching chars.
    nMatch = 0
    for d in merc.descriptor_list:
        # Check for match against restrictions.
        # Don't use trust as that exposes trusted mortals.
        if not d.is_connected(nanny.con_playing) or not ch.can_see(d.character):
            continue

        wch = handler_ch.CH(d)

        if not ch.can_see(wch):
            continue

        if wch.level < iLevelLower or wch.level > iLevelUpper \
                or (fImmortalOnly and wch.level < merc.LEVEL_IMMORTAL) \
                or (fClassRestrict and not rgfClass[wch.guild.name]) \
                or (fRaceRestrict and not rgfRace[wch.race.name]) \
                or (fClan and not wch.is_clan()) or (fClanRestrict and not rgfClan[wch.clan.name]):
            continue

        nMatch += 1

        # Figure out what to print for class.
        guild = wch.guild.who_name
        if wch.level == merc.MAX_LEVEL - 0:
            guild = "IMP"
        elif wch.level == merc.MAX_LEVEL - 1:
            guild = "CRE"
        elif wch.level == merc.MAX_LEVEL - 2:
            guild = "SUP"
        elif wch.level == merc.MAX_LEVEL - 3:
            guild = "DEI"
        elif wch.level == merc.MAX_LEVEL - 4:
            guild = "GOD"
        elif wch.level == merc.MAX_LEVEL - 5:
            guild = "IMM"
        elif wch.level == merc.MAX_LEVEL - 6:
            guild = "DEM"
        elif wch.level == merc.MAX_LEVEL - 7:
            guild = "ANG"
        elif wch.level == merc.MAX_LEVEL - 8:
            guild = "AVA"
        # a little formatting
        ch.send("[[%2d %6s %s]] %s%s%s%s%s%s%s%s\n" % (
                wch.level,
                const.pc_race_table[wch.race.name].who_name if wch.race.name in const.pc_race_table else "     ",
                guild,
                "(Incog) " if wch.incog_level >= merc.LEVEL_HERO else "",
                "(Wizi) " if wch.invis_level >= merc.LEVEL_HERO else "",
                wch.clan.who_name,
                "[[AFK]] " if wch.comm.is_set(merc.COMM_AFK) else "",
                "(KILLER) " if wch.act.is_set(merc.PLR_KILLER) else "",
                "(THIEF) " if wch.act.is_set(merc.PLR_THIEF) else "",
                wch.name,
                "" if wch.is_npc() else wch.title))
    ch.send("\nPlayers found: %d\n" % nMatch)
    return


interp.register_command(interp.cmd_type('who', do_who, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
