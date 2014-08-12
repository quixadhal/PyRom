import logging

logger = logging.getLogger()

import merc
import hotfix
import interp


def do_reload(ch, argument):
    hotfix.reload_files(ch)
    ch.send("Files reloaded.\n")


interp.register_command(interp.cmd_type('reload', do_reload, merc.POS_DEAD, merc.ML, merc.LOG_NORMAL, 1))
