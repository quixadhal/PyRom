import logging

logger = logging.getLogger()

import handler_game
import merc
import interp
import game_utils
import instance


def do_pmote(ch, argument):
    if not ch.is_npc() and ch.comm.is_set(merc.COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    handler_game.act("$n $t", ch, argument, None, merc.TO_CHAR)
    for vch_id in ch.in_room.people:
        vch = instance.characters[vch_id]
        if vch.desc is None or vch == ch:
            continue
        if vch.name not in argument:
            handler_game.act("$N $t", vch, argument, ch, merc.TO_CHAR)
            continue
        temp = game_utils.mass_replace({vch.name: " you "}, argument)
        handler_game.act("$N $t", vch, temp, ch, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('pmote', do_pmote, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
