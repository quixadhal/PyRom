import logging

logger = logging.getLogger()

import merc
import interp
import instance


def do_areas(ch, argument):
    if argument:
        ch.send("No argument is used with this command.\n")
        return
    col = 0
    for iArea in instance.areas.values():
        ch.send("%-39s" % iArea.credits)
        col += 1
        if col % 2 == 0:
            ch.send("\n")


interp.register_command(interp.cmd_type('areas', do_areas, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
