import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_unalias(ch, argument):
    if not ch.desc:
        rch = ch
    else:
        rch = ch.desc.original if ch.desc.original else ch

    if rch.is_npc():
        return

    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Unalias what?\n\r")
        return

    if arg not in ch.alias:
        ch.send("No alias of that name to remove.\n\r")
        return
    del ch.alias[arg]
    ch.send("Alias removed.\n")
    return


interp.register_command(interp.cmd_type('unalias', do_unalias, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
