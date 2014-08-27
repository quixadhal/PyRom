import logging

logger = logging.getLogger()

import merc
import interp
import handler_ch


def do_inventory(ch, argument):
    ch.send("You are carrying:\n")
    handler_ch.show_list_to_char(ch.inventory, ch, True, True)
    return


interp.register_command(interp.cmd_type('inventory', do_inventory, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
