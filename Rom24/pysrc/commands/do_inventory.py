import logging
from handler_ch import show_list_to_char

logger = logging.getLogger()

import merc
import interp


def do_inventory(ch, argument):
    ch.send("You are carrying:\n")
    show_list_to_char(ch.inventory, ch, True, True)
    return


interp.register_command(interp.cmd_type('inventory', do_inventory, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
