import logging


logger = logging.getLogger()

import merc
import interp
import const
import game_utils


def do_skills(ch, argument):
    fAll = False
    found = False
    min_lev = 1
    max_lev = merc.LEVEL_HERO
    level = 0
    skill = None
    if ch.is_npc():
        return
    argument = argument.lower()
    if argument:
        fAll = True

        if not "all".startswith(argument):
            argument, arg = game_utils.read_word(argument)
            if not arg.isdigit():
                ch.send("Arguments must be numerical or all.\n")
                return

            max_lev = int(arg)

            if max_lev < 1 or max_lev > merc.LEVEL_HERO:
                ch.send("Levels must be between 1 and %d.\n" % merc.LEVEL_HERO)
                return

            if argument:
                argument, arg = game_utils.read_word(argument)
                if not arg.isdigit():
                    ch.send("Arguments must be numerical or all.\n")
                    return

                min_lev = max_lev
                max_lev = int(arg)

                if max_lev < 1 or max_lev > merc.LEVEL_HERO:
                    ch.send("Levels must be between 1 and %d.\n" % merc.LEVEL_HERO)
                    return

                if min_lev > max_lev:
                    ch.send("That would be silly.\n")
                    return

    skill_columns = {}
    skill_list = {}

    for sn, skill in const.skill_table.items():
        level = skill.skill_level[ch.guild.name]
        if level < merc.LEVEL_HERO + 1 \
                and (fAll or level <= ch.level) \
                and level >= min_lev and level <= max_lev \
                and skill.spell_fun is None \
                and sn in ch.learned:
            found = True
            level = skill.skill_level[ch.guild.name]
            if ch.level < level:
                buf = "%-18s n/a      " % skill.name
            else:
                buf = "%-18s %3d%%      " % (skill.name, ch.learned[sn])

            if level not in skill_list:
                skill_list[level] = "\nLevel %2d: %s" % (level, buf)
                skill_columns[level] = 0
            else:  # append
                skill_columns[level] += 1
                if skill_columns[level] % 2 == 0:
                    skill_list[level] += "\n          "
                skill_list[level] += buf

    # return results
    if not found:
        ch.send("No skills found.\n")
        return

    for level, buf in skill_list.items():
        ch.send(buf)
    ch.send("\n")


interp.register_command(interp.cmd_type('skills', do_skills, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
