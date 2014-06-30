import logging

logger = logging.getLogger()

from game_utils import read_word
from merc import *
from interp import register_command, cmd_type
from character import Character


def do_debug(ch, argument):
    global gdf
    if not argument:
        ch.send("Syntax: debug <command> "
                "<arguments>\n\n   "
                "Safely execute commands and "
                "get valuable debugging "
                "information.\n")
        return
    safety, word = read_word(argument)
    if word.startswith('debug'):
        ch.send("Nope.\n")
        return
    gdf = True
    Character.interpret(ch, argument)
    return


register_command(cmd_type('debug', do_debug, POS_DEAD, ML, LOG_NORMAL, 1))
