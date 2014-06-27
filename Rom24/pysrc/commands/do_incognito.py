import logging

logger = logging.getLogger()

import merc
import interp


def do_incognito(ch, argument):
    # RT code for taking a level argument
    argument, arg = merc.read_word(argument)
    if not arg:
        # take the default path
        if ch.incog_level:
            ch.incog_level = 0
            merc.act("$n is no longer cloaked.", ch, None, None, merc.TO_ROOM)
            ch.send("You are no longer cloaked.\n")
        else:
            ch.incog_level = ch.get_trust()
            merc.act("$n cloaks $s presence.", ch, None, None, merc.TO_ROOM)
            ch.send("You cloak your presence.\n")
    else:
        # do the level thing
        level = int(arg) if arg.isdigit() else -1
        if level < 2 or level > ch.get_trust():
            ch.send("Incog level must be between 2 and your level.\n")
            return
        else:
            ch.reply = None
            ch.incog_level = level
            merc.act("$n cloaks $s presence.", ch, None, None, merc.TO_ROOM)
            ch.send("You cloak your presence.\n")
    return


interp.register_command(interp.cmd_type('incognito', do_incognito, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
