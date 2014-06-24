import merc
import interp


def do_nosummon(ch, argument):
    if merc.IS_NPC(ch):
        if merc.IS_SET(ch.imm_flags, merc.IMM_SUMMON):
            ch.send("You are no longer immune to summon.\n")
            ch.imm_flags = merc.REMOVE_BIT(ch.imm_flags, merc.IMM_SUMMON)
        else:
            ch.send("You are now immune to summoning.\n")
            ch.imm_flags = merc.SET_BIT(ch.imm_flags, merc.IMM_SUMMON)
    else:
        if merc.IS_SET(ch.act, merc.PLR_NOSUMMON):
            ch.send("You are no longer immune to summon.\n")
            ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_NOSUMMON)
        else:
            ch.send("You are now immune to summoning.\n")
            ch.act = merc.SET_BIT(ch.act, merc.PLR_NOSUMMON)

interp.cmd_table['nosummon'] = interp.cmd_type('nosummon', do_nosummon, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)