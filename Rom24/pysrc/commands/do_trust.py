import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_trust(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg2 or not arg2.isdigit():
        ch.send("Syntax: trust <char> <level>.\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("That player is not here.\n")
        return
    level = int(arg2)
    if level < 0 or level > merc.MAX_LEVEL:
        ch.send("Level must be 0 (reset) or 1 to %d.\n" % merc.MAX_LEVEL)
        return
    if level > ch.trust:
        ch.send("Limited to your trust.\n")
        return
    victim.trust = level
    return


interp.register_command(interp.cmd_type('trust', do_trust, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))
