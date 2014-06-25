import merc
import interp


def do_autoloot(ch, argument):
    if merc.IS_NPC(ch):
        return

    if merc.IS_SET(ch.act, merc.PLR_AUTOLOOT):
        ch.send("Autolooting removed.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_AUTOLOOT)
    else:
        ch.send("Automatic corpse looting set.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_AUTOLOOT)

interp.cmd_table['autoloot'] = interp.cmd_type('autoloot', do_autoloot, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
