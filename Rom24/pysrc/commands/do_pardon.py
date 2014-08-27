import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_pardon(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    if not arg1 or not arg2:
        ch.send("Syntax: pardon <character> <killer|thief>.\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    if arg2 == "killer":
        if victim.act.is_set(merc.PLR_KILLER):
            victim.act = victim.act.rem_bit(merc.PLR_KILLER)
            ch.send("Killer flag removed.\n")
            victim.send("You are no longer a KILLER.\n")
        return
    if arg2 == "thief":
        if victim.act.is_set(merc.PLR_THIEF):
            victim.act = victim.act.rem_bit(merc.PLR_THIEF)
            ch.send("Thief flag removed.\n")
            victim.send("You are no longer a THIEF.\n")
        return
    ch.send("Syntax: pardon <character> <killer|thief>.\n")
    return


interp.register_command(interp.cmd_type('pardon', do_pardon, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1))
