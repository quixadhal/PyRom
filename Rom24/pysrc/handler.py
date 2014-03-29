
"""
/***************************************************************************
 *  Original Diku Mud copyright=C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright=C) 1992, 1993 by Michael          *
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
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                        *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""

from merc import *

def check_immune(ch,dam_type):
    immune = -1
    defence = IS_NORMAL;

    if dam_type is DAM_NONE:
        return immune

    if dam_type <= 3:
        if IS_SET(ch.imm_flags,IMM_WEAPON):
            defence = IS_IMMUNE
        elif IS_SET(ch.res_flags,RES_WEAPON):
            defence = IS_RESISTANT
        elif IS_SET(ch.vuln_flags,VULN_WEAPON):
            defence = IS_VULNERABLE
    else: # magical attack */
        if IS_SET(ch.imm_flags,IMM_MAGIC):
            defence = IS_IMMUNE
        elif IS_SET(ch.res_flags,RES_MAGIC):
            defence = IS_RESISTANT
        elif IS_SET(ch.vuln_flags,VULN_MAGIC):
            defence = IS_VULNERABLE

    bit = {  DAM_BASH:IMM_BASH,
             DAM_PIERCE:IMM_PIERCE,
             DAM_SLASH:IMM_SLASH,
             DAM_FIRE:IMM_FIRE,
             DAM_COLD:IMM_COLD,
             DAM_LIGHTNING:IMM_LIGHTNING,
             DAM_ACID:IMM_ACID,
             DAM_POISON:IMM_POISON,
             DAM_NEGATIVE:IMM_NEGATIVE,
             DAM_HOLY:IMM_HOLY,
             DAM_ENERGY:IMM_ENERGY,
             DAM_MENTAL:IMM_MENTAL,
             DAM_DISEASE:IMM_DISEASE,
             DAM_DROWNING:IMM_DROWNING,
             DAM_LIGHT:IMM_LIGHT,
             DAM_CHARM:IMM_CHARM,
             DAM_SOUND:IMM_SOUND }
    if dam_type not in bit:
        return defence
    bit = bit[dam_type]

    if IS_SET(ch.imm_flags,bit):
        immune = IS_IMMUNE
    elif IS_SET(ch.res_flags,bit) and immune is not IS_IMMUNE:
        immune = IS_RESISTANT
    elif IS_SET(ch.vuln_flags,bit):
        if immune == IS_IMMUNE:
            immune = IS_RESISTANT
        elif immune == IS_RESISTANT:
            immune = IS_NORMAL
    else:
        immune = IS_VULNERABLE

    if immune == -1:
        return defence
    else:
        return immune    



#* Retrieve a character's trusted level for permission checking.
def get_trust( ch ):
    if ch.desc and ch.desc.original:
        ch = ch.desc.original;

    if ch.trust:
        return ch.trust

    if IS_NPC(ch) and ch.level >= LEVEL_HERO:
        return LEVEL_HERO - 1
    else:
        return ch.level
