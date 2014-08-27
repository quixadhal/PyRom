import random
import logging

logger = logging.getLogger()

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
    container = ch.get_item_here(arg2)
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
        item = ch.get_item_carry(arg1, ch)
        if not item:
            ch.send("You do not have that item.\n")
            return
        if item == container:
            ch.send("You can't fold it into itself.\n")
            return
        if not ch.can_drop_item(item):
            ch.send("You can't let go of it.\n")
            return
        if state_checks.WEIGHT_MULT(item) != 100:
            ch.send("You have a feeling that would be a bad idea.\n")
            return
        if item.get_weight() + container.true_weight() > (container.value[0] * 10) \
                or item.get_weight() > (container.value[3] * 10):
            ch.send("It won't fit.\n")
            return
        if container.vnum == merc.OBJ_VNUM_PIT \
                and not container.flags.take:
            if item.timer:
                item.flags.had_timer = True
            else:
                item.timer = random.randint(100, 200)
        ch.get(item)
        container.put(item)

        if state_checks.IS_SET(container.value[1], merc.CONT_PUT_ON):
            handler_game.act("$n puts $p on $P.", ch, item, container, merc.TO_ROOM)
            handler_game.act("You put $p on $P.", ch, item, container, merc.TO_CHAR)
        else:
            handler_game.act("$n puts $p in $P.", ch, item, container, merc.TO_ROOM)
            handler_game.act("You put $p in $P.", ch, item, container, merc.TO_CHAR)
    else:
        # 'put all container' or 'put all.obj container'
        for item in ch.inventory[:]:
            if (len(arg1) == 3 or arg1[4:] in item.name ) \
                    and ch.can_see_item(item) and state_checks.WEIGHT_MULT(item) == 100 \
                    and not item.equipped_to and item != container \
                    and ch.can_drop_item(item) \
                    and item.get_weight() + container.true_weight() <= (container.value[0] * 10) \
                    and item.get_weight() < (container.value[3] * 10):
                if container.vnum == merc.OBJ_VNUM_PIT and not item.flags.take:
                    if item.timer:
                        item.flags.had_timer = True
                    else:
                        item.timer = random.randint(100, 200)
                ch.get(item)
                container.put(item)
                if state_checks.IS_SET(container.value[1], merc.CONT_PUT_ON):
                    handler_game.act("$n puts $p on $P.", ch, item, container, merc.TO_ROOM)
                    handler_game.act("You put $p on $P.", ch, item, container, merc.TO_CHAR)
                else:
                    handler_game.act("$n puts $p in $P.", ch, item, container, merc.TO_ROOM)
                    handler_game.act("You put $p in $P.", ch, item, container, merc.TO_CHAR)


interp.register_command(interp.cmd_type('put', do_put, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
