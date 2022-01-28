import logging

logger = logging.getLogger(__name__)

from rom24 import handler_pc
from rom24 import game_utils
from rom24 import interp
from rom24 import merc


def do_debug(ch, argument):
    if not argument:
        ch.send(
            "Syntax: debug <command> "
            "<arguments>\n\n   "
            "Safely execute commands and "
            "get valuable debugging "
            "information.\n"
        )
        return
    safety, word = game_utils.read_word(argument)
    if word.startswith("debug"):
        ch.send("Nope.\n")
        return
    handler_pc.Pc.interpret(ch, argument)
    return


interp.register_command(
    interp.cmd_type("debug", do_debug, merc.POS_DEAD, merc.ML, merc.LOG_NORMAL, 1)
)
