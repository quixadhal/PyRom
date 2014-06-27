import logging

logger = logging.getLogger()

import merc
import interp
import nanny


# for  keeping track of the player count
def do_count(ch, argument):
    count = len([d for d in merc.descriptor_list if d.is_connected(nanny.con_playing) and ch.can_see(merc.CH(d))])
    merc.max_on = max(count, merc.max_on)

    if merc.max_on == count:
        ch.send("There are %d characters on, the most so far today.\n" % count)
    else:
        ch.send("There are %d characters on, the most on today was %d.\n" % (count, merc.max_on))


interp.register_command(interp.cmd_type('count', do_count, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
