import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks

def do_smote(ch, argument):
    matches = 0
    if not ch.is_npc() and ch.comm.is_set(merc.COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    if ch.name not in argument:
        ch.send("You must include your name in an smote.\n")
        return
    ch.send(argument + "\n")
    for vch in merc.rooms[ch.in_room].people:
        if vch.desc == None or vch == ch:
            continue
        if vch.name not in argument:
            vch.send(argument + "\n")
            continue
        buf = game_utils.mass_replace({"%s's" % vch.name: 'your', vch.name: 'you'})
        vch.send(buf + "\n")
    return


interp.register_command(interp.cmd_type('smote', do_smote, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
