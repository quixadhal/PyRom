import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_pecho(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not argument or not arg:
        ch.send("Personal echo what?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("Target not found.\n")
        return
    if victim.trust >= ch.trust != merc.MAX_LEVEL:
        victim.send("personal> ")

    argument = argument.strip()
    victim.send(argument)
    victim.send("\n")
    ch.send("personal> ")
    ch.send(argument)
    ch.send("\n")


interp.register_command(interp.cmd_type('pecho', do_pecho, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
