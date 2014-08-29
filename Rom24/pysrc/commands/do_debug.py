import logging

logger = logging.getLogger()

import handler_pc
import game_utils
import interp
import merc
import handler_log


def do_debug(ch, argument):
    if not argument:
        ch.send("Syntax: debug <command> "
                "<arguments>\n\n   "
                "Safely execute commands and "
                "get valuable debugging "
                "information.\n")
        return
    safety, word = game_utils.read_word(argument)
    if word.startswith('debug'):
        ch.send("Nope.\n")
        return
    handler_log.GlobalDebugFlag.gdfset(True)
    handler_pc.Pc.interpret(ch, argument)
    return

interp.register_command(interp.cmd_type('debug', do_debug, merc.POS_DEAD, merc.ML, merc.LOG_NORMAL, 1))
