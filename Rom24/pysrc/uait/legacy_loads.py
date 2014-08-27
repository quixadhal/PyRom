import os
import pickle
import sys
import logging
import interp
import save

logger = logging.getLogger()

import const
import handler_item
import handler_room
import settings
import tables
import game_utils
import handler_ch
import handler_game
import world_classes
import merc
import state_checks

serializer_list = []

class AREA_SERIALIZER:
    def __init__(self):
        self.area_name = ""
        self.area = []
        self.rooms = []
        self.mobiles = []
        self.objects = []
        self.resets = []
        self.shops = []

    def to_Pickle(self):
        area_save_dir = settings.LEGACY_AREA_DIR + "/" + self.area_name
        room_save_dir = area_save_dir + "/rooms"
        obj_save_dir = area_save_dir + "/mobiles"
        mobile_save_dir = area_save_dir + "/objects"
        shop_save_dir = area_save_dir + "/shops"
        reset_save_dir = area_save_dir + "/resets"
        os.makedirs(area_save_dir, 0o755, True)
        os.makedirs(room_save_dir, 0o755, True)
        os.makedirs(obj_save_dir, 0o755, True)
        os.makedirs(mobile_save_dir, 0o755, True)
        os.makedirs(reset_save_dir, 0o755, True)
        os.makedirs(shop_save_dir, 0o755, True)
        for area in self.area:
            with open(area_save_dir + "/" + self.area_name + '.pickle', 'wb') as af:
                pickle.dump(area, af, pickle.HIGHEST_PROTOCOL)
                af.close()
        for room in self.rooms:
            with open(room_save_dir + "/" + str(room.vnum) + settings.PKL_EXTN, 'wb') as rf:
                pickle.dump(room, rf, pickle.HIGHEST_PROTOCOL)
                rf.close()
        for mob in self.mobiles:
            with open(mobile_save_dir + "/" + str(mob.vnum) + settings.PKL_EXTN, 'wb') as mf:
                pickle.dump(mob, mf, pickle.HIGHEST_PROTOCOL)
                mf.close()
        for object in self.objects:
            with open(obj_save_dir + "/" + str(object.vnum) + settings.PKL_EXTN, 'wb') as of:
                pickle.dump(object, of, pickle.HIGHEST_PROTOCOL)
                of.close()
        for shop in self.shops:
            with open(shop_save_dir + "/" + str(shop.keeper) + settings.PKL_EXTN, 'wb') as sf:
                pickle.dump(shop, sf, pickle.HIGHEST_PROTOCOL)
                sf.close()
        for reset in self.resets:
            with open(reset_save_dir + "/" + str(reset) + settings.PKL_EXTN, 'wb') as ref:
                pickle.dump(reset, ref, pickle.HIGHEST_PROTOCOL)
                ref.close()


__author__ = 'syn'
def do_apickle(ch, argument):
    ch.send("Saving areas to pickle format..\n\n")
    save.area_pickler(ch)
    open(os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST), 'w').close()  # lets write a clean list
    open(os.path.join(settings.LEGACY_AREA_DIR, settings.SOCIAL_LIST), 'w').close()
    with open(os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST), 'a') as alf:
        ch.send("Writing Area List...\n\n")
        for area in merc.area_list:
            alf.write(area.name)
        alf.write("$")
        alf.close()
        ch.send("Area List Saved.\n\n")
    with open(os.path.join(settings.LEGACY_AREA_DIR, settings.SOCIAL_LIST), 'a') as slf:
        ch.send("Writing Social List...\n\n")
        for social in merc.social_list:
            slf.write(social.name)
        slf.write("$")
        slf.close()
        ch.send("Social List Saved.\n\n")
    return

interp.register_command(interp.cmd_type('apickle', do_apickle, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))


to_Pickle()
    os.makedirs(settings.HELP_DIR, 0o755, True)
    with open(os.path.join(settings.HELP_DIR, 'help_files' + settings.PKL_EXTN), 'wb') as hf:
        pickle.dump(merc.help_list, hf, pickle.HIGHEST_PROTOCOL)
        print("\n\nSaving Helpfiles...\n\n")
        hf.close()
    for zsocial in merc.social_list:
        os.makedirs(settings.SOCIAL_DIR, 0o755, True)
        social_file = zsocial.name + settings.PKL_EXTN
        with open(os.path.join(settings.SOCIAL_DIR, social_file), 'wb') as sf:
            pickle.dump(zsocial, sf, pickle.HIGHEST_PROTOCOL)
            print("Saving Social: %s\n" % zsocial.name)
            sf.close()
    print("All Done..\n\n")

def to_Pickle():
    for area_serial in world_classes.serializer_list:
        area_save_dir = settings.LEGACY_AREA_DIR + "/" + area_serial.area_name
        room_save_dir = area_save_dir + "/rooms"
        obj_save_dir = area_save_dir + "/mobiles"
        mobile_save_dir = area_save_dir + "/objects"
        shop_save_dir = area_save_dir + "/shops"
        reset_save_dir = area_save_dir + "/resets"
        os.makedirs(area_save_dir, 0o755, True)
        os.makedirs(room_save_dir, 0o755, True)
        os.makedirs(obj_save_dir, 0o755, True)
        os.makedirs(mobile_save_dir, 0o755, True)
        os.makedirs(reset_save_dir, 0o755, True)
        os.makedirs(shop_save_dir, 0o755, True)
        for area in area_serial.area:
            with open(area_save_dir + "/" + area_serial.area_name + '.pickle', 'wb') as af:
                pickle.dump(area, af, pickle.HIGHEST_PROTOCOL)
                af.close()
        for room in area_serial.rooms:
            with open(room_save_dir + "/" + str(room.vnum) + settings.PKL_EXTN, 'wb') as rf:
                pickle.dump(room, rf, pickle.HIGHEST_PROTOCOL)
                rf.close()
        for mob in area_serial.mobiles:
            with open(mobile_save_dir + "/" + str(mob.vnum) + settings.PKL_EXTN, 'wb') as mf:
                pickle.dump(mob, mf, pickle.HIGHEST_PROTOCOL)
                mf.close()
        for object in area_serial.objects:
            with open(obj_save_dir + "/" + str(object.vnum) + settings.PKL_EXTN, 'wb') as of:
                pickle.dump(object, of, pickle.HIGHEST_PROTOCOL)
                of.close()
        for shop in area_serial.shops:
            with open(shop_save_dir + "/" + str(shop.keeper) + settings.PKL_EXTN, 'wb') as sf:
                pickle.dump(shop, sf, pickle.HIGHEST_PROTOCOL)
                sf.close()
        for reset in area_serial.resets:
            with open(reset_save_dir + "/" + str(reset) + settings.PKL_EXTN, 'wb') as ref:
                pickle.dump(reset, ref, pickle.HIGHEST_PROTOCOL)
                ref.close()

def load_areas():
    area_list = os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST)
    alf = open(area_list, 'r')
    parea = alf.readline().strip()
    while parea != "$":
        with open(os.path.join(settings.LEGACY_AREA_DIR, parea, parea + ".pickle"), 'rb') as af:
            zarea = pickle.load(af)
            merc.area_list.append(zarea)
            load_rooms(zarea.room_dict())
            load_mobiles(zarea.mobile_dict())
            load_objects(zarea.object_dict())
            load_shops(zarea.shop_dict())
            parea = alf.readline().strip()
            logger.info("Area %s loaded", zarea.name)
        af.close()
    alf.close()
    logger.info('Game Data Load Complete.')


def load_helps():
    count = 0
    with open(os.path.join(settings.HELP_DIR, settings.HELP_FILE + settings.PKL_EXTN), 'rb') as hf:
        helps = pickle.load(hf)
        for item in helps:
            count += 1
            merc.help_list.append(item)
        logger.info("Loaded %d helps", count)
    hf.close()


def load_mobiles(mobile_dict):
    count = 0
    for k, v in mobile_dict.items():
        instance.npc_templates[k] = v
        count += 1
    logger.info("%d mobiles loaded", count)


def load_objects(object_dict):
    count = 0
    for k, v in object_dict.items():
        instance.item_templates[k] = v
        count += 1
    logger.info("%d items loaded", count)


def load_resets(reset_dict):
    count = 0
    for k, v in reset_dict.items():
        merc.reset_list[k] = v
        count += 1
    logger.info("%d resets loaded", count)


def load_rooms(room_dict):
    count = 0
    for k, v in room_dict.items():
        instance.room_templates[k] = v
        count += 1
    logger.info("%d rooms loaded", count)


def load_shops(shop_dict):
    count = 0
    for k, v in shop_dict.items():
        merc.shop_list[k] = v
        count += 1
    logger.info("%d shops loaded", count)


def load_socials():
    slf = open(settings.SOCIAL_LIST, 'r')
    social = slf.readline().strip()
    while social != "$":
        with open(os.path.join(settings.SOCIAL_DIR, social + settings.PKL_EXTN), 'rb') as sf:
            social_file = pickle.load(sf)
            merc.social_list.append(social_file)
            logger.info("Social %s loaded", social_file.name)
        sf.close()
    slf.close()

def load_areas():
    logger.info('Loading Areas...')
    narea_list = os.path.join(settings.LEGACY_AREA_DIR, settings.AREA_LIST)
    parea_list = os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST)
    fp = open(narea_list, 'r')
    area = fp.readline().strip()
    while area != "$":
        afp = open(os.path.join(settings.LEGACY_AREA_DIR, area), 'r')
        load_area(afp.read())
        area = fp.readline().strip()
        afp.close()
    fp.close()
    fp = open(parea_list, 'r')
    parea = fp.readline().strip()
    while parea != "$":
        with open(os.path.join(settings.LEGACY_AREA_DIR, parea, parea + ".pickle"), 'rb') as ff:
            zarea = pickle.load(ff)
            merc.area_list.append(zarea)
            parea = fp.readline().strip()
            print(zarea.name, "loaded area name from pickle")
        ff.close()
    fp.close()
    logger.info('Done. (loading areas)')


def load_area(area):
    if not area.strip():
        return

    area, w = game_utils.read_word(area, False)
    pArea = None
    while area:
        if w == "#AREA":
            pArea = world_classes.Area()
            area, pArea.file_name = game_utils.read_string(area)
            area, pArea.name = game_utils.read_string(area)
            area, pArea.credits = game_utils.read_string(area)
            area, pArea.min_vnum = game_utils.read_int(area)
            area, pArea.max_vnum = game_utils.read_int(area)
            logger.info("    Loading %s", pArea)

        elif w == "#HELPS":
            area = load_helps(area)
        elif w == "#MOBILES":
            area = load_mobiles(area, pArea)
        elif w == "#OBJECTS":
            area = load_objects(area, pArea)
        elif w == "#RESETS":
            area = load_resets(area, pArea)
        elif w == "#ROOMS":
            area = load_rooms(area, pArea)
        elif w == "#SHOPS":
            area = load_shops(area, pArea)
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


def load_mobiles(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound

    while w != '0':
        mob = handler_ch.Mobile()
        mob.vnum = int(w)
        instance.npc_templates[mob.vnum] = mob
        area, mob.name = game_utils.read_string(area)
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
        area, mob.hit_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit_dice[2] = game_utils.read_int(area)
        area, mob.mana_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana_dice[2] = game_utils.read_int(area)
        area, mob.dam_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.dam_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.dam_dice[2] = game_utils.read_int(area)
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
        pArea.mobile_dict[mob.vnum] = mob
        w = w[1:]  # strip the pound
    return area


def load_objects(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        obj = handler_item.Items()
        obj.vnum = int(w)
        instance.item_templates[obj.vnum] = obj
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
        elif obj.item_type == merc.ITEM_POTION or obj.item_type == merc.ITEM_SCROLL or obj.item_type == merc.ITEM_PILL:
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
                ed = world_classes.ExtraDescrData()
                area, ed.keyword = game_utils.read_string(area)
                area, ed.description = game_utils.read_string(area)
                obj.extra_descr.append(ed)

            area, w = game_utils.read_word(area, False)

        pArea.object_dict[obj.vnum] = obj
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

        reset = world_classes.Reset()
        reset.command = letter
        area, number = game_utils.read_int(area)  # if_flag
        area, reset.arg1 = game_utils.read_int(area)
        area, reset.arg2 = game_utils.read_int(area)
        area, reset.arg3 = (area, 0) if letter == 'G' or letter == 'R' else game_utils.read_int(area)
        area, reset.arg4 = game_utils.read_int(area) if letter == 'P' or letter == 'M' else (area, 0)
        area, t = game_utils.read_to_eol(area)
        pArea.reset_list.append(reset)
        merc.reset_list.append(reset)
        pArea.reset_dict[reset] = reset
    return area


def load_rooms(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        room = handler_room.Room()
        room.vnum = int(w)
        if room.vnum in instance.room_templates:
            logger.critical('Dupicate room Vnum: %d', room.vnum)
            sys.exit(1)

        instance.room_templates[room.vnum] = room
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
                nexit = world_classes.Exit()
                area, door = game_utils.read_int(area)
                area, nexit.description = game_utils.read_string(area)
                area, nexit.keyword = game_utils.read_string(area)
                area, locks = game_utils.read_int(area)
                area, nexit.key = game_utils.read_int(area)
                area, nexit.to_room = game_utils.read_int(area)
                room.exit[door] = nexit
            elif letter == 'E':
                ed = world_classes.ExtraDescrData()
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
        pArea.room_dict[room.vnum] = room
    return area


def load_shops(area, pArea):
    while True:
        area, keeper = game_utils.read_int(area)

        if keeper == 0:
            break
        shop = world_classes.Shop()
        shop.keeper = keeper
        for r in range(merc.MAX_TRADE):
            area, shop.buy_type[r] = game_utils.read_int(area)
        area, shop.profit_buy = game_utils.read_int(area)
        area, shop.profit_sell = game_utils.read_int(area)
        area, shop.open_hour = game_utils.read_int(area)
        area, shop.close_hour = game_utils.read_int(area)
        area, t = game_utils.read_to_eol(area)
        instance.npc_templates[keeper].pShop = shop
        merc.shop_list.append(shop)
        pArea.shop_dict[shop.keeper] = shop
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
            area, instance.npc_templates[vnum].spec_fun = game_utils.read_word(area, False)
        else:
            logger.error("Load_specials: letter noth *SM: %s", letter)

    return area
