import merc
import interp


def do_protect(ch, argument):
    if not argument:
        ch.send("Protect whom from snooping?\n")
        return
    victim = ch.get_char_world(argument)
    if not victim:
        ch.send("You can't find them.\n")
        return
    if merc.IS_SET(victim.comm, merc.COMM_SNOOP_PROOF):
        merc.act("$N is no longer snoop-proof.", ch, None, merc.victim, merc.TO_CHAR, merc.POS_DEAD)
        victim.send("Your snoop-proofing was just removed.\n")
        victim.comm = merc.REMOVE_BIT(victim.comm, merc.COMM_SNOOP_PROOF)
    else:
        merc.act("$N is now snoop-proof.", ch, None, victim, merc.TO_CHAR, merc.POS_DEAD)
        victim.send("You are now immune to snooping.\n")
        victim.comm = merc.SET_BIT(victim.comm, merc.COMM_SNOOP_PROOF)

interp.cmd_table['protect'] = interp.cmd_type('protect', do_protect, merc.POS_DEAD, merc.L1, merc.LOG_ALWAYS, 1)