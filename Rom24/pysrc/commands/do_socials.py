import logging

logger = logging.getLogger()

import merc
import interp


# RT does socials
def do_socials(ch, argument):
    for col, social in enumerate(merc.social_list):
        ch.send("%-12s" % social.name)
        if col % 6 == 0:
            ch.send("\n")
    if len(merc.social_list) % 6 != 0:
        ch.send("\n")
    return


interp.register_command(interp.cmd_type('socials', do_socials, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
