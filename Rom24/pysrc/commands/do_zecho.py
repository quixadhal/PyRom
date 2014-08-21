import logging

logger = logging.getLogger()

import merc
import interp
import nanny


def do_zecho(ch, argument):
    if not argument:
        ch.send("Zone echo what?\n")
        return
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) and d.character.in_room and ch.in_room \
                and d.character.in_room.area == ch.in_room.area:
            if d.character.trust >= ch.trust:
                d.send("zone> ")
            d.send(argument + "\n")


interp.register_command(interp.cmd_type('zecho', do_zecho, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
