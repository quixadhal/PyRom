import merc
import interp


def do_replay(ch, argument):
    if merc.IS_NPC(ch):
        ch.send("You can't replay.\n")
        return
    if not ch.pcdata.buffer:
        ch.send("You have no tells to replay.\n")
        return
    [ch.send(tell) for tell in ch.pcdata.buffer]
    ch.pcdata.buffer = []

interp.cmd_type('replay', do_replay, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1)