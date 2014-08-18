import os
import json
from collections import OrderedDict

import object_creator
import instance
from merc import *
import tables
import world_classes
import merc
import settings
import pc
import auth


def area_pickler():
    pass


def recursive_item_jsonify(item_to_json, inv_dir: str=None, equip_dir: str=None,
                           is_equipment: bool=False, is_in_inventory: bool=False):
    if is_equipment:
        to_equipped = json.dumps(item_to_json, default=instance.to_json, indent=4)
        equip_write = os.path.join(equip_dir, str(item_to_json.instance_id) + '.json')
        with open(equip_write, 'w') as eq:
            eq.write(to_equipped)
        if item_to_json.inventory:
            for item_id in item_to_json.inventory:
                new_item = merc.items[item_id]
                recursive_item_jsonify(new_item, equip_dir=equip_dir, is_equipment=True)
        else:
            return
    if is_in_inventory:
        to_inventory = json.dumps(item_to_json, default=instance.to_json, indent=4)
        inventory_write = os.path.join(inv_dir, str(item_to_json.instance_id) + '.json')
        with open(inventory_write, 'w') as inv:
            inv.write(to_inventory)
        if item_to_json.inventory:
            for item_id in item_to_json.inventory:
                new_item = merc.items[item_id]
                recursive_item_jsonify(new_item, inv_dir=inv_dir, is_in_inventory=True)
        else:
            return


def save_char_obj(ch):
    if ch.is_npc():
        return

    if ch.desc and ch.desc.original:
        ch = ch.desc.original
    #A Quick Quix fix!
    os.makedirs(settings.PLAYER_DIR, 0o755, True)
    os.makedirs(settings.PLAYER_DIR + "/" + ch.name, 0o755, True)
    os.makedirs(settings.PLAYER_DIR + "/" + ch.name + "/" + 'equipped', 0o755, True)
    os.makedirs(settings.PLAYER_DIR + "/" + ch.name + "/" + 'inventory', 0o755, True)
    char_dir = os.path.join(settings.PLAYER_DIR, ch.name)
    pfile = os.path.join(char_dir, ch.name + '.json')
    inventory = os.path.join(char_dir, 'inventory')
    equipped = os.path.join(char_dir, 'equipped')

    if ch.equipped:
        #fwrite['equipped'] = [fwrite_item(ch, merc.items[ins], None, loc) for loc, ins in ch.equipped.items() if ins]
        for item_id in ch.equipped.values():
            if item_id:
                recursive_item_jsonify(merc.items[item_id], equip_dir=equipped, is_equipment=True)

    if ch.inventory:
        for item_id in ch.inventory:
            recursive_item_jsonify(merc.items[item_id], inv_dir=inventory, is_in_inventory=True)
        #fwrite['inventory'] = [fwrite_item(ch, merc.items[i]) for i in ch.inventory]

    to_write = json.dumps(ch, default=instance.to_json, indent=4)
    with open(pfile, 'w') as pf:
        pf.write(to_write)

#    if ( ch.inventory != NULL )
 #       fwrite_obj( ch, ch.inventory, fp, 0 );
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
    found = False
    ch = pc.Pc.load(name)
    if ch:
        found = True
    else:
        ch = pc.Pc(name)
    ch.desc = d
    d.character = ch
    ch.send = d.send
    return found, ch
    

def fwrite_char(ch):
    chdict = OrderedDict()
    chdict['instance_id'] = ch.instance_id
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
        in_room = ch.was_in_room
    elif not ch.in_room:
        in_room = merc.instances_by_room[ROOM_VNUM_TEMPLE][0]
    else:
        in_room = ch.in_room
    chdict["Room"] = in_room.vnum
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
        if ch.auth:
            chdict["Auth"] = ch.auth.secret
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
    chdict['equipped'] = ch.equipped
    chdict['inventory'] = ch.inventory
    return chdict


def get_if_diff(s1, s2):
    return s1 if s1 != s2 else s2


def fwrite_item(ch, item, contained_by=None, equip_loc=None):
    #TODO make this eq-ified
    odict = OrderedDict()
    odict['instance_id'] = item.instance_id
    odict['Vnum'] = item.vnum
    odict['Enchanted'] = item.enchanted
    odict['Name'] = item.name
    odict['ShD'] = item.short_descr
    odict['Desc'] = item.description
    odict['EqpT'] = item.equips_to
    odict['IatR'] = item.item_attributes
    odict['IrsT'] = item.item_restrictions
    odict['WeaT'] = item.weapon_attributes
    odict['WeaF'] = item.equips_to
    odict['Ityp'] = item.item_type
    odict['Wt'] = item.weight
    odict['Cond'] = item.condition
    odict['Lev'] = item.level
    odict['timer'] = item.timer
    odict['cost'] = item.cost
    odict['Val'] = item.value

    odict['affected'] = [a for a in item.affected if a.type >= 0]
    odict['ExDe'] = {ed.keyword: ed.description for ed in item.extra_descr}
    if equip_loc:
        odict['to_loc'] = equip_loc
    if contained_by:
        odict['In'] = contained_by.instance_id
    if item.inventory:
        odict['inventory'] = [fwrite_item(ch, o, item) for o in item.inventory]
    return odict


def fread_char(chdict, ch):
    #instance_id is already set so is omitted
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
    ch.environment = room
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
        if "Auth" in chdict:
            ch.auth = auth.TwoFactorAuth(chdict["Auth"])
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
    if 'equipped' in chdict:
        fread_items(ch, chdict['equipped'])
    if 'inventory' in chdict:
        fread_items(ch, chdict['inventory'])
    return ch


def fread_items(contents, objects, contained_by=None):
    for odict in objects:
        item = fread_item(contents, odict)
        if not contained_by:
            contents.put(item)
        else:
            contained_by.put(item)
        if 'equipped_to' in odict:
            if contents.is_living:
                contents.equip(item, False, False, False, odict['to_loc'])
        if 'inventory' in odict:
            fread_items(contents, odict['inventory'], item)


def fread_item(contents, odict):
    item = object_creator.create_item(itemTemplate[odict['Vnum']], odict['Lev'], odict['instance_id'])
    item.enchanted = odict['Enchanted']
    item.name = odict['Name']
    item.short_descr = odict['ShD']
    item.description = odict['Desc']
    item.equips_to = odict['EqpT']
    item.item_attributes = odict['IatR']
    item.item_restrictions = odict['IrsT']
    item.weapon_attributes = odict['WeaT']
    item.item_type = odict['Ityp']
    item.weight = odict['Wt']
    item.condition = odict['Cond']
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
