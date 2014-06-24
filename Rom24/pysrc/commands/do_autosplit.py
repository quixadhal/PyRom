import merc
import interp


def do_autosplit(ch, argument):
    if merc.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOSPLIT):
        ch.send("Autosplitting removed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOSPLIT)
    else:
        ch.send("Automatic gold splitting set.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOSPLIT)

interp.cmd_table['autosplit'] = interp.cmd_type('autosplit', do_autosplit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)