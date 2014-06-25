import merc
import interp


def do_noloot(ch, argument):
    if merc.IS_NPC(ch):
        return
    if merc.IS_SET(ch.act, merc.PLR_CANLOOT):
        ch.send("Your corpse is now safe from thieves.\n")
        ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_CANLOOT)
    else:
        ch.send("Your corpse may now be looted.\n")
        ch.act = merc.SET_BIT(ch.act, merc.PLR_CANLOOT)

interp.cmd_table['noloot'] = interp.cmd_type('noloot', do_noloot, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)