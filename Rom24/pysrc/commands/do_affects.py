import logging

logger = logging.getLogger()

import merc
import interp


def do_affects(ch, argument):
    paf_last = None
    if ch.affected:
        ch.send("You are affected by the following spells:\n")
        for paf in ch.affected:
            if paf_last and paf.type == paf_last.type:
                if ch.level >= 20:
                    ch.send("                      ")
                else:
                    continue
            else:
                ch.send("Spell: %-15s" % paf.type.name)
            if ch.level >= 20:
                ch.send(": modifies %s by %d " % (merc.affect_loc_name(paf.location), paf.modifier))
            if paf.duration == -1:
                ch.send("permanently")
            else:
                ch.send("for %d hours" % paf.duration)
            ch.send("\n")
            paf_last = paf
    else:
        ch.send("You are not affected by any spells.\n")


interp.register_command(interp.cmd_type('affects', do_affects, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
