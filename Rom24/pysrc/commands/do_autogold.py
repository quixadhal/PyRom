import merc
import interp


def do_autogold(ch, argument):
    if merc.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOGOLD):
        ch.send("Autogold removed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOGOLD)
    else:
        ch.send("Automatic gold looting set.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOGOLD)

interp.cmd_type('autogold', do_autogold, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)