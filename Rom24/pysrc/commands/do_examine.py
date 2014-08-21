import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_examine(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Examine what?\n")
        return
    ch.do_look(arg)
    buf = ""
    obj = ch.get_item_here(arg)
    if obj:
        if obj.item_type == merc.ITEM_JUKEBOX:
            ch.do_play("list")
        elif obj.item_type == merc.ITEM_MONEY:
            if obj.value[0] == 0:
                if obj.value[1] == 0:
                    buf = "Odd...there's no coins in the pile.\n"
                elif obj.value[1] == 1:
                    buf = "Wow. One gold coin.\n"
                else:
                    buf = "There are %d gold coins in the pile.\n" % obj.value[1]
            elif obj.value[1] == 0:
                if obj.value[0] == 1:
                    buf = "Wow. One silver coin.\n"
                else:
                    buf = "There are %d silver coins in the pile.\n" % obj.value[0]
            else:
                buf = "There are %d gold and %d silver coins in the pile.\n" % (obj.value[1], obj.value[0])
            ch.send(buf)
        elif obj.item_type == merc.ITEM_DRINK_CON \
                or obj.item_type == merc.ITEM_CONTAINER \
                or obj.item_type == merc.ITEM_CORPSE_NPC \
                or obj.item_type == merc.ITEM_CORPSE_PC:
            ch.do_look("in %s" % arg)


interp.register_command(interp.cmd_type('examine', do_examine, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
