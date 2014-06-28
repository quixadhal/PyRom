import logging

logger = logging.getLogger()

import merc
import interp
import settings
import handler_game

# RT anti-newbie code
def do_newlock(ch, argument):
    if not settings.NEWLOCK:
        handler_game.wiznet("$N locks out new characters.", ch, None, 0, 0, 0)
        ch.send("New characters have been locked out.\n")
        settings.NEWLOCK = True
    else:
        handler_game.wiznet("$N allows new characters back in.", ch, None, 0, 0, 0)
        ch.send("Newlock removed.\n")
        settings.NEWLOCK = False
    return


interp.register_command(interp.cmd_type('newlock', do_newlock, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
