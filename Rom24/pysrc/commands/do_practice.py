import logging


logger = logging.getLogger()

import merc
import interp
import const
import handler_game
import state_checks

def do_practice(ch, argument):
    if ch.is_npc():
        return
    if not argument:
        col = 0
        for sn, skill in const.skill_table.items():
            if ch.level < skill.skill_level[ch.guild.name] \
                    or sn not in ch.learned or ch.learned[sn] < 1:  # skill is not known
                continue

            ch.send("%-18s %3d%%  " % (skill.name, ch.learned[sn]))
            col += 1
            if col % 3 == 0:
                ch.send("\n")
        if col % 3 != 0:
            ch.send("\n")

        ch.send("You have %d practice sessions left.\n" % ch.practice)
    else:
        if not ch.is_awake():
            ch.send("In your dreams, or what?\n")
            return
        mob = None
        prac_mobs = [mob for mob in merc.rooms[ch.in_room].people if state_checks.IS_NPC(mob) and \
                     state_checks.IS_SET(mob.act, merc.ACT_PRACTICE)][:1]
        if not prac_mobs:
            ch.send("You can't do that here.\n")
            return
        else:
            mob = prac_mobs[0]
        if ch.practice <= 0:
            ch.send("You have no practice sessions left.\n")
            return
        skill = state_checks.prefix_lookup(const.skill_table, argument)
        if not skill or not ch.is_npc() \
                and (ch.level < skill.skill_level[ch.guild.name] or ch.learned[skill.name] < 1 \
                             or skill.rating[ch.guild.name] == 0):
            ch.send("You can't practice that.\n")
            return
        adept = 100 if ch.is_npc() else ch.guild.skill_adept

        if ch.learned[skill.name] >= adept:
            ch.send("You are already learned at %s.\n" % skill.name)
        else:
            ch.practice -= 1
            ch.learned[skill.name] += const.int_app[ch.stat(merc.STAT_INT)].learn // skill.rating[
                ch.guild.name]
            if ch.learned[skill.name] < adept:
                handler_game.act("You practice $T.", ch, None, skill.name, merc.TO_CHAR)
                handler_game.act("$n practices $T.", ch, None, skill.name, merc.TO_ROOM)
            else:
                ch.learned[skill.name] = adept
                handler_game.act("You are now learned at $T.", ch, None, skill.name, merc.TO_CHAR)
                handler_game.act("$n is now learned at $T.", ch, None, skill.name, merc.TO_ROOM)
    return


interp.register_command(interp.cmd_type('practice', do_practice, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
