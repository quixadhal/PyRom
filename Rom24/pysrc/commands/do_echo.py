import logging

logger = logging.getLogger()

import merc
import interp
import nanny


def do_echo(ch, argument):
    if not argument:
        ch.send("Global echo what?\n")
        return
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing):
            if d.character.trust >= ch.trust:
                d.send("global> ")
            d.send(argument + "\n")
    return


interp.register_command(interp.cmd_type('gecho', do_echo, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
