import logging

logger = logging.getLogger()

import merc
import const
import interp
import tables
import game_utils
import state_checks

def do_mset(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    argument, arg3 = game_utils.read_word(argument)

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set char <name> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    str int wis dex con sex class level\n")
        ch.send("    race group gold silver hp mana move prac\n")
        ch.send("    align train thirst hunger drunk full\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    # clear zones for mobs
    victim.zone = None
    # Snarf the value (which need not be numeric).
    value = int(arg3) if arg3.isdigit() else -1
    # Set something.
    if arg2 == "str":
        if value < 3 or value > victim.get_max_train(merc.STAT_STR):
            ch.send("Strength range is 3 to %d\n." % victim.get_max_train(merc.STAT_STR))
            return
        victim.perm_stat[merc.STAT_STR] = value
        ch.send("Str set to %d.\n" % value)
        return
    if arg2 == "int":
        if value < 3 or value > victim.get_max_train(merc.STAT_INT):
            ch.send("Intelligence range is 3 to %d.\n" % victim.get_max_train(merc.STAT_INT))
            return
        ch.send("Int set to %d.\n" % value)
        victim.perm_stat[merc.STAT_INT] = value
        return
    if arg2 == "wis":
        if value < 3 or value > victim.get_max_train(merc.STAT_WIS):
            ch.send("Wisdom range is 3 to %d.\n" % victim.get_max_train(merc.STAT_WIS))
            return
        victim.perm_stat[merc.STAT_WIS] = value
        return
    if arg2 == "dex":
        if value < 3 or value > victim.get_max_train(merc.STAT_DEX):
            ch.send("Dexterity range is 3 to %d.\n" % victim.get_max_train(merc.STAT_DEX))
            return
        ch.send("Dex set to %d.\n" % value)
        victim.perm_stat[merc.STAT_DEX] = value
        return
    if arg2 == "con":
        if value < 3 or value > victim.get_max_train(merc.STAT_CON):
            ch.send("Constitution range is 3 to %d.\n" % victim.get_max_train(merc.STAT_CON))
            return
        ch.send("Con set to %d.\n" % value)
        victim.perm_stat[merc.STAT_CON] = value
        return
    if "sex".startswith(arg2):
        if value < 0 or value > 2:
            ch.send("Sex range is 0 to 2.\n")
            return
        victim.sex = value
        if not victim.is_npc():
            victim.true_sex = value
        ch.send("Sex set to %s.\n" % tables.sex_table[value])
        return
    if "class".startswith(arg2):
        if victim.is_npc():
            ch.send("Mobiles have no class.\n")
            return
        guild = state_checks.prefix_lookup(const.guild_table, arg3)
        if not guild:
            ch.send("Possible classes are: ")
            for guild in const.guild_table.keys():
                ch.send("%s " % guild)
            ch.send(".\n")
            return
        ch.send("Guild set to %s\n" % guild.name)
        victim.guild = guild
        return
    if "level".startswith(arg2):
        if not victim.is_npc():
            ch.send("Not on PC's.\n")
            return
        if value < 0 or value > merc.MAX_LEVEL:
            ch.send("Level range is 0 to %d.\n" % merc.MAX_LEVEL)
            return
        ch.send("Level set to %d.\n" % value)
        victim.level = value
        return
    if "gold".startswith(arg2):
        victim.gold = value
        ch.send("Gold set to %d\n" % victim.gold)
        return
    if "silver".startswith(arg2):
        victim.silver = value
        ch.send("Silver set to %d\n" % victim.silver)
        return
    if "hp".startswith(arg2):
        if value < -10 or value > 30000:
            ch.send("Hp range is -10 to 30,000 hit points.\n")
            return
        victim.max_hit = value
        ch.send("Max Hitpoints set to %d\n" % value)
        if not victim.is_npc():
            victim.perm_hit = value
        return
    if "mana".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Mana range is 0 to 30,000 mana points.\n")
            return
        victim.max_mana = value
        ch.send("Max Mana set to %d\n" % value)
        if not victim.is_npc():
            victim.perm_mana = value
        return
    if "move".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Move range is 0 to 30,000 move points.\n")
            return
        victim.max_move = value
        ch.send("Max Move set to %d.\n" % value)
        if not victim.is_npc():
            victim.perm_move = value
        return
    if "practice".startswith(arg2):
        if value < 0 or value > 250:
            ch.send("Practice range is 0 to 250 sessions.\n")
            return
        victim.practice = value
        ch.send("Victims practices set to %d.\n" % value)
        return
    if "train".startswith(arg2):
        if value < 0 or value > 50:
            ch.send("Training session range is 0 to 50 sessions.\n")
            return
        victim.train = value
        ch.send("Trains set to %d.\n" % value)
        return
    if "align".startswith(arg2):
        if value < -1000 or value > 1000:
            ch.send("Alignment range is -1000 to 1000.\n")
            return
        victim.alignment = value
        ch.send("Alignment set to %d.\n" % value)
        return
    if "thirst".startswith(arg2):
        if victim.is_npc():
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Thirst range is -1 to 100.\n")
            return
        victim.condition[merc.COND_THIRST] = value
        ch.send("Victims thirst set to %d.\n" % value)
        return
    if "drunk".startswith(arg2):
        if victim.is_npc():
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Drunk range is -1 to 100.\n")
            return
        victim.condition[merc.COND_DRUNK] = value
        ch.send("Victims Drunk set to %d.\n" % value)
        return
    if "full".startswith(arg2):
        if victim.is_npc():
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        ch.send("Full condition set to %d\n" % value)
        victim.condition[merc.COND_FULL] = value
        return
    if "hunger".startswith(arg2):
        if victim.is_npc():
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        ch.send("Hunger set to %d.\n" % value)
        victim.condition[merc.COND_HUNGER] = value
        return
    if "race".startswith(arg2):
        race = state_checks.prefix_lookup(const.race_table, arg3)
        if not race:
            ch.send("That is not a valid race.\n")
            return
        if not victim.is_npc() and race.name not in const.pc_race_table:
            ch.send("That is not a valid player race.\n")
            return
        ch.send("Race set to %s.\n" % race.name)
        victim.race = race
        return
    if "group".startswith(arg2):
        if not victim.is_npc():
            ch.send("Only on NPCs.\n")
            return
        victim.group = value
        return
    # Generate usage message.
    ch.do_mset("")


interp.register_command(interp.cmd_type('mset', do_mset, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1))
