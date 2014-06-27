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
            if d.character.get_trust() >= ch.get_trust():
                d.send("global> ")
            d.send(argument + "\n")
    return


interp.register_command(interp.cmd_type('gecho', do_echo, interp.POS_DEAD, interp.L4, interp.LOG_ALWAYS, 1))
