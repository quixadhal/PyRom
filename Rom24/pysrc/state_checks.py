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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
__author__ = 'syn'
import time
import logging

logger = logging.getLogger()

import merc


def IS_SET(flag, bit):
    return flag & bit


def SET_BIT(var, bit):
    return var | bit


def REMOVE_BIT(var, bit):
    return var & ~bit


#utility functions
def name_lookup(pdict, arg, key='name'):
    for i, n in pdict.items():
        if getattr(n, key) == arg:
            return i


def prefix_lookup(pdict, arg):
    if not arg:
        return None
    results = [v for k, v in pdict.items() if k.startswith(arg)]
    if results:
        return results[0]
    return None


def value_lookup(pdict, arg):
    if not arg:
        return None
    for k, v in pdict.items():
        if v == arg:
            return k


def PERS(ch, looker):
    if not looker.can_see(ch):
        return "someone"
    if ch.is_npc():
        return ch.short_descr
    else:
        return ch.name


def OPERS(looker, item):
    if not looker.can_see_item(item.instance_id):
        return "something"
    return item.short_descr


def IS_NPC(ch):
    return ch.act.is_set(merc.ACT_IS_NPC)


def IS_IMMORTAL(ch):
    return ch.trust >= merc.LEVEL_IMMORTAL


def IS_HERO(ch):
    return ch.trust >= merc.LEVEL_HERO


def IS_TRUSTED(ch, level):
    return ch.trust >= level


def is_affected(ch, sn):
    return True if [paf for paf in ch.affected if paf.type == sn][:1] else False


def IS_AFFECTED(ch, bit):
    return IS_SET(ch.affected_by, bit)


def GET_AGE(ch):
    return int((17 + (ch.played + time.time() - ch.logon) / 72000))


def IS_GOOD(ch):
    return ch.alignment >= 350


def IS_EVIL(ch):
    return ch.alignment <= -350


def IS_NEUTRAL(ch):
    return not IS_GOOD(ch) and not IS_EVIL(ch)


def IS_AWAKE(ch):
    return ch.position > merc.POS_SLEEPING


def GET_AC(ch, ptype):
    from const import dex_app
    return ch.armor[ptype] + (dex_app[ch.stat(merc.STAT_DEX)].defensive if IS_AWAKE(ch) else 0)


def GET_HITROLL(ch):
    from const import str_app
    return ch.hitroll + str_app[ch.stat(merc.STAT_STR)].tohit


def GET_DAMROLL(ch):
    from const import str_app
    return ch.damroll + str_app[ch.stat(merc.STAT_STR)].todam


def IS_OUTSIDE(ch):
    return not IS_SET(ch.in_room.room_flags, merc.ROOM_INDOORS)


def WAIT_STATE(ch, npulse):
    ch.wait = max(ch.wait, npulse)


def DAZE_STATE(ch, npulse):
    ch.daze = max(ch.daze, npulse)


def get_carry_weight(ch):
    return ch.carry_weight + (ch.silver // 10 + (ch.gold * 2 // 5))


 # Object macros.

def CAN_WEAR(item, part):
    return IS_SET(item.wear_flags, part)


def IS_WEAPON_STAT(item, stat):
    return IS_SET(item.value[4], stat)


def WEIGHT_MULT(item):
    return item.value[4] if item.item_type is merc.ITEM_CONTAINER else 100

def check_blind(ch):
    if not IS_NPC(ch) and IS_SET(ch.act, merc.PLR_HOLYLIGHT):
        return True

    if IS_AFFECTED(ch, merc.AFF_BLIND):
        ch.send("You can't see a thing!\n\r")
        return False
    return True


# find an effect in an affect list */
def affect_find(paf, sn):
    found = [paf_find for paf_find in paf if paf_find.type == sn][:1]
    if found:
        return found[0]
    else:
        return None
