import logging

logger = logging.getLogger()

import comm
import handler_ch
import merc
import interp


def do_shutdown(ch, argument):
    if ch.invis_level < merc.LEVEL_HERO:
        ch.do_echo("Shutdown by %s." % ch.name)
    comm.done = True
    for d in merc.descriptor_list[:]:
        vch = handler_ch.CH(d)
        if vch:
            vch.save(logout=True, force=True)
            comm.close_socket(d)


def do_shutdow(ch, argument):
    ch.send("If you want to SHUTDOWN, spell it out.\n")
    return


interp.register_command(interp.cmd_type('shutdown', do_shutdown, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1))
interp.register_command(interp.cmd_type('shutdow', do_shutdow, merc.POS_DEAD, merc.L1, merc.LOG_NORMAL, 0))
