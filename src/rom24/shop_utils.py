__author__ = "syn"
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import game_utils
from rom24 import instance


# get an object from a shopkeeper's list */
def get_obj_keeper(ch, keeper, argument):
    number, arg = game_utils.number_argument(argument)
    count = 0
    for obj_id in keeper.inventory[:]:
        obj = instance.items[obj_id]
        if (
            not obj.equipped_to
            and keeper.can_see_item(obj)
            and ch.can_see_item(obj)
            and game_utils.is_name(arg, obj.name)
        ):
            count += 1
            if count == number:
                return obj

    return None


# insert an object at the right spot for the keeper */
def obj_to_keeper(item, ch):
    # see if any duplicates are found */
    n_item = None
    spot = -1
    for i, t_item_id in enumerate(ch.inventory):
        t_item = instance.items[t_item_id]
        if item.vnum == t_item.vnum and item.short_descr == t_item.short_descr:
            # if this is an unlimited item, destroy the new one */
            if t_item.inventory:
                item.extract()
                return
            item.cost = t_item.cost  # keep it standard */
            n_item = t_item
            spot = i
            break

    if n_item is None or spot == -1:
        ch.inventory.remove(item)
    else:
        ch.inventory.insert(spot, t_item)
    item.environment.instance_id = ch.instance_id
    item.in_room = None
    item.in_item = None
    ch.carry_number += item.get_number()
    ch.carry_weight += item.get_weight()


def get_cost(keeper, item, fBuy):
    if not item or not instance.npc_templates[keeper.vnum].pShop:
        return 0
    pShop = instance.npc_templates[keeper.vnum].pShop
    if fBuy:
        cost = item.cost * pShop.profit_buy // 100
    else:
        cost = 0
        for itype in pShop.buy_type:
            if item.item_type == itype:
                cost = item.cost * pShop.profit_sell // 100
                break

        if not item.sell_extract:
            for item2_id in keeper.inventory[:]:
                item2 = instance.items[item2_id]
                if (
                    item.vnum == item2_id.vnum
                    and item.short_descr == item2_id.short_descr
                ):
                    if item.inventory:
                        cost /= 2
                    else:
                        cost = cost * 3 / 4
    if item.item_type == merc.ITEM_STAFF or item.item_type == merc.ITEM_WAND:
        if item.value[1] == 0:
            cost /= 4
        else:
            cost = cost * item.value[2] / item.value[1]
    return cost


# * Shopping commands.
def find_keeper(ch):
    pShop = None
    for keeper_id in ch.in_room.people[:]:
        keeper = instance.characters[keeper_id]
        keeperTemplate = instance.npc_templates[keeper.vnum]
        if keeper.is_npc() and keeperTemplate.pShop:
            pShop = keeperTemplate.pShop
            break
    if not pShop:
        ch.send("You can't do that here.\n")
        return None
    # * Undesirables.
    # if not IS_NPC(ch) and IS_SET(ch.act, PLR_KILLER):
    #    keeper.do_say("Killers are not welcome!")
    #    keeper.do_yell("%s the KILLER is over here!\n" % ch.name)
    #    return None
    # if not IS_NPC(ch) and IS_SET(ch.act, PLR_THIEF):
    #    keeper.do_say("Thieves are not welcome!")
    #    keeper.do_yell("%s the THIEF is over here!\n" % ch.name)
    #    return None
    # * Shop hours.
    if handler_game.time_info.hour < pShop.open_hour:
        keeper.do_say("Sorry, I am closed. Come back later.")
        return None
    if handler_game.time_info.hour > pShop.close_hour:
        keeper.do_say("Sorry, I am closed. Come back tomorrow.")
        return None
    # * Invisible or hidden people.
    if not keeper.can_see(ch):
        keeper.do_say("I don't trade with folks I can't see.")
        return None
    return keeper
