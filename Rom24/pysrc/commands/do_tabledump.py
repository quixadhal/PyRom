import logging

logger = logging.getLogger()

import database
import merc
import interp


def do_tabledump(ch, argument):
    if not argument:
        ch.send("Dumping all tables.\n")
        database.write.write_tables(ch)

interp.register_command(interp.cmd_type('tabledump', do_tabledump, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))