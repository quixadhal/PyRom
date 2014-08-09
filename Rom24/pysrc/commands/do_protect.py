import logging

logger = logging.getLogger()

import merc
import interp
import state_checks
import handler_game

def do_protect(ch, argument):
    if not argument:
        ch.send("Protect whom from snooping?\n")
        return
    victim = ch.get_char_world(argument)
    if not victim:
        ch.send("You can't find them.\n")
        return
    if victim.comm.is_set(merc.COMM_SNOOP_PROOF):
        handler_game.act("$N is no longer snoop-proof.", ch, None, victim, merc.TO_CHAR, merc.POS_DEAD)
        victim.send("Your snoop-proofing was just removed.\n")
        victim.comm = state_checks.REMOVE_BIT(victim.comm, merc.COMM_SNOOP_PROOF)
    else:
        handler_game.act("$N is now snoop-proof.", ch, None, victim, merc.TO_CHAR, merc.POS_DEAD)
        victim.send("You are now immune to snooping.\n")
        victim.comm = state_checks.SET_BIT(victim.comm, merc.COMM_SNOOP_PROOF)


interp.register_command(interp.cmd_type('protect', do_protect, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1))
