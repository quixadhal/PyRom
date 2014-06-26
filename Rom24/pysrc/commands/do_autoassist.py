import merc
import interp


def do_autoassist(ch, argument):
    if merc.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOASSIST):
        ch.send("Autoassist removed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOASSIST)
    else:
        ch.send("You will now assist when needed.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOASSIST)

interp.cmd_type('autoassist', do_autoassist, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)