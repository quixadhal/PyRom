import logging

logger = logging.getLogger()

import merc
import interp
import update
import game_utils
import handler_game
import handler_magic


def do_eat(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Eat what?\n")
        return
    obj = ch.get_item_carry(arg, ch)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    if not ch.is_immortal():
        if obj.item_type != merc.ITEM_FOOD and obj.item_type != merc.ITEM_PILL:
            ch.send("That's not edible.\n")
            return
        if not ch.is_npc() and ch.condition[merc.COND_FULL] > 40:
            ch.send("You are too full to eat more.\n")
            return
    handler_game.act("$n eats $p.", ch, obj, None, merc.TO_ROOM)
    handler_game.act("You eat $p.", ch, obj, None, merc.TO_CHAR)
    if obj.item_type == merc.ITEM_FOOD:
        if not ch.is_npc():
            condition = ch.condition[merc.COND_HUNGER]
            update.gain_condition(ch, merc.COND_FULL, obj.value[0])
            update.gain_condition(ch, merc.COND_HUNGER, obj.value[1])
            if condition == 0 and ch.condition[merc.COND_HUNGER] > 0:
                ch.send("You are no longer hungry.\n")
            elif ch.condition[merc.COND_FULL] > 40:
                ch.send("You are full.\n")
        if obj.value[3] != 0:
            # The food was poisoned!
            af = handler_game.AFFECT_DATA()
            handler_game.act("$n chokes and gags.", ch, 0, 0, merc.TO_ROOM)
            ch.send("You choke and gag.\n")
            af.where = merc.TO_AFFECTS
            af.type = "poison"
            af.level = game_utils.number_fuzzy(obj.value[0])
            af.duration = 2 * obj.value[0]
            af.location = merc.APPLY_NONE
            af.modifier = 0
            af.bitvector = merc.AFF_POISON
            ch.affect_join(af)
    elif obj.item_type == merc.ITEM_PILL:
        handler_magic.obj_cast_spell(obj.value[1], obj.value[0], ch, ch, None)
        handler_magic.obj_cast_spell(obj.value[2], obj.value[0], ch, ch, None)
        handler_magic.obj_cast_spell(obj.value[3], obj.value[0], ch, ch, None)
    obj.extract()
    return


interp.register_command(interp.cmd_type('eat', do_eat, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
