import os
import json
from collections import OrderedDict

import object_creator
from merc import *
import tables
import world_classes
import merc
import settings
import pc


def area_pickler():
    pass



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

#    if ( ch.contents != NULL )
 #       fwrite_obj( ch, ch.contents, fp, 0 );
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
    ch = pc.Pc(name)
    found = False
    pfile = os.path.join(settings.PLAYER_DIR, name + '.json')
    if os.path.isfile(pfile):
        chdict = json.load(open(pfile, 'r'))
        ch = fread_char(chdict, ch)
        found = True

    ch.desc = d
    d.character = ch
    ch.send = d.send
    return found, ch
    

def fwrite_char(ch):
    chdict = OrderedDict()
    chdict['instance_id'] = ch.instace_id
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
    if merc.rooms[ch.in_room].vnum == ROOM_VNUM_LIMBO and ch.was_in_room:
        in_room = ch.was_in_room
    elif not ch.in_room:
        in_room = merc.instances_by_room[ROOM_VNUM_TEMPLE][0]
    else:
        in_room = ch.in_room
    chdict["Room"] = in_room
    chdict["HMV"] = [ch.hit, ch.max_hit, ch.mana, ch.max_mana, ch.move, ch.max_move]
    chdict["Gold"] = min(0, ch.gold)
    chdict["Silv"] = min(0, ch.silver)
    chdict["Exp"] = ch.exp
    chdict["Act"] = ch.act.print_flags(tables.plr_flags)
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
        chdict["Vnum"] = ch.vnum
    else:
        chdict["Pass"] = ch.pwd
    chdict["Bin"] = ch.bamfin
    chdict["Bout"] = ch.bamfout
    chdict["Titl"] = ch.title
    chdict["Pnts"] = ch.points
    chdict["TSex"] = ch.true_sex
    chdict["LLev"] = ch.last_level
    chdict["HMVP"] = [ch.perm_hit, ch.perm_mana, ch.perm_move]
    chdict["Cnd"] = ch.condition
    chdict['alias'] = ch.alias
    chdict['skills'] = ch.learned
    chdict['groups'] = ch.group_known
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
        odict['In'] = contained_by.instance_id
    if obj.contents:
        odict['contents'] = [fwrite_obj(ch, o, obj) for o in obj.contents]
    return odict


def fread_char(chdict, ch):
    ch.name = chdict['name']
    ch.id = chdict['id']
    ch.short_descr = chdict["ShD"]
    ch.long_descr = chdict["LnD"]
    ch.description = chdict["Desc"]
    ch.prompt = chdict["Prom"]
    ch.race = chdict["Race"]
    ch.clan = chdict["Clan"]
    ch.sex = int(chdict["Sex"])
    ch._guild = chdict["Cla"]
    ch.level = chdict["Levl"]
    ch.trust = chdict["Tru"]
    ch.played = chdict["Plyd"]
    ch.lines = chdict["Scro"]
    room = merc.instances_by_room[chdict["Room"]][0]
    if not room:
        room = chdict["Room"]
    ch.in_environment = room
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
        ch.vnum = chdict["Vnum"]
    else:
        ch.pwd = chdict["Pass"]
    ch.bamfin = chdict["Bin"]
    ch.bamfout = chdict["Bout"]
    ch.title = chdict["Titl"]
    ch.points = chdict["Pnts"]
    ch.true_sex = chdict["TSex"]
    ch.last_level = chdict["LLev"]
    ch.perm_hit, ch.perm_mana, ch.perm_move = chdict["HMVP"]
    ch.condition = chdict["Cnd"]
    ch.alias = chdict['alias']
    ch.learned = chdict['skills']
    ch.group_known = chdict['groups']
    ch.affected = chdict['affected']
    if 'contents' in chdict:
        fread_items(ch, chdict['contents'])
    return ch


def fread_items(contents, objects, contained_by=None):
    for odict in objects:
        item = fread_item(contents, odict)
        if not contained_by:
            item.to_environment(contents)
        else:
            item.to_environment(contained_by)
        if 'contents' in odict:
            fread_items(contents, odict['contents'], item)


def fread_item(contents, odict):
    item = object_creator.create_item(itemTemplate[odict['Vnum']], odict['Lev'])
    item.enchanted = odict['Enchanted']
    item.name = odict['Name']
    item.short_descr = odict['ShD']
    item.description = odict['Desc']
    item.extra_flags = odict['ExtF']
    item.wear_flags = odict['WeaF']
    item.item_type = odict['Ityp']
    item.weight = odict['Wt']
    item.condition = odict['Cond']
    item.wear_loc = odict['Wear']
    item.level = odict['Lev']
    item.timer = odict['timer']
    item.cost = odict['cost']
    item.value = odict['Val']

    item.affected = odict['affected']
    extra_descr = []
    for k, v in odict['ExDe'].items():
        newed = world_classes.ExtraDescrData()
        newed.keyword = k
        newed.description = v
        extra_descr.append(newed)
    item.extra_descr = extra_descr
    return item
