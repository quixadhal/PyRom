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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import logging

logger = logging.getLogger()

import os
import random
import sys
import time

import merc
import handler_ch
import handler_obj
import handler_room
import settings
import special
import state_checks
import tables
import game_utils
import handler_game
import handler_olc
import const


def boot_db():
    init_time()
    load_areas()
    fix_exits()
    area_update()
    logger.info('    Loaded %d Help files', len(merc.help_list))
    logger.info('    Loaded %d Areas', len(merc.area_list))
    logger.info('    Loaded %d Mobile Indexes', len(merc.mob_index_hash))
    logger.info('    Loaded %d Object Indexes', len(merc.obj_index_hash))
    logger.info('    Loaded %d Room Indexes', len(merc.room_index_hash))
    logger.info('    Loaded %d Resets', len(merc.reset_list))
    logger.info('    Loaded %d Shops', len(merc.shop_list))
    logger.info('    Loaded %d Socials', len(merc.social_list))


def load_areas():
    logger.info('Loading Areas...')
    narea_list = os.path.join(settings.AREA_DIR, settings.AREA_LIST)
    fp = open(narea_list, 'r')
    area = fp.readline().strip()
    while area != "$":
        afp = open(os.path.join(settings.AREA_DIR, area), 'r')
        load_area(afp.read())
        area = fp.readline().strip()
        afp.close()
    fp.close()
    logger.info('Done. (loading areas)')


def load_area(area):
    if not area.strip():
        return

    area, w = game_utils.read_word(area, False)
    pArea = None
    while area:
        if w == "#AREA":
            pArea = handler_olc.AREA_DATA()
            area, pArea.file_name = game_utils.read_string(area)
            area, pArea.name = game_utils.read_string(area)
            area, pArea.credits = game_utils.read_string(area)
            area, pArea.min_vnum = game_utils.read_int(area)
            area, pArea.max_vnum = game_utils.read_int(area)
            merc.area_list.append(pArea)
            logger.info("    Loading %s", pArea)

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
            logger.error('Bad section name: %s', w)

        area, w = game_utils.read_word(area, False)


def load_helps(area):
    while True:
        nhelp = handler_game.HELP_DATA()
        area, nhelp.level = game_utils.read_int(area)
        area, nhelp.keyword = game_utils.read_string(area)

        if nhelp.keyword == '$':
            del nhelp
            break

        area, nhelp.text = game_utils.read_string(area)

        if nhelp.keyword == "GREETING":
            merc.greeting_list.append(nhelp)

        merc.help_list.append(nhelp)
    return area


def load_mobiles(area):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound

    while w != '0':
        mob = handler_ch.MOB_INDEX_DATA()
        mob.vnum = int(w)
        merc.mob_index_hash[mob.vnum] = mob
        area, mob.player_name = game_utils.read_string(area)
        area, mob.short_descr = game_utils.read_string(area)
        area, mob.long_descr = game_utils.read_string(area)
        area, mob.description = game_utils.read_string(area)
        area, mob.race = game_utils.read_string(area)
        mob.race = const.race_table[mob.race]
        area, mob.act = game_utils.read_flags(area)
        mob.act = mob.act | merc.ACT_IS_NPC | mob.race.act
        area, mob.affected_by = game_utils.read_flags(area)
        mob.affected_by = mob.affected_by | mob.race.aff
        area, mob.alignment = game_utils.read_int(area)
        area, mob.group = game_utils.read_int(area)
        area, mob.level = game_utils.read_int(area)
        area, mob.hitroll = game_utils.read_int(area)
        area, mob.hit[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit[2] = game_utils.read_int(area)
        area, mob.mana[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana[2] = game_utils.read_int(area)
        area, mob.damage[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.damage[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.damage[2] = game_utils.read_int(area)
        area, mob.dam_type = game_utils.read_word(area, False)
        mob.dam_type = state_checks.name_lookup(const.attack_table, mob.dam_type)
        area, mob.ac[0] = game_utils.read_int(area)
        area, mob.ac[1] = game_utils.read_int(area)
        area, mob.ac[2] = game_utils.read_int(area)
        area, mob.ac[3] = game_utils.read_int(area)
        area, mob.off_flags = game_utils.read_flags(area)
        mob.off_flags = mob.off_flags | mob.race.off
        area, mob.imm_flags = game_utils.read_flags(area)
        mob.imm_flags = mob.imm_flags | mob.race.imm
        area, mob.res_flags = game_utils.read_flags(area)
        mob.res_flags = mob.res_flags | mob.race.res
        area, mob.vuln_flags = game_utils.read_flags(area)
        mob.vuln_flags = mob.vuln_flags | mob.race.vuln
        area, mob.start_pos = game_utils.read_word(area, False)
        area, mob.default_pos = game_utils.read_word(area, False)
        mob.start_pos = state_checks.name_lookup(tables.position_table, mob.start_pos, 'short_name')
        mob.default_pos = state_checks.name_lookup(tables.position_table, mob.default_pos, 'short_name')
        area, sex = game_utils.read_word(area, False)
        mob.sex = state_checks.value_lookup(tables.sex_table, sex)
        area, mob.wealth = game_utils.read_int(area)
        area, mob.form = game_utils.read_flags(area)
        mob.form = mob.form | mob.race.form
        area, mob.parts = game_utils.read_flags(area)
        mob.parts = mob.parts | mob.race.parts
        area, mob.size = game_utils.read_word(area, False)
        area, mob.material = game_utils.read_word(area, False)
        area, w = game_utils.read_word(area, False)
        mob.size = tables.size_table.index(mob.size)
        while w == 'F':
            area, word = game_utils.read_word(area, False)
            area, vector = game_utils.read_flags(area)
            area, w = game_utils.read_word(area, False)

        w = w[1:]  # strip the pound
    return area


def load_objects(area):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        obj = handler_obj.OBJ_INDEX_DATA()
        obj.vnum = int(w)
        merc.obj_index_hash[obj.vnum] = obj
        area, obj.name = game_utils.read_string(area)
        area, obj.short_descr = game_utils.read_string(area)

        area, obj.description = game_utils.read_string(area)
        area, obj.material = game_utils.read_string(area)
        area, item_type = game_utils.read_word(area, False)
        area, obj.extra_flags = game_utils.read_flags(area)
        area, obj.wear_flags = game_utils.read_flags(area)
        obj.item_type = item_type

        if obj.item_type == merc.ITEM_WEAPON:
            area, obj.value[0] = game_utils.read_word(area, False)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_word(area, False)
            obj.value[3] = state_checks.name_lookup(const.attack_table, obj.value[3])
            area, obj.value[4] = game_utils.read_flags(area)
        elif obj.item_type == merc.ITEM_CONTAINER:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_flags(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_int(area)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_DRINK_CON or obj.item_type == merc.ITEM_FOUNTAIN:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_word(area, False)
            area, obj.value[3] = game_utils.read_int(area)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_WAND or obj.item_type == merc.ITEM_STAFF:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_word(area, False)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_POTION or obj.item_type == merc.ITEM_POTION or obj.item_type == merc.ITEM_PILL:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_word(area, False)
            area, obj.value[2] = game_utils.read_word(area, False)
            area, obj.value[3] = game_utils.read_word(area, False)
            area, obj.value[4] = game_utils.read_word(area, False)
        else:
            area, obj.value[0] = game_utils.read_flags(area)
            area, obj.value[1] = game_utils.read_flags(area)
            area, obj.value[2] = game_utils.read_flags(area)
            area, obj.value[3] = game_utils.read_flags(area)
            area, obj.value[4] = game_utils.read_flags(area)

        area, obj.level = game_utils.read_int(area)
        area, obj.weight = game_utils.read_int(area)
        area, obj.cost = game_utils.read_int(area)
        area, obj.condition = game_utils.read_word(area, False)
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

        area, w = game_utils.read_word(area, False)

        while w == 'F' or w == 'A' or w == 'E':
            if w == 'F':
                area, word = game_utils.read_word(area, False)
                area, number = game_utils.read_int(area)
                area, number = game_utils.read_int(area)
                area, flags = game_utils.read_flags(area)
            elif w == 'A':
                area, number = game_utils.read_int(area)
                area, number = game_utils.read_int(area)
            elif w == 'E':
                ed = handler_olc.EXTRA_DESCR_DATA()
                area, ed.keyword = game_utils.read_string(area)
                area, ed.description = game_utils.read_string(area)
                obj.extra_descr.append(ed)

            area, w = game_utils.read_word(area, False)

        w = w[1:]  # strip the pound
    return area


def load_resets(area, pArea):
    while True:
        area, letter = game_utils.read_letter(area)
        if letter == 'S':
            break

        if letter == '*':
            area, t = game_utils.read_to_eol(area)
            continue

        reset = handler_olc.RESET_DATA()
        reset.command = letter
        area, number = game_utils.read_int(area)  # if_flag
        area, reset.arg1 = game_utils.read_int(area)
        area, reset.arg2 = game_utils.read_int(area)
        area, reset.arg3 = (area, 0) if letter == 'G' or letter == 'R' else game_utils.read_int(area)
        area, reset.arg4 = game_utils.read_int(area) if letter == 'P' or letter == 'M' else (area, 0)
        area, t = game_utils.read_to_eol(area)
        pArea.reset_list.append(reset)
        merc.reset_list.append(reset)
    return area


def load_rooms(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        room = handler_room.ROOM_INDEX_DATA()
        room.vnum = int(w)
        if room.vnum in merc.room_index_hash:
            logger.critical('Dupicate room Vnum: %d', room.vnum)
            sys.exit(1)

        merc.room_index_hash[room.vnum] = room
        room.area = pArea
        area, room.name = game_utils.read_string(area)
        area, room.description = game_utils.read_string(area)
        area, number = game_utils.read_int(area)  # area number
        area, room.room_flags = game_utils.read_flags(area)
        area, room.sector_type = game_utils.read_int(area)
        while True:
            area, letter = game_utils.read_letter(area)

            if letter == 'S':
                break
            elif letter == 'H':  # Healing Room
                area, room.heal_rate = game_utils.read_int(area)
            elif letter == 'M':  # Mana Room
                area, room.mana_rate = game_utils.read_int(area)
            elif letter == 'C':  # Clan
                area, room.clan = game_utils.read_string(area)
            elif letter == 'D':  # exit
                nexit = handler_olc.EXIT_DATA()
                area, door = game_utils.read_int(area)
                area, nexit.description = game_utils.read_string(area)
                area, nexit.keyword = game_utils.read_string(area)
                area, locks = game_utils.read_int(area)
                area, nexit.key = game_utils.read_int(area)
                area, nexit.to_room = game_utils.read_int(area)
                room.exit[door] = nexit
            elif letter == 'E':
                ed = handler_olc.EXTRA_DESCR_DATA()
                area, ed.keyword = game_utils.read_string(area)
                area, ed.description = game_utils.read_string(area)
                room.extra_descr.append(ed)
            elif letter == 'O':
                area, room.owner = game_utils.read_string(area)
            else:
                logger.critical("RoomIndexData(%d) has flag other than SHMCDEO: %s", (room.vnum, letter))
                sys.exit(1)
        area, w = game_utils.read_word(area, False)
        w = w[1:]  # strip the pound
    return area


def load_shops(area):
    while True:
        area, keeper = game_utils.read_int(area)

        if keeper == 0:
            break
        shop = handler_olc.SHOP_DATA()
        shop.keeper = keeper
        for r in range(merc.MAX_TRADE):
            area, shop.buy_type[r] = game_utils.read_int(area)
        area, shop.profit_buy = game_utils.read_int(area)
        area, shop.profit_sell = game_utils.read_int(area)
        area, shop.open_hour = game_utils.read_int(area)
        area, shop.close_hour = game_utils.read_int(area)
        area, t = game_utils.read_to_eol(area)
        merc.mob_index_hash[keeper].pShop = shop
        merc.shop_list.append(shop)
    return area


def load_socials(area):
    while True:
        area, word = game_utils.read_word(area, False)

        if word == '#0':
            return
        social = handler_game.SOCIAL_DATA()
        social.name = word
        area, throwaway = game_utils.read_to_eol(area)
        area, line = game_utils.read_to_eol(area)
        if line == '$':
            social.char_no_arg = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_no_arg = line

        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_no_arg = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_no_arg = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.vict_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.vict_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_not_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_not_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_auto = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_auto = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_auto = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_auto = line

        if social not in merc.social_list:
            merc.social_list.append(social)
    return area


def load_specials(area):
    while True:
        area, letter = game_utils.read_letter(area)

        if letter == '*':
            area, t = game_utils.read_to_eol(area)
            continue
        elif letter == 'S':
            return area
        elif letter == 'M':
            area, vnum = game_utils.read_int(area)
            area, merc.mob_index_hash[vnum].spec_fun = game_utils.read_word(area, False)
        else:
            logger.error("Load_specials: letter noth *SM: %s", letter)

    return area


def fix_exits():
    for k, r in merc.room_index_hash.items():
        for e in r.exit[:]:
            if e and type(e.to_room) == int:
                if e.to_room not in merc.room_index_hash:
                    logger.error("Fix_exits: Failed to find to_room for %d: %d", r.vnum, e.to_room)
                    e.to_room = None
                    r.exit.remove(e)
                else:
                    e.to_room = merc.room_index_hash[e.to_room]


# * Repopulate areas periodically.
def area_update():
    for pArea in merc.area_list:
        pArea.age += 1
        if pArea.age < 3:
            continue
        #
        # * Check age and reset.
        #* Note: Mud School resets every 3 minutes (not 15).
        #*/
        if (not pArea.empty and (pArea.nplayer == 0 or pArea.age >= 15)) or pArea.age >= 31:
            reset_area(pArea)
            handler_game.wiznet("%s has just been reset." % pArea.name, None, None, merc.WIZ_RESETS, 0, 0)

        pArea.age = random.randint(0, 3)
        pRoomIndex = merc.room_index_hash[merc.ROOM_VNUM_SCHOOL]
        if pRoomIndex and pArea == pRoomIndex.area:
            pArea.age = 15 - 2
        elif pArea.nplayer == 0:
            pArea.empty = True


#
# * Reset one area.
def reset_area(pArea):
    mob = None
    last = True
    level = 0
    for pReset in pArea.reset_list:
        if pReset.command == 'M':
            if pReset.arg1 not in merc.mob_index_hash:
                logger.error("Reset_area: 'M': bad vnum %d.", pReset.arg1)
                continue
            pMobIndex = merc.mob_index_hash[pReset.arg1]

            if pReset.arg3 not in merc.room_index_hash:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            pRoomIndex = merc.room_index_hash[pReset.arg3]

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

            mob = create_mobile(pMobIndex)

            #
            # * Check for pet shop.
            # */

            if pRoomIndex.vnum - 1 in merc.room_index_hash:
                pRoomIndexPrev = merc.room_index_hash[pRoomIndex.vnum - 1]
                if state_checks.IS_SET(pRoomIndexPrev.room_flags, merc.ROOM_PET_SHOP):
                    mob.act = state_checks.SET_BIT(mob.act, merc.ACT_PET)

            # set area */
            mob.zone = pRoomIndex.area

            mob.to_room(pRoomIndex)
            level = max(0, min(mob.level - 2, merc.LEVEL_HERO - 1))
            last = True

        elif pReset.command == 'O':
            if pReset.arg1 not in merc.obj_index_hash:
                logger.error("Reset_area: 'O': bad vnum %d.", pReset.arg1)
                continue
            pObjIndex = merc.obj_index_hash[pReset.arg1]

            if pReset.arg3 not in merc.room_index_hash:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            pRoomIndex = merc.room_index_hash[pReset.arg3]

            if pArea.nplayer > 0 or handler_obj.count_obj_list(pObjIndex, pRoomIndex.contents) > 0:
                last = False
                continue

            obj = create_object(pObjIndex, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1))
            obj.cost = 0
            obj.to_room(pRoomIndex)
            last = True
            continue

        elif pReset.command == 'P':
            if pReset.arg1 not in merc.obj_index_hash:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg1)
                continue
            pObjIndex = merc.obj_index_hash[pReset.arg1]

            if pReset.arg3 not in merc.obj_index_hash:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg3)
                continue
            pObjToIndex = merc.obj_index_hash[pReset.arg3]
            if pReset.arg2 > 50:  # old format */
                limit = 6
            elif pReset.arg2 == -1:  # no limit */
                limit = 999
            else:
                limit = pReset.arg2

            obj_to = handler_obj.get_obj_type(pObjToIndex)

            if pArea.nplayer > 0 \
                    or not obj_to \
                    or (obj_to.in_room is None and not last) \
                    or ( pObjIndex.count >= limit and random.randint(0, 4) != 0) \
                    or handler_obj.count_obj_list(pObjIndex, obj_to.contains) > pReset.arg4:
                last = False
                break
            count = handler_obj.count_obj_list(pObjIndex, obj_to.contains)
            while count < pReset.arg4:
                obj = create_object(pObjIndex, game_utils.number_fuzzy(obj_to.level))
                obj.to_obj(obj_to)
                count += 1
                if pObjIndex.count >= limit:
                    break

            # fix object lock state! */
            obj_to.value[1] = obj_to.pIndexData.value[1]
            last = True
        elif pReset.command == 'G' or pReset.command == 'E':
            if pReset.arg1 not in merc.obj_index_hash:
                logger.error("Reset_area: 'E' or 'G': bad vnum %d.", pReset.arg1)
                continue
            pObjIndex = merc.obj_index_hash[pReset.arg1]
            if not last:
                continue

            if not mob:
                logger.error("Reset_area: 'E' or 'G': None mob for vnum %d.", pReset.arg1)
                last = False
                continue
            olevel = 0
            if mob.pIndexData.pShop:
                if not pObjIndex.new_format:
                    if pObjIndex.item_type == merc.ITEM_PILL \
                            or pObjIndex.item_type == merc.ITEM_POTION \
                            or pObjIndex.item_type == merc.ITEM_SCROLL:
                        olevel = 53
                        for i in pObjIndex.value:
                            if i > 0:
                                for j in const.skill_table[pObjIndex.value[i]].skill_level:
                                    olevel = min(olevel, j)

                        olevel = max(0, (olevel * 3 // 4) - 2)

                    elif pObjIndex.item_type == merc.ITEM_WAND:
                        olevel = random.randint(10, 20)
                    elif pObjIndex.item_type == merc.ITEM_STAFF:
                        olevel = random.randint(15, 25)
                    elif pObjIndex.item_type == merc.ITEM_ARMOR:
                        olevel = random.randint(5, 15)
                    elif pObjIndex.item_type == merc.ITEM_WEAPON:
                        olevel = random.randint(5, 15)
                    elif pObjIndex.item_type == merc.ITEM_TREASURE:
                        olevel = random.randint(10, 20)

                obj = create_object(pObjIndex, olevel)
                obj.extra_flags = state_checks.SET_BIT(obj.extra_flags, merc.ITEM_INVENTORY)
            else:
                if pReset.arg2 > 50:  # old format */
                    limit = 6
                elif pReset.arg2 == -1:  # no limit */
                    limit = 999
                else:
                    limit = pReset.arg2

                if pObjIndex.count < limit or random.randint(0, 4) == 0:
                    obj = create_object(pObjIndex, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1))
                # error message if it is too high */
                if obj.level > mob.level + 3 \
                        or (obj.item_type == merc.ITEM_WEAPON
                            and pReset.command == 'E'
                            and obj.level < mob.level - 5
                            and obj.level < 45):
                    logger.error("Err: obj %s (%d) -- %d, mob %s (%d) -- %d",
                        obj.short_descr, obj.pIndexData.vnum, obj.level,
                        mob.short_descr, mob.pIndexData.vnum, mob.level)
                else:
                    continue
            obj.to_char(mob)
            if pReset.command == 'E':
                mob.equip(obj, pReset.arg3)
                last = True
                continue

        elif pReset.command == 'D':
            if pReset.arg1 not in merc.room_index_hash:
                logger.error("Reset_area: 'D': bad vnum %d.", pReset.arg1)
                continue
            pRoomIndex = merc.room_index_hash[pReset.arg1]
            pexit = pRoomIndex.exit[pReset.arg2]
            if not pexit:
                continue

            if pReset.arg3 == 0:
                pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_CLOSED)
                pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
                continue
            elif pReset.arg3 == 1:
                pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_CLOSED)
                pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
                continue
            elif pReset.arg3 == 2:
                pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_CLOSED)
                pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_LOCKED)
                continue
            last = True
            continue

        elif pReset.command == 'R':
            if pReset.arg1 not in merc.room_index_hash:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg1)
                continue
            pRoomIndex = merc.room_index_hash[pReset.arg1]
            for d0 in range(pReset.arg2 - 1):
                d1 = random.randint(d0, pReset.arg2 - 1)
                pexit = pRoomIndex.exit[d0]
                pRoomIndex.exit[d0] = pRoomIndex.exit[d1]
                pRoomIndex.exit[d1] = pexit
                break
        else:
            logger.error("Reset_area: bad command %c.", pReset.command)


#
# * Create an instance of a mobile.

def create_mobile(pMobIndex):
    if pMobIndex is None:
        logger.critical("Create_mobile: None pMobIndex.")
        sys.exit(1)

    mob = handler_ch.CHAR_DATA()

    mob.pIndexData = pMobIndex

    mob.name = pMobIndex.player_name
    mob.id = game_utils.get_mob_id()
    mob.short_descr = pMobIndex.short_descr
    mob.long_descr = pMobIndex.long_descr
    mob.description = pMobIndex.description
    if pMobIndex.spec_fun:
        mob.spec_fun = special.spec_table[pMobIndex.spec_fun]
    mob.prompt = None

    if pMobIndex.wealth == 0:
        mob.silver = 0
        mob.gold = 0
    else:
        wealth = random.randint(pMobIndex.wealth // 2, 3 * pMobIndex.wealth // 2)
        mob.gold = random.randint(wealth // 200, wealth // 100)
        mob.silver = wealth - (mob.gold * 100)

    if pMobIndex.new_format:
        # load in new style */
        # read from prototype */
        mob.group = pMobIndex.group
        mob.act = pMobIndex.act
        mob.comm = merc.COMM_NOCHANNELS | merc.COMM_NOSHOUT | merc.COMM_NOTELL
        mob.affected_by = pMobIndex.affected_by
        mob.alignment = pMobIndex.alignment
        mob.level = pMobIndex.level
        mob.hitroll = pMobIndex.hitroll
        mob.damroll = pMobIndex.damage[merc.DICE_BONUS]
        mob.max_hit = game_utils.dice(pMobIndex.hit[merc.DICE_NUMBER], pMobIndex.hit[merc.DICE_TYPE]) + pMobIndex.hit[
            merc.DICE_BONUS]
        mob.hit = mob.max_hit
        mob.max_mana = game_utils.dice(pMobIndex.mana[merc.DICE_NUMBER], pMobIndex.mana[merc.DICE_TYPE]) + pMobIndex.mana[
            merc.DICE_BONUS]
        mob.mana = mob.max_mana
        mob.damage[merc.DICE_NUMBER] = pMobIndex.damage[merc.DICE_NUMBER]
        mob.damage[merc.DICE_TYPE] = pMobIndex.damage[merc.DICE_TYPE]
        mob.dam_type = pMobIndex.dam_type
        if mob.dam_type == 0:
            num = random.randint(1, 3)
            if num == 1:
                mob.dam_type = 3  # slash */
            elif num == 2:
                mob.dam_type = 7  # pound */
            elif num == 3:
                mob.dam_type = 11  # pierce */
        for i in range(4):
            mob.armor[i] = pMobIndex.ac[i]
        mob.off_flags = pMobIndex.off_flags
        mob.imm_flags = pMobIndex.imm_flags
        mob.res_flags = pMobIndex.res_flags
        mob.vuln_flags = pMobIndex.vuln_flags
        mob.start_pos = pMobIndex.start_pos
        mob.default_pos = pMobIndex.default_pos
        mob.sex = pMobIndex.sex
        if type(pMobIndex.sex) != int or mob.sex == 3:  # random sex */
            mob.sex = random.randint(1, 2)
        mob.race = pMobIndex.race
        mob.form = pMobIndex.form
        mob.parts = pMobIndex.parts
        mob.size = int(pMobIndex.size)
        mob.material = pMobIndex.material

        # computed on the spot */
        for i in range(merc.MAX_STATS):
            mob.perm_stat[i] = min(25, 11 + mob.level // 4)

        if state_checks.IS_SET(mob.act, merc.ACT_WARRIOR):
            mob.perm_stat[merc.STAT_STR] += 3
            mob.perm_stat[merc.STAT_INT] -= 1
            mob.perm_stat[merc.STAT_CON] += 2

        if state_checks.IS_SET(mob.act, merc.ACT_THIEF):
            mob.perm_stat[merc.STAT_DEX] += 3
            mob.perm_stat[merc.STAT_INT] += 1
            mob.perm_stat[merc.STAT_WIS] -= 1

        if state_checks.IS_SET(mob.act, merc.ACT_CLERIC):
            mob.perm_stat[merc.STAT_WIS] += 3
            mob.perm_stat[merc.STAT_DEX] -= 1
            mob.perm_stat[merc.STAT_STR] += 1

        if state_checks.IS_SET(mob.act, merc.ACT_MAGE):
            mob.perm_stat[merc.STAT_INT] += 3
            mob.perm_stat[merc.STAT_STR] -= 1
            mob.perm_stat[merc.STAT_DEX] += 1

        if state_checks.IS_SET(mob.off_flags, merc.OFF_FAST):
            mob.perm_stat[merc.STAT_DEX] += 2

        mob.perm_stat[merc.STAT_STR] += mob.size - merc.SIZE_MEDIUM
        mob.perm_stat[merc.STAT_CON] += (mob.size - merc.SIZE_MEDIUM) // 2
        af = handler_game.AFFECT_DATA()
        # let's get some spell action */
        if state_checks.IS_AFFECTED(mob, merc.AFF_SANCTUARY):
            af.where = merc.TO_AFFECTS
            af.type = "sanctuary"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_NONE
            af.modifier = 0
            af.bitvector = merc.AFF_SANCTUARY
            mob.affect_add(af)

        if state_checks.IS_AFFECTED(mob, merc.AFF_HASTE):
            af.where = merc.TO_AFFECTS
            af.type = "haste"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_DEX
            af.modifier = 1 + (mob.level >= 18) + (mob.level >= 25) + (mob.level >= 32)
            af.bitvector = merc.AFF_HASTE
            mob.affect_add(af)

        if state_checks.IS_AFFECTED(mob, merc.AFF_PROTECT_EVIL):
            af.where = merc.TO_AFFECTS
            af.type = "protection evil"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_EVIL
            mob.affect_add(af)

        if state_checks.IS_AFFECTED(mob, merc.AFF_PROTECT_GOOD):
            af.where = merc.TO_AFFECTS
            af.type = "protection good"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_GOOD
            mob.affect_add(af)
    else:  # read in old format and convert */
        mob.act = pMobIndex.act
        mob.affected_by = pMobIndex.affected_by
        mob.alignment = pMobIndex.alignment
        mob.level = pMobIndex.level
        mob.hitroll = pMobIndex.hitroll
        mob.damroll = 0
        mob.max_hit = mob.level * 8 + random.randint(mob.level * mob.level // 4, mob.level * mob.level)
        mob.max_hit *= .9
        mob.hit = mob.max_hit
        mob.max_mana = 100 + game_utils.dice(mob.level, 10)
        mob.mana = mob.max_mana
        num = random.randint(1, 3)
        if num == 1:
            mob.dam_type = 3  # slash */
        elif num == 2:
            mob.dam_type = 7  # pound */
        elif num == 3:
            mob.dam_type = 11  # pierce */
        for i in range(3):
            mob.armor[i] = game_utils.interpolate(mob.level, 100, -100)
        mob.armor[3] = game_utils.interpolate(mob.level, 100, 0)
        mob.race = pMobIndex.race
        mob.off_flags = pMobIndex.off_flags
        mob.imm_flags = pMobIndex.imm_flags
        mob.res_flags = pMobIndex.res_flags
        mob.vuln_flags = pMobIndex.vuln_flags
        mob.start_pos = pMobIndex.start_pos
        mob.default_pos = pMobIndex.default_pos
        mob.sex = pMobIndex.sex
        mob.form = pMobIndex.form
        mob.parts = pMobIndex.parts
        mob.size = merc.SIZE_MEDIUM
        mob.material = ""

        for i in merc.MAX_STATS:
            mob.perm_stat[i] = 11 + mob.level // 4
    mob.position = mob.start_pos

    # link the mob to the world list */
    merc.char_list.append(mob)
    return mob


# duplicate a mobile exactly -- except inventory */
def clone_mobile(parent, clone):
    if not parent or not clone or not state_checks.IS_NPC(parent):
        return

    # start fixing values */
    clone.name = parent.name
    clone.version = parent.version
    clone.short_descr = parent.short_descr
    clone.long_descr = parent.long_descr
    clone.description = parent.description
    clone.group = parent.group
    clone.sex = parent.sex
    clone.guild = parent.guild
    clone.race = parent.race
    clone.level = parent.level
    clone.trust = 0
    clone.timer = parent.timer
    clone.wait = parent.wait
    clone.hit = parent.hit
    clone.max_hit = parent.max_hit
    clone.mana = parent.mana
    clone.max_mana = parent.max_mana
    clone.move = parent.move
    clone.max_move = parent.max_move
    clone.gold = parent.gold
    clone.silver = parent.silver
    clone.exp = parent.exp
    clone.act = parent.act
    clone.comm = parent.comm
    clone.imm_flags = parent.imm_flags
    clone.res_flags = parent.res_flags
    clone.vuln_flags = parent.vuln_flags
    clone.invis_level = parent.invis_level
    clone.affected_by = parent.affected_by
    clone.position = parent.position
    clone.practice = parent.practice
    clone.train = parent.train
    clone.saving_throw = parent.saving_throw
    clone.alignment = parent.alignment
    clone.hitroll = parent.hitroll
    clone.damroll = parent.damroll
    clone.wimpy = parent.wimpy
    clone.form = parent.form
    clone.parts = parent.parts
    clone.size = parent.size
    clone.material = parent.material
    clone.off_flags = parent.off_flags
    clone.dam_type = parent.dam_type
    clone.start_pos = parent.start_pos
    clone.default_pos = parent.default_pos
    clone.spec_fun = parent.spec_fun

    for i in range(4):
        clone.armor[i] = parent.armor[i]

    for i in range(merc.MAX_STATS):
        clone.perm_stat[i] = parent.perm_stat[i]
        clone.mod_stat[i] = parent.mod_stat[i]

    for i in range(3):
        clone.damage[i] = parent.damage[i]

    # now add the affects */
    for paf in parent.affected:
        clone.affect_add(paf)


# * Create an instance of an object.
def create_object(pObjIndex, level):
    if not pObjIndex:
        logger.critical("Create_object: None pObjIndex.")
        sys.exit(1)

    obj = handler_obj.OBJ_DATA()

    obj.pIndexData = pObjIndex
    obj.in_room = None
    obj.enchanted = False

    if pObjIndex.new_format is True:
        obj.level = pObjIndex.level
    else:
        obj.level = max(0, level)
    obj.wear_loc = -1

    obj.name = pObjIndex.name
    obj.short_descr = pObjIndex.short_descr
    obj.description = pObjIndex.description
    obj.material = pObjIndex.material
    obj.item_type = pObjIndex.item_type
    obj.extra_flags = pObjIndex.extra_flags
    obj.wear_flags = pObjIndex.wear_flags
    obj.value = pObjIndex.value[:]
    obj.weight = pObjIndex.weight

    if level == -1 or pObjIndex.new_format:
        obj.cost = pObjIndex.cost
    else:
        obj.cost = game_utils.number_fuzzy(10) * game_utils.number_fuzzy(level) * game_utils.number_fuzzy(level)

        # Mess with object properties.
    if obj.item_type == merc.ITEM_LIGHT:
        if obj.value[2] == 999:
            obj.value[2] = -1
    elif obj.item_type == merc.ITEM_FURNITURE \
            or obj.item_type == merc.ITEM_TRASH \
            or obj.item_type == merc.ITEM_CONTAINER \
            or obj.item_type == merc.ITEM_DRINK_CON \
            or obj.item_type == merc.ITEM_KEY \
            or obj.item_type == merc.ITEM_FOOD \
            or obj.item_type == merc.ITEM_BOAT \
            or obj.item_type == merc.ITEM_CORPSE_NPC \
            or obj.item_type == merc.ITEM_CORPSE_PC \
            or obj.item_type == merc.ITEM_FOUNTAIN \
            or obj.item_type == merc.ITEM_MAP \
            or obj.item_type == merc.ITEM_CLOTHING \
            or obj.item_type == merc.ITEM_PORTAL:
        if not pObjIndex.new_format:
            obj.cost //= 5
    elif obj.item_type == merc.ITEM_TREASURE \
            or obj.item_type == merc.ITEM_WARP_STONE \
            or obj.item_type == merc.ITEM_ROOM_KEY \
            or obj.item_type == merc.ITEM_GEM \
            or obj.item_type == merc.ITEM_JEWELRY:
        pass
    elif obj.item_type == merc.ITEM_JUKEBOX:
        obj.value = [-1 for i in range(5)]
    elif obj.item_type == merc.ITEM_SCROLL:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0] = game_utils.number_fuzzy(obj.value[0])
    elif obj.item_type == merc.ITEM_WAND \
            or obj.item_type == merc.ITEM_STAFF:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0] = game_utils.number_fuzzy(obj.value[0])
            obj.value[1] = game_utils.number_fuzzy(obj.value[1])
            obj.value[2] = obj.value[1]
        if not pObjIndex.new_format:
            obj.cost *= 2
    elif obj.item_type == merc.ITEM_WEAPON:
        if level != -1 and not pObjIndex.new_format:
            obj.value[1] = game_utils.number_fuzzy(game_utils.number_fuzzy(1 * level // 4 + 2))
            obj.value[2] = game_utils.number_fuzzy(game_utils.number_fuzzy(3 * level // 4 + 6))
    elif obj.item_type == merc.ITEM_ARMOR:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0] = game_utils.number_fuzzy(level // 5 + 3)
            obj.value[1] = game_utils.number_fuzzy(level // 5 + 3)
            obj.value[2] = game_utils.number_fuzzy(level // 5 + 3)
    elif obj.item_type == merc.ITEM_POTION \
            or obj.item_type == merc.ITEM_PILL:
        if level != -1 and not pObjIndex.new_format:
            obj.value[0] = game_utils.number_fuzzy(game_utils.number_fuzzy(obj.value[0]))
    elif obj.item_type == merc.ITEM_MONEY:
        if not pObjIndex.new_format:
            obj.value[0] = obj.cost
    else:
        logger.error("Bad item_type pObjIndex vnum: %s(%s)" % (pObjIndex.vnum, obj.item_type ))

    for paf in pObjIndex.affected:
        if paf.location == merc.APPLY_SPELL_AFFECT:
            obj.affect_add(paf)
    obj.extra_descr = pObjIndex.extra_descr
    merc.object_list.append(obj)
    return obj


# duplicate an object exactly -- except contents */
def clone_object(parent, clone):
    if not parent or not clone:
        return

    # start fixing the object */
    clone.name = parent.name
    clone.short_descr = parent.short_descr
    clone.description = parent.description
    clone.item_type = parent.item_type
    clone.extra_flags = parent.extra_flags
    clone.wear_flags = parent.wear_flags
    clone.weight = parent.weight
    clone.cost = parent.cost
    clone.level = parent.level
    clone.condition = parent.condition
    clone.material = parent.material
    clone.timer = parent.timer

    for i in parent.value:
        clone.value[i] = i

    # affects */
    clone.enchanted = parent.enchanted

    for paf in parent.affected:
        clone.affect_add(paf)

    # extended desc */
    for ed in parent.extra_descr:
        ed_new = handler_olc.EXTRA_DESCR_DATA()
        ed_new.keyword = ed.keyword
        ed_new.description = ed.description
        clone.extra_descr.append(ed)


#
# * Clear a new character.
# */
def clear_char(ch):
    ch.name = ""
    ch.short_descr = ""
    ch.long_descr = ""
    ch.description = ""
    ch.prompt = ""
    ch.logon = time.time()
    ch.lines = 22
    for i in range(4):
        ch.armor[i] = 100
    ch.position = merc.POS_STANDING
    ch.hit = 20
    ch.max_hit = 20
    ch.mana = 100
    ch.max_mana = 100
    ch.move = 100
    ch.max_move = 100
    ch.on = None
    for i in merc.MAX_STATS:
        ch.perm_stat[i] = 13
        ch.mod_stat[i] = 0
    return


# * Create a 'money' obj.
def create_money(gold, silver):
    if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
        logger.warn("BUG: Create_money: zero or negative money. %d ", min(gold, silver))
        gold = max(1, gold)
        silver = max(1, silver)

    if gold == 0 and silver == 1:
        obj = create_object(merc.obj_index_hash[merc.OBJ_VNUM_SILVER_ONE], 0)
    elif gold == 1 and silver == 0:
        obj = create_object(merc.obj_index_hash[merc.OBJ_VNUM_GOLD_ONE], 0)
    elif silver == 0:
        obj = create_object(merc.obj_index_hash[merc.OBJ_VNUM_GOLD_SOME], 0)
        obj.short_descr += " %d" % gold
        obj.value[1] = gold
        obj.cost = gold
        obj.weight = gold // 5
    elif gold == 0:
        obj = create_object(merc.obj_index_hash[merc.OBJ_VNUM_SILVER_SOME], 0)
        obj.short_descr += " %d" % silver
        obj.value[0] = silver
        obj.cost = silver
        obj.weight = silver // 20
    else:
        obj = create_object(merc.obj_index_hash[merc.OBJ_VNUM_COINS], 0)
        obj.short_descr += " %d %d" % (gold, silver)
        obj.value[0] = silver
        obj.value[1] = gold
        obj.cost = 100 * gold + silver
        obj.weight = gold // 5 + silver // 20
    return obj


def init_time():
    lhour = (time.time() - 650336715) // (merc.PULSE_TICK // merc.PULSE_PER_SECOND)
    lhour = int(lhour)
    handler_game.time_info.hour = lhour % 24
    lday = lhour // 24
    handler_game.time_info.day = int(lday % 35)
    lmonth = lday // 35
    handler_game.time_info.month = lmonth % 17
    handler_game.time_info.year = lmonth // 17

    if handler_game.time_info.hour < 5:
        handler_game.weather_info.sunlight = merc.SUN_DARK
    elif handler_game.time_info.hour < 6:
        handler_game.weather_info.sunlight = merc.SUN_RISE
    elif handler_game.time_info.hour < 19:
        handler_game.weather_info.sunlight = merc.SUN_LIGHT
    elif handler_game.time_info.hour < 20:
        handler_game.weather_info.sunlight = merc.SUN_SET
    else:
        handler_game.weather_info.sunlight = merc.SUN_DARK
    handler_game.weather_info.change = 0
    handler_game.weather_info.mmhg = 960
    if 7 <= handler_game.time_info.month <= 12:
        handler_game.weather_info.mmhg += random.randint(1, 50)
    else:
        handler_game.weather_info.mmhg += random.randint(1, 80)

    if handler_game.weather_info.mmhg <= 980:
        handler_game.weather_info.sky = merc.SKY_LIGHTNING
    elif handler_game.weather_info.mmhg <= 1000:
        handler_game.weather_info.sky = merc.SKY_RAINING
    elif handler_game.weather_info.mmhg <= 1020:
        handler_game.weather_info.sky = merc.SKY_CLOUDY
    else:
        handler_game.weather_info.sky = merc.SKY_CLOUDLESS
