import logging

logger = logging.getLogger()

import merc
import object_creator
import interp
import game_utils
import handler_game
import instance


def do_oload(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg1.isdigit():
        ch.send("Syntax: load obj <vnum> <level>.\n")
        return
    level = ch.trust  # default

    if arg2:  # load with a level
        if not arg2.isdigit():
            ch.send("Syntax: oload <vnum> <level>.\n")
            return
        level = int(arg2)
        if level < 0 or level > ch.trust:
            ch.send("Level must be be between 0 and your level.\n")
            return
    vnum = int(arg1)
    if vnum not in instance.item_templates:
        ch.send("No object has that vnum.\n")
        return
    item = object_creator.create_item(instance.item_templates[vnum], level)
    if item.flags.take:
        ch.put(item)
    else:
        ch.in_room.put(item)
    handler_game.act("$n has created $p!", ch, item, None, merc.TO_ROOM)
    handler_game.wiznet("$N loads $p.", ch, item, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.trust)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('oload', do_oload, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
