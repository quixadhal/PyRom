import random
import sys

import logging

logger = logging.getLogger()

import game_utils
import handler
import handler_game
import handler_item
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

    room = handler_room.Room(roomTemplate)
    return room


def clone_room(parent, clone):
    if not parent or not clone:
        return
    '''Clone a room, minus contents and exits'''
    clone = handler_room.Room(parent)
    clone.contents = None
    clone.people = None
    clone.contents = []
    clone.people = []


def setup_exits():
    for room in merc.rooms.values():
        if room.exit:
            for door, pexit in enumerate(room.exit):
                if pexit:
                    iexit = world_classes.Exit(pexit)
                    room.exit[door] = iexit


def create_shop(shopTemplate, keeper, room):
    shop = world_classes.Shop()
    shop.buy_type = shopTemplate.template_buy_type
    shop.mobTemplate = shopTemplate.template_keeper
    shop.keeper_instance = keeper.instance_id
    shop.room_instance = room.instance_id
    shop.close_hour = shopTemplate.template_close_hour
    shop.open_hour = shopTemplate.template_open_hour
    shop.profit_buy = shopTemplate.template_profit_buy
    shop.profit_sell = shopTemplate.template_profit_sell


def clone_shop(parent, clone, room, keeper):
    clone.buy_type = parent.buy_type
    clone.mobTemplate = parent.keeper
    clone.keeper_instance = keeper.instance_id
    clone.room_instance = room.instance_id
    clone.close_hour = parent.close_hour
    clone.open_hour = parent.open_hour
    clone.profit_buy = parent.profit_buy
    clone.profit_sell = parent.profit_sell


def create_mobile(mobTemplate):
    if mobTemplate is None:
        logger.critical("Create_mobile: None pMobIndex.")
        sys.exit(1)

    mob = mobile.Mobile()
    mob.vnum = mobTemplate.vnum
    handler.Instancer.id_generator(mob)
    mob.name = mobTemplate.name
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
        mob.damroll = mobTemplate.dam_dice[merc.DICE_BONUS]
        mob.max_hit = game_utils.dice(mobTemplate.hit_dice[merc.DICE_NUMBER], mobTemplate.hit_dice[merc.DICE_TYPE]) + mobTemplate.hit_dice[
            merc.DICE_BONUS]
        mob.hit = mob.max_hit
        mob.max_mana = game_utils.dice(mobTemplate.mana_dice[merc.DICE_NUMBER], mobTemplate.mana_dice[merc.DICE_TYPE]) + mobTemplate.mana_dice[
            merc.DICE_BONUS]
        mob.mana = mob.max_mana
        mob.damage[merc.DICE_NUMBER] = mobTemplate.dam_dice[merc.DICE_NUMBER]
        mob.damage[merc.DICE_TYPE] = mobTemplate.dam_dice[merc.DICE_TYPE]
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
            mob.armor[i] = mobTemplate.armor[i]
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
def create_item(item_template, level):
    if not item_template:
        logger.critical("Create_object: No objTemplate.")
        sys.exit(1)

    item = handler_item.Items(item_template)
    item.in_room = None
    item.enchanted = False

    if item_template.new_format is False:
        item.level = max(0, level)

    if level != -1 or not item_template.new_format:
        item.cost = game_utils.number_fuzzy(10) * game_utils.number_fuzzy(level) * game_utils.number_fuzzy(level)

        # Mess with object properties.
    if item.item_type == merc.ITEM_LIGHT:
        if item.value[2] == 999:
            item.value[2] = -1
    elif item.item_type == merc.ITEM_FURNITURE \
            or item.item_type == merc.ITEM_TRASH \
            or item.item_type == merc.ITEM_CONTAINER \
            or item.item_type == merc.ITEM_DRINK_CON \
            or item.item_type == merc.ITEM_KEY \
            or item.item_type == merc.ITEM_FOOD \
            or item.item_type == merc.ITEM_BOAT \
            or item.item_type == merc.ITEM_CORPSE_NPC \
            or item.item_type == merc.ITEM_CORPSE_PC \
            or item.item_type == merc.ITEM_FOUNTAIN \
            or item.item_type == merc.ITEM_MAP \
            or item.item_type == merc.ITEM_CLOTHING \
            or item.item_type == merc.ITEM_PORTAL:
        if not item_template.new_format:
            item.cost //= 5
    elif item.item_type == merc.ITEM_TREASURE \
            or item.item_type == merc.ITEM_WARP_STONE \
            or item.item_type == merc.ITEM_ROOM_KEY \
            or item.item_type == merc.ITEM_GEM \
            or item.item_type == merc.ITEM_JEWELRY:
        pass
    elif item.item_type == merc.ITEM_JUKEBOX:
        item.value = [-1 for i in range(5)]
    elif item.item_type == merc.ITEM_SCROLL:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(item.value[0])
    elif item.item_type == merc.ITEM_WAND \
            or item.item_type == merc.ITEM_STAFF:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(item.value[0])
            item.value[1] = game_utils.number_fuzzy(item.value[1])
            item.value[2] = item.value[1]
        if not item_template.new_format:
            item.cost *= 2
    elif item.item_type == merc.ITEM_WEAPON:
        if level != -1 and not item_template.new_format:
            item.value[1] = game_utils.number_fuzzy(game_utils.number_fuzzy(1 * level // 4 + 2))
            item.value[2] = game_utils.number_fuzzy(game_utils.number_fuzzy(3 * level // 4 + 6))
    elif item.item_type == merc.ITEM_ARMOR:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(level // 5 + 3)
            item.value[1] = game_utils.number_fuzzy(level // 5 + 3)
            item.value[2] = game_utils.number_fuzzy(level // 5 + 3)
    elif item.item_type == merc.ITEM_POTION \
            or item.item_type == merc.ITEM_PILL:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(game_utils.number_fuzzy(item.value[0]))
    elif item.item_type == merc.ITEM_MONEY:
        if not item_template.new_format:
            item.value[0] = item.cost
    else:
        logger.error("Bad item_type objTemplate vnum: %s(%s)" % (item_template.vnum, item.item_type))

    for paf in item_template.affected:
        if paf.location == merc.APPLY_SPELL_AFFECT:
            item.affect_add(paf)
    return item


# duplicate an object exactly -- except contents */
def clone_item(parent, clone):
    if not parent or not clone:
        return

    # start fixing the object */
    clone = handler_item.Items(parent)
    return clone

# * Create a 'money' obj.
def create_money(gold, silver):
    if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
        logger.warn("BUG: Create_money: zero or negative money. %d ", min(gold, silver))
        gold = max(1, gold)
        silver = max(1, silver)

    if gold == 0 and silver == 1:
        item = create_item(merc.itemTemplate[merc.OBJ_VNUM_SILVER_ONE], 0)
    elif gold == 1 and silver == 0:
        item = create_item(merc.itemTemplate[merc.OBJ_VNUM_GOLD_ONE], 0)
    elif silver == 0:
        item = create_item(merc.itemTemplate[merc.OBJ_VNUM_GOLD_SOME], 0)
        item.short_descr += " %d" % gold
        item.value[1] = gold
        item.cost = gold
        item.weight = gold // 5
    elif gold == 0:
        item = create_item(merc.itemTemplate[merc.OBJ_VNUM_SILVER_SOME], 0)
        item.short_descr += " %d" % silver
        item.value[0] = silver
        item.cost = silver
        item.weight = silver // 20
    else:
        item = create_item(merc.itemTemplate[merc.OBJ_VNUM_COINS], 0)
        item.short_descr += " %d %d" % (gold, silver)
        item.value[0] = silver
        item.value[1] = gold
        item.cost = 100 * gold + silver
        item.weight = gold // 5 + silver // 20
    return item

