__author__ = 'syn'
import logging

logger = logging.getLogger()

import interp
import merc
import handler_log
import game_utils


def do_gdstate(ch, argument):
    if ch.level <= merc.ML -1:
        ch.send("Huh?\n\n")

    if not argument:
        ch.send("This command allows global debug mode for commands. "
                "gdebug <enable> to turn on, gdebug <disable> to turn off.\n\n")
        return

    word, arg = game_utils.read_word(argument)

    if arg.startswith('enable'):
        handler_log.GlobalDebugFlag.gdcfset(True)
        ch.send("Global Debug enabled.\n\n")
        return

    elif arg.startswith('disable'):
        handler_log.GlobalDebugFlag.gdcfset(False)
        ch.send("Global Debug disabled. debug (command) will still function.\n\n")
        return
    else:
        ch.send("accepted arguments: enable or disable\n")
        return

interp.register_command(interp.cmd_type('gdebug', do_gdstate, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))
