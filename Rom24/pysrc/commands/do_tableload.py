import logging
from interp import register_command, cmd_type
from merc import LOG_ALWAYS, ML, POS_DEAD

logger = logging.getLogger()


from database.read.read_tables import read_tables


def do_tableload(ch, argument):
    if not argument:
        ch.send("Reloading all tables.")
        read_tables(ch)


register_command(cmd_type('tableload', do_tableload, POS_DEAD, ML, LOG_ALWAYS, 1))