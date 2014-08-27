import logging

logger = logging.getLogger()

import game_utils
import merc
import const
import interp
import nanny
import handler_ch


def do_whois(ch, argument):
    found = False
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("You must provide a name.\n")
        return
    for d in merc.descriptor_list[:]:
        if not d.is_connected(nanny.con_playing) or not ch.can_see(d.character):
            continue
        wch = handler_ch.CH(d)
        if not ch.can_see(wch):
            continue
        if wch.name.lower().startswith(arg):
            found = True
            # work out the printing
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
            # a little formatting */
            ch.send("[[%2d %6s %s]] %s%s%s%s%s%s%s%s\n" % (
                    wch.level,
                    (const.pc_race_table[wch.race.name].who_name if wch.race.name in const.pc_race_table else "     "),
                    guild,
                    ("(Incog) " if wch.incog_level >= merc.LEVEL_HERO else ""),
                    ("(Wizi) " if wch.invis_level >= merc.LEVEL_HERO else ""),
                    wch.clan.who_name if wch.clan else "",
                    ("[[AFK]] " if wch.comm.is_set(merc.COMM_AFK) else ""),
                    ("(KILLER) " if wch.act.is_set(merc.PLR_KILLER) else ""),
                    ("(THIEF) " if wch.act.is_set(merc.PLR_THIEF) else ""),
                    wch.name,
                    ("" if wch.is_npc() else wch.title)))

    if not found:
        ch.send("No one of that name is playing.\n")
        return


interp.register_command(interp.cmd_type('whois', do_whois, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
