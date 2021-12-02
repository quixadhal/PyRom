import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_room
from rom24 import interp
from rom24 import object_creator
from rom24 import shop_utils
from rom24 import state_checks
from rom24 import instance


def do_buy(ch, argument):
    if not argument:
        ch.send("Buy what?\n")
        return
    if state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_PET_SHOP):
        if ch.is_npc():
            return
        argument, arg = merc.read_word(argument)
        pRoomIndexNext = None
        # hack to make new thalos pets work
        if ch.in_room.vnum == 9621:
            if 9706 in instance.room_templates:
                pRoomIndexNext = handler_room.get_room_by_vnum(9706)
        else:
            if ch.in_room.vnum + 1 in instance.room_templates:
                pRoomIndexNext = handler_room.get_room_by_vnum(ch.in_room.vnum + 1)
        if not pRoomIndexNext:
            logger.warn("BUG: Do_buy: bad pet shop at vnum %d.", ch.in_room.vnum)
            ch.send("Sorry, you can't buy that here.\n")
            return
        in_room = ch.in_room
        ch.in_environment = pRoomIndexNext
        pet = ch.get_char_room(arg)
        ch.in_environment = in_room

        if not pet or not state_checks.IS_SET(pet.act, handler_game.act_PET):
            ch.send("Sorry, you can't buy that here.\n")
            return
        if ch.pet:
            ch.send("You already own a pet.\n")
            return
        cost = 10 * pet.level * pet.level

        if (ch.silver + 100 * ch.gold) < cost:
            ch.send("You can't afford it.\n")
            return
        if ch.level < pet.level:
            ch.send("You're not powerful enough to master this pet.\n")
            return
        # haggle
        roll = random.randint(1, 99)
        if roll < ch.get_skill("haggle"):
            cost -= cost // 2 * roll // 100
            ch.send("You haggle the price down to %d coins.\n" % cost)
            if ch.is_pc:
                ch.check_improve("haggle", True, 4)
        ch.deduct_cost(cost)
        pet = object_creator.create_mobile(pet.pIndexData)
        pet.act = state_checks.SET_BIT(pet.act, handler_game.act_PET)
        pet.affected_by = state_checks.SET_BIT(pet.affected_by, merc.AFF_CHARM)
        pet.comm = merc.COMM_NOTELL | merc.COMM_NOSHOUT | merc.COMM_NOCHANNELS

        argument, arg = merc.read_word(argument)
        if arg:
            pet.name = "%s %s" % (pet.name, arg)
        pet.description = "%sA neck tag says 'I belong to %s'.\n" % (
            pet.description,
            ch.name,
        )
        pet.put(ch.in_room)
        merc.add_follower(pet, ch)
        pet.leader = ch
        ch.pet = pet
        ch.send("Enjoy your pet.\n")
        handler_game.act("$n bought $N as a pet.", ch, None, pet, merc.TO_ROOM)
        return
    else:
        keeper = shop_utils.find_keeper(ch)
        if not keeper:
            return
        number, arg = game_utils.number_argument(argument)
        # TODO: Allow multiple purchase arguments.
        # number = 1
        # number, arg = merc.mult_argument(argument)
        obj = shop_utils.get_obj_keeper(ch, keeper, arg)
        cost = shop_utils.get_cost(keeper, obj, True)
        if number < 1 or number > 99:
            handler_game.act("$n tells you 'Get real!", keeper, None, ch, merc.TO_VICT)
            return
        if cost <= 0 or not ch.can_see_item(obj):
            handler_game.act(
                "$n tells you 'I don't sell that -- try 'list''.",
                keeper,
                None,
                ch,
                merc.TO_VICT,
            )
            ch.reply = keeper
            return
        items = []
        if not obj.flags.shop_inventory:
            count = 0
            for t_obj_id in keeper.inventory[:]:
                t_obj = instance.items[t_obj_id]
                if t_obj.vnum == obj.vnum and t_obj.short_descr == obj.short_descr:
                    items.append(t_obj)
                    count += 1
            if count < number:
                handler_game.act(
                    "$n tells you 'I don't have that many in stock.",
                    keeper,
                    None,
                    ch,
                    merc.TO_VICT,
                )
                ch.reply = keeper
                return
        if (ch.silver + ch.gold * 100) < cost * number:
            if number > 1:
                handler_game.act(
                    "$n tells you 'You can't afford to buy that many.",
                    keeper,
                    obj,
                    ch,
                    merc.TO_VICT,
                )
            else:
                handler_game.act(
                    "$n tells you 'You can't afford to buy $p'.",
                    keeper,
                    obj,
                    ch,
                    merc.TO_VICT,
                )
            ch.reply = keeper
            return
        if obj.level > ch.level:
            handler_game.act(
                "$n tells you 'You can't use $p yet'.", keeper, obj, ch, merc.TO_VICT
            )
            ch.reply = keeper
            return
        if ch.carry_number + number * obj.get_number() > ch.can_carry_n():
            ch.send("You can't carry that many items.\n")
            return
        if ch.carry_weight + number * obj.get_weight() > ch.can_carry_w():
            ch.send("You can't carry that much weight.\n")
            return
        # haggle
        roll = random.randint(1, 99)
        if not obj.flags.sell_extract and roll < ch.get_skill("haggle"):
            cost -= obj.cost // 2 * roll // 100
            handler_game.act("You haggle with $N.", ch, None, keeper, merc.TO_CHAR)
            if ch.is_pc:
                ch.check_improve("haggle", True, 4)

        if number > 1:
            handler_game.act("$n buys $p[[%d]]." % number, ch, obj, None, merc.TO_ROOM)
            handler_game.act(
                "You buy $p[[%d]] for %d silver." % (number, cost * number),
                ch,
                obj,
                None,
                merc.TO_CHAR,
            )
        else:
            handler_game.act("$n buys $p.", ch, obj, None, merc.TO_ROOM)
            handler_game.act(
                "You buy $p for %d silver." % cost, ch, obj, None, merc.TO_CHAR
            )

        ch.deduct_cost(cost * number)
        keeper.gold += cost * number / 100
        keeper.silver += cost * number - (cost * number / 100) * 100
        t_obj = None
        if obj.flags.shop_inventory:
            items = []
            for count in range(number):
                t_obj = object_creator.create_item(
                    instance.item_templates[obj.vnum], obj.level
                )
                items.append(t_obj)
        for t_obj in items[:]:
            if not obj.flags.shop_inventory:
                t_obj.in_living.get(t_obj)

            if t_obj.timer > 0 and not t_obj.had_timer:
                t_obj.timer = 0
            t_obj.extra_flags = t_obj.had_timer = False
            ch.put(t_obj)
            if cost < t_obj.cost:
                t_obj.cost = cost


interp.register_command(
    interp.cmd_type("buy", do_buy, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
