import logging

logger = logging.getLogger()

import merc
import interp

#TODO: Known broken.
def do_memory(ch, argument):
    pass


interp.register_command(interp.cmd_type('memory', do_memory, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
