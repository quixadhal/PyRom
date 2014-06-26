import merc
import interp
import skills
import db


def do_buy(ch, argument):
    if not argument:
        ch.send("Buy what?\n")
        return
    if merc.IS_SET(ch.in_room.room_flags, merc.ROOM_PET_SHOP):
        if merc.IS_NPC(ch):
            return
        argument, arg = merc.read_word(argument)
        pRoomIndexNext = None
  # hack to make new thalos pets work */
        if ch.in_room.vnum == 9621:
            if 9706 in merc.room_index_hash:
                pRoomIndexNext = merc.room_index_hash[9706]
        else:
            if ch.in_room.vnum+1 in merc.room_index_hash:
                pRoomIndexNext = merc.room_index_hash[ch.in_room.vnum+1]
        if not pRoomIndexNext:
            print("BUG: Do_buy: bad pet shop at vnum %d." % ch.in_room.vnum)
            ch.send("Sorry, you can't buy that here.\n")
            return
        in_room = ch.in_room
        ch.in_room = pRoomIndexNext
        pet = ch.get_char_room(arg)
        ch.in_room = in_room

        if not pet or not merc.IS_SET(pet.act, merc.ACT_PET):
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
        # haggle */
        roll = random.randint(1,99)
        if roll < ch.get_skill("haggle"):
            cost -= cost // 2 * roll // 100
            ch.send("You haggle the price down to %d coins.\n" % cost)
            skills.check_improve(ch,"haggle",True,4)
        ch.deduct_cost(cost)
        pet = db.create_mobile(pet.pIndexData)
        pet.act = merc.SET_BIT(pet.act, merc.ACT_PET)
        pet.affected_by = merc.SET_BIT(pet.affected_by, merc.AFF_CHARM)
        pet.comm = merc.COMM_NOTELL|merc.COMM_NOSHOUT|merc.COMM_NOCHANNELS

        argument, arg = merc.read_word(argument)
        if arg:
            pet.name = "%s %s" % (pet.name, arg)
        pet.description = "%sA neck tag says 'I belong to %s'.\n" % (pet.description, ch.name)
        pet.to_room(ch.in_room)
        merc.add_follower(pet, ch)
        pet.leader = ch
        ch.pet = pet
        ch.send("Enjoy your pet.\n")
        merc.act("$n bought $N as a pet.", ch, None, pet, merc.TO_ROOM)
        return
    else:
        keeper = merc.find_keeper(ch)
        if not keeper:
            return
        number, arg = merc.mult_argument(argument)
        obj = merc.get_obj_keeper(ch, keeper, arg)
        cost = merc.get_cost(keeper, obj, True)
        if number < 1 or number > 99:
            merc.act("$n tells you 'Get real!", keeper, None, ch, merc.TO_VICT)
            return
        if cost <= 0 or not ch.can_see_obj(obj):
            merc.act("$n tells you 'I don't sell that -- try 'list''.", keeper, None, ch, merc.TO_VICT)
            ch.reply = keeper
            return
        items = None
        if not merc.IS_OBJ_STAT(obj, merc.ITEM_INVENTORY):
            items = [t_obj for t_obj in keeper.carrying if t_obj.pIndexData == obj.pIndexData and t_obj.short_descr == obj.short_descr][:number]
            count = len(items)
            if count < number:
                merc.act("$n tells you 'I don't have that many in stock.", keeper, None, ch, merc.TO_VICT)
                ch.reply = keeper
                return
        if (ch.silver + ch.gold * 100) < cost * number:
            if number > 1:
                merc.act("$n tells you 'You can't afford to buy that many.", keeper, obj, ch, merc.TO_VICT)
            else:
                merc.act("$n tells you 'You can't afford to buy $p'.", keeper, obj, ch, merc.TO_VICT)
            ch.reply = keeper
            return
        if obj.level > ch.level:
            merc.act( "$n tells you 'You can't use $p yet'.", keeper, obj, ch, merc.TO_VICT)
            ch.reply = keeper
            return
        if ch.carry_number +  number * obj.get_number() > ch.can_carry_n():
            ch.send("You can't carry that many items.\n")
            return
        if ch.carry_weight + number * obj.get_weight() > ch.can_carry_w():
            ch.send("You can't carry that much weight.\n")
            return
        # haggle */
        roll = random.randint(1,99)
        if not merc.IS_OBJ_STAT(obj, merc.ITEM_SELL_EXTRACT) and roll < ch.get_skill("haggle"):
            cost -= obj.cost // 2 * roll // 100
            merc.act("You haggle with $N.",ch,None,keeper, merc.TO_CHAR)
            skills.check_improve(ch, "haggle", True, 4)

        if number > 1:
            merc.act("$n buys $p[%d]." % number,ch,obj,None, merc.TO_ROOM)
            merc.act("You buy $p[%d] for %d silver." % (number,cost * number),ch,obj,None, merc.TO_CHAR)
        else:
            merc.act("$n buys $p.", ch, obj, None, merc.TO_ROOM )
            merc.act("You buy $p for %d silver." % cost, ch, obj, None, merc.TO_CHAR)

        ch.deduct_cost(cost * number)
        keeper.gold += cost * number/100
        keeper.silver += cost * number - (cost * number/100) * 100
        t_obj = None
        if merc.IS_SET(obj.extra_flags, merc.ITEM_INVENTORY):
            items = []
            for count in range(number):
                t_obj = db.create_object(obj.pIndexData, obj.level)
                items.append(t_obj)
        for t_obj in items[:]:
            if not merc.IS_SET(obj.extra_flags, merc.ITEM_INVENTORY):
                t_obj.from_char()

            if t_obj.timer > 0 and not merc.IS_OBJ_STAT(t_obj, merc.ITEM_HAD_TIMER):
                t_obj.timer = 0
            t_obj.extra_flags = merc.REMOVE_BIT(t_obj.extra_flags, merc.ITEM_HAD_TIMER)
            t_obj.to_char(ch)
            if cost < t_obj.cost:
                t_obj.cost = cost

interp.cmd_table['buy'] = interp.cmd_type('buy', do_buy, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)