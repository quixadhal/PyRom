import logging


logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import handler_magic

def do_quaff(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Quaff what?\n")
        return
    obj = ch.get_item_carry(arg, ch)
    if not obj:
        ch.send("You do not have that potion.\n")
        return
    if obj.item_type != merc.ITEM_POTION:
        ch.send("You can quaff only potions.\n")
        return
    if ch.level < obj.level:
        ch.send("This liquid is too powerful for you to drink.\n")
        return
    handler_game.act("$n quaffs $p.", ch, obj, None, merc.TO_ROOM)
    handler_game.act("You quaff $p.", ch, obj, None, merc.TO_CHAR)

    handler_magic.obj_cast_spell(obj.value[1], obj.value[0], ch, ch, None)
    handler_magic.obj_cast_spell(obj.value[2], obj.value[0], ch, ch, None)
    handler_magic.obj_cast_spell(obj.value[3], obj.value[0], ch, ch, None)

    obj.extract()
    return


interp.register_command(interp.cmd_type('quaff', do_quaff, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
