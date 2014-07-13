import logging

logger = logging.getLogger()

import merc
import interp


def do_replay(ch, argument):
    if ch.is_npc():
        ch.send("You can't replay.\n")
        return
    if not ch.buffer:
        ch.send("You have no tells to replay.\n")
        return
    [ch.send(tell) for tell in ch.buffer]
    ch.buffer = []


interp.register_command(interp.cmd_type('replay', do_replay, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
