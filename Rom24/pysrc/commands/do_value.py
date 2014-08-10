import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import shop_utils


def do_value(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Value what?\n")
        return
    keeper = shop_utils.find_keeper(ch)
    if not keeper:
        return
    obj = ch.get_item_carry(arg, ch)
    if not obj:
        handler_game.act("$n tells you 'You don't have that item'.", keeper, None, ch, merc.TO_VICT)
        ch.reply = keeper
        return
    if not keeper.can_see_item(obj):
        handler_game.act("$n doesn't see what you are offering.",keeper,None,ch, merc.TO_VICT)
        return
    if not ch.can_drop_item(obj):
        ch.send("You can't let go of it.\n")
        return
    cost = shop_utils.get_cost(keeper, obj, False)
    if cost <= 0:
        handler_game.act( "$n looks uninterested in $p.", keeper, obj, ch, merc.TO_VICT)
        return
    handler_game.act("$n tells you 'I'll give you %d silver and %d gold coins for $p'." % (cost - (cost//100) * 100, cost//100),
      keeper, obj, ch, merc.TO_VICT)
    ch.reply = keeper
    return


interp.register_command(interp.cmd_type('value', do_value, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
