import logging

logger = logging.getLogger()

# changes your scroll
import merc
import interp


def do_scroll(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        if ch.lines == 0:
            ch.send("You do not page long messages.\n")
        else:
            ch.send("You currently display %d lines per page.\n" % (
                ch.lines + 2))
        return
    if not arg.isdigit():
        ch.send("You must provide a number.\n")
        return
    lines = int(arg)
    if lines == 0:
        ch.send("Paging disabled.\n")
        ch.lines = 0
        return
    if lines < 10 or lines > 100:
        ch.send("You must provide a reasonable number.\n")
        return
    ch.send("Scroll set to %d lines.\n" % lines)
    ch.lines = lines - 2


interp.register_command(interp.cmd_type('scroll', do_scroll, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
