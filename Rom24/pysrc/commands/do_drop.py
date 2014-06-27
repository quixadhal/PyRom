import merc
import interp


def do_drop(ch, argument):
    found = False
    argument, arg = merc.read_word(argument)

    if not arg:
        ch.send("Drop what?\n")
        return
    if arg.isdigit():
        # 'drop NNNN coins' */
        gold = 0
        silver = 0
        amount   = int(arg)
        argument, arg  = merc.read_word(argument)
        if amount <= 0 or ( arg != "coins" and arg != "coin" and arg != "gold" and arg != "silver"):
            ch.send("Sorry, you can't do that.\n")
            return
        if arg == "coins" or arg == "coin" or arg == "silver":
            if ch.silver < amount:
                ch.send("You don't have that much silver.\n")
                return
            ch.silver -= amount
            silver = amount
        else:
            if ch.gold < amount:
                ch.send("You don't have that much gold.\n")
                return
            ch.gold -= amount
            gold = amount
        for obj in ch.in_room.contents[:]:
            if obj.pIndexData.vnum == merc.OBJ_VNUM_SILVER_ONE:
                silver += 1
                obj.extract()
            elif obj.pIndexData.vnum == merc.OBJ_VNUM_GOLD_ONE:
                gold += 1
                obj.extract()
            elif obj.pIndexData.vnum == merc.OBJ_VNUM_SILVER_SOME:
                silver += obj.value[0]
                obj.extract()
            elif obj.pIndexData.vnum == merc.OBJ_VNUM_GOLD_SOME:
                gold += obj.value[1]
                obj.extract()
            elif obj.pIndexData.vnum == merc.OBJ_VNUM_COINS:
                silver += obj.value[0]
                gold += obj.value[1]
                obj.extract()
        db.create_money(gold, silver).to_room(ch.in_room)
        merc.act( "$n drops some coins.", ch, None, None, merc.TO_ROOM )
        ch.send("OK.\n")
        return
    if not arg.startswith("all"):
        # 'drop obj' */
        obj = ch.get_obj_carry(arg, ch)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        if not ch.can_drop_obj(obj):
            ch.send("You can't let go of it.\n")
            return
        obj.from_char()
        obj.to_room(ch.in_room)
        merc.act("$n drops $p.", ch, obj, None, merc.TO_ROOM)
        merc.act("You drop $p.", ch, obj, None, merc.TO_CHAR)
        if merc.IS_OBJ_STAT(obj, merc.ITEM_MELT_DROP):
            merc.act("$p dissolves into smoke.", ch, obj, None, merc.TO_ROOM)
            merc.act("$p dissolves into smoke.", ch, obj, None, merc.TO_CHAR)
            obj.extract()
    else:
        # 'drop all' or 'drop all.obj' */
        found = False
        for obj in ch.carrying[:]:
            if (len(arg) == 3 or arg[4:] in obj.name) \
            and ch.can_see_obj(obj) \
            and obj.wear_loc == merc.WEAR_NONE \
            and ch.can_drop_obj(obj):
                found = True
                obj.from_char()
                obj.to_room(ch.in_room)
                merc.act("$n drops $p.", ch, obj, None, merc.TO_ROOM)
                merc.act("You drop $p.", ch, obj, None, merc.TO_CHAR)
                if merc.IS_OBJ_STAT(obj, merc.ITEM_MELT_DROP):
                    merc.act("$p dissolves into smoke.", ch, obj, None, merc.TO_ROOM)
                    merc.act("$p dissolves into smoke.", ch, obj, None, merc.TO_CHAR)
                    obj.extract()
        if not found:
            if arg == 'all':
                merc.act("You are not carrying anything.", ch, None, arg, merc.TO_CHAR)
            else:
                merc.act("You are not carrying any $T.", ch, None, arg[4:], merc.TO_CHAR)

interp.cmd_type('drop', do_drop, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)