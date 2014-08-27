import logging

logger = logging.getLogger()

import handler_game
import merc
import interp


def do_emote(ch, argument):
    if not ch.is_npc() and ch.comm.is_set(merc.COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    handler_game.act("$n $T", ch, None, argument, merc.TO_ROOM)
    handler_game.act("$n $T", ch, None, argument, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('emote', do_emote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type(',', do_emote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0))
