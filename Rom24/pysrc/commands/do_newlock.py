import merc
import interp
import settings


# RT anti-newbie code */
def do_newlock(ch, argument):
    if not settings.NEWLOCK:
        merc.wiznet("$N locks out new characters.", ch, None, 0, 0, 0)
        ch.send("New characters have been locked out.\n")
        settings.NEWLOCK = True
    else:
        merc.wiznet("$N allows new characters back in.", ch, None, 0, 0, 0)
        ch.send("Newlock removed.\n")
        settings.NEWLOCK = False
    return

interp.cmd_type('newlock', do_newlock, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1)