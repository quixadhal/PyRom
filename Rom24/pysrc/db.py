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
import time

import merc
import data_loader
import entity_instancer
import handler_obj
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
    entity_instancer.setup_exits()
    logger.info('    Loaded %d Help files', len(merc.help_list))
    logger.info('    Loaded %d Areas', len(merc.area_templates))
    logger.info('    Loaded %d Mobile Indexes', len(merc.mob_templates))
    logger.info('    Loaded %d Object Indexes', len(merc.obj_templates))
    logger.info('    Loaded %d Room Indexes', len(merc.room_templates))
    logger.info('    Loaded %d Resets', len(merc.reset_list))
    logger.info('    Loaded %d Shops', len(merc.shop_list))
    logger.info('    Loaded %d Socials', len(merc.social_list))


def init_instance():
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
    for k, r in merc.room_templates.items():
        for e in r.template_exit[:]:
            if e and type(e.template_to_room) == int:
                if e.template_to_room not in merc.room_templates:
                    logger.error("Fix_exits: Failed to find to_room for %d: %d", r.template_vnum, e.template_to_room)
                    e.template_to_room = None
                    r.template_exit.remove(e)
                else:
                    e.template_to_room = merc.room_templates[e.template_to_room]


# * Repopulate areas periodically.
def area_update():
    for aid, area in merc.area_instances.items():
        area.age += 1
        if area.age < 3:
            continue
        #
        # * Check age and reset.
        #* Note: Mud School resets every 3 minutes (not 15).
        #*/
        if (not area.empty and (area.character == 0 or area.age >= 15)) or area.age >= 31:
            reset_area(area.name)
            handler_game.wiznet("%s has just been reset." % area.name, None, None, merc.WIZ_RESETS, 0, 0)

        area.age = random.randint(0, 3)
        pRoomIndex = merc.room_templates[merc.ROOM_VNUM_SCHOOL]
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
    pArea = merc.area_templates[area]
    for pReset in pArea.reset_list:
        if pReset.command == 'M':
            if pReset.arg1 not in merc.mob_templates:
                logger.error("Reset_area: 'M': bad vnum %d.", pReset.arg1)
                continue
            mobTemplate = merc.mob_templates[pReset.arg1]

            if pReset.arg3 not in merc.room_templates:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            pRoomInstance = game_utils.find_vnum_instance('room', 1, pReset.arg3)

            if mobTemplate.count >= pReset.arg2:
                last = False
                break
            count = 0
            for k, v in merc.room_instances.items():
                if v.vnum == pRoomInstance.vnum:
                    for mob in v.people:
                        for k1, v1 in merc.mob_instances.items():
                            if v1.mobTemplate == mobTemplate.vnum:
                                count += 1
                                if count >= pReset.arg4:
                                    last = False
                                    break

            if count >= pReset.arg4:
                continue

            mob = entity_instancer.create_mobile(mobTemplate)

            #
            # * Check for pet shop.
            # */

            if pRoomInstance.vnum - 1 in merc.room_templates:
                pRoomIndexPrev = merc.room_templates[pRoomInstance.vnum - 1]
                if state_checks.IS_SET(pRoomIndexPrev.room_flags, merc.ROOM_PET_SHOP):
                    mob.act.set_bit(merc.ACT_PET)

            # set area */
            mob.zone = pRoomInstance.area

            mob.to_room(pRoomInstance)
            level = max(0, min(mob.level - 2, merc.LEVEL_HERO - 1))
            last = True

        elif pReset.command == 'O':
            if pReset.arg1 not in merc.obj_templates:
                logger.error("Reset_area: 'O': bad vnum %d.", pReset.arg1)
                continue
            objTemplate = merc.obj_templates[pReset.arg1]

            if pReset.arg3 not in merc.room_templates:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
                continue
            pRoomInstanceID = game_utils.find_vnum_instance('room', 1, pReset.arg2)
            pRoomInstance = merc.room_instances[pRoomInstanceID]
            if pArea.nplayer > 0 or handler_obj.count_obj_list(objTemplate, pRoomInstance.contents) > 0:
                last = False
                continue

            obj = entity_instancer.create_object(objTemplate, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1))
            obj.cost = 0
            obj.to_room(pRoomInstanceID)
            last = True
            continue

        elif pReset.command == 'P':
            if pReset.arg1 not in merc.obj_templates:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg1)
                continue
            objTemplate = merc.obj_templates[pReset.arg1]

            if pReset.arg3 not in merc.obj_templates:
                logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg3)
                continue
            pObjToIndex = merc.obj_templates[pReset.arg3]
            if pReset.arg2 > 50:  # old format */
                limit = 6
            elif pReset.arg2 == -1:  # no limit */
                limit = 999
            else:
                limit = pReset.arg2

            obj_to = handler_obj.get_obj_type(pObjToIndex)

            if pArea.nplayer > 0 \
                    or not obj_to \
                    or (obj_to.in_room_instance == 0 and not last) \
                    or (objTemplate.template_count >= limit and random.randint(0, 4) != 0) \
                    or handler_obj.count_obj_list(objTemplate, obj_to.contains) > pReset.arg4:
                last = False
                break
            count = handler_obj.count_obj_list(objTemplate, obj_to.contains)
            while count < pReset.arg4:
                obj = entity_instancer.create_object(objTemplate, game_utils.number_fuzzy(obj_to.level))
                obj.to_obj(obj_to)
                count += 1
                if objTemplate.template_count >= limit:
                    break

            # fix object lock state! */
            obj_to.value[1] = merc.obj_templates[obj_to.objTemplate].value[1]
            last = True
        elif pReset.command == 'G' or pReset.command == 'E':
            if pReset.arg1 not in merc.obj_templates:
                logger.error("Reset_area: 'E' or 'G': bad vnum %d.", pReset.arg1)
                continue
            objTemplate = merc.obj_templates[pReset.arg1]
            if not last:
                continue

            if not mob:
                logger.error("Reset_area: 'E' or 'G': None mob for vnum %d.", pReset.arg1)
                last = False
                continue
            olevel = 0
            if merc.mob_templates[mob.mobTemplate].pShop:
                if not objTemplate.template_new_format:
                    if objTemplate.template_item_type == merc.ITEM_PILL \
                            or objTemplate.template_item_type == merc.ITEM_POTION \
                            or objTemplate.template_item_type == merc.ITEM_SCROLL:
                        olevel = 53
                        for i in objTemplate.template_value:
                            if i > 0:
                                for j in const.skill_table[objTemplate.template_value[i]].skill_level:
                                    olevel = min(olevel, j)

                        olevel = max(0, (olevel * 3 // 4) - 2)

                    elif objTemplate.template_item_type == merc.ITEM_WAND:
                        olevel = random.randint(10, 20)
                    elif objTemplate.template_item_type == merc.ITEM_STAFF:
                        olevel = random.randint(15, 25)
                    elif objTemplate.template_item_type == merc.ITEM_ARMOR:
                        olevel = random.randint(5, 15)
                    elif objTemplate.template_item_type == merc.ITEM_WEAPON:
                        olevel = random.randint(5, 15)
                    elif objTemplate.template_item_type == merc.ITEM_TREASURE:
                        olevel = random.randint(10, 20)

                obj = entity_instancer.create_object(objTemplate, olevel)
                obj.extra_flags = state_checks.SET_BIT(obj.extra_flags, merc.ITEM_INVENTORY)
            else:
                if pReset.arg2 > 50:  # old format */
                    limit = 6
                elif pReset.arg2 == -1:  # no limit */
                    limit = 999
                else:
                    limit = pReset.arg2

                if objTemplate.template_count < limit or random.randint(0, 4) == 0:
                    obj = entity_instancer.create_object(objTemplate,
                                                                min(game_utils.number_fuzzy(level),
                                                                    merc.LEVEL_HERO - 1))
                # error message if it is too high */
                if obj.level > mob.level + 3 \
                        or (obj.item_type == merc.ITEM_WEAPON
                            and pReset.command == 'E'
                            and obj.level < mob.level - 5
                            and obj.level < 45):
                    logger.error("Err: obj %s (%d) -- %d, mob %s (%d) -- %d",
                                 obj.short_descr, obj.instance_id, obj.level,
                                 mob.short_descr, mob.instance_id, mob.level)
                else:
                    continue
            obj.to_char(mob)
            if pReset.command == 'E':
                mob.equip(obj, pReset.arg3)
                last = True
                continue

        elif pReset.command == 'D':
            if pReset.arg1 not in merc.room_templates:
                logger.error("Reset_area: 'D': bad vnum %d.", pReset.arg1)
                continue
            pRoomInstance = merc.room_templates[pReset.arg1]
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
            if pReset.arg1 not in merc.room_templates:
                logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg1)
                continue
            pRoomInstance = merc.room_templates[pReset.arg1]
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
