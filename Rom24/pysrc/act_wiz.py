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
 ************/
"""
from merc import *
import nanny
from handler import get_trust, get_eq_char, obj_to_char, equip_char
from db import create_object
from const import weapon_table

def wiznet( string, ch, obj, flag, flag_skip, min_level):
    for d in descriptor_list:
        if   d.connected == nanny.con_playing \
        and  IS_IMMORTAL(d.character) \
        and  IS_SET(d.character.wiznet, WIZ_ON) \
        and  (not flag or IS_SET(d.character.wiznet,flag)) \
        and  (not flag_skip or not IS_SET(d.character.wiznet,flag_skip)) \
        and  get_trust(d.character) >= min_level \
        and  d.character != ch:
            if IS_SET(d.character.wiznet,WIZ_PREFIX):
                d.send("-. ",d.character)
            act(string,d.character,obj,ch,TO_CHAR,POS_DEAD)


# equips a character */
def do_outfit ( self, argument ):
    ch = self
    if ch.level > 5 or IS_NPC(ch):
        ch.send("Find it yourself!\n\r")
        return  

    obj = get_eq_char(ch, WEAR_LIGHT)
    if not obj:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_BANNER], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_LIGHT )

    obj = get_eq_char(ch, WEAR_BODY) 
    if not obj:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_VEST], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_BODY )

    # do the weapon thing */
    obj = get_eq_char(ch,WEAR_WIELD)
    if not obj:
        sn = 'dagger'
        vnum = OBJ_VNUM_SCHOOL_SWORD # just in case! */
        for k,weapon in weapon_table.iteritems():
            if sn not in ch.pcdata.learned or (weapon.gsn in ch.pcdata.learned and ch.pcdata.learned[sn] < ch.pcdata.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum

        obj = create_object(obj_index_hash[vnum],0)
        obj_to_char(obj,ch)
        equip_char(ch,obj,WEAR_WIELD)

    obj = get_eq_char(ch,WEAR_WIELD) 
    shield = get_eq_char( ch, WEAR_SHIELD )
    if (not obj or not IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS)) and not shield:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_SHIELD], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_SHIELD )

    ch.send("You have been equipped by Mota.\n\r")
