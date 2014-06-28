import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks

def do_title(ch, argument):
    if state_checks.IS_NPC(ch):
        return
    if not argument:
        ch.send("Change your title to what?\n")
        return
    if len(argument) > 45:
        argument = argument[:45]
    game_utils.set_title(ch, argument)
    ch.send("Ok.\n")


interp.register_command(interp.cmd_type('title', do_title, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
