import merc
import interp
import settings


def do_wizlock(ch, argument):
    if not settings.WIZLOCK:
        merc.wiznet("$N has wizlocked the game.", ch, None, 0, 0, 0)
        ch.send("Game wizlocked.\n")
        settings.WIZLOCK = True
    else:
        merc.wiznet("$N removes wizlock.", ch, None, 0, 0, 0)
        ch.send("Game un-wizlocked.\n")
        settings.WIZLOCK = False
    return

interp.cmd_type('wizlock', do_wizlock, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1)