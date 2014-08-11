__author__ = 'venom'
import merc
import state_checks
import handler_game
import game_utils

# get an object from a shopkeeper's list */
def get_obj_keeper(ch, keeper, argument):
    number, arg = game_utils.number_argument(argument)
    count = 0
    for obj in keeper.contents:
        if obj.wear_loc == merc.WEAR_NONE and keeper.can_see_item(obj) and ch.can_see_item(obj) and game_utils.is_name(arg, obj.name):
            count += 1
            if count == number:
                return obj

    return None

# insert an object at the right spot for the keeper */
def obj_to_keeper(obj, ch):
    # see if any duplicates are found */
    n_obj = None
    spot = -1
    for i, t_obj in enumerate(ch.contents):
        if obj.pIndexData == t_obj.pIndexData \
                and obj.short_descr == t_obj.short_descr:
            # if this is an unlimited item, destroy the new one */
            if state_checks.is_item_stat(t_obj, merc.ITEM_INVENTORY):
                obj.extract()
                return
            obj.cost = t_obj.cost  # keep it standard */
            n_obj = t_obj
            spot = i
            break

    if n_obj is None or spot == -1:
        ch.contents.remove(obj)
    else:
        ch.contents.insert(spot, t_obj)
    obj.in_living = ch
    obj.in_room = None
    obj.in_item = None
    ch.carry_number += obj.get_number()
    ch.carry_weight += obj.get_weight()

def get_cost(keeper, obj, fBuy):
    if not obj or not keeper.pIndexData.pShop:
        return 0
    pShop = keeper.pIndexData.pShop
    if fBuy:
        cost = obj.cost * pShop.profit_buy // 100
    else:
        cost = 0
        for itype in pShop.buy_type:
            if obj.item_type == itype:
                cost = obj.cost * pShop.profit_sell // 100
                break

        if not state_checks.is_item_stat(obj, merc.ITEM_SELL_EXTRACT):
            for obj2 in keeper.contents:
                if obj.pIndexData == obj2.pIndexData and obj.short_descr == obj2.short_descr:
                    if state_checks.is_item_stat(obj2, merc.ITEM_INVENTORY):
                        cost /= 2
                    else:
                        cost = cost * 3 / 4
    if obj.item_type == merc.ITEM_STAFF or obj.item_type == merc.ITEM_WAND:
        if obj.value[1] == 0:
            cost /= 4
        else:
            cost = cost * obj.value[2] / obj.value[1]
    return cost

#* Shopping commands.
def find_keeper(ch):
    pShop = None
    for keeper_id in ch.in_room.people:
        keeper = merc.characters[keeper_id]
        if keeper.is_npc() and keeper.pShop:
            pShop = keeper.pShop
            break
    if not pShop:
        ch.send("You can't do that here.\n")
        return None
    #* Undesirables.
    #if not IS_NPC(ch) and IS_SET(ch.act, PLR_KILLER):
    #    keeper.do_say("Killers are not welcome!")
    #    keeper.do_yell("%s the KILLER is over here!\n" % ch.name)
    #    return None
    #if not IS_NPC(ch) and IS_SET(ch.act, PLR_THIEF):
    #    keeper.do_say("Thieves are not welcome!")
    #    keeper.do_yell("%s the THIEF is over here!\n" % ch.name)
    #    return None
    #* Shop hours.
    if handler_game.time_info.hour < pShop.open_hour:
        keeper.do_say("Sorry, I am closed. Come back later.")
        return None
    if handler_game.time_info.hour > pShop.close_hour:
        keeper.do_say("Sorry, I am closed. Come back tomorrow.")
        return None
    #* Invisible or hidden people.
    if not keeper.can_see(ch):
        keeper.do_say("I don't trade with folks I can't see.")
        return None
    return keeper


