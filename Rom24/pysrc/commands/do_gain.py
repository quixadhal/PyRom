import logging

logger = logging.getLogger()

import merc
import interp
import skills
import const
import magic
import game_utils
import state_checks


def do_gain(ch, argument):
    if ch.is_npc():
        return
    trainer = [t for t in merc.rooms[ch.in_room].people if state_checks.IS_NPC(t) and state_checks.IS_SET(t.act, merc.ACT_GAIN)]
    # find a trainer
    if not trainer or not ch.can_see(trainer):
        ch.send("You can't do that here.\n")
        return
    argmod, arg = game_utils.read_word(argument)
    if not arg:
        trainer.do_say("Pardon me?")
        return
    if "list".startswith(arg):
        col = 0
        ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("group", "cost", "group", "cost", "group", "cost"))
        for gn, group in const.group_table.items():
            if gn not in ch.group_known and group.rating[ch.guild.name] > 0:
                ch.send("%-18s %-5d " % group.name, group.rating[ch.guild.name])
                col += 1
                if (col % 3) == 0:
                    ch.send("\n")
        if (col % 3) != 0:
            ch.send("\n")
        ch.send("\n")
        col = 0
        ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("skill", "cost", "skill", "cost", "skill", "cost"))

        for sn, skill in const.skill_table.items():
            if sn not in ch.learned \
                    and skill.rating[ch.guild.name] > 0 \
                    and skill.spell_fun == magic.spell_null:
                ch.send("%-18s %-5d " % (const.skill_table[sn].name, skill.rating[ch.guild.name]))
                col += 1
                if (col % 3) == 0:
                    ch.send("\n")
        if (col % 3) != 0:
            ch.send("\n")
        return

    if "convert".startswith(arg):
        if ch.practice < 10:
            act("$N tells you 'You are not yet ready.'", ch, None, trainer, merc.TO_CHAR)
            return
        act("$N helps you apply your practice to training", ch, None, trainer, merc.TO_CHAR)
        ch.practice -= 10
        ch.train += 1
        return

    if "points".startswith(arg):
        if ch.train < 2:
            act("$N tells you 'You are not yet ready.'", ch, None, trainer, merc.TO_CHAR)
            return

        if ch.points <= 40:
            act("$N tells you 'There would be no point in that.'", ch, None, trainer, merc.TO_CHAR)
            return
        act("$N trains you, and you feel more at ease with your skills.", ch, None, trainer, merc.TO_CHAR)
        ch.train -= 2
        ch.points -= 1
        ch.exp = ch.exp_per_level(ch.points) * ch.level
        return
    if argument.lower() in const.group_table:
        gn = const.group_table[argument.lower()]
        if gn.name in ch.group_known:
            act("$N tells you 'You already know that group!'", ch, None, trainer, merc.TO_CHAR)
            return
        if gn.rating[ch.guild.name] <= 0:
            act("$N tells you 'That group is beyond your powers.'", ch, None, trainer, merc.TO_CHAR)
            return

        if ch.train < gn.rating[ch.guild.name]:
            act("$N tells you 'You are not yet ready for that group.'", ch, None, trainer, merc.TO_CHAR)
            return

        # add the group
        skills.gn_add(ch, gn)
        act("$N trains you in the art of $t", ch, gn.name, trainer, merc.TO_CHAR)
        ch.train -= gn.rating[ch.guild.name]
        return

    if argument.lower() in const.skill_table:
        sn = const.skill_table[argument.lower()]
        if sn.spell_fun is not None:
            act("$N tells you 'You must learn the full group.'", ch, None, trainer, merc.TO_CHAR)
            return
        if sn.name in ch.learned:
            act("$N tells you 'You already know that skill!'", ch, None, trainer, merc.TO_CHAR)
            return
        if sn.rating[ch.guild.name] <= 0:
            act("$N tells you 'That skill is beyond your powers.'", ch, None, trainer, merc.TO_CHAR)
            return
        if ch.train < sn.rating[ch.guild.name]:
            act("$N tells you 'You are not yet ready for that skill.'", ch, None, trainer, merc.TO_CHAR)
            return
        # add the skill
        ch.learned[sn.name] = 1
        act("$N trains you in the art of $t", ch, sn.name, trainer, merc.TO_CHAR)
        ch.train -= sn.rating[ch.guild.name]
        return

    act("$N tells you 'I do not understand...'", ch, None, trainer, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('gain', do_gain, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1))
