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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor (rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor (gtaylor@hypercube.org)			               *
*	    Brian Moore (zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
import os, sys
from settings import AREA_DIR, AREA_LIST
from merc import *

def boot_db():
    print "Loading Areas..."
    load_areas()
    fix_exits()
    print "\t...Loaded %d Helpfiles" % len(help_list)
    print "\t...Loaded %d Areas" % len(area_list)
    print "\t...Loaded %d Mobile Indexes" % len(mob_index_hash)
    print "\t...Loaded %d Object Indexes" % len(obj_index_hash)
    print "\t...Loaded %d Room Indexes" % len(room_index_hash)
    print "\t...Loaded %d Resets" % len(reset_list)
    print "\t...Loaded %d Shops" % len(shop_list)
    print "\t...Loaded %d Socials" % len(social_list)

def load_areas():
    area_list = os.path.join(AREA_DIR, AREA_LIST)
    fp = open(area_list, 'r')
    area = fp.readline().strip()
    while area != "$":
        afp = open(os.path.join(AREA_DIR, area), 'r' )
        load_area( afp.read() )
        area = fp.readline().strip()
        afp.close()
    fp.close()

def load_area(area):
    if not area.strip():
        return

    area, w = read_word(area,False)
    pArea = None
    while ( area ):
        if w == "#AREA":
            pArea = AREA_DATA()
            area, pArea.file_name = read_string(area)
            area, pArea.name = read_string(area)
            area, pArea.credits = read_string(area)
            area, pArea.min_vnum = read_int(area)
            area, pArea.max_vnum = read_int(area)
            area_list.append(pArea)
            print "\t...%s" % pArea

        elif w == "#HELPS":
            area = load_helps(area)
        elif w == "#MOBILES":
            area = load_mobiles(area)
        elif w == "#OBJECTS":
            area = load_objects(area)
        elif w == "#RESETS":
            area = load_resets(area, pArea)
        elif w == "#ROOMS":
            area = load_rooms(area, pArea)
        elif w == "#SHOPS":
            area = load_shops(area)
        elif w == "#SOCIALS":
            area = load_socials(area)
        elif w == "#SPECIALS":
            area = load_specials(area)
        elif w == '#$':
            break
        else:
            print "Bad section name: " + w

        area, w = read_word(area,False)
    

def load_helps(area):
    while True:
        help = HELP_DATA()
        area, help.level = read_int(area)
        area, help.keyword = read_string(area)
        
        if help.keyword == '$':
            del help
            break

        area, help.text = read_string(area)
        
        if help.keyword == "GREETING":
            greeting_list.append(help)
            
        help_list.append(help)
    return area
         

def load_mobiles(area):
    area, w = read_word(area,False)
    w = w[1:] # strip the pound

    while w != '0':
        mob = MOB_INDEX_DATA()
        mob.vnum = int(w)
        mob_index_hash[mob.vnum] = mob
        area, mob.player_name = read_string(area)
        area, mob.short_descr = read_string(area)
        area, mob.long_descr = read_string(area)
        area, mob.description = read_string(area)
        area, mob.race = read_string(area)
        area, mob.act = read_flags(area)
        area, mob.affected_by = read_flags(area)
        area, mob.alignment = read_int(area)
        area, mob.group = read_int(area)
        area, mob.level = read_int(area)
        area, mob.hitroll = read_int(area)
        area, mob.hit[0] = read_int(area)
        area = read_forward(area)
        area, mob.hit[1] = read_int(area)
        area = read_forward(area)
        area, mob.hit[2] = read_int(area)
        area, mob.mana[0] = read_int(area)
        area = read_forward(area)
        area, mob.mana[1] = read_int(area)
        area = read_forward(area)
        area, mob.mana[2] = read_int(area)
        area, mob.damage[0] = read_int(area)
        area = read_forward(area)
        area, mob.damage[1] = read_int(area)
        area = read_forward(area)
        area, mob.damage[2] = read_int(area)
        area, mob.dam_type = read_word(area,False)
        area, mob.ac[0] = read_int(area)
        area, mob.ac[1] = read_int(area)
        area, mob.ac[2] = read_int(area)
        area, mob.ac[3] = read_int(area)
        area, mob.off_flags = read_flags(area)
        area, mob.imm_flags = read_flags(area)
        area, mob.res_flags = read_flags(area)
        area, mob.vuln_flags = read_flags(area)
        area, mob.start_pos = read_word(area,False)
        area, mob.default_pos = read_word(area,False)
        area, mob.sex = read_word(area,False)
        area, mob.wealth = read_int(area)
        area, mob.form = read_flags(area)
        area, mob.parts = read_flags(area)
        area, mob.size = read_word(area,False)
        area, mob.material = read_word(area,False)
        area, w = read_word(area,False)

        while w == 'F':
            area, word = read_word(area,False)
            area, vector = read_flags(area)
            area, w = read_word(area,False)

        w = w[1:] # strip the pound         
    return area

def load_objects(area):
    area, w = read_word(area,False)
    w = w[1:] # strip the pound
    while w != '0':
        obj = OBJ_INDEX_DATA()
        obj.vnum = int(w)
        obj_index_hash[obj.vnum] = obj
        area, obj.name = read_string(area)
        area, obj.short_descr = read_string(area)
        
        area, obj.description = read_string(area)
        area, obj.material = read_string(area)
        area, item_type = read_word(area,False)
        area, obj.extra_flags = read_flags(area)
        area, obj.wear_flags = read_flags(area)

        if obj.item_type == ITEM_WEAPON:
            area, obj.value[0] = read_word(area,False)
            area, obj.value[1] = read_int(area)
            area, obj.value[2] = read_int(area)
            area, obj.value[3] = read_word(area,False)
            area, obj.value[4] = read_flags(area)
        elif obj.item_type == ITEM_CONTAINER:
            area, obj.value[0] = read_int(area)
            area, obj.value[1] = read_flags(area)
            area, obj.value[2] = read_int(area)
            area, obj.value[3] = read_int(area)
            area, obj.value[4] = read_int(area)
        elif obj.item_type == ITEM_DRINK_CON or obj.item_type == ITEM_FOUNTAIN:
            area, obj.value[0] = read_int(area)
            area, obj.value[1] = read_int(area)
            area, obj.value[2] = read_word(area,False)
            area, obj.value[3] = read_word(area,False)
            area, obj.value[4] = read_int(area)
        elif obj.item_type == ITEM_WAND or obj.item_type == ITEM_STAFF:
            area, obj.value[0] = read_int(area)
            area, obj.value[1] = read_int(area)
            area, obj.value[2] = read_int(area)
            area, obj.value[3] = read_word(area,False)
            area, obj.value[4] = read_int(area)
        elif obj.item_type == ITEM_POTION or obj.item_type == ITEM_POTION or obj.item_type == ITEM_PILL:
            area, obj.value[0] = read_int(area)
            area, obj.value[1] = read_word(area,False)
            area, obj.value[2] = read_word(area,False)
            area, obj.value[3] = read_word(area,False)
            area, obj.value[4] = read_word(area,False)
        else:
            area, obj.value[0] = read_flags(area)
            area, obj.value[1] = read_flags(area)
            area, obj.value[2] = read_flags(area)
            area, obj.value[3] = read_flags(area)
            area, obj.value[4] = read_flags(area)
        obj.item_type = item_type
        area, obj.level = read_int(area)
        area, obj.weight = read_int(area)
        area, obj.cost = read_int(area)
        area, obj.condition = read_word(area,False)
        if obj.condition == 'P':
            obj.condition = 100
        elif obj.condition == 'G':
            obj.condition = 90
        elif obj.condition == 'A':
            obj.condition = 75
        elif obj.condition == 'W':
            obj.condition = 50
        elif obj.condition == 'D':
            obj.condition = 25
        elif obj.condition == 'B':
            obj.condition = 10
        elif obj.condition == 'R':
            obj.condition = 0
        else:
            obj.condition = 100

        area, w = read_word(area,False)

        while w == 'F' or w == 'A' or w == 'E':
            if w == 'F':
                area, word = read_word(area,False)
                area, number = read_int(area)
                area, number = read_int(area)
                area, flags = read_flags(area)
            elif w == 'A':
                area, number = read_int(area)
                area, number = read_int(area)
            elif w == 'E':
                area, string = read_string(area)
                area, string = read_string(area)

            area, w = read_word(area,False)

        w = w[1:] # strip the pound         
    return area

def load_resets(area, pArea):
    while True:
        area, letter = read_letter(area)
        if letter == 'S':
            break

        if letter == '*':
            area, t = read_to_eol(area)
            continue

        reset = RESET_DATA()
        reset.command = letter
        area, number = read_int(area) #if_flag
        area, reset.arg1 = read_int(area)
        area, reset.arg2 = read_int(area)
        area, reset.arg3 = (area, 0) if letter == 'G' or letter == 'R' else read_int(area)
        area, reset.arg4 = read_int(area) if letter == 'P' or letter == 'M' else (area, 0)
        area, t = read_to_eol(area)
        pArea.reset_list.append(reset)
        reset_list.append(reset)
    return area


def load_rooms(area, pArea):
    area, w = read_word(area,False)
    w = w[1:] # strip the pound
    while w != '0':
        room = ROOM_INDEX_DATA()
        room.vnum = int(w)
        if room.vnum in room_index_hash:
            print "Dupicate room Vnum: %d" % room.vnum
            sys.exit(1)

        room_index_hash[room.vnum] = room
        room.area = pArea
        area, room.name = read_string(area)
        area, room.description = read_string(area)
        area, number = read_int(area) #area number
        area, room.room_flags = read_flags(area)
        area, room.sector_type = read_int(area)
        while True:
            area, letter = read_letter(area)
            
            if letter == 'S':
                break
            elif letter == 'H': #Healing Room
                area, room.heal_rate = read_int(area)
            elif letter == 'M': #Mana Room
                area, room.mana_rate = read_int(area)
            elif letter == 'C': #Clan
                area, room.clan = read_string(area)
            elif letter == 'D': #exit
                exit = EXIT_DATA()
                area, door = read_int(area)
                area, exit.description = read_string(area)
                area, exit.keyword = read_string(area)
                area, locks = read_int(area)
                area, exit.key = read_int(area)
                area, exit.vnum = read_int(area)
                room.exit[door] = exit
            elif letter == 'E':
                ed = EXTRA_DESCR_DATA()
                area, ed.keyword = read_string(area)
                area, ed.description = read_string(area)
                room.extra_descr.append(ed)
            elif letter == 'O':
                area, room.owner = read_string(area)
            else:
                print "RoomIndexData(%d) has flag other than SHMCDEO: %s" % ( room.vnum, letter )
                sys.exit(1)
        area, w = read_word(area,False)
        w = w[1:] # strip the pound         
    return area

def load_shops(area):
    while True:
        area, keeper = read_int(area)

        if keeper == 0:
            break
        shop = SHOP_DATA()
        shop.keeper = keeper
        for r in range(MAX_TRADE):
            area, shop.buy_type[r] = read_int(area)
        area, shop.profit_buy = read_int(area)            
        area, shop.profit_sell = read_int(area)
        area, shop.open_hour = read_int(area)
        area, shop.close_hour = read_int(area)
        area, t = read_to_eol(area)
        mob_index_hash[keeper].pShop = shop
        shop_list.append(shop)
    return area

def load_socials(area):
    while True:
        area, word = read_word(area,False)

        if word == '#0':
            return
        social = SOCIAL_DATA()
        area, line = read_to_eol(area)

        if line == '$':
            social.char_no_arg = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.char_no_arg = line

        area, line = read_to_eol(area)

        if line == '$':
            social.others_no_arg = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.others_no_arg = line
        area, line = read_to_eol(area)

        if line == '$':
            social.char_found = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.char_found = line
        area, line = read_to_eol(area)

        if line == '$':
            social.others_found = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.others_found = line
        area, line = read_to_eol(area)

        if line == '$':
            social.vict_found = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.vict_found = line
        area, line = read_to_eol(area)

        if line == '$':
            social.char_not_found = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.char_not_found = line
        area, line = read_to_eol(area)

        if line == '$':
            social.char_auto = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.char_auto = line
        area, line = read_to_eol(area)

        if line == '$':
            social.others_auto = None
        elif line == '#':
            if social not in social_list:
                social_list.append(social)
            continue
        else:
            social.others_auto = line

        if social not in social_list:
            social_list.append(social)
    return area

def load_specials(area):
    while True:
        area, letter = read_letter(area)

        if letter == '*':
            area, t = read_to_eol(area)
            continue
        elif letter == 'S':
            return area
        elif letter == 'M':
            area, vnum = read_int(area)
            area, mob_index_hash[vnum].spec_fun = read_word(area,False)
        else:
            print "Load_specials: letter noth *SM: " + letter
    
    return area

def fix_exits():
    for k, r in room_index_hash.iteritems():
        for e in r.exit:
            if type(e.to_room) == int:
                if e.to_room not in room_index_hash:
                    print "Fix_exits: Failed to find to_room for %d: %d" % (room, e.to_room)
                else:
                    e.to_room = room_index_hash[e.to_room]



# * Create an instance of an object.
def create_object( pObjIndex, level ):
    if not pObjIndex:
        print "Create_object: None pObjIndex."
        sys.exit( 1 )

    obj = OBJ_DATA()

    obj.pIndexData = pObjIndex
    obj.in_room    = None
    obj.enchanted  = False

    if pObjIndex.new_format == True:
        obj.level = pObjIndex.level
    else:
        obj.level      = max(0,level)
    obj.wear_loc   = -1

    obj.name       = pObjIndex.name
    obj.short_descr    = pObjIndex.short_descr
    obj.description    = pObjIndex.description
    obj.material   = pObjIndex.material
    obj.item_type  = pObjIndex.item_type
    obj.extra_flags    = pObjIndex.extra_flags
    obj.wear_flags = pObjIndex.wear_flags
    obj.value = pObjIndex.value[:]
    obj.weight     = pObjIndex.weight

    if level == -1 or pObjIndex.new_format:
        obj.cost   = pObjIndex.cost
    else:
        obj.cost   = number_fuzzy( 10 ) * number_fuzzy( level ) * number_fuzzy( level )


     # Mess with object properties.
    if obj.item_type == ITEM_LIGHT:
        if obj.value[2] == 999:
            obj.value[2] = -1
    elif obj.item_type == ITEM_FURNITURE \
      or obj.item_type == ITEM_TRASH \
      or obj.item_type == ITEM_CONTAINER \
      or obj.item_type == ITEM_DRINK_CON \
      or obj.item_type == ITEM_KEY \
      or obj.item_type == ITEM_FOOD \
      or obj.item_type == ITEM_BOAT \
      or obj.item_type == ITEM_CORPSE_NPC \
      or obj.item_type == ITEM_CORPSE_PC \
      or obj.item_type == ITEM_FOUNTAIN \
      or obj.item_type == ITEM_MAP \
      or obj.item_type == ITEM_CLOTHING \
      or obj.item_type == ITEM_PORTAL:
        if not pObjIndex.new_format:
            obj.cost /= 5
    elif obj.item_type == ITEM_TREASURE \
      or obj.item_type == ITEM_WARP_STONE \
      or obj.item_type == ITEM_ROOM_KEY \
      or obj.item_type == ITEM_GEM \
      or obj.item_type == ITEM_JEWELRY:
        pass
    elif obj.item_type == ITEM_JUKEBOX:
        obj.value = [-1 for i in range(5)]
    elif obj.item_type == ITEM_SCROLL:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0]   = number_fuzzy( obj.value[0] )
    elif obj.item_type == ITEM_WAND \
      or obj.item_type == ITEM_STAFF:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0]   = number_fuzzy( obj.value[0] )
            obj.value[1]   = number_fuzzy( obj.value[1] )
            obj.value[2]   = obj.value[1]
        if not pObjIndex.new_format:
            obj.cost *= 2
    elif obj.item_type == ITEM_WEAPON:
        if level != -1 and not pObjIndex.new_format:
            obj.value[1] = number_fuzzy( number_fuzzy( 1 * level / 4 + 2 ) )
            obj.value[2] = number_fuzzy( number_fuzzy( 3 * level / 4 + 6 ) )
    elif obj.item_type == ITEM_ARMOR:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0]   = number_fuzzy( level / 5 + 3 )
            obj.value[1]   = number_fuzzy( level / 5 + 3 )
            obj.value[2]   = number_fuzzy( level / 5 + 3 )
    elif obj.item_type == ITEM_POTION \
      or obj.item_type == ITEM_PILL:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0] = number_fuzzy( number_fuzzy( obj.value[0] ) )
    elif obj.item_type == ITEM_MONEY:
        if not pObjIndex.new_format:
            obj.value[0]   = obj.cost
    else:
        print "Bad item_type pObjIndex vnum: %s(%s)" % (pObjIndex.vnum, obj.item_type )
  
    for paf in pObjIndex.affected:
        if paf.location == APPLY_SPELL_AFFECT:
            affect_to_obj(obj,paf)
  
    object_list.append(obj)
    return obj

