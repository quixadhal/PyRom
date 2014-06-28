import logging

logger = logging.getLogger()

import random
import merc
import interp
import game_utils
import handler_game
import state_checks

def do_put(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if arg2 == "in" or arg2 == "on":
        argument, arg2 = game_utils.read_word(argument)
    if not arg1 or not arg2:
        ch.send("Put what in what?\n")
        return
    if arg2.startswith("all") or "all" == arg2:
        ch.send("You can't do that.\n")
        return
    container = ch.get_obj_here(arg2)
    if not container:
        handler_game.act("I see no $T here.", ch, None, arg2, merc.TO_CHAR)
        return
    if container.item_type != merc.ITEM_CONTAINER:
        ch.send("That's not a container.\n")
        return
    if state_checks.IS_SET(container.value[1], merc.CONT_CLOSED):
        handler_game.act("The $d is closed.", ch, None, container.name, merc.TO_CHAR)
        return
    if arg1 != "all" and not arg1.startswith("all."):
        # 'put obj container'
        obj = ch.get_obj_carry(arg1, ch)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        if obj == container:
            ch.send("You can't fold it into itself.\n")
            return
        if not ch.can_drop_obj(obj):
            ch.send("You can't let go of it.\n")
            return
        if state_checks.WEIGHT_MULT(obj) != 100:
            ch.send("You have a feeling that would be a bad idea.\n")
            return
        if obj.get_weight() + container.true_weight() > (container.value[0] * 10) \
                or obj.get_weight() > (container.value[3] * 10):
            ch.send("It won't fit.\n")
            return
        if container.pIndexData.vnum == merc.OBJ_VNUM_PIT \
                and not state_checks.CAN_WEAR(container, merc.ITEM_TAKE):
            if obj.timer:
                obj.extra_flags = state_checks.SET_BIT(obj.extra_flags, merc.ITEM_HAD_TIMER)
            else:
                obj.timer = random.randint(100, 200)
        obj.from_char()
        obj.to_obj(container)

        if state_checks.IS_SET(container.value[1], merc.CONT_PUT_ON):
            handler_game.act("$n puts $p on $P.", ch, obj, container, merc.TO_ROOM)
            handler_game.act("You put $p on $P.", ch, obj, container, merc.TO_CHAR)
        else:
            handler_game.act("$n puts $p in $P.", ch, obj, container, merc.TO_ROOM)
            handler_game.act("You put $p in $P.", ch, obj, container, merc.TO_CHAR)
    else:
        # 'put all container' or 'put all.obj container'
        for obj in ch.carrying[:]:
            if (len(arg1) == 3 or arg1[4:] in obj.name ) \
                    and ch.can_see_obj(obj) and state_checks.WEIGHT_MULT(obj) == 100 \
                    and obj.wear_loc == merc.WEAR_NONE and obj != container \
                    and ch.can_drop_obj(obj) \
                    and obj.get_weight() + container.true_weight() <= (container.value[0] * 10) \
                    and obj.get_weight() < (container.value[3] * 10):
                if container.pIndexData.vnum == merc.OBJ_VNUM_PIT and not state_checks.CAN_WEAR(obj, merc.ITEM_TAKE):
                    if obj.timer:
                        obj.extra_flags = state_checks.SET_BIT(obj.extra_flags, merc.ITEM_HAD_TIMER)
                    else:
                        obj.timer = random.randint(100, 200)
                obj.from_char()
                obj.to_obj(container)
                if state_checks.IS_SET(container.value[1], merc.CONT_PUT_ON):
                    handler_game.act("$n puts $p on $P.", ch, obj, container, merc.TO_ROOM)
                    handler_game.act("You put $p on $P.", ch, obj, container, merc.TO_CHAR)
                else:
                    handler_game.act("$n puts $p in $P.", ch, obj, container, merc.TO_ROOM)
                    handler_game.act("You put $p in $P.", ch, obj, container, merc.TO_CHAR)


interp.register_command(interp.cmd_type('put', do_put, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
