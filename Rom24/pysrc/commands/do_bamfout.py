import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_bamfout(ch, argument):
    if not state_checks.IS_NPC(ch):
        if not argument:
            ch.send("Your poofout is %s\n" % ch.pcdata.bamfout)
            return
        if ch.name not in argument:
            ch.send("You must include your name.\n")
            return
        ch.pcdata.bamfout = argument
        ch.send("Your poofout is now %s\n" % ch.pcdata.bamfout)
    return


interp.register_command(interp.cmd_type('poofout', do_bamfout, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1))
