import logging
import traceback

logger = logging.getLogger()

from game_utils import read_word
from merc import POS_DEAD, LOG_NORMAL, ML
from interp import register_command, cmd_type, interpret

def do_debug(ch, argument):
    if not argument:
        ch.send("Syntax: debug <command> <arguments>\n\n   Safely execute commands and get valuable debugging information.\n")
        return
    safety, word = read_word(argument)
    if word.startswith('debug'):
        ch.send("Nope.\n")
        return
    try:
        interpret(ch, argument)
    except:
        ch.send(traceback.format_exc())
        logger.exception('Failed to execute %s', word)

register_command(cmd_type('debug', do_debug, POS_DEAD, ML, LOG_NORMAL, 1))