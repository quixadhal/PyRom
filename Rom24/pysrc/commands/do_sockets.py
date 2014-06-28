import logging

logger = logging.getLogger()

import merc
import interp
import game_utils

def do_sockets(ch, argument):
    count = 0
    argument, arg = game_utils.read_word(argument)
    for d in merc.descriptor_list:
        if d.character and ch.can_see(d.character) \
                and (not arg or arg not in d.character.name) \
                or (d.original and game_utils.is_name(arg, d.original.name)):
            count += 1
            ch.send("%s@%s\n" % (
                d.original.name if d.original else d.character.name if d.character else "(none)",
                d.address))
    if count == 0:
        ch.send("No one by that name is connected.\n")
        return
    ch.send("%d user%s\n" % (count, "" if count == 1 else "s" ))
    return


interp.register_command(interp.cmd_type('sockets', do_sockets, merc.POS_DEAD, merc.L4, merc.LOG_NORMAL, 1))
