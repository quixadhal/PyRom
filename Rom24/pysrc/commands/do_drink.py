import merc
import const
import interp
import update


def do_drink(ch, argument):
    argument, arg = merc.read_word(argument)
    obj = None
    if not arg:
        obj = [f for f in ch.in_room.contents if f.item_type == merc.ITEM_FOUNTAIN][:1]
        if obj:
            obj = obj[0]
        if not obj:
            ch.send("Drink what?\n")
            return
    else:
        obj = ch.get_obj_here(arg)
        if not obj:
            ch.send("You can't find it.\n")
            return

    if not merc.IS_NPC(ch) and ch.pcdata.condition[merc.COND_DRUNK] > 10:
        ch.send("You fail to reach your mouth.  *Hic*\n")
        return
    amount = 0
    liquid = -1
    if obj.item_type == merc.ITEM_FOUNTAIN:
        liquid = obj.value[2]
        if liquid < 0:
            print("BUG: Do_drink: bad liquid number %s." % liquid)
            liquid = obj.value[2] = 0
        amount = const.liq_table[liquid].liq_affect[4] * 3
    elif obj.item_type == merc.ITEM_DRINK_CON:
        if obj.value[1] <= 0:
            ch.send("It is already empty.\n")
            return
        liquid = obj.value[2]
        if liquid < 0:
            print("BUG: Do_drink: bad liquid number %s." % liquid)
            liquid = obj.value[2] = 0
        amount = const.liq_table[liquid].liq_affect[4]
        amount = min(amount, obj.value[1])
    else:
        ch.send("You can't drink from that.\n")
        return
    if not merc.IS_NPC(ch) and not merc.IS_IMMORTAL(ch) and ch.pcdata.condition[merc.COND_FULL] > 45:
        ch.send("You're too full to drink more.\n")
        return
    merc.act( "$n drinks $T from $p.", ch, obj, const.liq_table[liquid].liq_name, merc.TO_ROOM )
    merc.act( "You drink $T from $p.", ch, obj, const.liq_table[liquid].liq_name, merc.TO_CHAR )
    update.gain_condition( ch, merc.COND_DRUNK, amount * const.liq_table[liquid].liq_affect[merc.COND_DRUNK] / 36 )
    update.gain_condition( ch, merc.COND_FULL, amount * const.liq_table[liquid].liq_affect[merc.COND_FULL] / 4 )
    update.gain_condition( ch, merc.COND_THIRST,amount * const.liq_table[liquid].liq_affect[merc.COND_THIRST] / 10 )
    update.gain_condition(ch, merc.COND_HUNGER, amount * const.liq_table[liquid].liq_affect[merc.COND_HUNGER] / 2 )
    if not merc.IS_NPC(ch) and ch.pcdata.condition[merc.COND_DRUNK] > 10:
        ch.send("You feel drunk.\n")
    if not merc.IS_NPC(ch) and ch.pcdata.condition[merc.COND_FULL] > 40:
        ch.send("You are full.\n")
    if not merc.IS_NPC(ch) and ch.pcdata.condition[merc.COND_THIRST] > 40:
        ch.send("Your thirst is quenched.\n")
    if obj.value[3] != 0:
        # The drink was poisoned ! */
        af = merc.AFFECT_DATA()
        merc.act("$n chokes and gags.", ch, None, None, merc.TO_ROOM)
        ch.send("You choke and gag.\n")
        af.where = merc.TO_AFFECTS
        af.type = "poison"
        af.level = merc.number_fuzzy(amount)
        af.duration = 3 * amount
        af.location = merc.APPLY_NONE
        af.modifier = 0
        af.bitvector = merc.AFF_POISON
        ch.affect_join(af)
    if obj.value[0] > 0:
        obj.value[1] -= amount
    return

interp.cmd_table['drink'] = interp.cmd_type('drink', do_drink, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)