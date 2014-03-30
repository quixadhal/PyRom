"""
/***************************************************************************
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

/***************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""

from merc import *
from const import *

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
    
    if name in skill_table:
        sn = skill_table[name]
        if sn.name not in ch.pcdata.learned: # i.e. not known */
            ch.pcdata.learned[sn.name] = 1
        if deduct:
            ch.pcdata.points += sn.rating[ch.guild.name] 
        return

    # now check groups */

    if name in group_table:
        gn = group_table[name]
        if gn.name not in ch.pcdata.group_known:
            ch.pcdata.group_known[gn.name] = True
        if deduct:
            ch.pcdata.points += gn.rating[ch.guild.name]
    
        gn_add(ch,gn) # make sure all skills in the group are known */


# used for processing a skill or group for deletion -- no points back! */

def group_remove(ch, name):
    
    if name in skill_table:
        sn = skill_table[name]
        if sn.name in ch.pcdata.learned:
            del ch.pcdata.learned[sn.name]
            return

    # now check groups */
    if name in group_table:
        gn = group_table[name]
        
        if gn.name in ch.pcdata.group_known:
            del ch.pcdata.group_known[gn.name]
            gn_remove(ch,gn) # be sure to call gn_add on all remaining groups */
