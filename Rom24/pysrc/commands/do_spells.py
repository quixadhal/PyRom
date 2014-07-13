import logging

logger = logging.getLogger()

import merc
import const
import interp
import game_utils

# RT spells and skills show the players spells (or skills)
def do_spells(ch, argument):
    fAll = False
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

    found = False
    spell_list = {}
    spell_column = {}
    for sn, skill in const.skill_table.items():
        level = skill.skill_level[ch.guild.name]
        if level < merc.LEVEL_HERO + 1 \
                and (fAll or level <= ch.level) \
                and level >= min_lev and level <= max_lev \
                and skill.spell_fun is not None \
                and sn in ch.learned:
            found = True
            level = skill.skill_level[ch.guild.name]
            if ch.level < level:
                buf = "%-18s  n/a      " % skill.name
            else:
                mana = max(skill.min_mana, 100 / (2 + ch.level - level))
                buf = "%-18s  %3d mana  " % (skill.name, mana)

            if level not in spell_list:
                spell_list[level] = "\nLevel %2d: %s" % (level, buf)
                spell_column[level] = 0
            else:  # append
                spell_column[level] += 1
                if spell_column[level] % 2 == 0:
                    spell_list[level] += "\n          "
                spell_list[level] += buf

    # return results
    if not found:
        ch.send("No spells found.\n")
        return

    for level, buf in spell_list.items():
        ch.send(buf)
    ch.send("\n")


interp.register_command(interp.cmd_type('spells', do_spells, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
