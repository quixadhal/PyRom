import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp


def do_rent(ch, argument):
    ch.send("There is no rent here.  Just save and quit.\n")
    return


interp.register_command(
    interp.cmd_type("rent", do_rent, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0)
)
