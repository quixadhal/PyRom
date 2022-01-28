import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import db


def do_freset(ch, argument):
    if not ch.in_area:
        ch.send("You are not in an area. And that's really weird.\n")
        return
    db.reset_area(ch.in_area)
    ch.send("Area reset.\n")


interp.register_command(
    interp.cmd_type("freset", do_freset, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
)
