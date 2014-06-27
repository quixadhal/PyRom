import merc
import interp


def do_prefix(ch, argument):
    if not argument:
        if not ch.prefix:
            ch.send("You have no prefix to clear.\r\n")
            return
        ch.send("Prefix removed.\r\n")
        ch.prefix = ""
        return
    if ch.prefix:
        ch.send("Prefix changed to %s.\r\n" % argument)
        ch.prefix = ""
    else:
        ch.send("Prefix set to %s.\r\n" % argument)
    ch.prefix = argument

interp.cmd_type('prefix', do_prefix, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)