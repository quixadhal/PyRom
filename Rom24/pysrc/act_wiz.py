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

def wiznet( string, ch, obj, flag, flag_skip, min_level):
    for d in descriptor_list
        if   d.connected == CON_PLAYING \
        and  IS_IMMORTAL(d.character) \
        and  IS_SET(d.character.wiznet, WIZ_ON) \
        and  (not flag or IS_SET(d.character.wiznet,flag)) \
        and  (not flag_skip or not IS_SET(d.character.wiznet,flag_skip)) \
        and  get_trust(d.character) >= min_level \
        and  d.character != ch:
            if IS_SET(d.character.wiznet,WIZ_PREFIX):
                d.send("-. ",d.character)
            act(string,d.character,obj,ch,TO_CHAR,POS_DEAD)
