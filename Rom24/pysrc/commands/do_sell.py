import logging

import game_utils
import shop_utils
import state_checks


logger = logging.getLogger()

import random
import merc
import interp


def do_sell(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Sell what?\n")
        return
    keeper = shop_utils.find_keeper(ch)
    if not keeper:
        return
    obj = ch.get_item_carry(arg, ch)
    if not obj:
        act("$n tells you 'You don't have that item'.", keeper, None, ch, merc.TO_VICT)
        ch.reply = keeper
        return
    if not ch.can_drop_item(obj):
        ch.send("You can't let go of it.\n")
        return
    if not keeper.can_see_item(obj):
        act("$n doesn't see what you are offering.", keeper, None, ch, merc.TO_VICT)
        return
    cost = shop_utils.get_cost(keeper, obj, False)
    if cost <= 0:
        act("$n looks uninterested in $p.", keeper, obj, ch, merc.TO_VICT)
        return
    if cost > (keeper.silver + 100 * keeper.gold):
        act("$n tells you 'I'm afraid I don't have enough wealth to buy $p.", keeper, obj, ch,
                         merc.TO_VICT)
        return
    act("$n sells $p.", ch, obj, None, merc.TO_ROOM)
    # haggle
    roll = random.randint(1, 99)
    if not state_checks.is_item_stat(obj, merc.ITEM_SELL_EXTRACT) and roll < ch.get_skill("haggle"):
        ch.send("You haggle with the shopkeeper.\n")
        cost += obj.cost // 2 * roll // 100
        cost = min(cost, 95 * shop_utils.get_cost(keeper, obj, True) // 100)
        cost = min(cost, (keeper.silver + 100 * keeper.gold))
        ch.check_improve( "haggle", True, 4)
    act("You sell $p for %d silver and %d gold piece%s." % (
        cost - (cost // 100) * 100, cost // 100, ("" if cost == 1 else "s")), ch, obj, None, merc.TO_CHAR)
    ch.gold += cost // 100
    ch.silver += cost - (cost // 100) * 100

    keeper.deduct_cost(cost)
    if keeper.gold < 0:
        keeper.gold = 0
    if keeper.silver < 0:
        keeper.silver = 0
    if obj.item_type == merc.ITEM_TRASH or state_checks.is_item_stat(obj, merc.ITEM_SELL_EXTRACT):
        obj.extract()
    else:
        obj.from_char()
        if obj.timer:
            obj.extra_flags = state_checks.SET_BIT(obj.extra_flags, merc.ITEM_HAD_TIMER)
        else:
            obj.timer = random.randint(50, 100)
        shop_utils.obj_to_keeper(obj, keeper)
    return


interp.register_command(interp.cmd_type('sell', do_sell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
