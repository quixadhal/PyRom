import logging

logger = logging.getLogger()

import merc
import interp


def do_bamfout(ch, argument):
    if not ch.is_npc():
        if not argument:
            ch.send("Your poofout is %s\n" % ch.bamfout)
            return
        if ch.name not in argument:
            ch.send("You must include your name.\n")
            return
        ch.bamfout = argument
        ch.send("Your poofout is now %s\n" % ch.bamfout)
    return


interp.register_command(interp.cmd_type('poofout', do_bamfout, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1))
