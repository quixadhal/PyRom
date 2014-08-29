import logging

logger = logging.getLogger()

import merc
import interp
import comm
import handler_ch

def do_reboot(ch, argument):
    if ch.invis_level < merc.LEVEL_HERO:
        ch.do_echo("Reboot by %s." % ch.name)
    comm.done = True
    for d in merc.descriptor_list[:]:
        vch = handler_ch.CH(d)
        if vch:
            vch.save(logout=True, force=True)
            comm.close_socket(d)


def do_reboo(ch, argument):
    ch.send("If you want to REBOOT, spell it out.\n")
    return


interp.register_command(interp.cmd_type('reboot', do_reboot, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1))
interp.register_command(interp.cmd_type('reboo', do_reboo, merc.POS_DEAD, merc.L1, merc.LOG_NORMAL, 0))
