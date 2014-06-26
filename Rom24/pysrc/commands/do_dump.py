import merc
import interp


def do_dump(ch,argument):
    pass

interp.cmd_type('dump', do_dump, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 0)