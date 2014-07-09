import random
import sys

import logging

logger = logging.getLogger()

import game_utils
import handler
import handler_game
import handler_obj
import handler_room
import world_classes
import merc
import mobile
import special
import state_checks
__author__ = 'venom'

def create_room(roomTemplate):
    if roomTemplate is None:
        logger.critical("Create_room: No roomTemplate given.")
        sys.exit(1)

    room = handler_room.ROOM_DATA()

    room.roomTemplate = roomTemplate.template_vnum
    room.instance_id = handler.global_instance_generator()
    room.contents = []
    room.people = []
    merc.global_instances[room.instance_id] = room
    merc.room_instances[room.instance_id] = merc.global_instances[room.instance_id]
    room.name = roomTemplate.template_name
    room.area = roomTemplate.template_area
    room.description = roomTemplate.template_description
    room.extra_descr = roomTemplate.template_extra_descr
    room.clan = roomTemplate.template_clan
    room.heal_rate = roomTemplate.template_heal_rate
    room.mana_rate = roomTemplate.template_mana_rate
    room.room_flags = roomTemplate.template_room_flags
    room.sector_type = roomTemplate.template_sector_type
    room.owner = roomTemplate.template_owner
    room.light = roomTemplate.template_light
    room.exit = roomTemplate.template_exit
    room.old_exit = roomTemplate.template_old_exit


def clone_room(parent, clone):
    if not parent or not clone:
        return
    '''Clone a room, minus contents and exits'''
    clone.instance_id = handler.global_instance_generator()
    merc.global_instances[clone.instance_id] = clone
    merc.room_instances[clone.instance_id] = merc.global_instances[clone.instance_id]
    clone.roomTemplate = parent.roomTemplate
    clone.name = parent.name
    clone.area = parent.area
    clone.description = parent.description
    clone.extra_descr = parent.extra_descr
    clone.clan = parent.clan
    clone.heal_rate = parent.heal_rate
    clone.mana_rate = parent.mana_rate
    clone.room_flags = parent.room_flags
    clone.sector_type = parent.sector_type
    clone.owner = parent.owner
    clone.light = parent.light

def setup_exits():
    for id, room in merc.room_instances.items():
        if room.exit:
            for door, pexit in enumerate(room.exit):
                if pexit:
                    template = merc.exit_templates[pexit]
                    exit_instance = world_classes.EXIT_DATA(template)
                    room.exit[door] = exit_instance.name


def create_shop(shopTemplate, keeper, room):
    shop = world_classes.SHOP_DATA()

    shop.instance_id = handler.global_instance_generator()
    merc.global_instances[shop.instance_id] = shop
    merc.shops_instances[shop.instance_id] = merc.global_instances[shop.instance_id]

    shop.buy_type = shopTemplate.template_buy_type
    shop.mobTemplate = shopTemplate.template_keeper
    shop.keeper_instance = keeper.instance_id
    shop.room_instance = room.instance_id
    shop.close_hour = shopTemplate.template_close_hour
    shop.open_hour = shopTemplate.template_open_hour
    shop.profit_buy = shopTemplate.template_profit_buy
    shop.profit_sell = shopTemplate.template_profit_sell


def clone_shop(parent, clone, room, keeper):
    clone.instance_id = handler.global_instance_generator()
    merc.global_instances[clone.instance_id] = clone
    merc.shops_instances[clone.instance_id] = merc.global_instances[clone.instance_id]

    clone.buy_type = parent.buy_type
    clone.mobTemplate = parent.keeper
    clone.keeper_instance = keeper.instance_id
    clone.room_instance = room.instance_id
    clone.close_hour = parent.close_hour
    clone.open_hour = parent.open_hour
    clone.profit_buy = parent.profit_buy
    clone.profit_sell = parent.profit_sell


def create_exit(exitTemplate):
    pexit = world_classes.EXIT_DATA()

    pexit.instance_id = handler.global_instance_generator()
    merc.global_instances[pexit.instance_id] = pexit
    merc.exit_instances[pexit.instance_id] = merc.global_instances[pexit.instance_id]




def create_mobile(mobTemplate):
    if mobTemplate is None:
        logger.critical("Create_mobile: None pMobIndex.")
        sys.exit(1)

    mob = mobile.Mobile()

    mob.mobTemplate = mobTemplate.vnum
    mob.instance_id = handler.global_instance_generator()
    merc.global_instances[mob.instance_id] = mob
    merc.mob_instances[mob.instance_id] = merc.global_instances[mob.instance_id]
    mob.name = mobTemplate.player_name
    mob.id = game_utils.get_mob_id()
    mob.short_descr = mobTemplate.short_descr
    mob.long_descr = mobTemplate.long_descr
    mob.description = mobTemplate.description
    if mobTemplate.spec_fun:
        mob.spec_fun = special.spec_table[mobTemplate.spec_fun]
    mob.prompt = None

    if mobTemplate.wealth == 0:
        mob.silver = 0
        mob.gold = 0
    else:
        wealth = random.randint(mobTemplate.wealth // 2, 3 * mobTemplate.wealth // 2)
        mob.gold = random.randint(wealth // 200, wealth // 100)
        mob.silver = wealth - (mob.gold * 100)

    if mobTemplate.new_format:
        # load in new style */
        # read from prototype */
        mob.group = mobTemplate.group
        mob.act.set_bit(mobTemplate.act)
        mob.comm.set_bit(merc.COMM_NOCHANNELS | merc.COMM_NOSHOUT | merc.COMM_NOTELL)
        mob.affected_by.set_bit(mobTemplate.affected_by)
        mob.alignment = mobTemplate.alignment
        mob.level = mobTemplate.level
        mob.hitroll = mobTemplate.hitroll
        mob.damroll = mobTemplate.damage[merc.DICE_BONUS]
        mob.max_hit = game_utils.dice(mobTemplate.hit[merc.DICE_NUMBER], mobTemplate.hit[merc.DICE_TYPE]) + mobTemplate.hit[
            merc.DICE_BONUS]
        mob.hit = mob.max_hit
        mob.max_mana = game_utils.dice(mobTemplate.mana[merc.DICE_NUMBER], mobTemplate.mana[merc.DICE_TYPE]) + mobTemplate.mana[
            merc.DICE_BONUS]
        mob.mana = mob.max_mana
        mob.damage[merc.DICE_NUMBER] = mobTemplate.damage[merc.DICE_NUMBER]
        mob.damage[merc.DICE_TYPE] = mobTemplate.damage[merc.DICE_TYPE]
        mob.dam_type = mobTemplate.dam_type
        if mob.dam_type == 0:
            num = random.randint(1, 3)
            if num == 1:
                mob.dam_type = 3  # slash */
            elif num == 2:
                mob.dam_type = 7  # pound */
            elif num == 3:
                mob.dam_type = 11  # pierce */
        for i in range(4):
            mob.armor[i] = mobTemplate.ac[i]
        mob.off_flags.set_bit(mobTemplate.off_flags)
        mob.imm_flags.set_bit(mobTemplate.imm_flags)
        mob.res_flags.set_bit(mobTemplate.res_flags)
        mob.vuln_flags.set_bit(mobTemplate.vuln_flags)
        mob.start_pos = mobTemplate.start_pos
        mob.default_pos = mobTemplate.default_pos
        mob.sex = mobTemplate.sex
        if type(mobTemplate.sex) != int or mob.sex == 3:  # random sex */
            mob.sex = random.randint(1, 2)
        mob.race = mobTemplate.race
        mob.form.set_bit(mobTemplate.form)
        mob.parts.set_bit(mobTemplate.parts)
        mob.size = int(mobTemplate.size)
        mob.material = mobTemplate.material

        # computed on the spot */
        for i in range(merc.MAX_STATS):
            mob.perm_stat[i] = min(25, 11 + mob.level // 4)

        if mob.act.is_set(merc.ACT_WARRIOR):
            mob.perm_stat[merc.STAT_STR] += 3
            mob.perm_stat[merc.STAT_INT] -= 1
            mob.perm_stat[merc.STAT_CON] += 2

        if mob.act.is_set(merc.ACT_THIEF):
            mob.perm_stat[merc.STAT_DEX] += 3
            mob.perm_stat[merc.STAT_INT] += 1
            mob.perm_stat[merc.STAT_WIS] -= 1

        if mob.act.is_set(merc.ACT_CLERIC):
            mob.perm_stat[merc.STAT_WIS] += 3
            mob.perm_stat[merc.STAT_DEX] -= 1
            mob.perm_stat[merc.STAT_STR] += 1

        if mob.act.is_set(merc.ACT_MAGE):
            mob.perm_stat[merc.STAT_INT] += 3
            mob.perm_stat[merc.STAT_STR] -= 1
            mob.perm_stat[merc.STAT_DEX] += 1

        if mob.off_flags.is_set(merc.OFF_FAST):
            mob.perm_stat[merc.STAT_DEX] += 2

        mob.perm_stat[merc.STAT_STR] += mob.size - merc.SIZE_MEDIUM
        mob.perm_stat[merc.STAT_CON] += (mob.size - merc.SIZE_MEDIUM) // 2
        af = handler_game.AFFECT_DATA()
        # let's get some spell action */
        if mob.is_affected(merc.AFF_SANCTUARY):
            af.where = merc.TO_AFFECTS
            af.type = "sanctuary"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_NONE
            af.modifier = 0
            af.bitvector = merc.AFF_SANCTUARY
            mob.affect_add(af)

        if mob.is_affected(merc.AFF_HASTE):
            af.where = merc.TO_AFFECTS
            af.type = "haste"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_DEX
            af.modifier = 1 + (mob.level >= 18) + (mob.level >= 25) + (mob.level >= 32)
            af.bitvector = merc.AFF_HASTE
            mob.affect_add(af)

        if mob.is_affected(merc.AFF_PROTECT_EVIL):
            af.where = merc.TO_AFFECTS
            af.type = "protection evil"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_EVIL
            mob.affect_add(af)

        if mob.is_affected(merc.AFF_PROTECT_GOOD):
            af.where = merc.TO_AFFECTS
            af.type = "protection good"
            af.level = mob.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_GOOD
            mob.affect_add(af)
    else:  # read in old format and convert */
        mob.act.set_bit(mobTemplate.act)
        mob.affected_by.set_bit(mobTemplate.affected_by)
        mob.alignment = mobTemplate.alignment
        mob.level = mobTemplate.level
        mob.hitroll = mobTemplate.hitroll
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
        mob.race = mobTemplate.race
        mob.off_flags.set_bit(mobTemplate.off_flags)
        mob.imm_flags.set_bit(mobTemplate.imm_flags)
        mob.res_flags.set_bit(mobTemplate.res_flags)
        mob.vuln_flags.set_bit(mobTemplate.vuln_flags)
        mob.start_pos = mobTemplate.start_pos
        mob.default_pos = mobTemplate.default_pos
        mob.sex = mobTemplate.sex
        mob.form.set_bit(mobTemplate.form)
        mob.parts.set_bit(mobTemplate.parts)
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
    clone.instance = handler.global_instance_generator()
    merc.global_instances[clone.instance_id] = clone
    merc.mob_instances[clone.instance_id] = merc.global_instances[clone.instance_id]
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
def create_object(objTemplate, level):
    if not objTemplate:
        logger.critical("Create_object: No objTemplate.")
        sys.exit(1)

    obj = handler_obj.OBJ_DATA()
    obj.instance_id = handler.global_instance_generator()
    merc.global_instances[obj.instance_id] = obj
    merc.obj_instances[obj.instance_id] = merc.global_instances[obj.instance_id]
    obj.in_room = 0
    obj.enchanted = False

    if objTemplate.template_new_format is True:
        obj.level = objTemplate.template_level
    else:
        obj.level = max(0, level)
    obj.wear_loc = -1

    obj.name = objTemplate.template_name
    obj.short_descr = objTemplate.template_short_descr
    obj.description = objTemplate.template_description
    obj.material = objTemplate.template_material
    obj.item_type = objTemplate.template_item_type
    obj.extra_flags = objTemplate.template_extra_flags
    obj.wear_flags = objTemplate.template_wear_flags
    obj.value = objTemplate.template_value[:]
    obj.weight = objTemplate.template_weight

    if level == -1 or objTemplate.template_new_format:
        obj.cost = objTemplate.template_cost
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
        if not objTemplate.template_new_format:
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
        if level != -1 and not objTemplate.template_new_format:
            obj.value[0] = game_utils.number_fuzzy(obj.value[0])
    elif obj.item_type == merc.ITEM_WAND \
            or obj.item_type == merc.ITEM_STAFF:
        if level != -1 and not objTemplate.template_new_format:
            obj.value[0] = game_utils.number_fuzzy(obj.value[0])
            obj.value[1] = game_utils.number_fuzzy(obj.value[1])
            obj.value[2] = obj.value[1]
        if not objTemplate.template_new_format:
            obj.cost *= 2
    elif obj.item_type == merc.ITEM_WEAPON:
        if level != -1 and not objTemplate.template_new_format:
            obj.value[1] = game_utils.number_fuzzy(game_utils.number_fuzzy(1 * level // 4 + 2))
            obj.value[2] = game_utils.number_fuzzy(game_utils.number_fuzzy(3 * level // 4 + 6))
    elif obj.item_type == merc.ITEM_ARMOR:
        if level != -1 and not objTemplate.template_new_format:
            obj.value[0] = game_utils.number_fuzzy(level // 5 + 3)
            obj.value[1] = game_utils.number_fuzzy(level // 5 + 3)
            obj.value[2] = game_utils.number_fuzzy(level // 5 + 3)
    elif obj.item_type == merc.ITEM_POTION \
            or obj.item_type == merc.ITEM_PILL:
        if level != -1 and not objTemplate.template_new_format:
            obj.value[0] = game_utils.number_fuzzy(game_utils.number_fuzzy(obj.value[0]))
    elif obj.item_type == merc.ITEM_MONEY:
        if not objTemplate.template_new_format:
            obj.value[0] = obj.cost
    else:
        logger.error("Bad item_type objTemplate vnum: %s(%s)" % (objTemplate.template_vnum, obj.item_type ))

    for paf in objTemplate.template_affected:
        if paf.location == merc.APPLY_SPELL_AFFECT:
            obj.affect_add(paf)
    obj.extra_descr = objTemplate.template_extra_descr
    merc.object_list.append(obj)
    obj.objTemplate = objTemplate.vnum
    return obj


# duplicate an object exactly -- except contents */
def clone_object(parent, clone):
    if not parent or not clone:
        return

    # start fixing the object */
    clone.name = parent.name
    clone.instance = handler.global_instance_generator()
    merc.global_instances[clone.instance_id] = clone
    merc.obj_instances[clone.instance_id] = merc.global_instances[clone.instance_id]
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
        ed_new = world_classes.EXTRA_DESCR_DATA()
        ed_new.keyword = ed.keyword
        ed_new.description = ed.description
        clone.extra_descr.append(ed)

# * Create a 'money' obj.
def create_money(gold, silver):
    if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
        logger.warn("BUG: Create_money: zero or negative money. %d ", min(gold, silver))
        gold = max(1, gold)
        silver = max(1, silver)

    if gold == 0 and silver == 1:
        obj = create_object(merc.obj_templates[merc.OBJ_VNUM_SILVER_ONE], 0)
        obj.instance_id = handler.global_instance_generator()
        merc.global_instances[obj.instance_id] = obj
        merc.obj_instances[obj.instance_id] = merc.global_instances[obj.instance_id]
    elif gold == 1 and silver == 0:
        obj = create_object(merc.obj_templates[merc.OBJ_VNUM_GOLD_ONE], 0)
    elif silver == 0:
        obj = create_object(merc.obj_templates[merc.OBJ_VNUM_GOLD_SOME], 0)
        obj.short_descr += " %d" % gold
        obj.value[1] = gold
        obj.cost = gold
        obj.weight = gold // 5
    elif gold == 0:
        obj = create_object(merc.obj_templates[merc.OBJ_VNUM_SILVER_SOME], 0)
        obj.short_descr += " %d" % silver
        obj.value[0] = silver
        obj.cost = silver
        obj.weight = silver // 20
    else:
        obj = create_object(merc.obj_templates[merc.OBJ_VNUM_COINS], 0)
        obj.short_descr += " %d %d" % (gold, silver)
        obj.value[0] = silver
        obj.value[1] = gold
        obj.cost = 100 * gold + silver
        obj.weight = gold // 5 + silver // 20
    return obj

