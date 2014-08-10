import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game

def do_mload(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg or not arg.isdigit():
        ch.send("Syntax: load mob <vnum>.\n")
        return
    vnum = int(arg)
    if vnum not in merc.characterTemplate:
        ch.send("No mob has that vnum.\n")
        return
    pMobIndex = merc.characterTemplate[vnum]
    victim = instancer.create_mobile(pMobIndex)
    victim.to_environment(ch.in_room)
    handler_game.act("$n has created $N!", ch, None, victim, merc.TO_ROOM)
    handler_game.wiznet("$N loads %s." % victim.short_descr, ch, None, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.trust)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('mload', do_mload, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
