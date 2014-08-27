import logging

logger = logging.getLogger()

import game_utils
import merc
import interp
import handler_game


def do_compare(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1:
        ch.send("Compare what to what?\n")
        return
    obj1 = ch.get_item_carry(arg1, ch)
    if not obj1:
        ch.send("You do not have that item.\n")
        return
    obj2 = None
    if not arg2:
        for obj2 in ch.inventory[:]:
            if obj2.equipped_to and ch.can_see_item(obj2) and obj1.item_type == obj2.item_type \
                    and (obj1.equips_to & obj2.equips_to & ~merc.ITEM_TAKE) != 0:
                break

        if not obj2:
            ch.send("You aren't wearing anything comparable.\n")
            return
    else:
        obj2 = ch.get_item_carry(arg2, ch)
        if not obj2:
            ch.send("You do not have that item.\n")
            return

    msg = None
    value1 = 0
    value2 = 0

    if obj1 is obj2:
        msg = "You compare $p to itself.  It looks about the same."
    elif obj1.item_type != obj2.item_type:
        msg = "You can't compare $p and $P."
    else:
        if obj1.item_type == merc.ITEM_ARMOR:
            value1 = obj1.value[0] + obj1.value[1] + obj1.value[2]
            value2 = obj2.value[0] + obj2.value[1] + obj2.value[2]
        elif obj1.item_type == merc.ITEM_WEAPON:
            value1 = (1 + obj1.value[2]) * obj1.value[1]
            value2 = (1 + obj2.value[2]) * obj2.value[1]
        else:
            msg = "You can't compare $p and $P."
    if msg is None:
        if value1 == value2:
            msg = "$p and $P look about the same."
        elif value1 > value2:
            msg = "$p looks better than $P."
        else:
            msg = "$p looks worse than $P."
    handler_game.act(msg, ch, obj1, obj2, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('compare', do_compare, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
