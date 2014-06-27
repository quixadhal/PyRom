import logging

logger = logging.getLogger()

import merc
import db
import interp


def do_oload(ch, argument):
    argument, arg1 = merc.read_word(argument)
    argument, arg2 = merc.read_word(argument)

    if not arg1 or not arg1.isdigit():
        ch.send("Syntax: load obj <vnum> <level>.\n")
        return
    level = ch.get_trust()  # default

    if arg2:  # load with a level
        if not arg2.isdigit():
            ch.send("Syntax: oload <vnum> <level>.\n")
            return
        level = int(arg2)
        if level < 0 or level > ch.get_trust():
            ch.send("Level must be be between 0 and your level.\n")
            return
    vnum = int(arg1)
    if vnum not in merc.obj_index_hash:
        ch.send("No object has that vnum.\n")
        return
    obj = db.create_object(merc.obj_index_hash[vnum], level)
    if merc.CAN_WEAR(obj, merc.ITEM_TAKE):
        obj.to_char(ch)
    else:
        obj.to_room(ch.in_room)
    merc.act("$n has created $p!", ch, obj, None, merc.TO_ROOM)
    merc.wiznet("$N loads $p.", ch, obj, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.get_trust())
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('oload', do_oload, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
