import logging

logger = logging.getLogger()

import game_utils
import merc
import interp
import instance


def do_at(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg or not argument:
        ch.send("At where what?\n")
        return
    location = game_utils.find_location(ch, arg)
    if not location:
        ch.send("No such location.\n")
        return
    if not ch.is_room_owner(location) and location.is_private() \
            and ch.trust < merc.MAX_LEVEL:
        ch.send("That room is private right now.\n")
        return
    original = ch.in_room
    on = ch.on
    original.get(ch)
    location.put(ch)
    ch.interpret(argument)

    # See if 'ch' still exists before continuing!
    # Handles 'at XXXX quit' case.
    for wch in instance.characters.values():
        if wch == ch:
            location.get(ch)
            original.put(ch)
            ch.on = on
            break


interp.register_command(interp.cmd_type('at', do_at, merc.POS_DEAD, merc.L6, merc.LOG_NORMAL, 1))
