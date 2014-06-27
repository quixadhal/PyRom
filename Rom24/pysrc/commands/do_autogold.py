import merc
import interp
import state_checks


def do_autogold(ch, argument):
    if state_checks.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOGOLD):
        ch.send("Autogold removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOGOLD)
    else:
        ch.send("Automatic gold looting set.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOGOLD)

interp.cmd_type('autogold', do_autogold, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
