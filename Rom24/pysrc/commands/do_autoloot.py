import merc
import interp
import state_checks


def do_autoloot(ch, argument):
    if state_checks.IS_NPC(ch):
        return

    if state_checks.IS_SET(ch.act, merc.PLR_AUTOLOOT):
        ch.send("Autolooting removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOLOOT)
    else:
        ch.send("Automatic corpse looting set.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOLOOT)

interp.cmd_type('autoloot', do_autoloot, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
