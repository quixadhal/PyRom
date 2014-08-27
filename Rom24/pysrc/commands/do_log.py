import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks


def do_log(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Log whom?\n")
        return
    if arg == "all":
        #TODO: fix this by either adding it to merc, or figuring out an alternative
        if fLogAll:
            fLogAll = False
            ch.send("Log ALL off.\n")
        else:
            fLogAll = True
            ch.send("Log ALL on.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    # No level check, gods can log anyone.
    if victim.act.is_set(merc.PLR_LOG):
        victim.act = victim.act.rem_bit(merc.PLR_LOG)
        ch.send("LOG removed.\n")
    else:
        victim.act = state_checks.SET_BIT(victim.act, merc.PLR_LOG)
        ch.send("LOG set.\n")
    return


interp.register_command(interp.cmd_type('log', do_log, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1))
