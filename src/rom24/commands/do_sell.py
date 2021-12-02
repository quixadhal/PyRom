import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import handler_game
from rom24 import shop_utils


def do_sell(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Sell what?\n")
        return
    keeper = shop_utils.find_keeper(ch)
    if not keeper:
        return
    item = ch.get_item_carry(arg, ch)
    if not item:
        handler_game.act(
            "$n tells you 'You don't have that item'.", keeper, None, ch, merc.TO_VICT
        )
        ch.reply = keeper
        return
    if not ch.can_drop_item(item):
        ch.send("You can't let go of it.\n")
        return
    if not keeper.can_see_item(item):
        handler_game.act(
            "$n doesn't see what you are offering.", keeper, None, ch, merc.TO_VICT
        )
        return
    cost = shop_utils.get_cost(keeper, item, False)
    if cost <= 0:
        handler_game.act("$n looks uninterested in $p.", keeper, item, ch, merc.TO_VICT)
        return
    if cost > (keeper.silver + 100 * keeper.gold):
        handler_game.act(
            "$n tells you 'I'm afraid I don't have enough wealth to buy $p.",
            keeper,
            item,
            ch,
            merc.TO_VICT,
        )
        return
    handler_game.act("$n sells $p.", ch, item, None, merc.TO_ROOM)
    # haggle
    roll = random.randint(1, 99)
    if not item.sell_extract and roll < ch.get_skill("haggle"):
        ch.send("You haggle with the shopkeeper.\n")
        cost += item.cost // 2 * roll // 100
        cost = min(cost, 95 * shop_utils.get_cost(keeper, item, True) // 100)
        cost = min(cost, (keeper.silver + 100 * keeper.gold))
        if ch.is_pc:
            ch.check_improve("haggle", True, 4)
    handler_game.act(
        "You sell $p for %d silver and %d gold piece%s."
        % (cost - (cost // 100) * 100, cost // 100, ("" if cost == 1 else "s")),
        ch,
        item,
        None,
        merc.TO_CHAR,
    )
    ch.gold += cost // 100
    ch.silver += cost - (cost // 100) * 100

    keeper.deduct_cost(cost)
    if keeper.gold < 0:
        keeper.gold = 0
    if keeper.silver < 0:
        keeper.silver = 0
    if item.item_type == merc.ITEM_TRASH or item.sell_extract:
        item.extract()
    else:
        item.get()
        if item.timer:
            item.flags.had_timer = True
        else:
            item.timer = random.randint(50, 100)
        shop_utils.obj_to_keeper(item, keeper)
    return


interp.register_command(
    interp.cmd_type("sell", do_sell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
