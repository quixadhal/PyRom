import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import instance


def do_smote(ch, argument):
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
    for vch_id in ch.in_room.people:
        vch = instance.characters[vch_id]
        if vch.desc is None or vch == ch:
            continue
        if vch.name not in argument:
            vch.send(argument + "\n")
            continue
        buf = game_utils.mass_replace({"%s's" % vch.name: "your", vch.name: "you"})
        vch.send(buf + "\n")
    return


interp.register_command(
    interp.cmd_type("smote", do_smote, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)
)
