import merc
import interp
import state_checks


def do_autosac(ch, argument):
    if state_checks.IS_NPC(ch):
        return
    if state_checks.IS_SET(ch.act, merc.PLR_AUTOSAC):
        ch.send("Autosacrificing removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOSAC)
    else:
        ch.send("Automatic corpse sacrificing set.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOSAC)

interp.cmd_type('autosac', do_autosac, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
