import merc
import interp


def do_memory(ch, argument):
    pass

interp.cmd_type('memory', do_memory, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)