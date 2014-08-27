import logging

logger = logging.getLogger()

import merc
import const
import interp
import game_utils
import handler_game


def do_pour(ch, argument):
    argument, arg = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg or not arg2:
        ch.send("Pour what into what?\n")
        return
    out = ch.get_item_carry(arg, ch)
    if not out:
        ch.send("You don't have that item.\n")
        return
    if out.item_type != merc.ITEM_DRINK_CON:
        ch.send("That's not a drink container.\n")
        return
    if arg2 == "out":
        if out.value[1] == 0:
            ch.send("It's already empty.\n")
            return
        out.value[1] = 0
        out.value[3] = 0
        handler_game.act("You invert $p, spilling %s all over the ground." % const.liq_table[out.value[2]].name, ch, out,
                 None, merc.TO_CHAR)
        handler_game.act("$n inverts $p, spilling %s all over the ground." % const.liq_table[out.value[2]].name, ch, out,
                 None, merc.TO_ROOM)
        return
    into = ch.get_item_here(arg2)
    vch = None
    if not into:
        vch = ch.get_char_room(arg2)

        if vch is None:
            ch.send("Pour into what?\n")
            return
        into = vch.get_eq('held')
        if not into:
            ch.send("They aren't holding anything.")

    if into.item_type != merc.ITEM_DRINK_CON:
        ch.send("You can only pour into other drink containers.\n")
        return
    if into == out:
        ch.send("You cannot change the laws of physics!\n")
        return
    if into.value[1] != 0 and into.value[2] != out.value[2]:
        ch.send("They don't hold the same liquid.\n")
        return
    if out.value[1] == 0:
        handler_game.act("There's nothing in $p to pour.", ch, out, None, merc.TO_CHAR)
        return
    if into.value[1] >= into.value[0]:
        handler_game.act("$p is already filled to the top.", ch, into, None, merc.TO_CHAR)
        return
    amount = min(out.value[1], into.value[0] - into.value[1])

    into.value[1] += amount
    out.value[1] -= amount
    into.value[2] = out.value[2]

    if not vch:
        handler_game.act("You pour %s from $p into $P." % const.liq_table[out.value[2]].name, ch, out, into,
                         merc.TO_CHAR)
        handler_game.act("$n pours %s from $p into $P." % const.liq_table[out.value[2]].name, ch, out, into,
                         merc.TO_ROOM)
    else:
        handler_game.act("You pour some %s for $N." % const.liq_table[out.value[2]].name, ch, None, vch,
                         merc.TO_CHAR)
        handler_game.act("$n pours you some %s." % const.liq_table[out.value[2]].name, ch, None, vch, merc.TO_VICT)
        handler_game.act("$n pours some %s for $N." % const.liq_table[out.value[2]].name, ch, None, vch,
                         merc.TO_NOTVICT)


interp.register_command(interp.cmd_type('pour', do_pour, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
