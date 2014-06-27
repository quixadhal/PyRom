import logging

logger = logging.getLogger()

import merc
import interp


def do_pmote(ch, argument):
    if not merc.IS_NPC(ch) and merc.IS_SET(ch.comm, merc.COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    merc.act("$n $t", ch, argument, None, merc.TO_CHAR)
    for vch in ch.in_room.people:
        if vch.desc is None or vch == ch:
            continue
        if vch.name not in argument:
            merc.act("$N $t", vch, argument, ch, merc.TO_CHAR)
            continue
        temp = merc.mass_replace({vch.name: " you "}, argument)
        merc.act("$N $t", vch, temp, ch, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('pmote', do_pmote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
