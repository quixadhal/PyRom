import logging

logger = logging.getLogger()

import interp
import merc
import database


def do_tableload(ch, argument):
    if not argument:
        ch.send("Reloading all tables.")
        database.read.read_tables(ch)


interp.register_command(interp.cmd_type('tableload', do_tableload, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))
