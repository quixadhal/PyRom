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
import pc
import update

logger = logging.getLogger()

import os
import random
import time

import merc
import data_loader
import object_creator
import handler_item
import settings
import state_checks
import game_utils
import handler_game
import const
import database.read.read_tables as read


def boot_db():
    init_time()
    init_instance()
    read.read_tables()
    data_loader.load_areas()
    #fix_exits()
    area_update()
    object_creator.setup_exits()
    update.instance_number_save()
    logger.info('    Loaded %d Help files', len(merc.help_list))
    logger.info('    Loaded %d Areas', len(merc.areaTemplate))
    logger.info('    Loaded %d Npc Templates', len(merc.characterTemplate))
    logger.info('    Loaded %d Item Templates', len(merc.itemTemplate))
    logger.info('    Loaded %d Room Templates', len(merc.roomTemplate))
    logger.info('    Loaded %d Resets', len(merc.reset_list))
    logger.info('    Loaded %d Shops', len(merc.shop_list))
    logger.info('    Loaded %d Socials', len(merc.social_list))


def init_instance():
    #First lets add the bad terms we dont want to pass during instancing, while copying attributes
    merc.not_to_instance.append('instance_id')
    merc.not_to_instance.append('act')
    instance_num_file = os.path.join(settings.AREA_DIR, "instance_tracker.txt")
    fp = open(instance_num_file, 'a')  # in case the file doesnt exist open in append mode to not wipe
    fp.close()
    fp = open(instance_num_file, 'r')
    junk, merc.instance_number = game_utils.read_int(fp.read())
    fp.close()
    if merc.instance_number == 0 or not merc.instance_number:
        logger.info("First run, or problem with instance, setting 0")
        merc.instance_number = 0
    else:
        logger.info("Global Instance Tracker, instances thus far: %d", merc.instance_number)


def fix_exits():
    for k, r in merc.roomTemplate.items():
        for e in r.template_exit[:]:
            if e and type(e.template_to_room) == int:
                if e.template_to_room not in merc.roomTemplate:
                    logger.error("Fix_exits: Failed to find to_room for %d: %d", r.template_vnum, e.template_to_room)
                    e.template_to_room = None
                    r.template_exit.remove(e)
                else:
                    e.template_to_room = merc.roomTemplate[e.template_to_room]


# * Repopulate areas periodically.
def area_update():
    for aid, area in merc.areas.items():
        area.age += 1
        if area.age < 3:
            continue
        #
        # * Check age and reset.
        #* Note: Mud School resets every 3 minutes (not 15).
        #*/
        if (not area.empty and (area.character == 0 or area.age >= 15)) or area.age >= 31:
            reset_area(area.instance_id)
            handler_game.wiznet("%s has just been reset." % area.name, None, None, merc.WIZ_RESETS, 0, 0)

        area.age = random.randint(0, 3)
        pRoomIndex = merc.roomTemplate[merc.ROOM_VNUM_SCHOOL]
        #TODO change this later when area instances are properly tracked
        if pRoomIndex and area.name == pRoomIndex.area:
            area.age = 15 - 2
        elif area.nplayer == 0:
            area.empty = True


#
# * Reset one area.
def reset_area(area):
    mob = None
    last = True
    level = 0
    #TODO fix this into instances
    areaInstance = merc.areas[area]
    for pReset in areaInstance.reset_list:
        if pReset.command == 'M':
            if pReset.arg1 not in merc.characterTemplate:
                logger.error("Reset_area: 'M': bad vnum %d.", pReset.arg1)
                continue
            mobTemplate = merc.characterTemplate[pReset.arg1]

            if pReset.arg3 not in merc.roomTemplate:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            roomInstanceID = merc.instances_by_room[pReset.arg3][0]
            roomInstance = merc.rooms[roomInstanceID]

            if mobTemplate.count >= pReset.arg2:
                last = False
                break
            count = 0
            for instanceID in roomInstance.people:
                if instanceID:
                    mob = merc.characters[instanceID]
                    if isinstance(mob, pc.Pc):
                        break
                    if mob.vnum == mobTemplate.vnum:
                        count += 1
                        if count >= pReset.arg4:
                            last = False
                            break

            if count >= pReset.arg4:
                continue

            mob = object_creator.create_mobile(mobTemplate)

            #
            # * Check for pet shop.
            # */
            prevTemplate = roomInstance.vnum - 1
            if prevTemplate in merc.roomTemplate:
                prevRoomID = merc.instances_by_room[prevTemplate][0]
                prevInstance = merc.rooms[prevRoomID]
                if state_checks.IS_SET(prevInstance.room_flags, merc.ROOM_PET_SHOP):
                    mob.act.set_bit(merc.ACT_PET)

            # set area */
            mob.zone = roomInstance.area

            mob.to_room(roomInstance.instance_id)
            level = max(0, min(mob.level - 2, merc.LEVEL_HERO - 1))
            last = True

        elif pReset.command == 'O':
            if pReset.arg1 not in merc.itemTemplate:
                logger.error("Reset_area: 'O': bad vnum %d.", pReset.arg1)
                continue
            item_template = merc.itemTemplate[pReset.arg1]

            if pReset.arg3 not in merc.roomTemplate:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            pRoomInstanceID = merc.instances_by_room[pReset.arg3][0]
            pRoomInstance = merc.rooms[pRoomInstanceID]
            if areaInstance.nplayer > 0 or handler_item.count_obj_list(pRoomInstance, pRoomInstance.contents) > 0:
                last = False
                continue

            item = object_creator.create_item(item_template, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1))
            item.cost = 0
            item.to_room(pRoomInstanceID)
            last = True
            continue

        elif pReset.command == 'P':
            if pReset.arg1 not in merc.itemTemplate:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg1)
                continue
            item_template = merc.itemTemplate[pReset.arg1]

            if pReset.arg3 not in merc.itemTemplate:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg3)
                continue
            item_to_item_template = merc.itemTemplate[pReset.arg3]
            if pReset.arg2 > 50:  # old format */
                limit = 6
            elif pReset.arg2 == -1:  # no limit */
                limit = 999
            else:
                limit = pReset.arg2
            item_to_instance_id = merc.instances_by_item[item_to_item_template.vnum][0]
            item_to = merc.items[item_to_instance_id]

            if areaInstance.nplayer > 0 \
                    or not item_to \
                    or (item_to.in_room is None and not last) \
                    or (item_template.count >= limit and random.randint(0, 4) != 0) \
                    or handler_item.count_obj_list(item_to, item_to.contents) > pReset.arg4:
                last = False
                break
            count = handler_item.count_obj_list(item_template, item_to.contents)
            while count < pReset.arg4:
                item = object_creator.create_item(item_template, game_utils.number_fuzzy(item_to.level))
                item.to_item(item_to)
                count += 1
                if item_template.count >= limit:
                    break

            # fix object lock state! */
            item_to.value[1] = merc.itemTemplate[item_to.vnum].value[1]
            last = True
        elif pReset.command == 'G' or pReset.command == 'E':
            if pReset.arg1 not in merc.itemTemplate:
                logger.error("Reset_area: 'E' or 'G': bad vnum %d.", pReset.arg1)
                continue
            item_template = merc.itemTemplate[pReset.arg1]
            if not last:
                continue

            if not mob:
                logger.error("Reset_area: 'E' or 'G': None mob for vnum %d.", pReset.arg1)
                last = False
                continue
            olevel = 0
            if merc.characterTemplate[mob.vnum].pShop:
                if not item_template.new_format:
                    if item_template.item_type == merc.ITEM_PILL \
                            or item_template.item_type == merc.ITEM_POTION \
                            or item_template.item_type == merc.ITEM_SCROLL:
                        olevel = 53
                        for i in item_template.value:
                            if i > 0:
                                for j in const.skill_table[item_template.value[i]].skill_level:
                                    olevel = min(olevel, j)

                        olevel = max(0, (olevel * 3 // 4) - 2)

                    elif item_template.item_type == merc.ITEM_WAND:
                        olevel = random.randint(10, 20)
                    elif item_template.item_type == merc.ITEM_STAFF:
                        olevel = random.randint(15, 25)
                    elif item_template.item_type == merc.ITEM_ARMOR:
                        olevel = random.randint(5, 15)
                    elif item_template.item_type == merc.ITEM_WEAPON:
                        olevel = random.randint(5, 15)
                    elif item_template.item_type == merc.ITEM_TREASURE:
                        olevel = random.randint(10, 20)

                item = object_creator.create_item(item_template, olevel)
                item.extra_flags = state_checks.SET_BIT(item.extra_flags, merc.ITEM_INVENTORY)
            else:
                if pReset.arg2 > 50:  # old format */
                    limit = 6
                elif pReset.arg2 == -1:  # no limit */
                    limit = 999
                else:
                    limit = pReset.arg2

                if item_template.count < limit or random.randint(0, 4) == 0:
                    item = object_creator.create_item(item_template,
                                                                min(game_utils.number_fuzzy(level),
                                                                    merc.LEVEL_HERO - 1))
                # error message if it is too high */
                if item.level > mob.level + 3 \
                        or (item.item_type == merc.ITEM_WEAPON
                            and pReset.command == 'E'
                            and item.level < mob.level - 5
                            and item.level < 45):
                    logger.error("Err: obj %s (%d) -- %d, mob %s (%d) -- %d",
                                 item.short_descr, item.instance_id, item.level,
                                 mob.short_descr, mob.instance_id, mob.level)
                else:
                    continue
            item.to_char(mob)
            if pReset.command == 'E':
                mob.equip(item.instance_id, pReset.arg3)
                last = True
                continue

        elif pReset.command == 'D':
            if pReset.arg1 not in merc.roomTemplate:
                logger.error("Reset_area: 'D': bad vnum %d.", pReset.arg1)
                continue
            pRoomInstance = merc.roomTemplate[pReset.arg1]
            pexit = pRoomInstance.exit[pReset.arg2]
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
            if pReset.arg1 not in merc.roomTemplate:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg1)
                continue
            pRoomInstance = merc.roomTemplate[pReset.arg1]
            for d0 in range(pReset.arg2 - 1):
                d1 = random.randint(d0, pReset.arg2 - 1)
                pexit = pRoomInstance.exit[d0]
                pRoomInstance.exit[d0] = pRoomInstance.exit[d1]
                pRoomInstance.exit[d1] = pexit
                break
        else:
            logger.error("Reset_area: bad command %c.", pReset.command)


#
# * Create an instance of a mobile.



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
    ch.on_instance = 0
    ch.in_room_instance = 0
    for i in merc.MAX_STATS:
        ch.perm_stat[i] = 13
        ch.mod_stat[i] = 0
    return


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
