import logging

logger = logging.getLogger()

import game_utils
import shop_utils
import state_checks
import collections
import merc
import handler_room
import interp
import instance


def do_list(ch, argument):
    if state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_PET_SHOP):
        # hack to make new thalos pets work
        pRoomIndexNext = None
        if ch.in_room.vnum == 9621:
            if 9706 in instance.room_templates:
                pRoomIndexNext = handler_room.get_room_by_vnum(9706)
        else:
            if ch.in_room.vnum + 1 in instance.room_templates:
                pRoomIndexNext = handler_room.get_room_by_vnum(ch.in_room.vnum + 1)
        if not pRoomIndexNext:
            logger.warn("BUG: Do_list: bad pet shop at vnum %d.", ch.in_room.vnum)
            ch.send("You can't do that here.\n")
            return
        found = False
        for pet in pRoomIndexNext.people[:]:
            if pet.act.is_set(merc.ACT_PET):
                if not found:
                    found = True
                    ch.send("Pets for sale:\n")
                ch.send("[[%2d]] %8d - %s\n" % (pet.level, 10 * pet.level * pet.level, pet.short_descr))
        if not found:
            ch.send("Sorry, we're out of pets right now.\n")
        return
    else:
        keeper = shop_utils.find_keeper(ch)
        if not keeper:
            return
        argument, arg = game_utils.read_word(argument)
        items = collections.OrderedDict()
        for item_id in keeper.inventory[:]:
            item = instance.items[item_id]
            cost = shop_utils.get_cost(keeper, item, True)
            if not item.equipped_to and ch.can_see_item(item) and cost > 0 \
                    and (not arg or arg in item.name.lower()):
                if item.inventory:
                    items[(item.vnum, item.short_descr)] = (item.vnum, -1)
                else:
                    k = (item.vnum, item.short_descr)
                    if k not in items:
                        items[k] = (item, 1)
                    else:
                        items[k][1] += 1
        if not items:
            ch.send("You can't buy anything here.\n")
            return
        ch.send("[[Lv Price Qty]] Item\n")
        for k, p in items.items():
            item, count = p
            cost = shop_utils.get_cost(keeper, item, True)
            ch.send("[[%2d %5d %2s ]] %s" % (item.level, cost, ("--" if item.flags.shop_inventory else count), item.short_descr))
            if ch.act.is_set(merc.PLR_OMNI):
                ch.send("(%d)" % item.vnum)
            ch.send("\n")


interp.register_command(interp.cmd_type('list', do_list, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
