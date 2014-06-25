import merc
import interp


def do_say(ch, argument):
    if not argument:
        ch.send("Say what?\n")
        return
    merc.act("$n says '$T'", ch, None, argument, merc.TO_ROOM)
    merc.act("You say '$T'", ch, None, argument, merc.TO_CHAR)
    return

interp.cmd_table['say'] = interp.cmd_type('say', do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
interp.cmd_table["'"] = interp.cmd_type("'", do_say, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)