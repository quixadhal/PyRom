import os
import random
import time
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import update
from rom24 import data_loader
from rom24 import object_creator
from rom24 import handler_item
from rom24 import settings
from rom24 import state_checks
from rom24 import game_utils
from rom24 import handler_game
from rom24 import const
from rom24.database.read import read_tables as read
from rom24 import instance


def boot_db():
    from rom24 import handler_npc
    from rom24 import handler_room
    from rom24 import world_classes

    init_time()
    init_instance()
    read.read_tables()
    data_loader.load_areas()
    # fix_exits()
    area_update()
    object_creator.setup_exits()
    update.instance_number_save()

    results = (
        "-----------------------------------------",
        "    Loaded %d Areas" % world_classes.Area.template_count,
        "    Loaded %d Npc Templates" % handler_npc.Npc.template_count,
        "    Loaded %d Item Templates" % handler_item.Items.template_count,
        "    Loaded %d Room Templates" % handler_room.Room.template_count,
        "    Loaded %d Shops" % len(instance.shop_templates),
        "    Loaded %d Total Templates"
        % (
            world_classes.Area.template_count
            + handler_npc.Npc.template_count
            + handler_item.Items.template_count
            + handler_room.Room.template_count
        ),
        "-----------------------------------------",
        "    Loaded %d Resets" % world_classes.Reset.load_count,
        "-----------------------------------------",
        "    Loaded %d Area Instances" % world_classes.Area.instance_count,
        "    Loaded %d Npc Instances" % handler_npc.Npc.instance_count,
        "    Loaded %d Item Instances" % handler_item.Items.instance_count,
        "    Loaded %d Room Instances" % handler_room.Room.instance_count,
        "    Loaded %d Total Instances"
        % (
            world_classes.Area.instance_count
            + handler_room.Room.instance_count
            + handler_item.Items.instance_count
            + handler_npc.Npc.instance_count
        ),
        "-----------------------------------------",
        "    Loaded %d Help files" % len(merc.help_list),
        "    Loaded %d Socials" % len(merc.social_list),
        "-----------------------------------------",
    )
    spaces = "\n" + " " * 51
    logger.info(spaces.join(results))


def init_instance():
    # First lets add the bad terms we dont want to pass during instancing, while copying attributes
    instance.not_to_instance.append("instance_id")
    instance.not_to_instance.append("act")
    fp = open(
        settings.INSTANCE_NUM_FILE, "a"
    )  # in case the file doesnt exist open in append mode to not wipe
    fp.close()
    fp = open(settings.INSTANCE_NUM_FILE, "r")
    junk, instance.max_instance_id = game_utils.read_int(fp.read())
    fp.close()
    if instance.max_instance_id == 0 or not instance.max_instance_id:
        logger.info("First run, or problem with instance, setting 0")
        instance.max_instance_id = 0
    else:
        logger.info(
            "Global Instance Tracker, instances thus far: %d", instance.max_instance_id
        )


def fix_exits():
    for k, r in instance.room_templates.items():
        for e in r.template_exit[:]:
            if e and type(e.template_to_room) == int:
                if e.template_to_room not in instance.room_templates:
                    logger.error(
                        "Fix_exits: Failed to find to_room for %d: %d",
                        r.template_vnum,
                        e.template_to_room,
                    )
                    e.template_to_room = None
                    r.template_exit.remove(e)
                else:
                    e.template_to_room = instance.room_templates[e.template_to_room]


# * Repopulate areas periodically.
def area_update():
    for area_id, area in instance.areas.items():
        area.age += 1
        if area.age < 3:
            continue
        #
        # * Check age and reset.
        # * Note: Mud School resets every 3 minutes (not 15).
        # */
        if (
            not area.empty and (area.character == 0 or area.age >= 15)
        ) or area.age >= 31:
            reset_area(area)
            handler_game.wiznet(
                "%s has just been reset." % area.name, None, None, merc.WIZ_RESETS, 0, 0
            )

        area.age = random.randint(0, 3)
        school_instance_id = instance.instances_by_room[merc.ROOM_VNUM_SCHOOL][0]
        school_instance = instance.rooms[school_instance_id]
        if school_instance and area_id == school_instance.area:
            area.age = 15 - 2
        elif area.player_count == 0:
            area.empty = True


def m_reset(pReset, last, level, npc):
    if pReset.arg1 not in instance.npc_templates.keys():
        logger.error("Reset_area: 'M': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        npcTemplate = instance.npc_templates[pReset.arg1]

    if pReset.arg3 not in instance.room_templates.keys():
        logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
        return last, level, npc
    else:
        roomInstance_id = instance.instances_by_room[pReset.arg3][0]
        roomInstance = instance.global_instances[roomInstance_id]

    if npcTemplate.count >= pReset.arg2:
        last = False
        return last, level, npc
    count = 0
    for npc_id in roomInstance.people[:]:
        npc = instance.global_instances[npc_id]
        if npc.is_npc():
            if npc.vnum == npcTemplate.vnum:
                count += 1
                if count >= pReset.arg4:
                    last = False
                    break

    if count >= pReset.arg4:
        return last, level, npc

    npc = object_creator.create_mobile(npcTemplate)

    #
    # * Check for pet shop.
    # */

    if roomInstance.vnum - 1 in instance.room_templates.keys():
        prevRoomInstance_id = instance.instances_by_room[roomInstance.vnum - 1][0]
        prevRoomInstance = instance.global_instances[prevRoomInstance_id]
        if state_checks.IS_SET(prevRoomInstance.room_flags, merc.ROOM_PET_SHOP):
            npc.act.set_bit(merc.ACT_PET)

    # set area */
    npc.area = roomInstance.area

    roomInstance.put(npc)
    level = max(0, min(npc.level - 2, merc.LEVEL_HERO - 1))
    last = True
    return last, level, npc


def o_reset(pArea, pReset, last, level, npc):
    item = None
    if pReset.arg1 not in instance.item_templates.keys():
        logger.error("Reset_area: 'O': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        itemTemplate = instance.item_templates[pReset.arg1]

    if pReset.arg3 not in instance.room_templates.keys():
        logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg3)
        return last, level, npc
    else:
        roomInstance_id = instance.instances_by_room[pReset.arg3][0]
        roomInstance = instance.global_instances[roomInstance_id]

    if (
        pArea.player_count > 0
        or handler_item.count_obj_list(itemTemplate, roomInstance.items) > 0
    ):
        last = False
        return last, level, npc

    item = object_creator.create_item(
        itemTemplate, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1)
    )
    item.cost = 0
    roomInstance.put(item)
    item = None
    last = True
    return last, level, npc


def p_reset(pArea, pReset, last, level, npc):
    item = None
    if pReset.arg1 not in instance.item_templates.keys():
        logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        itemTemplate = instance.item_templates[pReset.arg1]

    if pReset.arg3 not in instance.item_templates.keys():
        logger.error("Reset_area: 'P': bad vnum %d.", pReset.arg3)
        return last, level, npc
    else:
        item_toTemplate = instance.item_templates[pReset.arg3]
    if pReset.arg2 > 50:  # old format */
        limit = 6
    elif pReset.arg2 == -1:  # no limit */
        limit = 999
    else:
        limit = pReset.arg2
    item_to = None
    item_to_list = instance.instances_by_item.get(item_toTemplate.vnum, None)
    if item_to_list:
        item_to = instance.global_instances[item_to_list[0]]

    if (
        pArea.player_count > 0
        or not item_to
        or (not item_to.in_room and not last)
        or (itemTemplate.count >= limit and random.randint(0, 4) != 0)
        or handler_item.count_obj_list(itemTemplate, item_to.inventory) > pReset.arg4
    ):
        last = False
        return last, level, npc
    count = handler_item.count_obj_list(itemTemplate, item_to.inventory)
    # Converted while to For Loop, testing indicated
    # While loop was ~.002-.004
    # For loop ~.0009-.001
    if item_to:
        for i in range(pReset.arg4):
            item = object_creator.create_item(
                itemTemplate, game_utils.number_fuzzy(item_to.level)
            )
            item_to.put(item)
            item = None
            count += 1
            if count >= pReset.arg4:
                break
            if itemTemplate.count >= limit:
                break

        # fix object lock state! */
        item_to.value[1] = item_toTemplate.value[1]
    last = True
    return last, level, npc


def g_e_reset(pReset, last, level, npc):
    item = None
    if pReset.arg1 not in instance.item_templates.keys():
        logger.error("Reset_area: 'E' or 'G': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        itemTemplate = instance.item_templates[pReset.arg1]
    # if not last:
    #    continue

    if not npc:
        logger.error("Reset_area: 'E' or 'G': None mob for vnum %d.", pReset.arg1)
        last = False
        return last, level, npc

    olevel = 0
    if instance.npc_templates[npc.vnum].pShop:
        if not itemTemplate.new_format:
            if (
                itemTemplate.item_type == merc.ITEM_PILL
                or itemTemplate.item_type == merc.ITEM_POTION
                or itemTemplate.item_type == merc.ITEM_SCROLL
            ):
                olevel = 53
                for i in itemTemplate.value:
                    if i > 0:
                        for j in const.skill_table[itemTemplate.value[i]].skill_level:
                            olevel = min(olevel, j)

                olevel = max(0, (olevel * 3 // 4) - 2)

            elif itemTemplate.item_type == merc.ITEM_WAND:
                olevel = random.randint(10, 20)
            elif itemTemplate.item_type == merc.ITEM_STAFF:
                olevel = random.randint(15, 25)
            elif itemTemplate.item_type == merc.ITEM_ARMOR:
                olevel = random.randint(5, 15)
            elif itemTemplate.item_type == merc.ITEM_WEAPON:
                olevel = random.randint(5, 15)
            elif itemTemplate.item_type == merc.ITEM_TREASURE:
                olevel = random.randint(10, 20)

        item = object_creator.create_item(itemTemplate, olevel)
        item.flags.shop_inventory = True
    else:
        if pReset.arg2 > 50:  # old format */
            limit = 6
        elif pReset.arg2 == -1:  # no limit */
            limit = 999
        else:
            limit = pReset.arg2

        if itemTemplate.count < limit or random.randint(0, 4) == 0:
            item = object_creator.create_item(
                itemTemplate, min(game_utils.number_fuzzy(level), merc.LEVEL_HERO - 1)
            )
        else:
            return last, level, npc
    npc.put(item)
    if pReset.command == "E":
        npc.equip(item, True)
    item = None
    last = True
    return last, level, npc


def d_reset(pReset, last, level, npc):
    if pReset.arg1 not in instance.room_templates.keys():
        logger.error("Reset_area: 'D': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        roomInstance_id = instance.instances_by_room[pReset.arg1][0]
        roomInstance = instance.global_instances[roomInstance_id]
        pexit = roomInstance.exit[pReset.arg2]
    if not pexit:
        return last, level, npc

    if pReset.arg3 == 0:
        pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_CLOSED)
        pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
        return last, level, npc
    elif pReset.arg3 == 1:
        pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_CLOSED)
        pexit.exit_info = state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
        return last, level, npc
    elif pReset.arg3 == 2:
        pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_CLOSED)
        pexit.exit_info = state_checks.SET_BIT(pexit.exit_info, merc.EX_LOCKED)
        return last, level, npc
    last = True
    return last, level, npc


def r_reset(pReset, last, level, npc):
    if pReset.arg1 not in instance.room_templates.keys():
        logger.error("Reset_area: 'R': bad vnum %d.", pReset.arg1)
        return last, level, npc
    else:
        roomInstance_id = instance.instances_by_room[pReset.arg1][0]
        roomInstance = instance.global_instances[roomInstance_id]
    for d0 in range(pReset.arg2 - 1):
        d1 = random.randint(d0, pReset.arg2 - 1)
        pexit = roomInstance.exit[d0]
        roomInstance.exit[d0] = roomInstance.exit[d1]
        roomInstance.exit[d1] = pexit
        break
    return last, level, npc


def reset_area(pArea):
    npc = None
    last = True
    level = 0
    for pReset in pArea.reset_list[:]:
        if pReset.command.startswith("M"):
            last, level, npc = m_reset(pReset, last, level, npc)
        elif pReset.command.startswith("O"):
            last, level, npc = o_reset(pArea, pReset, last, level, npc)
        elif pReset.command.startswith("P"):
            last, level, npc = p_reset(pArea, pReset, last, level, npc)
        elif pReset.command.startswith("G") or pReset.command.startswith("E"):
            last, level, npc = g_e_reset(pReset, last, level, npc)
        elif pReset.command.startswith("D"):
            last, level, npc = d_reset(pReset, last, level, npc)
        elif pReset.command.startswith("R"):
            last, level, npc = r_reset(pReset, last, level, npc)
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
