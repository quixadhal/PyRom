import logging

logger = logging.getLogger()

import merc
import interp
import state_checks

def do_nosummon(ch, argument):
    if state_checks.IS_NPC(ch):
        if state_checks.IS_SET(ch.imm_flags, merc.IMM_SUMMON):
            ch.send("You are no longer immune to summon.\n")
            ch.imm_flags = state_checks.REMOVE_BIT(ch.imm_flags, merc.IMM_SUMMON)
        else:
            ch.send("You are now immune to summoning.\n")
            ch.imm_flags = state_checks.SET_BIT(ch.imm_flags, merc.IMM_SUMMON)
    else:
        if state_checks.IS_SET(ch.act, merc.PLR_NOSUMMON):
            ch.send("You are no longer immune to summon.\n")
            ch.act = state_checks.REMOVE_BIT(ch.act, merc.PLR_NOSUMMON)
        else:
            ch.send("You are now immune to summoning.\n")
            ch.act = state_checks.SET_BIT(ch.act, merc.PLR_NOSUMMON)


interp.register_command(interp.cmd_type('nosummon', do_nosummon, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
