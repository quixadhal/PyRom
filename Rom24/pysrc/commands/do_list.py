import logging

logger = logging.getLogger()

import game_utils
import shop_utils
import state_checks
import collections
import merc
import interp


def do_list(ch, argument):
    if state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_PET_SHOP):
        # hack to make new thalos pets work
        pRoomIndexNext = None
        if merc.rooms[ch.in_room].vnum == 9621:
            if 9706 in merc.roomTemplate:
                pRoomIndexNext = merc.roomTemplate[9706]
        else:
            if merc.rooms[ch.in_room].vnum + 1 in merc.roomTemplate:
                pRoomIndexNext = merc.roomTemplate[ch.in_room.vnum + 1]
        if not pRoomIndexNext:
            logger.warn("BUG: Do_list: bad pet shop at vnum %d.", merc.rooms[ch.in_room].vnum)
            ch.send("You can't do that here.\n")
            return
        found = False
        for pet in pRoomIndexNext.people:
            if state_checks.IS_SET(pet.act, merc.ACT_PET):
                if not found:
                    found = True
                    ch.send("Pets for sale:\n")
                ch.send("[%2d] %8d - %s\n" % (pet.level, 10 * pet.level * pet.level, pet.short_descr))
        if not found:
            ch.send("Sorry, we're out of pets right now.\n")
        return
    else:
        keeper = shop_utils.find_keeper(ch)
        if not keeper:
            return
        argument, arg = game_utils.read_word(argument)
        items = collections.OrderedDict()
        for obj in keeper.contents:
            cost = shop_utils.get_cost(keeper, obj, True)
            if obj.wear_loc == merc.WEAR_NONE and ch.can_see_item(obj) and cost > 0 \
                    and ( not arg or arg in obj.name.lower()):
                if state_checks.is_item_stat(obj, merc.ITEM_INVENTORY):
                    items[(obj.pIndexData, obj.short_descr)] = (obj, -1)
                else:
                    k = (obj.pIndexData, obj.short_descr)
                    if k not in items:
                        items[k] = (obj, 1)
                    else:
                        items[k][1] += 1
        if not items:
            ch.send("You can't buy anything here.\n")
            return
        ch.send("[Lv Price Qty] Item\n")
        for k, p in items.items():
            obj, count = p
            cost = shop_utils.get_cost(keeper, obj, True)
            ch.send("[%2d %5d %2s ] %s" % (obj.level, cost, ("--" if count == -1 else count), obj.short_descr))
            if ch.act.is_set(merc.PLR_OMNI):
                ch.send("(%d)" % obj.pIndexData.vnum)
            ch.send("\n")


interp.register_command(interp.cmd_type('list', do_list, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
