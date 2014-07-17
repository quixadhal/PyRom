import logging

logger = logging.getLogger()

import merc
import interp
import pyprogs
from handler_game import act

def do_say(ch, argument):
    if not argument:
        ch.send("Say what?\n")
        return

    act("$n says '$T'", ch, None, argument, merc.TO_ROOM)
    act("You say '$T'", ch, None, argument, merc.TO_CHAR)
    pyprogs.emit_signal('say', actor=ch, argument=argument, audience=ch.in_room.people)
    return


interp.register_command(interp.cmd_type('say', do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type("'", do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0))
