import logging

logger = logging.getLogger()

import merc
import interp


def do_shutdown(ch, argument):
    if ch.invis_level < merc.LEVEL_HERO:
        ch.do_echo("Shutdown by %s." % ch.name)
    merc_down = True  # TODO:  fix this at some point
    for d in merc.descriptor_list[:]:
        vch = merc.CH(d)
        if vch:
            save.save_char_obj(vch)
            comm.close_socket(d)


interp.register_command(interp.cmd_type('shutdown', do_shutdown, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1))
