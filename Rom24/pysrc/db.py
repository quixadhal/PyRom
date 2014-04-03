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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor (rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor (gtaylor@hypercube.org)			               *
*	    Brian Moore (zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
#***********
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




# * Repopulate areas periodically.
def area_update( ):
    for pArea in area_list:
        pArea.age += 1
        if pArea.age < 3:
            continue

        #
        #* Check age and reset.
        #* Note: Mud School resets every 3 minutes (not 15).
        #*/
        if(not pArea.empty and (pArea.nplayer == 0 or pArea.age >= 15)) or pArea.age >= 31:
            reset_area( pArea )
            wiznet("%s has just been reset." % pArea.name,None,None,WIZ_RESETS,0,0)
    
        pArea.age = random.randint( 0, 3 )
        pRoomIndex = room_index_hash[ROOM_VNUM_SCHOOL]
        if pRoomIndex and pArea == pRoomIndex.area:
            pArea.age = 15 - 2
        elif pArea.nplayer == 0:
            pArea.empty = True

#
# * Reset one area.
def reset_area( pArea ):
    mob     = None
    last    = True
    level   = 0
    for pReset in pArea.reset_first:
        if pReset.command == 'M':
            if pReset.arg1 not in mob_index_hash:
                print "Reset_area: 'M': bad vnum %d." % pReset.arg1
                continue
            pMobIndex = mob_index_hash[pReset.arg1]

            if pReset.arg3 not in room_index_hash:
                print "Reset_area: 'R': bad vnum %d." % pReset.arg3
                continue
            pRoomIndex = room_index_hash[pReset.arg3]

            if pMobIndex.count >= pReset.arg2:
                last = False
                break
            count = 0
            for mob in pRoomIndex.people:
                if mob.pIndexData == pMobIndex:
                    count += 1
                    if count >= pReset.arg4:
                        last = False
                        break

            if count >= pReset.arg4:
                continue

            mob = create_mobile( pMobIndex )

            #
            #* Check for pet shop.
            # */
            
            
            if pRoomIndex.vnum-1 in room_index_hash:
                pRoomIndexPrev = room_index_hash[pRoomIndex.vnum-1]
                if IS_SET(pRoomIndexPrev.room_flags, ROOM_PET_SHOP):
                    SET_BIT(mob.act, ACT_PET)

            # set area */
            mob.zone = pRoomIndex.area

            char_to_room( mob, pRoomIndex )
            level = min( 0, max(mob.level - 2, LEVEL_HERO - 1 ) )
            last  = True

        elif pReset.command ==  'O':
            if pReset.arg1 not in obj_index_hash:
                print "Reset_area: 'O': bad vnum %d." % pReset.arg1
                continue
            pObjIndex = obj_index_hash[pReset.arg1]

            if pReset.arg3 not in room_index_hash:
                print "Reset_area: 'R': bad vnum %d." % pReset.arg3
                continue
            pRoomIndex = room_index_hash[pReset.arg3]

            if pArea.nplayer > 0 or count_obj_list( pObjIndex, pRoomIndex.contents ) > 0:
                last = False
                continue

            obj = create_object( pObjIndex, min(number_fuzzy(level), LEVEL_HERO - 1) )
            obj.cost = 0
            obj_to_room( obj, pRoomIndex )
            last = True
            continue

        elif pReset.command == 'P':
            if pReset.arg1 not in obj_index_hash:
                print "Reset_area: 'P': bad vnum %d." % pReset.arg1
                continue
            pObjIndex = obj_index_hash[pReset.arg1]

            if pReset.arg3 not in obj_index_hash:
                print "Reset_area: 'P': bad vnum %d." % pReset.arg3
                continue
            pObjToIndex = obj_index_hash[pReset.arg3]
            if pReset.arg2 > 50: # old format */
                limit = 6
            elif pReset.arg2 == -1: # no limit */
                limit = 999
            else:
                limit = pReset.arg2
            
            obj_to = get_obj_type(pObjToIndex)
            count = count_obj_list(pObjIndex, obj_to.contains)
            if pArea.nplayer > 0 \
            or not obj_to \
            or (obj_to.in_room == None and not last) \
            or ( pObjIndex.count >= limit and random.randint(0,4) != 0) \
            or count > pReset.arg4:
                last = False
                break
            while count < pReset.arg4:
                obj = create_object( pObjIndex, number_fuzzy(obj_to.level) )
                obj_to_obj( obj, obj_to )
                count += 1
                if pObjIndex.count >= limit:
                    break

            # fix object lock state! */
            obj_to.value[1] = obj_to.pIndexData.value[1]
            last = True
        elif pReset.command == 'G' or pReset.command == 'E':
            if pReset.arg1 not in obj_index_hash:
                print "Reset_area: 'E' or 'G': bad vnum %d." % pReset.arg1
                continue
            pObjIndex = obj_index_hash[pReset.arg1]
            if not last:
                continue

            if not mob:
                print "Reset_area: 'E' or 'G': None mob for vnum %d." % pReset.arg1
                last = False
                continue
            olevel = 0
            if mob.pIndexData.pShop:
                if not pObjIndex.new_format:
                    if pObjIndex.item_type == ITEM_PILL \
                    or pObjIndex.item_type == ITEM_POTION \
                    or pObjIndex.item_type == ITEM_SCROLL:
                        olevel = 53
                        for i in pObjIndex.value:
                            if i > 0:
                                for j in skill_table[pObjIndex.value[i]].skill_level:
                                    olevel = min(olevel, j)
                       
                        olevel = max(0,(olevel * 3 / 4) - 2)
                        
                    elif pObjIndex.item_type == ITEM_WAND: olevel = random.randint( 10, 20 )
                    elif pObjIndex.item_type == ITEM_STAFF: olevel = random.randint( 15, 25 )
                    elif pObjIndex.item_type == ITEM_ARMOR: olevel = random.randint(  5, 15 )
                    elif pObjIndex.item_type == ITEM_WEAPON: olevel = random.randint(  5, 15 )
                    elif pObjIndex.item_type == ITEM_TREASURE: olevel = random.randint( 10, 20 )


                obj = create_object( pObjIndex, olevel )
                SET_BIT( obj.extra_flags, ITEM_INVENTORY )
            else:
                if pReset.arg2 > 50: # old format */
                    limit = 6
                elif pReset.arg2 == -1: # no limit */
                    limit = 999
                else:
                    limit = pReset.arg2

                if pObjIndex.count < limit or random.randint(0,4) == 0:
                    obj = create_object(pObjIndex,min(number_fuzzy(level), LEVEL_HERO - 1))
                # error message if it is too high */
                if obj.level > mob.level + 3 \
                or  (obj.item_type == ITEM_WEAPON  \
                and   pReset.command == 'E' \
                and   obj.level < mob.level -5 and obj.level < 45):
                    print "Err: obj %s (%d) -- %d, mob %s (%d) -- %d\n" % (
                    obj.short_descr,obj.pIndexData.vnum,obj.level,
                    mob.short_descr,mob.pIndexData.vnum,mob.level)
                else:
                    continue
            obj_to_char( obj, mob )
            if pReset.command == 'E':
                equip_char( mob, obj, pReset.arg3 )
                last = True
                continue

        elif pReset.command == 'D':
            if pReset.arg2 not in room_index_hash:
                print "Reset_area: 'D': bad vnum %d." % pReset.arg1
                continue
            pRoomIndex = room_index_hash[pReset.arg1]
            pexit = pRoomIndex.exit[pReset.arg2]
            if not pexit:
                continue

            if pReset.arg3 == 0:
                REMOVE_BIT( pexit.exit_info, EX_CLOSED )
                REMOVE_BIT( pexit.exit_info, EX_LOCKED )
                continue
            elif pReset.arg3 == 1:
                SET_BIT(pexit.exit_info, EX_CLOSED )
                REMOVE_BIT(pexit.exit_info, EX_LOCKED )
                continue
            elif pReset.arg3 == 2:
                SET_BIT(pexit.exit_info, EX_CLOSED )
                SET_BIT(pexit.exit_info, EX_LOCKED )
                continue
            last = True
            continue

        elif pReset.command == 'R':
            if pReset.arg1 not in room_index_hash:
                print "Reset_area: 'R': bad vnum %d." % pReset.arg1
                continue
            pRoomIndex = room_index_hash[pReset.arg1]
            for d0 in range(pReset.arg2 - 1):
                d1                   = random.randint( d0, pReset.arg2-1 )
                pexit                = pRoomIndex.exit[d0]
                pRoomIndex.exit[d0] = pRoomIndex.exit[d1]
                pRoomIndex.exit[d1] = pexit
                break
        else:
            print "Reset_area: bad command %c." % pReset.command


#
# * Create an instance of a mobile.

def create_mobile( pMobIndex ):
    mobile_count += 1
    if pMobIndex == None:
        print "Create_mobile: None pMobIndex."
        sys.exit( 1 )
    
    mob = CHAR_DATA()

    mob.pIndexData = pMobIndex

    mob.name = pMobIndex.player_name
    mob.id = get_mob_id()
    mob.short_descr = pMobIndex.short_descr
    mob.long_descr = pMobIndex.long_descr
    mob.description = pMobIndex.description
    mob.spec_fun = pMobIndex.spec_fun
    mob.prompt = None

    if pMobIndex.wealth == 0:
        mob.silver = 0
        mob.gold   = 0
    else:
        wealth = random.randint(pMobIndex.wealth/2, 3 * pMobIndex.wealth/2)
        mob.gold = random.randint(wealth/200,wealth/100)
        mob.silver = wealth - (mob.gold * 100)


    if pMobIndex.new_format:
    # load in new style */
        # read from prototype */
        mob.group = pMobIndex.group
        mob.act = pMobIndex.act
        mob.comm = COMM_NOCHANNELS|COMM_NOSHOUT|COMM_NOTELL
        mob.affected_by = pMobIndex.affected_by
        mob.alignment = pMobIndex.alignment
        mob.level = pMobIndex.level
        mob.hitroll = pMobIndex.hitroll
        mob.damroll = pMobIndex.damage[DICE_BONUS]
        mob.max_hit = dice(pMobIndex.hit[DICE_NUMBER], pMobIndex.hit[DICE_TYPE]) + pMobIndex.hit[DICE_BONUS]
        mob.hit = mob.max_hit
        mob.max_mana = dice(pMobIndex.mana[DICE_NUMBER], pMobIndex.mana[DICE_TYPE]) + pMobIndex.mana[DICE_BONUS]
        mob.mana = mob.max_mana
        mob.damage[DICE_NUMBER] = pMobIndex.damage[DICE_NUMBER]
        mob.damage[DICE_TYPE] = pMobIndex.damage[DICE_TYPE]
        mob.dam_type = pMobIndex.dam_type
        if mob.dam_type == 0:
            num = random.randint(1,3)
            if num == 1: mob.dam_type = 3 # slash */
            elif num == 2: mob.dam_type = 7 # pound */
            elif num == 3: mob.dam_type = 11 # pierce */
        for i in range(4):
            mob.armor[i] = pMobIndex.ac[i] 
        mob.off_flags      = pMobIndex.off_flags
        mob.imm_flags      = pMobIndex.imm_flags
        mob.res_flags      = pMobIndex.res_flags
        mob.vuln_flags     = pMobIndex.vuln_flags
        mob.start_pos      = pMobIndex.start_pos
        mob.default_pos    = pMobIndex.default_pos
        mob.sex        = pMobIndex.sex
        if mob.sex == 3: # random sex */
            mob.sex = random.randint(1,2)
        mob.race = pMobIndex.race
        mob.form = pMobIndex.form
        mob.parts = pMobIndex.parts
        mob.size = pMobIndex.size
        mob.material = pMobIndex.material

        # computed on the spot */
        for i in range(MAX_STATS):
            mob.perm_stat[i] = min(25,11 + mob.level/4)
            
        if IS_SET(mob.act,ACT_WARRIOR):
            mob.perm_stat[STAT_STR] += 3
            mob.perm_stat[STAT_INT] -= 1
            mob.perm_stat[STAT_CON] += 2
        
        if IS_SET(mob.act,ACT_THIEF):
            mob.perm_stat[STAT_DEX] += 3
            mob.perm_stat[STAT_INT] += 1
            mob.perm_stat[STAT_WIS] -= 1
        
        if IS_SET(mob.act,ACT_CLERIC):
            mob.perm_stat[STAT_WIS] += 3
            mob.perm_stat[STAT_DEX] -= 1
            mob.perm_stat[STAT_STR] += 1
        
        if IS_SET(mob.act,ACT_MAGE):
            mob.perm_stat[STAT_INT] += 3
            mob.perm_stat[STAT_STR] -= 1
            mob.perm_stat[STAT_DEX] += 1
        
        if IS_SET(mob.off_flags,OFF_FAST):
            mob.perm_stat[STAT_DEX] += 2
            
        mob.perm_stat[STAT_STR] += mob.size - SIZE_MEDIUM
        mob.perm_stat[STAT_CON] += (mob.size - SIZE_MEDIUM) / 2
        af = AFFECT_DATA()
        # let's get some spell action */
        if IS_AFFECTED(mob,AFF_SANCTUARY):
            af.where     = TO_AFFECTS
            af.type      = "sanctuary"
            af.level     = mob.level
            af.duration  = -1
            af.location  = APPLY_NONE
            af.modifier  = 0
            af.bitvector = AFF_SANCTUARY
            affect_to_char( mob, af )

        if IS_AFFECTED(mob,AFF_HASTE):
            af.where     = TO_AFFECTS
            af.type      = "haste"
            af.level     = mob.level
            af.duration  = -1
            af.location  = APPLY_DEX
            af.modifier  = 1 + (mob.level >= 18) + (mob.level >= 25) + (mob.level >= 32)
            af.bitvector = AFF_HASTE
            affect_to_char( mob, af )

        if IS_AFFECTED(mob,AFF_PROTECT_EVIL):
            af.where     = TO_AFFECTS
            af.type  = "protection evil"
            af.level     = mob.level
            af.duration  = -1
            af.location  = APPLY_SAVES
            af.modifier  = -1
            af.bitvector = AFF_PROTECT_EVIL
            affect_to_char(mob,af)

        if IS_AFFECTED(mob,AFF_PROTECT_GOOD):
            af.where     = TO_AFFECTS
            af.type      = "protection good"
            af.level     = mob.level
            af.duration  = -1
            af.location  = APPLY_SAVES
            af.modifier  = -1
            af.bitvector = AFF_PROTECT_GOOD
            affect_to_char(mob,af)
    else: # read in old format and convert */
        mob.act        = pMobIndex.act
        mob.affected_by    = pMobIndex.affected_by
        mob.alignment      = pMobIndex.alignment
        mob.level      = pMobIndex.level
        mob.hitroll        = pMobIndex.hitroll
        mob.damroll        = 0
        mob.max_hit        = mob.level * 8 + random.randint( mob.level * mob.level/4, mob.level * mob.level)
        mob.max_hit *= .9
        mob.hit        = mob.max_hit
        mob.max_mana       = 100 + dice(mob.level,10)
        mob.mana       = mob.max_mana
        num = random.randint(1,3)
        if num == 1: mob.dam_type = 3 # slash */
        elif num == 2: mob.dam_type = 7  # pound */
        elif num == 3: mob.dam_type = 11  # pierce */
        for i in range(3):
            mob.armor[i] = interpolate(mob.level,100,-100)
        mob.armor[3] = interpolate(mob.level,100,0)
        mob.race       = pMobIndex.race
        mob.off_flags      = pMobIndex.off_flags
        mob.imm_flags      = pMobIndex.imm_flags
        mob.res_flags      = pMobIndex.res_flags
        mob.vuln_flags     = pMobIndex.vuln_flags
        mob.start_pos      = pMobIndex.start_pos
        mob.default_pos    = pMobIndex.default_pos
        mob.sex        = pMobIndex.sex
        mob.form       = pMobIndex.form
        mob.parts      = pMobIndex.parts
        mob.size       = SIZE_MEDIUM
        mob.material       = ""

        for i in MAX_STATS:
            mob.perm_stat[i] = 11 + mob.level/4
    mob.position = mob.start_pos


    # link the mob to the world list */
    char_list.append(mob)
    return mob

# duplicate a mobile exactly -- except inventory */
def clone_mobile(parent, clone):
    if not parent or not clone or not IS_NPC(parent):
        return
    
    # start fixing values */ 
    clone.name     = parent.name
    clone.version  = parent.version
    clone.short_descr  = parent.short_descr
    clone.long_descr   = parent.long_descr
    clone.description  = parent.description
    clone.group    = parent.group
    clone.sex      = parent.sex
    clone.guild    = parent.guild
    clone.race     = parent.race
    clone.level    = parent.level
    clone.trust    = 0
    clone.timer    = parent.timer
    clone.wait     = parent.wait
    clone.hit      = parent.hit
    clone.max_hit  = parent.max_hit
    clone.mana     = parent.mana
    clone.max_mana = parent.max_mana
    clone.move     = parent.move
    clone.max_move = parent.max_move
    clone.gold     = parent.gold
    clone.silver   = parent.silver
    clone.exp      = parent.exp
    clone.act      = parent.act
    clone.comm     = parent.comm
    clone.imm_flags    = parent.imm_flags
    clone.res_flags    = parent.res_flags
    clone.vuln_flags   = parent.vuln_flags
    clone.invis_level  = parent.invis_level
    clone.affected_by  = parent.affected_by
    clone.position = parent.position
    clone.practice = parent.practice
    clone.train    = parent.train
    clone.saving_throw = parent.saving_throw
    clone.alignment    = parent.alignment
    clone.hitroll  = parent.hitroll
    clone.damroll  = parent.damroll
    clone.wimpy    = parent.wimpy
    clone.form     = parent.form
    clone.parts    = parent.parts
    clone.size     = parent.size
    clone.material = parent.material
    clone.off_flags    = parent.off_flags
    clone.dam_type = parent.dam_type
    clone.start_pos    = parent.start_pos
    clone.default_pos  = parent.default_pos
    clone.spec_fun = parent.spec_fun
    
    for i in range(4):
        clone.armor[i] = parent.armor[i]

    for i in range(MAX_STATS):
        clone.perm_stat[i] = parent.perm_stat[i]
        clone.mod_stat[i]  = parent.mod_stat[i]
    
    for i in range(3):
        clone.damage[i]    = parent.damage[i]

    # now add the affects */
    for paf in parent.affected:
        affect_to_char(clone,paf)

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


# duplicate an object exactly -- except contents */
def clone_object(parent, clone):
    if not parent or not clone:
        return

    # start fixing the object */
    clone.name     = parent.name
    clone.short_descr  = parent.short_descr
    clone.description  = parent.description
    clone.item_type    = parent.item_type
    clone.extra_flags  = parent.extra_flags
    clone.wear_flags   = parent.wear_flags
    clone.weight   = parent.weight
    clone.cost     = parent.cost
    clone.level    = parent.level
    clone.condition    = parent.condition
    clone.material = parent.material
    clone.timer    = parent.timer

    for i in parent.value:
        clone.value[i] = i

    # affects */
    clone.enchanted    = parent.enchanted
  
    for paf in parent.affected:
        affect_to_obj(clone,paf)

    # extended desc */
    for ed in parent.extra_descr:
        ed_new                  = EXTRA_DESCR_DATA()
        ed_new.keyword     =  ed.keyword
        ed_new.description     = ed.description
        clone.extra_descr.append(ed)

#
# * Clear a new character.
# */
def clear_char( ch ):
    ch.name            = ""
    ch.short_descr     = ""
    ch.long_descr      = ""
    ch.description     = ""
    ch.prompt          = ""
    ch.logon           = time.time()
    ch.lines           = 22
    for i in range(4):
        ch.armor[i]        = 100
    ch.position        = POS_STANDING
    ch.hit         = 20
    ch.max_hit         = 20
    ch.mana            = 100
    ch.max_mana        = 100
    ch.move            = 100
    ch.max_move        = 100
    ch.on          = None
    for i in MAX_STATS:
        ch.perm_stat[i] = 13 
        ch.mod_stat[i] = 0
    return
#
# * Get an extra description from a list.
def get_extra_descr( name, edlist ):
    for ed in edlist:
        if name.lower() in ed.keyword:
            return ed.description
    return None
