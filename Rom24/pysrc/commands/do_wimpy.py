import logging

logger = logging.getLogger()

import game_utils
import merc
import interp

# 'Wimpy' originally by Dionysos.
def do_wimpy(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        wimpy = ch.max_hit // 5
    else:
        wimpy = int(arg)
    if wimpy < 0:
        ch.send("Your courage exceeds your wisdom.\n")
        return
    if wimpy > ch.max_hit // 2:
        ch.send("Such cowardice ill becomes you.\n")
        return
    ch.wimpy = wimpy
    ch.send("Wimpy set to %d hit points.\n" % wimpy)
    return


interp.register_command(interp.cmd_type('wimpy', do_wimpy, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
