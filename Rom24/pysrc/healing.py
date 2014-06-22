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
from magic import *
from const import skill_table

def do_heal(ch, argument):
    # check for healer */
    mob = [mob for mob in ch.in_room.people if IS_NPC(mob) and IS_SET(mob.act, ACT_IS_HEALER)][:1]
    if not mob:
        ch.send("You can't do that here.\n\r")
        return
    mob = mob[0]
    argument, arg = read_word(argument)
    if not arg:
        # display price list */
        act("$N says 'I offer the following spells:'",ch,None,mob,TO_CHAR)
        ch.send("  light: cure light wounds      10 gold\n\r")
        ch.send("  serious: cure serious wounds  15 gold\n\r")
        ch.send("  critic: cure critical wounds  25 gold\n\r")
        ch.send("  heal: healing spell       50 gold\n\r")
        ch.send("  blind: cure blindness         20 gold\n\r")
        ch.send("  disease: cure disease         15 gold\n\r")
        ch.send("  poison:  cure poison          25 gold\n\r") 
        ch.send("  uncurse: remove curse         50 gold\n\r")
        ch.send("  refresh: restore movement      5 gold\n\r")
        ch.send("  mana:  restore mana       10 gold\n\r")
        ch.send(" Type heal <type> to be healed.\n\r")
        return
    spell = None
    sn = None
    words = None
    cost = 0
    if "light".startswith(arg):
        spell = spell_cure_light
        sn = skill_table["cure light"]
        words = "judicandus dies"
        cost  = 1000
    elif "serious".startswith(arg):
        spell = spell_cure_serious
        sn = skill_table["cure serious"]
        words = "judicandus gzfuajg"
        cost  = 1600
    elif "critical".startswith(arg):
        spell = spell_cure_critical
        sn = skill_table["cure critical"]
        words = "judicandus qfuhuqar"
        cost  = 2500
    elif "heal".startswith(arg):
        spell = spell_heal
        sn = skill_table["heal"]
        words = "pzar"
        cost = 5000
    elif "blindness".startswith(arg):
        spell = spell_cure_blindness
        sn = skill_table["cure blindness"]
        words = "judicandus noselacri"     
        cost  = 2000
    elif "disease".startswith(arg):
        spell = spell_cure_disease
        sn = skill_table["cure disease"]
        words = "judicandus eugzagz"
        cost = 1500
    elif "poison".startswith(arg):
        spell = spell_cure_poison
        sn = skill_table["cure poison"]
        words = "judicandus sausabru"
        cost  = 2500
    elif "uncurse".startswith(arg) or "curse".startswith(arg):
        spell = spell_remove_curse 
        sn = skill_table["remove curse"]
        words = "candussido judifgz"
        cost  = 5000
    elif "mana".startswith(arg) or "energize".startswith(arg):
        spell = None
        sn = None
        words = "energizer"
        cost = 1000
    elif "refresh".startswith(arg) or "moves".startswith(arg):
        spell =  spell_refresh
        sn = skill_table["refresh"]
        words = "candusima" 
        cost  = 500
    else:
        act("$N says 'Type 'heal' for a list of spells.'",ch,None,mob,TO_CHAR)
        return
    if cost > (ch.gold * 100 + ch.silver):
        act("$N says 'You do not have enough gold for my services.'",ch,None,mob,TO_CHAR)
        return
    WAIT_STATE(ch,PULSE_VIOLENCE)

    ch.deduct_cost(cost)
    mob.gold += cost / 100
    mob.silver += cost % 100
    act("$n utters the words '$T'.",mob,None,words,TO_ROOM)
  
    if spell == None: # restore mana trap...kinda hackish */ kinda?
        ch.mana += dice(2,8) + mob.level / 3
        ch.mana = UMIN(ch.mana,ch.max_mana)
        ch.send("A warm glow passes through you.\n\r")
        return
    if sn == -1:
        return
    spell(sn,mob.level,mob,ch,TARGET_CHAR)
