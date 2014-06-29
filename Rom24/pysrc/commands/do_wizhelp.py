import logging

logger = logging.getLogger()

import merc
import interp


def do_wizhelp(ch, argument):
    col = 0
    for key, cmd in interp.cmd_table.items():
        if merc.LEVEL_HERO <= cmd.level <= ch.trust and cmd.show:
            ch.send("%-12s" % key)
            col += 1
            if col % 6 == 0:
                ch.send("\n")
    if col % 6 != 0:
        ch.send("\n")
    return


interp.register_command(interp.cmd_type('wizhelp', do_wizhelp, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
