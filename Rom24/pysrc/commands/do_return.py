import logging

logger = logging.getLogger()

import merc
import interp


def do_return(ch, argument):
    if not ch.desc:
        return
    if not ch.desc.original:
        ch.send("You aren't switched.\n")
        return
    ch.send("You return to your original body. Type replay to see any missed tells.\n")
    if ch.prompt:
        ch.prompt = ''
    merc.wiznet("$N returns from %s." % ch.short_descr, ch.desc.original, 0, merc.WIZ_SWITCHES, merc.WIZ_SECURE,
                ch.get_trust())
    ch.desc.character = ch.desc.original
    ch.desc.original = None
    ch.desc.character.desc = ch.desc
    ch.desc = None
    return


interp.register_command(interp.cmd_type('return', do_return, merc.POS_DEAD, merc.L6, merc.LOG_NORMAL, 1))
