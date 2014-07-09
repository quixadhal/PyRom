import logging

logger = logging.getLogger()

import merc
import interp
import handler_game
import pyprogs

def do_say(ch, argument):
    if not argument:
        ch.send("Say what?\n")
        return

    handler_game.act("$n says '$T'", ch, None, argument, merc.TO_ROOM)
    handler_game.act("You say '$T'", ch, None, argument, merc.TO_CHAR)
    pyprogs.emit_signal('say', actor=ch, argument=argument, audience=ch.in_room.people)
    return


interp.register_command(interp.cmd_type('say', do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type("'", do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0))
