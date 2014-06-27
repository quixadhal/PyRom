import merc
import interp
import state_checks


def do_autoassist(ch, argument):
    if state_checks.IS_NPC(ch):
        return

    if state_checks.IS_SET(ch.act, merc.PLR_AUTOASSIST):
        ch.send("Autoassist removed.\n")
        ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_AUTOASSIST)
    else:
        ch.send("You will now assist when needed.\n")
        ch.act = state_checks.SET_BIT(ch.act, merc.PLR_AUTOASSIST)

interp.cmd_type('autoassist', do_autoassist, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
