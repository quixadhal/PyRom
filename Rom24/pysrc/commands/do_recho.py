import logging

logger = logging.getLogger()

import merc
import interp
import nanny


def do_recho(ch, argument):
    if not argument:
        ch.send("Local echo what?\n")
        return
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) and d.character.in_room == ch.in_room:
            if d.character.trust >= ch.trust:
                d.send("local> ")
            d.send(argument + "\n")

    return


interp.register_command(interp.cmd_type('echo', do_recho, merc.POS_DEAD, merc.L6, merc.LOG_ALWAYS, 1))
