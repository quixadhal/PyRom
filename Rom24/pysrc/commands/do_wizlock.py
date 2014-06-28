import logging

logger = logging.getLogger()

import merc
import interp
import settings
import handler_game


def do_wizlock(ch, argument):
    if not settings.WIZLOCK:
        handler_game.wiznet("$N has wizlocked the game.", ch, None, 0, 0, 0)
        ch.send("Game wizlocked.\n")
        settings.WIZLOCK = True
    else:
        handler_game.wiznet("$N removes wizlock.", ch, None, 0, 0, 0)
        ch.send("Game un-wizlocked.\n")
        settings.WIZLOCK = False
    return


interp.register_command(interp.cmd_type('wizlock', do_wizlock, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1))
