import logging


logger = logging.getLogger()

from database.write.write_tables import write_tables
from merc import ML, LOG_ALWAYS, POS_DEAD
from interp import register_command, cmd_type


def do_tabledump(ch, argument):
    if not argument:
        ch.send("Dumping all tables.\n")
        write_tables(ch)

register_command(cmd_type('tabledump', do_tabledump, POS_DEAD, ML, LOG_ALWAYS, 1))