import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_bamfin(ch, argument):
    if not ch.is_npc():
        if not argument:
            ch.send("Your poofin is %s\n" % ch.pcdata.bamfin)
            return
        if ch.name not in argument:
            ch.send("You must include your name.\n")
            return
        ch.pcdata.bamfin = argument
        ch.send("Your poofin is now %s\n" % ch.pcdata.bamfin)
    return


interp.register_command(interp.cmd_type('poofin', do_bamfin, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1))
