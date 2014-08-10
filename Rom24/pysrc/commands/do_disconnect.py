import logging

logger = logging.getLogger()

import merc
import interp
import comm
import game_utils
import handler_game


def do_disconnect(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Disconnect whom?\n")
        return
    if arg.isdigit():
        desc = int(arg)
        for d in merc.descriptor_list:
            if d.descriptor == desc:
                comm.close_socket(d)
                ch.send("Ok.\n")
                return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.desc is None:
        handler_game.act("$N doesn't have a descriptor.", ch, None, victim, merc.TO_CHAR)
        return
    for d in merc.descriptor_list:
        if d == victim.desc:
            comm.close_socket(d)
            ch.send("Ok.\n")
            return
    logger.warn("BUG: Do_disconnect: desc not found.")
    ch.send("Descriptor not found!\n")
    return


interp.register_command(interp.cmd_type('disconnect', do_disconnect, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1))
