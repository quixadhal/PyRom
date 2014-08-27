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
import random
import logging

logger = logging.getLogger()

from merc import *
import const
import game_utils
import magic


# recursively adds a group given its number -- uses group_add */
def gn_add( ch, gn):
    ch.group_known[gn.name] = True
    for i in gn.spells:
        if not i:
            break
        group_add(ch,i,False)

# recusively removes a group given its number -- uses group_remove */
def gn_remove( ch, gn):
    if gn.name in ch.group_known:
        del ch.group_known[gn.name]

    for i in gn.spells:
        if not i:
            return
        group_remove(ch,i)

# use for processing a skill or group for addition  */
def group_add( ch, name, deduct):
    if ch.is_npc(): # NPCs do not have skills */
        return
    
    if name in const.skill_table:
        sn = const.skill_table[name]
        if sn.name not in ch.learned: # i.e. not known */
            ch.learned[sn.name] = 1
        if deduct:
            ch.points += sn.rating[ch.guild.name]
        return

    # now check groups */

    if name in const.group_table:
        gn = const.group_table[name]
        if gn.name not in ch.group_known:
            ch.group_known[gn.name] = True
        if deduct:
            ch.points += gn.rating[ch.guild.name]
    
        gn_add(ch,gn) # make sure all skills in the group are known */


# used for processing a skill or group for deletion -- no points back! */

def group_remove(ch, name):
    
    if name in const.skill_table:
        sn = const.skill_table[name]
        if sn.name in ch.learned:
            del ch.learned[sn.name]
            return

    # now check groups */
    if name in const.group_table:
        gn = const.group_table[name]
        
        if gn.name in ch.group_known:
            del ch.group_known[gn.name]
            gn_remove(ch,gn) # be sure to call gn_add on all remaining groups */




# shows skills, groups and costs (only if not bought) */
def list_group_costs(ch):
    if ch.is_npc():
        return
    col = 0
    ch.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("group","cp","group","cp","group","cp"))

    for gn, group in const.group_table.items():
        if gn not in ch.gen_data.group_chosen and gn not in ch.group_known and group.rating[ch.guild.name] > 0:
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
        and sn not in ch.learned \
        and  skill.spell_fun == magic.spell_null \
        and  skill.rating[ch.guild.name] > 0:
            ch.send("%-18s %-5d " % (skill.name, skill.rating[ch.guild.name]))
            col += 1
            if col % 3 == 0:
                ch.send("\n")
    if  col % 3 != 0:
        ch.send( "\n" )
    ch.send("\n")

    ch.send("Creation points: %d\n" % ch.points)
    ch.send("Experience per level: %d\n" % ch.exp_per_level(ch.gen_data.points_chosen))
    return

def list_group_chosen(ch):
    if ch.is_npc():
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

    argument, arg = game_utils.read_word(argument)
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
            if gn.name in ch.gen_data.group_chosen or gn.name in ch.group_known:
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
            ch.points += gn.rating[ch.guild.name]
            return True

        if argument in const.skill_table:
            sn = const.skill_table[argument]
            if sn.name in ch.gen_data.skill_chosen or sn.name in ch.learned:
                ch.send("You already know that skill!\n")
                return True

            if sn.rating[ch.guild.name] < 1 or sn.spell_fun != magic.spell_null:
                ch.send("That skill is not available.\n")
                return True
            # Close security hole */
            if ch.gen_data.points_chosen + sn.rating[ch.guild.name] > 300:
                ch.send("You cannot take more than 300 creation points.\n")
                return True
            
            ch.send("%s skill added\n" % sn.name)
            ch.gen_data.skill_chosen[sn.name] = True
            ch.gen_data.points_chosen += sn.rating[ch.guild.name]
            ch.learned[sn] = 1
            ch.points += sn.rating[ch.guild.name]
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
            ch.points -= gn.rating[ch.guild.name]
            return True
     
        if argument in const.skill_table and argument in ch.gen_data.skill_chosen:
            sn = const.skill_table[argument]
            ch.send("Skill dropped.\n")
            del ch.gen_data.skill_chosen[sn.name]
            ch.gen_data.points_chosen -= sn.rating[ch.guild.name]
            del ch.learned[sn]
            ch.points -= sn.rating[ch.guild.name]
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
# checks for skill improvement */
def check_improve( ch, sn, success, multiplier ):
    import const
    import update
    if ch.is_npc():
        return
    if type(sn) == str:
        sn = const.skill_table[sn]

    if ch.level < sn.skill_level[ch.guild.name] \
    or sn.rating[ch.guild.name] == 0 \
    or sn.name not in ch.learned \
    or ch.learned[sn.name] == 100:
        return  # skill is not known */ 

    # check to see if the character has a chance to learn */
    chance = 10 * const.int_app[ch.stat(STAT_INT)].learn
    chance /= (multiplier * sn.rating[ch.guild.name] * 4)
    chance += ch.level

    if random.randint(1,1000) > chance:
        return

    # now that the character has a CHANCE to learn, see if they really have */ 

    if success:
        chance = max(5, min(100 - ch.learned[sn.name], 95))
        if random.randint(1,99) < chance:
            ch.send("You have become better at %s!\n" % sn.name)
            ch.learned[sn.name] += 1
            update.gain_exp(ch,2 * sn.rating[ch.guild.name])
    else:
        chance = max(5, min(ch.learned[sn.name]/2,30))
        if random.randint(1,99) < chance:
            ch.send("You learn from your mistakes, and your %s skill improves.\n" % sn.name)
            ch.learned[sn.name] += random.randint(1,3)
            ch.learned[sn.name] = min(ch.learned[sn.name],100)
            update.gain_exp(ch,2 * sn.rating[ch.guild.name])
