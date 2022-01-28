import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import const
from rom24 import interp
from rom24 import update
from rom24 import game_utils
from rom24 import handler_game
from rom24 import instance


def do_drink(ch, argument):
    argument, arg = game_utils.read_word(argument)
    obj = None
    if not arg:
        for f_id in ch.in_room.items:
            f = instance.items[f_id]
            if f.item_type == merc.ITEM_FOUNTAIN:
                obj = f
                break
        if not obj:
            ch.send("Drink what?\n")
            return
    else:
        obj = ch.get_item_here(arg)
        if not obj:
            ch.send("You can't find it.\n")
            return

    if not ch.is_npc() and ch.condition[merc.COND_DRUNK] > 10:
        ch.send("You fail to reach your mouth.  *Hic*\n")
        return
    amount = 0
    liquid = -1
    if obj.item_type == merc.ITEM_FOUNTAIN:
        liquid = obj.value[2]
        if liquid < 0:
            logger.warn("BUG: Do_drink: bad liquid number %s.", liquid)
            liquid = obj.value[2] = 0
        amount = const.liq_table[liquid].liq_affect[4] * 3
    elif obj.item_type == merc.ITEM_DRINK_CON:
        if obj.value[1] <= 0:
            ch.send("It is already empty.\n")
            return
        liquid = obj.value[2]
        if not liquid:
            logger.warn("BUG: Do_drink: bad liquid number %s.", liquid)
            liquid = obj.value[2] = 0
        amount = const.liq_table[liquid].liq_affect[4]
        amount = min(amount, obj.value[1])
    else:
        ch.send("You can't drink from that.\n")
        return
    if not ch.is_npc() and not ch.is_immortal() and ch.condition[merc.COND_FULL] > 45:
        ch.send("You're too full to drink more.\n")
        return
    handler_game.act(
        "$n drinks $T from $p.", ch, obj, const.liq_table[liquid].name, merc.TO_ROOM
    )
    handler_game.act(
        "You drink $T from $p.", ch, obj, const.liq_table[liquid].name, merc.TO_CHAR
    )
    update.gain_condition(
        ch, merc.COND_DRUNK, amount * const.liq_table[liquid].proof / 36
    )
    update.gain_condition(ch, merc.COND_FULL, amount * const.liq_table[liquid].full / 4)
    update.gain_condition(
        ch, merc.COND_THIRST, amount * const.liq_table[liquid].thirst / 10
    )
    update.gain_condition(
        ch, merc.COND_HUNGER, amount * const.liq_table[liquid].food / 2
    )
    if not ch.is_npc() and ch.condition[merc.COND_DRUNK] > 10:
        ch.send("You feel drunk.\n")
    if not ch.is_npc() and ch.condition[merc.COND_FULL] > 40:
        ch.send("You are full.\n")
    if not ch.is_npc() and ch.condition[merc.COND_THIRST] > 40:
        ch.send("Your thirst is quenched.\n")
    if obj.value[3] != 0:
        # The drink was poisoned !
        af = handler_game.AFFECT_DATA()
        handler_game.act("$n chokes and gags.", ch, None, None, merc.TO_ROOM)
        ch.send("You choke and gag.\n")
        af.where = merc.TO_AFFECTS
        af.type = "poison"
        af.level = game_utils.number_fuzzy(amount)
        af.duration = 3 * amount
        af.location = merc.APPLY_NONE
        af.modifier = 0
        af.bitvector = merc.AFF_POISON
        ch.affect_join(af)
    if obj.value[0] > 0:
        obj.value[1] -= amount
    return


interp.register_command(
    interp.cmd_type("drink", do_drink, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
