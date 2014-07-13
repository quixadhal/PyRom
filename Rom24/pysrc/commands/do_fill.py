import logging

logger = logging.getLogger()

import merc
import const
import interp
import game_utils


def do_fill(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Fill what?\n")
        return
    obj = ch.get_item_carry(arg, ch)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    fountain = [f for f in merc.rooms[ch.in_room].contents if f.item_type == merc.ITEM_FOUNTAIN][:1]
    if not fountain:
        ch.send("There is no fountain here!\n")
        return
    fountain = fountain[0]
    if obj.item_type != merc.ITEM_DRINK_CON:
        ch.send("You can't fill that.\n")
        return
    if obj.value[1] != 0 and obj.value[2] != fountain.value[2]:
        ch.send("There is already another liquid in it.\n")
        return
    if obj.value[1] >= obj.value[0]:
        ch.send("Your container is full.\n")
        return
    act("You fill $p with %s from $P." % const.liq_table[fountain.value[2]].liq_name, ch, obj, fountain,
                     merc.TO_CHAR)
    act("$n fills $p with %s from $P." % const.liq_table[fountain.value[2]].liq_name, ch, obj, fountain,
                     merc.TO_ROOM)
    obj.value[2] = fountain.value[2]
    obj.value[1] = obj.value[0]
    return


interp.register_command(interp.cmd_type('fill', do_fill, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
