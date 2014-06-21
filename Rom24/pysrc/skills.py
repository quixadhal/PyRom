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
import const
import update

# used to get new skills */
def do_gain(self, argument):
    ch = self
    if IS_NPC(ch):
        return
    trainer = [t for t in ch.in_room.people if IS_NPC(t) and IS_SET(t.act,ACT_GAIN)]
    # find a trainer */
    if not trainer or not ch.can_see(trainer):
        ch.send("You can't do that here.\n")
        return
   
    argmod, arg = read_word(argument)

    if not arg:
        trainer.do_say("Pardon me?")
        return

    if "list".startswith(arg):
        col = 0
        ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("group","cost","group","cost","group","cost") )
        for gn,group in const.group_table.items():
            if gn not in ch.pcdata.group_known and  group.rating[ch.guild.name] > 0:
                ch.send("%-18s %-5d " % group.name,group.rating[ch.guild.name])
                col+=1
                if (col % 3) == 0:
                    ch.send("\n")
        if (col % 3) != 0:
            ch.send("\n")
    
        ch.send("\n")        

        col = 0

        ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("skill","cost","skill","cost","skill","cost"))
 
        for sn,skill in const.skill_table.items():
            if sn not in ch.pcdata.learned \
            and  skill.rating[ch.guild.name] > 0 \
            and  skill.spell_fun == spell_null:
                ch.send("%-18s %-5d " % (const.skill_table[sn].name,skill.rating[ch.guild.name]))
                col += 1
                if (col % 3) == 0:
                    ch.send("\n")
        if (col % 3) != 0:
            ch.send("\n")
        return

    if "convert".startswith(arg):
        if ch.practice < 10:
            act("$N tells you 'You are not yet ready.'",ch,None,trainer,TO_CHAR)
            return
        act("$N helps you apply your practice to training", ch,None,trainer,TO_CHAR)
        ch.practice -= 10
        ch.train +=1 
        return

    if "points".startswith(arg):
        if ch.train < 2:
            act("$N tells you 'You are not yet ready.'", ch,None,trainer,TO_CHAR)
            return

        if ch.pcdata.points <= 40:
            act("$N tells you 'There would be no point in that.'", ch,None,trainer,TO_CHAR)
            return
        act("$N trains you, and you feel more at ease with your skills.", ch,None,trainer,TO_CHAR)

        ch.train -= 2
        ch.pcdata.points -= 1
        ch.exp = ch.exp_per_level(ch.pcdata.points) * ch.level
        return

    
    
    if argument.lower() in const.group_table:
        gn = const.group_table[argument.lower()]
        if gn.name in ch.pcdata.group_known:
            act("$N tells you 'You already know that group!'", ch,None,trainer,TO_CHAR)
            return
        if gn.rating[ch.guild.name] <= 0:
            act("$N tells you 'That group is beyond your powers.'", ch,None,trainer,TO_CHAR)
            return

        if ch.train < gn.rating[ch.guild.name]:
            act("$N tells you 'You are not yet ready for that group.'", ch,None,trainer,TO_CHAR)
            return

        # add the group */
        gn_add(ch,gn)
        act("$N trains you in the art of $t", ch,gn.name,trainer,TO_CHAR)
        ch.train -= gn.rating[ch.guild.name]
        return

    if argument.lower() in const.skill_table:
        sn = const.skill_table[argument.lower()]
        if sn.spell_fun != spell_null:
            act("$N tells you 'You must learn the full group.'", ch,None,trainer,TO_CHAR)
            return
        
        if sn.name in ch.pcdata.learned:
            act("$N tells you 'You already know that skill!'", ch,None,trainer,TO_CHAR)
            return

        if sn.rating[ch.guild.name] <= 0:
            act("$N tells you 'That skill is beyond your powers.'", ch,None,trainer,TO_CHAR)
            return

 
        if ch.train < sn.rating[ch.guild.name]:
            act("$N tells you 'You are not yet ready for that skill.'", ch,None,trainer,TO_CHAR)
            return
        # add the skill */
        ch.pcdata.learned[sn.name] = 1
        act("$N trains you in the art of $t", sn.name,trainer,TO_CHAR)
        ch.train -= sn.rating[ch.guild.name]
        return

    act("$N tells you 'I do not understand...'",ch,None,trainer,TO_CHAR)
    return

# RT spells and skills show the players spells (or skills) */
def do_spells(self, argument):
    ch = self
    fAll = False
    min_lev = 0
    max_lev = 0
    level = 0
    skill = None

    if IS_NPC(ch):
      return
    argument = argument.lower()
    if not argument:
        fAll = True

        if "all".startswith(argument):
            argument, arg = read_word(argument)
            if not arg.isdigit():
                ch.send("Arguments must be numerical or all.\n")
                return

            max_lev = int(arg)

            if max_lev < 1 or max_lev > LEVEL_HERO:
                ch.send("Levels must be between 1 and %d.\n" % LEVEL_HERO)
                return

            if argument:
                argument, arg = read_word(argument)
                if not arg.isdigit():
                    ch.send("Arguments must be numerical or all.\n")
                    return
                
                min_lev = max_lev
                max_lev = int(arg)

                if max_lev < 1 or max_lev > LEVEL_HERO:
                    ch.send("Levels must be between 1 and %d.\n" % LEVEL_HERO)
                    return

                if min_lev > max_lev:
                    ch.send("That would be silly.\n")
                    return

    found = False
    spell_list = {} 
    spell_column = {}
    for sn, skill in const.skill_table.items():
        level = skill.skill_level[ch.guild.name]
        if level < LEVEL_HERO + 1 \
        and  (fAll or level <= ch.level) \
        and  level >= min_lev and level <= max_lev \
        and  skill.spell_fun != spell_null \
        and  sn in ch.pcdata.learned:
            found = True
            level = skill.skill_level[ch.guild.name]
            if ch.level < level:
                buf = "%-18s  n/a      " % skill.name
            else:
                mana = max(skill.min_mana, 100/(2 + ch.level - level))
                buf = "%-18s  %3d mana  " % (skill.name,mana)
 
            if level not in spell_list:
                spell_list[level] = "\nLevel %2d: %s" % (level,buf)
                spell_column[level] = 0
            else: # append */
                spell_column[level] += 1
                if spell_columns[level] % 2 == 0:
                    spell_list[level] += "\n          "
                spell_list[level] += buf

    # return results */
    if not found:
        ch.send("No spells found.\n")
        return

    for level, buf in spell_list.items():
        ch.send(buf)
    ch.send("\n")

# recursively adds a group given its number -- uses group_add */
def gn_add( ch, gn):
    ch.pcdata.group_known[gn.name] = True
    for i in gn.spells:
        if not i:
            break
        group_add(ch,i,False)

# recusively removes a group given its number -- uses group_remove */
def gn_remove( ch, gn):
    if gn.name in ch.pcdata.group_known:
        del ch.pcdata.group_known[gn.name]

    for i in gn.spells:
        if not i:
            return
        group_remove(ch,i)

# use for processing a skill or group for addition  */
def group_add( ch, name, deduct):
    if IS_NPC(ch): # NPCs do not have skills */
        return
    
    if name in const.skill_table:
        sn = const.skill_table[name]
        if sn.name not in ch.pcdata.learned: # i.e. not known */
            ch.pcdata.learned[sn.name] = 1
        if deduct:
            ch.pcdata.points += sn.rating[ch.guild.name] 
        return

    # now check groups */

    if name in const.group_table:
        gn = const.group_table[name]
        if gn.name not in ch.pcdata.group_known:
            ch.pcdata.group_known[gn.name] = True
        if deduct:
            ch.pcdata.points += gn.rating[ch.guild.name]
    
        gn_add(ch,gn) # make sure all skills in the group are known */


# used for processing a skill or group for deletion -- no points back! */

def group_remove(ch, name):
    
    if name in const.skill_table:
        sn = const.skill_table[name]
        if sn.name in ch.pcdata.learned:
            del ch.pcdata.learned[sn.name]
            return

    # now check groups */
    if name in const.group_table:
        gn = const.group_table[name]
        
        if gn.name in ch.pcdata.group_known:
            del ch.pcdata.group_known[gn.name]
            gn_remove(ch,gn) # be sure to call gn_add on all remaining groups */

def do_skills(self, argument):
    ch = self 
    if IS_NPC(ch):
      return
    argument = argument.lower()
    if not argument:
        fAll = True

        if "all".startswith(argument):
            argument, arg = read_word(argument)
            if not arg.isdigit():
                ch.send("Arguments must be numerical or all.\n")
                return

            max_lev = int(arg)

            if max_lev < 1 or max_lev > LEVEL_HERO:
                ch.send("Levels must be between 1 and %d.\n" % LEVEL_HERO)
                return

            if argument:
                argument, arg = read_word(argument)
                if not arg.isdigit():
                    ch.send("Arguments must be numerical or all.\n")
                    return
                
                min_lev = max_lev
                max_lev = int(arg)

                if max_lev < 1 or max_lev > LEVEL_HERO:
                    ch.send("Levels must be between 1 and %d.\n" % LEVEL_HERO)
                    return

                if min_lev > max_lev:
                    ch.send("That would be silly.\n")
                    return

    skill_columns = {}
    skill_list = {}
 
    for sn, skill in const.skills_table.items():
        level = skill.skill_level[ch.guild.name]
        if level < LEVEL_HERO + 1 \
        and  (fAll or level <= ch.level) \
        and  level >= min_lev and level <= max_lev \
        and  skill.spell_fun == spell_null \
        and  sn in ch.pcdata.learned:
            found = True
            level = skill.skill_level[ch.guild.name]
            if ch.level < level:
                buf = "%-18s n/a      " % skill.name
            else:
                buf = "%-18s %3d%%      " % (skill.name, ch.pcdata.learned[sn])
 
            if level not in skill_list:
                skill_list[level] =  "\nLevel %2d: %s" % (level,buf)
                skill_columns[level] = 0
            else: # append */
                skill_columns[level] += 1
                if skill_columns[level] % 2 == 0:
                    skill_list[level] += "\n          "
                skill_list[level] += buf
 
    # return results */
    if not found:
        ch.send("No skills found.\n")
        return

    for level, buf in skill_list.items():
        ch.send(buf)
    ch.send("\n")


# shows skills, groups and costs (only if not bought) */
def list_group_costs(ch):
    if IS_NPC(ch):
        return
    col = 0
    ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("group","cp","group","cp","group","cp"))

    for gn, group in const.group_table.items():
        if gn not in ch.gen_data.group_chosen and gn not in ch.pcdata.group_known and group.rating[ch.guild.name] > 0:
            ch.send("%-18s %-5d " % (const.group_table[gn].name, group.rating[ch.guild.name]))
            col += 1
            if col % 3 == 0:
                ch.send("\n")
    if col % 3 != 0:
        ch.send("\n")
    ch.send("\n")
    col = 0
 
    ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("skill","cp","skill","cp","skill","cp"))
 
    for sn, skill in const.skill_table.items():
        if sn not in ch.gen_data.skill_chosen \
        and sn not in ch.pcdata.learned \
        and  skill.spell_fun == spell_null \
        and  skill.rating[ch.guild.name] > 0:
            ch.send("%-18s %-5d " % (skill.name, skill.rating[ch.guild.name]))
            col += 1
            if col % 3 == 0:
                ch.send("\n")
    if  col % 3 != 0:
        ch.send( "\n" )
    ch.send("\n")

    ch.send("Creation points: %d\n" % ch.pcdata.points)
    ch.send("Experience per level: %d\n" % ch.exp_per_level(ch.gen_data.points_chosen))
    return

def list_group_chosen(ch):
    if IS_NPC(ch):
        return
    col = 0
    ch.send("%-18s %-5s %-18s %-5s %-18s %-5s" % ("group","cp","group","cp","group","cp\n"))
 
    for gn, group in const.group_table.items():
        if gn in ch.gen_data.group_chosen and group.rating[ch.guild.name] > 0:
            ch.send("%-18s %-5d " % (group.name, group.rating[ch.guild.name]) )
            col += 1
            if col % 3 == 0:
                ch.send("\n")
    if col % 3 != 0:
        ch.send( "\n" )
    ch.send("\n")
 
    col = 0
 
    ch.send("%-18s %-5s %-18s %-5s %-18s %-5s" % ("skill","cp","skill","cp","skill","cp\n"))

    for sn, skill in const.skill_table.items():
        if sn in ch.gen_data.skill_chosen and skill.rating[ch.guild.name] > 0:
            ch.send("%-18s %-5d " % ( skill.name, skill.rating[ch.guild.name]) )
            col += 1
            if col % 3 == 0:
                ch.send("\n")
    if col % 3 != 0:
        ch.send( "\n" )
    ch.send("\n")
 
    ch.send("Creation points: %d\n" % ch.gen_data.points_chosen)
    ch.send("Experience per level: %d\n" % ch.exp_per_level(ch.gen_data.points_chosen))
    return

# this procedure handles the input parsing for the skill generator */
def parse_gen_groups(ch, argument):
    if not argument.strip():
        return False

    argument, arg = read_word(argument)
    if "help".startswith(arg):
        if not argument:
            ch.do_help("group help")
            return True

        ch.do_help(argument)
        return True

    if "add".startswith(arg):
        if not argument:
            ch.send("You must provide a skill name.\n")
            return True
        argument = argument.lower()
        if argument in const.group_table:
            gn = const.group_table[argument]
            if gn.name in ch.gen_data.group_chosen or gn.name in ch.pcdata.group_known:
                ch.send("You already know that group!\n")
                return True
            
            if gn.rating[ch.guild.name] < 1:
                ch.send("That group is not available.\n")
                return True

            # Close security hole */
            if ch.gen_data.points_chosen + gn.rating[ch.guild.name] > 300:
                ch.send("You cannot take more than 300 creation points.\n")
                return True
            
            ch.send("%s group added\n" % gn.name)
            ch.gen_data.group_chosen[gn.name] = True
            ch.gen_data.points_chosen += gn.rating[ch.guild.name]
            gn_add(ch,gn)
            ch.pcdata.points += gn.rating[ch.guild.name]
            return True

        if argument in const.skill_table:
            sn = const.skill_table[argument]
            if sn.name in ch.gen_data.skill_chosen or sn.name in ch.pcdata.learned:
                ch.send("You already know that skill!\n")
                return True

            if sn.rating[ch.guild.name] < 1 or sn.spell_fun != spell_null:
                ch.send("That skill is not available.\n")
                return True
            # Close security hole */
            if ch.gen_data.points_chosen + sn.rating[ch.guild.name] > 300:
                ch.send("You cannot take more than 300 creation points.\n")
                return True
            
            ch.send("%s skill added\n" % sn.name)
            ch.gen_data.skill_chosen[sn.name] = True
            ch.gen_data.points_chosen += sn.rating[ch.guild.name]
            ch.pcdata.learned[sn] = 1
            ch.pcdata.points += sn.rating[ch.guild.name]
            return True

        ch.send("No skills or groups by that name...\n")
        return True

    if "drop".startswith(arg):
        if not argument:
            ch.send("You must provide a skill to drop.\n")
            return True
    
        argument = argument.lower()
        if argument in const.group_table and argument in ch.gen_data.group_chosen:
            gn = const.group_table[argument]
            ch.send("Group dropped.\n")
            del ch.gen_data.group_chosen[gn.name]
            ch.gen_data.points_chosen -= gn.rating[ch.guild.name]
            gn_remove(ch,gn)
            for k,v in ch.gen_data.group_chosen:
                gn_add(ch,const.group_table[k])
            ch.pcdata.points -= gn.rating[ch.guild.name]
            return True
     
        if argument in const.skill_table and argument in ch.gen_data.skill_chosen:
            sn = const.skill_table[argument]
            ch.send("Skill dropped.\n")
            del ch.gen_data.skill_chosen[sn.name]
            ch.gen_data.points_chosen -= sn.rating[ch.guild.name]
            del ch.pcdata.learned[sn]
            ch.pcdata.points -= sn.rating[ch.guild.name]
            return True

        ch.send("You haven't bought any such skill or group.\n")
        return True

    if "premise".startswith(arg):
        ch.do_help("premise")
        return True

    if "list".startswith(arg):
        list_group_costs(ch)
        return True

    if "learned".startswith(arg):
        list_group_chosen(ch)
        return True

    if "info".startswith(arg):
        ch.do_groups(argument)
        return True

    return False

# shows all groups, or the sub-members of a group */
def do_groups(self, argument):
    ch = self
    if IS_NPC(ch):
        return
    col = 0

    if not argument:
        # show all groups */
        for gn, group in const.group_table.items():
            if gn in ch.pcdata.group_known[gn]:
                ch.send("%-20s " % group.name)
                col += 1
                if col % 3 == 0:
                    ch.send("\n")
        if col % 3 != 0:
            ch.send( "\n" )
        ch.send("Creation points: %d\n" % ch.pcdata.points)
        return

    if "all" == argument.lower():
        for gn,group in const.group_table.items():
            ch.send("%-20s " % group.name)
            col += 1
            if col % 3 == 0:
                ch.send("\n")
        if col % 3 != 0:
            ch.send( "\n" )
        return
     
    # show the sub-members of a group */
    if argument.lower() not in const.group_table:
        ch.send("No group of that name exist.\n")
        ch.send("Type 'groups all' or 'info all' for a full listing.\n")
        return

    gn = const.group_table[argument.lower()]
    for sn in group.spells:
        if not sn:
            break
        ch.send("%-20s " % sn)
        col += 1
        if col % 3 == 0:
            ch.send("\n")
    if col % 3 != 0:
        ch.send( "\n" )


# checks for skill improvement */
def check_improve( ch, sn, success, multiplier ):
    if IS_NPC(ch):
        return
    if type(sn) == str:
        sn = const.skill_table[sn]

    if ch.level < sn.skill_level[ch.guild.name] \
    or sn.rating[ch.guild.name] == 0 \
    or sn.name not in ch.pcdata.learned \
    or ch.pcdata.learned[sn.name] == 100:
        return  # skill is not known */ 

    # check to see if the character has a chance to learn */
    chance = 10 * const.int_app[ch.get_curr_stat(STAT_INT)].learn
    chance /= (multiplier * sn.rating[ch.guild.name] * 4)
    chance += ch.level

    if random.randint(1,1000) > chance:
        return

    # now that the character has a CHANCE to learn, see if they really have */ 

    if success:
        chance = min(5, max(100 - ch.pcdata.learned[sn.name], 95))
        if random.randint(1,99) < chance:
            ch.send("You have become better at %s!\n" % sn.name)
            ch.pcdata.learned[sn.name] += 1
            update.gain_exp(ch,2 * sn.rating[ch.guild.name])
    else:
        chance = min(5, max(ch.pcdata.learned[sn.name]/2,30))
        if random.randint(1,99) < chance:
            ch.send("You learn from your mistakes, and your %s skill improves.\n" % sn.name)
            ch.pcdata.learned[sn.name] += random.randint(1,3)
            ch.pcdata.learned[sn.name] = min(ch.pcdata.learned[sn.name],100)
            update.gain_exp(ch,2 * sn.rating[ch.guild.name])
