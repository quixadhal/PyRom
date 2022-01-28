__author__ = "syn"

import random
import sys
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_item
from rom24 import handler_room
from rom24 import world_classes
from rom24 import merc
from rom24 import handler_npc
from rom24 import special
from rom24 import state_checks
from rom24 import instance


def create_room(room_template):
    if room_template is None:
        logger.critical("Create_room: No roomTemplate given.")
        sys.exit(1)

    room = handler_room.Room(room_template)
    return room


def clone_room(parent, clone):
    if not parent or not clone:
        return
    """Clone a room, minus contents and exits"""
    clone = handler_room.Room(parent)
    clone.inventory = None
    clone.people = None
    clone.inventory = []
    clone.people = []


def setup_exits():
    for room in instance.rooms.values():
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


def create_mobile(npc_template):
    if npc_template is None:
        logger.critical("Create_mobile: None pMobIndex.")
        sys.exit(1)

    npc = handler_npc.Npc(npc_template)
    npc.id = game_utils.get_mob_id()
    if npc_template.spec_fun:
        npc.spec_fun = special.spec_table[npc_template.spec_fun]
    npc.prompt = None

    if npc_template.wealth == 0:
        npc.silver = 0
        npc.gold = 0
    else:
        wealth = random.randint(npc_template.wealth // 2, 3 * npc_template.wealth // 2)
        npc.gold = random.randint(wealth // 200, wealth // 100)
        npc.silver = wealth - (npc.gold * 100)

    if npc_template.new_format:
        # load in new style */
        # read from prototype */
        # npc.group = npc_template.group
        # npc.act.bits = npc_template.act.bits
        npc.comm.set_bit(merc.COMM_NOCHANNELS | merc.COMM_NOSHOUT | merc.COMM_NOTELL)
        # npc.affected_by.bits = npc_template.affected_by.bits
        # npc.alignment = npc_template.alignment
        # npc.level = npc_template.level
        # npc.hitroll = npc_template.hitroll
        # npc.damroll = npc_template.dam_dice[merc.DICE_BONUS]
        npc.max_hit = (
            game_utils.dice(
                npc_template.hit_dice[merc.DICE_NUMBER],
                npc_template.hit_dice[merc.DICE_TYPE],
            )
            + npc_template.hit_dice[merc.DICE_BONUS]
        )
        npc.hit = npc.max_hit
        npc.max_mana = (
            game_utils.dice(
                npc_template.mana_dice[merc.DICE_NUMBER],
                npc_template.mana_dice[merc.DICE_TYPE],
            )
            + npc_template.mana_dice[merc.DICE_BONUS]
        )
        npc.mana = npc.max_mana
        npc.damage[merc.DICE_NUMBER] = npc_template.dam_dice[merc.DICE_NUMBER]
        npc.damage[merc.DICE_TYPE] = npc_template.dam_dice[merc.DICE_TYPE]
        # npc.dam_type = npc_template.dam_type
        if npc.dam_type == 0:
            num = random.randint(1, 3)
            if num == 1:
                npc.dam_type = 3  # slash */
            elif num == 2:
                npc.dam_type = 7  # pound */
            elif num == 3:
                npc.dam_type = 11  # pierce */
        for i in range(4):
            npc.armor[i] = npc_template.armor[i]
        # npc.off_flags.bits = npc_template.off_flags.bits
        # npc.imm_flags.bits = npc_template.imm_flags.bits
        # npc.res_flags.bits = npc_template.res_flags.bits
        # npc.vuln_flags.bits = npc_template.vuln_flags.bits
        # npc.start_pos = npc_template.start_pos
        # npc.default_pos = npc_template.default_pos
        # npc.sex = npc_template.sex
        if type(npc_template.sex) != int or npc.sex == 3:  # random sex */
            npc.sex = random.randint(1, 2)
        # npc.race = npc_template.race
        # npc.form.bits = npc_template.form.bits
        # npc.parts.bits = npc_template.parts.bits
        # npc.size = int(npc_template.size)
        # npc.material = npc_template.material

        # computed on the spot */
        for i in range(merc.MAX_STATS):
            npc.perm_stat[i] = min(25, 11 + npc.level // 4)

        if npc.act.is_set(merc.ACT_WARRIOR):
            npc.perm_stat[merc.STAT_STR] += 3
            npc.perm_stat[merc.STAT_INT] -= 1
            npc.perm_stat[merc.STAT_CON] += 2

        if npc.act.is_set(merc.ACT_THIEF):
            npc.perm_stat[merc.STAT_DEX] += 3
            npc.perm_stat[merc.STAT_INT] += 1
            npc.perm_stat[merc.STAT_WIS] -= 1

        if npc.act.is_set(merc.ACT_CLERIC):
            npc.perm_stat[merc.STAT_WIS] += 3
            npc.perm_stat[merc.STAT_DEX] -= 1
            npc.perm_stat[merc.STAT_STR] += 1

        if npc.act.is_set(merc.ACT_MAGE):
            npc.perm_stat[merc.STAT_INT] += 3
            npc.perm_stat[merc.STAT_STR] -= 1
            npc.perm_stat[merc.STAT_DEX] += 1

        if npc.is_npc() and npc.off_flags.is_set(merc.OFF_FAST):
            npc.perm_stat[merc.STAT_DEX] += 2

        npc.perm_stat[merc.STAT_STR] += npc.size - merc.SIZE_MEDIUM
        npc.perm_stat[merc.STAT_CON] += (npc.size - merc.SIZE_MEDIUM) // 2
        af = handler_game.AFFECT_DATA()
        # let's get some spell action */
        if npc.is_affected(merc.AFF_SANCTUARY):
            af.where = merc.TO_AFFECTS
            af.type = "sanctuary"
            af.level = npc.level
            af.duration = -1
            af.location = merc.APPLY_NONE
            af.modifier = 0
            af.bitvector = merc.AFF_SANCTUARY
            npc.affect_add(af)

        if npc.is_affected(merc.AFF_HASTE):
            af.where = merc.TO_AFFECTS
            af.type = "haste"
            af.level = npc.level
            af.duration = -1
            af.location = merc.APPLY_DEX
            af.modifier = 1 + (npc.level >= 18) + (npc.level >= 25) + (npc.level >= 32)
            af.bitvector = merc.AFF_HASTE
            npc.affect_add(af)

        if npc.is_affected(merc.AFF_PROTECT_EVIL):
            af.where = merc.TO_AFFECTS
            af.type = "protection evil"
            af.level = npc.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_EVIL
            npc.affect_add(af)

        if npc.is_affected(merc.AFF_PROTECT_GOOD):
            af.where = merc.TO_AFFECTS
            af.type = "protection good"
            af.level = npc.level
            af.duration = -1
            af.location = merc.APPLY_SAVES
            af.modifier = -1
            af.bitvector = merc.AFF_PROTECT_GOOD
            npc.affect_add(af)
    else:  # read in old format and convert */
        # npc.act.bits = npc_template.act.bits
        # npc.affected_by.bits = npc_template.affected_by.bits
        # npc.alignment = npc_template.alignment
        # npc.level = npc_template.level
        # npc.hitroll = npc_template.hitroll
        npc.damroll = 0
        npc.max_hit = npc.level * 8 + random.randint(
            npc.level * npc.level // 4, npc.level * npc.level
        )
        npc.max_hit *= 0.9
        npc.hit = npc.max_hit
        npc.max_mana = 100 + game_utils.dice(npc.level, 10)
        npc.mana = npc.max_mana
        num = random.randint(1, 3)
        if num == 1:
            npc.dam_type = 3  # slash */
        elif num == 2:
            npc.dam_type = 7  # pound */
        elif num == 3:
            npc.dam_type = 11  # pierce */
        for i in range(3):
            npc.armor[i] = game_utils.interpolate(npc.level, 100, -100)
        npc.armor[3] = game_utils.interpolate(npc.level, 100, 0)
        # npc.race = npc_template.race
        # npc.off_flags.bits = npc_template.off_flags.bits
        # npc.imm_flags.bits = npc_template.imm_flags.bits
        # npc.res_flags.bits = npc_template.res_flags.bits
        # npc.vuln_flags.bits = npc_template.vuln_flags.bits
        # npc.start_pos = npc_template.start_pos
        # npc.default_pos = npc_template.default_pos
        # npc.sex = npc_template.sex
        # npc.form.bits = npc_template.form.bits
        # npc.parts.bits = npc_template.parts.bits
        npc.size = merc.SIZE_MEDIUM
        npc.material = ""

        for i in merc.MAX_STATS:
            npc.perm_stat[i] = 11 + npc.level // 4
    npc.position = npc.start_pos

    # link the mob to the world list */
    return npc


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
def create_item(item_template, level, prev_instance_id: int = None):
    if not item_template:
        logger.critical("Create_object: No objTemplate.")
        sys.exit(1)

    item = handler_item.Items(item_template)
    if not prev_instance_id:
        pass  # item.instancer()
    else:
        item.instance_id = prev_instance_id
    # item.instance_setup()
    # item.enchanted = False

    if item_template.new_format is False:
        item.level = max(0, level)

    if level == -1 or not item_template.new_format:
        item.cost = (
            game_utils.number_fuzzy(10)
            * game_utils.number_fuzzy(level)
            * game_utils.number_fuzzy(level)
        )

        # Mess with object properties.
    if item.item_type == merc.ITEM_LIGHT:
        if item.value[2] == 999:
            item.value[2] = -1
    elif (
        item.item_type == merc.ITEM_FURNITURE
        or item.item_type == merc.ITEM_TRASH
        or item.item_type == merc.ITEM_CONTAINER
        or item.item_type == merc.ITEM_DRINK_CON
        or item.item_type == merc.ITEM_KEY
        or item.item_type == merc.ITEM_FOOD
        or item.item_type == merc.ITEM_BOAT
        or item.item_type == merc.ITEM_CORPSE_NPC
        or item.item_type == merc.ITEM_CORPSE_PC
        or item.item_type == merc.ITEM_FOUNTAIN
        or item.item_type == merc.ITEM_MAP
        or item.item_type == merc.ITEM_CLOTHING
        or item.item_type == merc.ITEM_PORTAL
    ):
        if not item_template.new_format:
            item.cost //= 5
    elif (
        item.item_type == merc.ITEM_TREASURE
        or item.item_type == merc.ITEM_WARP_STONE
        or item.item_type == merc.ITEM_ROOM_KEY
        or item.item_type == merc.ITEM_GEM
        or item.item_type == merc.ITEM_JEWELRY
    ):
        pass
    elif item.item_type == merc.ITEM_JUKEBOX:
        item.value = [-1 for i in range(5)]
    elif item.item_type == merc.ITEM_SCROLL:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(item.value[0])
    elif item.item_type == merc.ITEM_WAND or item.item_type == merc.ITEM_STAFF:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(item.value[0])
            item.value[1] = game_utils.number_fuzzy(item.value[1])
            item.value[2] = item.value[1]
        if not item_template.new_format:
            item.cost *= 2
    elif item.item_type == merc.ITEM_WEAPON:
        if level != -1 and not item_template.new_format:
            item.value[1] = game_utils.number_fuzzy(
                game_utils.number_fuzzy(1 * level // 4 + 2)
            )
            item.value[2] = game_utils.number_fuzzy(
                game_utils.number_fuzzy(3 * level // 4 + 6)
            )
    elif item.item_type == merc.ITEM_ARMOR:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(level // 5 + 3)
            item.value[1] = game_utils.number_fuzzy(level // 5 + 3)
            item.value[2] = game_utils.number_fuzzy(level // 5 + 3)
    elif item.item_type == merc.ITEM_POTION or item.item_type == merc.ITEM_PILL:
        if level != -1 and not item_template.new_format:
            item.value[0] = game_utils.number_fuzzy(
                game_utils.number_fuzzy(item.value[0])
            )
    elif item.item_type == merc.ITEM_MONEY:
        if not item_template.new_format:
            item.value[0] = item.cost
    else:
        logger.error(
            "Bad item_type objTemplate vnum: %s(%s)"
            % (item_template.vnum, item.item_type)
        )

    # for paf in item_template.affected:
    #   if paf.location == merc.APPLY_SPELL_AFFECT:
    #      item.affect_add(paf)
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
        item = create_item(instance.item_templates[merc.OBJ_VNUM_SILVER_ONE], 0)
    elif gold == 1 and silver == 0:
        item = create_item(instance.item_templates[merc.OBJ_VNUM_GOLD_ONE], 0)
    elif silver == 0:
        item = create_item(instance.item_templates[merc.OBJ_VNUM_GOLD_SOME], 0)
        item.short_descr = item.short_descr % gold
        item.value[1] = gold
        item.cost = gold
        item.weight = gold // 5
    elif gold == 0:
        item = create_item(instance.item_templates[merc.OBJ_VNUM_SILVER_SOME], 0)
        item.short_descr = item.short_descr % silver
        item.value[0] = silver
        item.cost = silver
        item.weight = silver // 20
    else:
        item = create_item(instance.item_templates[merc.OBJ_VNUM_COINS], 0)
        item.short_descr = item.short_descr % (gold, silver)
        item.value[0] = silver
        item.value[1] = gold
        item.cost = 100 * gold + silver
        item.weight = gold // 5 + silver // 20
    return item
