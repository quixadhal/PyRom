import logging

logger = logging.getLogger()

import merc
import interp
import settings


def do_bug(ch, argument):
    merc.append_file(ch, settings.BUG_FILE, argument)
    ch.send("Bug logged.\n")
    return


interp.register_command(interp.cmd_type('bug', do_bug, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
