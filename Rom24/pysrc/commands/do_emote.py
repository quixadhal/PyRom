import merc
import interp


def do_emote(ch, argument):
    if not merc.IS_NPC(ch) and merc.IS_SET(ch.comm, merc.COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    merc.act("$n $T", ch, None, argument, merc.TO_ROOM)
    merc.act("$n $T", ch, None, argument, merc.TO_CHAR)
    return

interp.cmd_type('emote', do_emote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
interp.cmd_table[','] = interp.cmd_type(',', do_emote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)
