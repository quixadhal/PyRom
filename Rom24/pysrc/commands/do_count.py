import logging

logger = logging.getLogger()

import handler_ch
import merc
import interp
import nanny

#TODO: Known broken
# for  keeping track of the player count
max_on = 0


def do_count(ch, argument):
    global max_on
    count = len([d for d in merc.descriptor_list if d.is_connected(nanny.con_playing) and ch.can_see(handler_ch.CH(d))])
    max_on = max(count, max_on)

    if max_on == count:
        ch.send("There are %d characters on, the most so far today.\n" % count)
    else:
        ch.send("There are %d characters on, the most on today was %d.\n" % (count, max_on))


interp.register_command(interp.cmd_type('count', do_count, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
