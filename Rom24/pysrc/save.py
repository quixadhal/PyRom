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
import os
import json
from collections import OrderedDict

from merc import *

import db
import handler_olc
import const
import handler_ch
import settings
import state_checks
import tables
import character

def save_char_obj(ch):
    if ch.is_npc():
        return

    if ch.desc and ch.desc.original:
        ch = ch.desc.original

    pfile = os.path.join(settings.PLAYER_DIR, ch.name + '.json')
    #A Quick Quix fix!
    os.makedirs(settings.PLAYER_DIR, 0o755, True)

    fwrite = fwrite_char(ch)
    if ch.contents:
        fwrite['contents'] = [fwrite_obj(ch, o) for o in ch.contents]

    to_write = json.dumps(fwrite, indent=4)
    with open(pfile, 'w') as pf:
        pf.write(to_write)

#    if ( ch.carrying != NULL )
 #       fwrite_obj( ch, ch.carrying, fp, 0 );
 #   /* save the pets */
 #   if (ch.pet != NULL and ch.pet.in_room == ch.in_room)
 #       fwrite_pet(ch.pet,fp);
 #   chdict["#END\n" );
 ##   }
  #  fclose( fp );
  #  rename(TEMP_FILE,strsave);
  #  fpReserve = fopen( NULL_FILE, "r" );


def load_char_obj(d, name):
    #ch = handler_ch.CHAR_DATA()
    #ch.pcdata = handler_ch.PC_DATA()
    ch = character.Character()
    ch.name = name
    found = False
    pfile = os.path.join(settings.PLAYER_DIR, name + '.json')
    if os.path.isfile(pfile):
        chdict = json.load(open(pfile, 'r'))
        ch = fread_char(chdict, ch)
        found = True

    ch.desc = d
    d.character = ch
    ch.send = d.send
    player_list.append(ch)
    return found, ch
    

def fwrite_char(ch):
    chdict = OrderedDict()
    chdict['name'] = ch.name
    chdict['id'] = ch.id
    chdict['logo'] = time.time()
    chdict['vers'] = 5
    chdict["ShD"] = ch.short_descr
    chdict["LnD"] = ch.long_descr
    chdict["Desc"] = ch.description
    chdict["Prom"] = ch.prompt
    chdict["Race"] = ch.race.name
    chdict["Clan"] = ch.clan.name
    chdict["Sex"] = ch.sex
    chdict["Cla"] = ch.guild.name
    chdict["Levl"] = ch.level
    chdict["Tru"] = ch.trust
    chdict["Plyd"] = ch.played + int(current_time - ch.logon)
    chdict["Scro"] = ch.lines
    if ch.in_room.vnum == ROOM_VNUM_LIMBO and ch.was_in_room:
        in_room = ch.was_in_room.vnum
    elif not ch.in_room:
        in_room = ROOM_VNUM_TEMPLE
    else:
        in_room = ch.in_room.vnum
    chdict["Room"] = in_room
    chdict["HMV"] = [ch.hit, ch.max_hit, ch.mana, ch.max_mana, ch.move, ch.max_move]
    chdict["Gold"] = min(0, ch.gold)
    chdict["Silv"] = min(0, ch.silver)
    chdict["Exp"] = ch.exp
    chdict["Act"] = repr(ch.act)
    chdict["AfBy"] = repr(ch.affected_by)
    chdict["Comm"] = repr(ch.comm)
    chdict["Wizn"] = repr(ch.wiznet)
    chdict["Invi"] = ch.invis_level
    chdict["Inco"] = ch.incog_level
    chdict["Pos"] = POS_STANDING if ch.position == POS_FIGHTING else ch.position
    chdict["Prac"] = ch.practice
    chdict["Trai"] = ch.train
    chdict["Save"] = ch.saving_throw
    chdict["Alig"] = ch.alignment
    chdict["Hit"] = ch.hitroll
    chdict["Dam"] = ch.damroll
    chdict["ACs"] = ch.armor
    chdict["Wimp"] = ch.wimpy
    chdict["Attr"] = ch.perm_stat
    chdict["AMod"] = ch.mod_stat
    if ch.is_npc():
        chdict["Vnum"] = ch.pIndexData.vnum
    else:
        chdict["Pass"] = ch.pcdata.pwd
    chdict["Bin"] = ch.pcdata.bamfin
    chdict["Bout"] = ch.pcdata.bamfout
    chdict["Titl"] = ch.pcdata.title
    chdict["Pnts"] = ch.pcdata.points
    chdict["TSex"] = ch.pcdata.true_sex
    chdict["LLev"] = ch.pcdata.last_level
    chdict["HMVP"] = [ch.pcdata.perm_hit, ch.pcdata.perm_mana, ch.pcdata.perm_move]
    chdict["Cnd"] = ch.pcdata.condition
    chdict['alias'] = ch.pcdata.alias
    chdict['skills'] = ch.pcdata.learned
    chdict['groups'] = ch.pcdata.group_known
    chdict['affected'] = [a for a in ch.affected if a.type >= 0]
    return chdict


def get_if_diff(s1, s2):
    return s1 if s1 != s2 else s2


def fwrite_obj(ch, obj, contained_by=None):
    odict = OrderedDict()
    odict['Vnum'] = obj.pIndexData.vnum
    odict['Enchanted'] = obj.enchanted
    odict['Name'] = get_if_diff(obj.name, obj.pIndexData.name)
    odict['ShD'] = get_if_diff(obj.short_descr, obj.pIndexData.short_descr)
    odict['Desc'] = get_if_diff(obj.description, obj.pIndexData.description)
    odict['ExtF'] = get_if_diff(obj.extra_flags, obj.pIndexData.extra_flags)
    odict['WeaF'] = get_if_diff(obj.wear_flags, obj.pIndexData.wear_flags)
    odict['Ityp'] = get_if_diff(obj.item_type, obj.pIndexData.item_type)
    odict['Wt'] = get_if_diff(obj.weight, obj.pIndexData.weight)
    odict['Cond'] = get_if_diff(obj.condition, obj.pIndexData.condition)
    
    odict['Wear'] = obj.wear_loc
    odict['Lev'] = obj.level
    odict['timer'] = obj.timer
    odict['cost'] = obj.cost
    odict['Val'] = get_if_diff(obj.value, obj.pIndexData.value)

    odict['affected'] = [a for a in obj.affected if a.type >= 0]
    odict['ExDe'] = {ed.keyword: ed.description for ed in obj.extra_descr}
    if contained_by:
        odict['In'] = contained_by.pIndexData.vnum 
    if obj.contains:
        odict['contains'] = [fwrite_obj(ch, o, obj) for o in obj.contains]
    return odict


def fread_char(chdict, ch):
    ch.name = chdict['name']
    ch.id = chdict['id']

    ch.short_descr = chdict["ShD"]
    ch.long_descr = chdict["LnD"]
    ch.description = chdict["Desc"]
    ch.prompt = chdict["Prom"]
    ch.race = const.race_table[chdict["Race"]]
    ch.clan = tables.clan_table[chdict["Clan"]]
    ch.sex = int(chdict["Sex"])
    ch._guild = chdict["Cla"]
    ch.level = chdict["Levl"]
    ch.trust = chdict["Tru"]
    ch.played = chdict["Plyd"]
    ch.lines = chdict["Scro"]
    ch.in_room = room_index_hash[chdict["Room"]]
    ch.hit, ch.max_hit, ch.mana, ch.max_mana, ch.move, ch.max_move = chdict["HMV"]
    ch.gold = chdict["Gold"]
    ch.silver = chdict["Silv"]
    ch.exp = chdict["Exp"]
    ch.act.set_bit(chdict["Act"])
    ch.affected_by.set_bit(chdict["AfBy"])
    ch.comm.set_bit(chdict["Comm"])
    ch.wiznet.set_bit(chdict["Wizn"])
    ch.invis_level = chdict["Invi"]
    ch.incog_level = chdict["Inco"]
    ch.position = chdict["Pos"]
    ch.practice = chdict["Prac"]
    ch.train = chdict["Trai"]
    ch.saving_throw = chdict["Save"]
    ch.alignment = chdict["Alig"]
    ch.hitroll = chdict["Hit"]
    ch.damroll = chdict["Dam"]
    ch.armor = chdict["ACs"]
    ch.wimpy = chdict["Wimp"]
    ch.perm_stat = chdict["Attr"]
    ch.mod_stat = chdict["AMod"]
    if ch.is_npc():
        ch.pIndexData.vnum = chdict["Vnum"]
    else:
        ch.pcdata.pwd = chdict["Pass"]
    ch.pcdata.bamfin = chdict["Bin"]
    ch.pcdata.bamfout = chdict["Bout"]
    ch.pcdata.title = chdict["Titl"]
    ch.pcdata.points = chdict["Pnts"]
    ch.pcdata.true_sex = chdict["TSex"]
    ch.pcdata.last_level = chdict["LLev"]
    ch.pcdata.perm_hit, ch.pcdata.perm_mana, ch.pcdata.perm_move = chdict["HMVP"]
    ch.pcdata.condition = chdict["Cnd"]
    ch.pcdata.alias = chdict['alias']
    ch.pcdata.learned = chdict['skills']
    ch.pcdata.group_known = chdict['groups']
    ch.affected = chdict['affected']
    if 'contents' in chdict:
        fread_objs(ch, chdict['contents'])
    return ch


def fread_objs(contents, objects, contained_by=None):
    for odict in objects:
        obj = fread_obj(contents, odict)
        if not contained_by:
            obj.to_char(contents)
        else:
            obj.to_obj(contained_by)
        if 'contains' in odict:
            fread_objs(contents, odict['contains'], obj)


def fread_obj(contents, odict):
    obj = db.create_object(obj_index_hash[odict['Vnum']], odict['Lev'])
    obj.enchanted = odict['Enchanted']
    obj.name = odict['Name']
    obj.short_descr = odict['ShD']
    obj.description = odict['Desc']
    obj.extra_flags = odict['ExtF']
    obj.wear_flags = odict['WeaF']
    obj.item_type = odict['Ityp']
    obj.weight = odict['Wt']
    obj.condition = odict['Cond']

    obj.wear_loc = odict['Wear']
    obj.level = odict['Lev']
    obj.timer = odict['timer']
    obj.cost = odict['cost']
    obj.value = odict['Val']

    obj.affected = odict['affected']
    extra_descr = []
    for k, v in odict['ExDe'].items():
        newed = handler_olc.EXTRA_DESCR_DATA()
        newed.keyword = k
        newed.description = v
        extra_descr.append(newed)
    obj.extra_descr = extra_descr
    return obj
