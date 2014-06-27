import merc
import interp


def do_eat(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Eat what?\n")
        return
    obj = ch.get_obj_carry(arg, ch)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    if not merc.IS_IMMORTAL(ch):
        if obj.item_type != merc.ITEM_FOOD and obj.item_type != merc.ITEM_PILL:
            ch.send("That's not edible.\n")
            return
        if not merc.IS_NPC(ch) and ch.pcdata.condition[merc.COND_FULL] > 40:
            ch.send("You are too full to eat more.\n")
            return
    merc.act("$n eats $p.",  ch, obj, None, merc.TO_ROOM)
    merc.act("You eat $p.", ch, obj, None, merc.TO_CHAR)
    if obj.item_type == merc.ITEM_FOOD:
        if not merc.IS_NPC(ch):
            condition = ch.pcdata.condition[merc.COND_HUNGER]
            update.gain_condition(ch, merc.COND_FULL, obj.value[0])
            update.gain_condition(ch, merc.COND_HUNGER, obj.value[1])
            if condition == 0 and ch.pcdata.condition[merc.COND_HUNGER] > 0:
                ch.send("You are no longer hungry.\n")
            elif ch.pcdata.condition[merc.COND_FULL] > 40:
                ch.send("You are full.\n")
        if obj.value[3] != 0:
            # The food was poisoned! */
            af = merc.AFFECT_DATA()
            act( "$n chokes and gags.", ch, 0, 0, merc.TO_ROOM)
            ch.send("You choke and gag.\n")
            af.where = merc.TO_AFFECTS
            af.type = "poison"
            af.level = merc.number_fuzzy(obj.value[0])
            af.duration = 2 * obj.value[0]
            af.location = merc.APPLY_NONE
            af.modifier = 0
            af.bitvector = merc.AFF_POISON
            ch.affect_join(af)
    elif obj.item_type == merc.ITEM_PILL:
        merc.obj_cast_spell( obj.value[1], obj.value[0], ch, ch, None)
        merc.obj_cast_spell( obj.value[2], obj.value[0], ch, ch, None)
        merc.obj_cast_spell( obj.value[3], obj.value[0], ch, ch, None)
    obj.extract()
    return

interp.cmd_type('eat', do_eat, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)