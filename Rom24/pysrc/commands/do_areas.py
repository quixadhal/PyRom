import logging

logger = logging.getLogger()

import merc
import interp


def do_areas(ch, argument):
    ch.send("Known not working. TODO: Make this work\n")
    if argument:
        ch.send("No argument is used with this command.\n")
        return
    col = 0
    for iArea in merc.area_list:
        ch.send("%-39s\n" % iArea.credits)
        col += 1
        if col % 2 == 0:
            ch.send("\n")


interp.register_command(interp.cmd_type('areas', do_areas, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
