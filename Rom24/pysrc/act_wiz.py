"""
#**************************************************************************
 *  Original Diku Mud copyright (C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright (C) 1992, 1993 by Michael          *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
from merc import *

def do_noshout(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Noshout whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if victim.get_trust() >= ch.get_trust():
          ch.send("You failed.\n")
          return
    if IS_SET(victim.comm, COMM_NOSHOUT):
        REMOVE_BIT(victim.comm, COMM_NOSHOUT)
        victim.send("You can shout again.\n")
        ch.send("NOSHOUT removed.\n")
        wiznet("$N restores shouts to %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOSHOUT)
        victim.send("You can't shout!\n")
        ch.send("NOSHOUT set.\n")
        wiznet("$N revokes %s's shouts." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return
def do_notell(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Notell whom?")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.get_trust() >= ch.get_trust():
        ch.send("You failed.\n")
        return
    if IS_SET(victim.comm, COMM_NOTELL):
        REMOVE_BIT(victim.comm, COMM_NOTELL)
        victim.send("You can tell again.\n")
        ch.send("NOTELL removed.\n")
        wiznet("$N restores tells to %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOTELL)
        victim.send("You can't tell!\n")
        ch.send("NOTELL set.\n")
        wiznet("$N revokes %s's tells." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return

def do_peace(self, argument):
    ch=self
    for rch in ch.in_room.people:
        if rch.fighting:
            stop_fighting( rch, True )
        if IS_NPC(rch) and IS_SET(rch.act,ACT_AGGRESSIVE):
            REMOVE_BIT(rch.act,ACT_AGGRESSIVE)
    ch.send("Ok.\n")
    return

def do_wizlock(self, argument):
    ch=self
    if not settings.WIZLOCK:
        wiznet("$N has wizlocked the game.",ch,None,0,0,0)
        ch.send("Game wizlocked.\n")
        settings.WIZLOCK = True
    else:
        wiznet("$N removes wizlock.",ch,None,0,0,0)
        ch.send("Game un-wizlocked.\n")
        settings.WIZLOCK = False
    return
# RT anti-newbie code */
def do_newlock(self, argument):
    ch=self
    if not settings.NEWLOCK:
        wiznet("$N locks out new characters.",ch,None,0,0,0)
        ch.send("New characters have been locked out.\n")
        settings.NEWLOCK = True
    else:
        wiznet("$N allows new characters back in.",ch,None,0,0,0)
        ch.send("Newlock removed.\n")
        settings.NEWLOCK = False 
    return

def do_slookup(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Lookup which skill or spell?\n")
        return
    if arg == "all" :
        for sn, skill in const.skill_table.items():
            ch.send("Sn: %15s  Slot: %3d  Skill/spell: '%s'\n", sn, skill.slot, skill.name )
    else:
        skill = prefix_lookup(const.skill_table, arg)
        if not skill:
            ch.send("No such skill or spell.\n")
            return
  
        ch.send("Sn: %15s  Slot: %3d  Skill/spell: '%s'\n", skill.name, skill.slot, skill.name )

# RT set replaces sset, mset, oset, and rset */
def do_set(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Syntax:\n")
        ch.send("  set mob   <name> <field> <value>\n")
        ch.send("  set obj   <name> <field> <value>\n")
        ch.send("  set room  <room> <field> <value>\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        return
    if "character".startswith(arg) or "mobile".startswith(arg):
        ch.do_mset(argument)
        return
    if "spell".startswith(arg) or "skill".startswith(arg):
        ch.do_sset(argument)
        return
    if "object".startswith(arg):
        ch.do_oset(argument)
        return
    if "room".startswith(arg):
        ch.do_rset(argument)
        return
    # echo syntax */
    ch.do_set("")

def do_sset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    argument, arg3  = read_word(argument)

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        ch.send("  set skill <name> all <value>\n")  
        ch.send("   (use the name of the skill, not the number)\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    fAll = arg2 == "all"
    sn = prefix_lookup(const.skill_table,arg2)
    if not fAll and not sn:
        ch.send("No such skill or spell.\n")
        return

    # Snarf the value.
    if not arg3.isdigit():
        ch.send("Value must be numeric.\n")
        return
    value = int( arg3 )
    if value < 0 or value > 100:
        ch.send("Value range is 0 to 100.\n")
        return

    if fAll:
        for sn in const.skill_table.keys():
            victim.pcdata.learned[sn] = value
    else:
        victim.pcdata.learned[sn.name] = value
    ch.send("Skill set.\n")

def do_mset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

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
    # clear zones for mobs */
    victim.zone = None
    #* Snarf the value (which need not be numeric).
    value = int(arg3) if arg3.isdigit() else -1
    #* Set something.
    if arg2 == "str" :
        if value < 3 or value > victim.get_max_train(STAT_STR):
            ch.send( "Strength range is 3 to %d\n." % victim.get_max_train(STAT_STR))
            return
        victim.perm_stat[STAT_STR] = value
        ch.send("Str set to %d.\n" % value)
        return
    if arg2 == "int" :
        if value < 3 or value > victim.get_max_train(STAT_INT):
            ch.send("Intelligence range is 3 to %d.\n" % victim.get_max_train(STAT_INT))
            return
        ch.send("Int set to %d.\n" % value)
        victim.perm_stat[STAT_INT] = value
        return
    if arg2 == "wis" :
        if value < 3 or value > victim.get_max_train(STAT_WIS):
            ch.send("Wisdom range is 3 to %d.\n" % victim.get_max_train(STAT_WIS))
            return
        victim.perm_stat[STAT_WIS] = value
        return
    if arg2 == "dex" :
        if value < 3 or value > victim.get_max_train(STAT_DEX):
            ch.send("Dexterity range is 3 to %d.\n" % victim.get_max_train(STAT_DEX))
            return
        ch.send("Dex set to %d.\n" % value)
        victim.perm_stat[STAT_DEX] = value
        return
    if arg2 == "con" :
        if value < 3 or value > victim.get_max_train(STAT_CON):
            ch.send("Constitution range is 3 to %d.\n" % victim.get_max_train(STAT_CON))
            return
        ch.send("Con set to %d.\n" % value)
        victim.perm_stat[STAT_CON] = value
        return
    if "sex".startswith(arg2):
        if value < 0 or value > 2:
            ch.send("Sex range is 0 to 2.\n")
            return
        victim.sex = value
        if not IS_NPC(victim):
            victim.pcdata.true_sex = value
        ch.send("Sex set to %s.\n" % tables.sex_table[value])
        return
    if "class".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Mobiles have no class.\n")
            return
        guild = prefix_lookup(const.guild_table, arg3)
        if not guild:
            ch.send("Possible classes are: " )
            for guild in const.guild_table.keys():
                ch.send("%s " % guild )
            ch.send(".\n" )
            return
        ch.send("Guild set to %s\n" % guild.name)
        victim.guild = guild
        return
    if "level".startswith(arg2):
        if not IS_NPC(victim):
            ch.send("Not on PC's.\n")
            return
        if value < 0 or value > MAX_LEVEL:
            ch.send("Level range is 0 to %d.\n" % MAX_LEVEL)
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
        if not IS_NPC(victim):
            victim.pcdata.perm_hit = value
        return
    if "mana".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Mana range is 0 to 30,000 mana points.\n")
            return
        victim.max_mana = value
        ch.send("Max Mana set to %d\n" % value)
        if not IS_NPC(victim):
            victim.pcdata.perm_mana = value
        return
    if "move".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Move range is 0 to 30,000 move points.\n")
            return
        victim.max_move = value
        ch.send("Max Move set to %d.\n" % value)
        if not IS_NPC(victim):
            victim.pcdata.perm_move = value
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
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Thirst range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_THIRST] = value
        ch.send("Victims thirst set to %d.\n" % value)
        return
    if "drunk".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Drunk range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_DRUNK] = value
        ch.send("Victims Drunk set to %d.\n" % value)
        return
    if "full".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        ch.send("Full condition set to %d\n" % value)
        victim.pcdata.condition[COND_FULL] = value
        return
    if "hunger".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        ch.send("Hunger set to %d.\n" % value)
        victim.pcdata.condition[COND_HUNGER] = value
        return
    if "race".startswith(arg2):
        race = prefix_lookup(const.race_table, arg3)
        if not race:
            ch.send("That is not a valid race.\n")
            return
        if not IS_NPC(victim) and race.name not in const.pc_race_table:
            ch.send("That is not a valid player race.\n")
            return
        ch.send("Race set to %s.\n" % race.name)
        victim.race = race
        return
    if "group".startswith(arg2):
        if not IS_NPC(victim):
            ch.send("Only on NPCs.\n")
            return
        victim.group = value
        return
    #* Generate usage message.
    ch.do_mset("" )

def do_string(self, argument):
    ch=self
    argument, type  = read_word(argument)
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

    if not type or not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  string char <name> <field> <string>\n")
        ch.send("    fields: name short long desc title spec\n")
        ch.send("  string obj  <name> <field> <string>\n")
        ch.send("    fields: name short long extended\n")
        return
    if "mobile".startswith(type) or "character".startswith(type):
        victim = ch.get_char_world(arg1)
        if not victim:
            ch.send("They aren't here.\n")
            return
        # clear zone for mobs */
        victim.zone = None
        # string something */
        if "name".startswith(arg2):
            if not IS_NPC(victim):
                ch.send("Not on PC's.\n")
                return
            victim.name = arg3
            return
        if "description".startswith(arg2):
            victim.description = arg3
            return
        if "short".startswith(arg2):
            victim.short_descr = arg3
            return
        if "long".startswith(arg2):
            victim.long_descr = arg3 + "\n"
            return
        if "title".startswith(arg2):
            if IS_NPC(victim):
                ch.send("Not on NPC's.\n")
                return
            set_title( victim, arg3 )
            return
        if "spec".startswith(arg2):
            if not IS_NPC(victim):
                ch.send("Not on PC's.\n")
                return
            spec = prefix_lookup(special.spec_table, arg3)
            if not spec:
                ch.send("No such spec fun.\n")
                return
            victim.spec_fun = spec
            ch.send("spec_fun set.\r\n")
            return
    if "object".startswith(type):
        # string an obj */
        obj = ch.get_obj_world(arg1)
        if not obj:
            ch.send("Nothing like that in heaven or earth.\n")
            return
        if "name".startswith(arg2):
            obj.name = arg3
            return
        if "short".startswith(arg2):
            obj.short_descr = arg3
            return
        if "long".startswith(arg2):
            obj.description = arg3
            return
        if "extended".startswith(arg2) or  "ed".startswith(arg2):
            argument, arg3  = read_word(argument)
            if argument == None:
                ch.send( "Syntax: oset <object> ed <keyword> <string>\n")
                return
            argument += "\n"
            ed = EXTRA_DESCR_DATA()
            ed.keyword = arg3
            ed.description = argument
            obj.extra_descr.append(ed)
            return
    # echo bad use message */
    ch.do_string("")

def do_oset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set obj <object> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    value0 value1 value2 value3 value4 (v1-v4)\n")
        ch.send("    extra wear level weight cost timer\n")
        return
    obj = ch.get_obj_world(arg1)
    if not obj:
        ch.send("Nothing like that in heaven or earth.\n")
        return
    #
    #* Snarf the value (which need not be numeric).
    value = int( arg3 ) if arg3.isdigit else -1
    if value == -1:
        ch.do_oset("")
    #* Set something.
    if arg2 == "value0" or arg2 == "v0":
        obj.value[0] = min(50,value)
        return
    if arg2 == "value1" or arg2 == "v1":
        obj.value[1] = value
        return
    if arg2 == "value2" or arg2 == "v2":
        obj.value[2] = value
        return
    if arg2 == "value3" or arg2 == "v3" :
        obj.value[3] = value
        return
    if arg2 == "value4" or arg2 == "v4":
        obj.value[4] = value
        return
    if "extra".startswith(arg2):
        obj.extra_flags = value
        return
    if "wear".startswith(arg2):
        obj.wear_flags = value
        return
    if "level".startswith(arg2):
        obj.level = value
        return
    if "weight" .startswith(arg2):
        obj.weight = value
        return
    if "cost" .startswith(arg2):
        obj.cost = value
        return
    if "timer" .startswith(arg2):
        obj.timer = value
        return
     
    #* Generate usage message.
    ch.do_oset("" )
    return

def do_rset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    strcpy( arg3, argument )

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set room <location> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    flags sector\n")
        return
    location = find_location( ch, arg1 )
    if not location:
        ch.send("No such location.\n")
        return
    if not ch.is_room_owner(location) and ch.in_room != location \
    and location.is_private() and not IS_TRUSTED(ch,IMPLEMENTOR):
        ch.send("That room is private right now.\n")
        return

    #* Snarf the value.
    if not arg3.isdigit():
        ch.send("Value must be numeric.\n")
        return
    value = int( arg3 )

    #* Set something.
    if "flags".startswith(arg2):
        location.room_flags  = value
        return
    if "sector".startswith(arg2):
        location.sector_type = value
        return
    #  Generate usage message.
    ch.do_rset("")
    return

def do_sockets(self, argument):
    ch=self
    count = 0
    argument, arg = read_word(argument)
    for d in descriptor_list:
        if d.character and ch.can_see(d.character) \
        and (not arg or arg not in  d.character.name) \
        or (d.original and is_name(arg,d.original.name)):
            count+=1
            ch.send("%s@%s\n" % (
                    d.original.name if d.original else d.character.name if d.character else "(none)",
                    d.address))
    if count == 0:
        ch.send("No one by that name is connected.\n")
        return
    ch.send("%d user%s\n" % (count, "" if count == 1 else "s" ) )
    return
#
# * Thanks to Grodyn for pointing out bugs in this function.
def do_force(self, argument):
    ch=self
    argument, arg  = read_word(argument)

    if not arg or not argument:
        ch.send("Force whom to do what?\n")
        return
    temp, arg2 = read_word(argument)
    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    buf = "$n forces you to '%s'." % argument
    if arg == "all":
        if ch.get_trust() < MAX_LEVEL - 3:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and vch.get_trust() < ch.get_trust():
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    elif arg == "players":
        if ch.get_trust() < MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and vch.get_trust() < ch.get_trust() and vch.level < LEVEL_HERO:
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    elif arg == "gods":
        if ch.get_trust() < MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and vch.get_trust() < ch.get_trust() and vch.level >= LEVEL_HERO:
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    else:
        victim = ch.get_char_world(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not ch.is_room_owner(victim.in_room) and  ch.in_room != victim.in_room \
        and victim.in_room.is_private() and not IS_TRUSTED(ch,IMPLEMENTOR):
            ch.send("That character is in a private room.\n")
            return
        if victim.get_trust() >= ch.get_trust():
            ch.send("Do it yourself!\n")
            return
        if not IS_NPC(victim) and ch.get_trust() < MAX_LEVEL -3:
            ch.send("Not at your level!\n")
            return
        act( buf, ch, None, victim, TO_VICT )
        interpret( victim, argument )
    ch.send("Ok.\n")
    return


# * New routines by Dionysos.
def do_invis(self, argument):
    ch=self
    # RT code for taking a level argument */
    argument, arg = read_word(argument)

    if not arg: 
    # take the default path */
        if ch.invis_level:
            ch.invis_level = 0
            act( "$n slowly fades into existence.", ch, None, None, TO_ROOM )
            ch.send("You slowly fade back into existence.\n")
        else:
            ch.invis_level = ch.get_trust()
            act( "$n slowly fades into thin air.", ch, None, None, TO_ROOM )
            ch.send("You slowly vanish into thin air.\n")
    else:
    # do the level thing */
          level = int(arg) if arg.isdigit() else -1
          if level < 2 or level > ch.get_trust():
              ch.send("Invis level must be between 2 and your level.\n")
              return
          else:
              ch.reply = None
              ch.invis_level = level
              act( "$n slowly fades into thin air.", ch, None, None, TO_ROOM )
              ch.send("You slowly vanish into thin air.\n")
              return


def do_incognito(self, argument):
    ch=self
    # RT code for taking a level argument */
    argument, arg = read_word(argument)
    if not arg:
    # take the default path */
        if ch.incog_level:
            ch.incog_level = 0
            act( "$n is no longer cloaked.", ch, None, None, TO_ROOM )
            ch.send("You are no longer cloaked.\n")
        else:
            ch.incog_level = ch.get_trust()
            act( "$n cloaks $s presence.", ch, None, None, TO_ROOM )
            ch.send("You cloak your presence.\n")
    else:
    # do the level thing */
          level = int(arg) if arg.isdigit() else -1
          if level < 2 or level > ch.get_trust():
              ch.send("Incog level must be between 2 and your level.\n")
              return
          else:
              ch.reply = None
              ch.incog_level = level
              act( "$n cloaks $s presence.", ch, None, None, TO_ROOM )
              ch.send("You cloak your presence.\n")
    return


def do_holylight(self, argument):
    ch=self
    if IS_NPC(ch):
        return
    if IS_SET(ch.act, PLR_HOLYLIGHT):
        REMOVE_BIT(ch.act, PLR_HOLYLIGHT)
        ch.send("Holy light mode off.\n")
    else:
        SET_BIT(ch.act, PLR_HOLYLIGHT)
        ch.send("Holy light mode on.\n")
    return
# prefix command: it will put the string typed on each line typed */
def do_prefi(self, argument):
    ch=self
    ch.send("You cannot abbreviate the prefix command.\r\n")
    return

def do_prefix(self, argument):
    ch=self
    if not argument:
        if not ch.prefix:
            ch.send("You have no prefix to clear.\r\n")
            return
        ch.send("Prefix removed.\r\n")
        ch.prefix = ""
        return
    if ch.prefix:
        ch.send("Prefix changed to %s.\r\n" % argument)
        ch.prefix = ""
    else:
        ch.send("Prefix set to %s.\r\n" % argument)
    ch.prefix = argument

def do_areas(ch, argument):
    if argument:
        ch.send("No argument is used with this command.\n")
        return
    col = 0
    for iArea in area_list:
        ch.send("%-39s\n" % iArea.credits)
        col += 1
        if col % 2 == 0:
            ch.send("\n")
        
def do_memory(ch, argument):
    pass

def do_dump(ch,argument):
    pass

def do_reload(ch, argument):
    from hotfix import reload_files
    reload_files(ch)
    ch.send("Files reload\n")

def do_omni(ch, argument):
    if IS_SET(ch.act, PLR_OMNI):
        ch.send("Omnimode removed\n")
        ch.act = REMOVE_BIT(ch.act, PLR_OMNI)
    else:
        ch.send("Omnimode enabled.\n")
        ch.act = SET_BIT(ch.act, PLR_OMNI)
