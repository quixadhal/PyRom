import merc
import interp


def do_autoexit(ch, argument):
    if merc.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOEXIT):
        ch.send("Exits will no longer be displayed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOEXIT)
    else:
        ch.send("Exits will now be displayed.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOEXIT)

interp.cmd_table['autoexit'] = interp.cmd_type('autoexit', do_autoexit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
