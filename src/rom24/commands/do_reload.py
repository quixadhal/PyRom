import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import nanny
from rom24 import hotfix
from rom24 import interp


def do_reload(ch, argument):
    hotfix.reload_files(ch)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing):
            if d.character.trust <= ch.trust:
                d.send(f"imp> {ch.name} reloaded files.")


interp.register_command(
    interp.cmd_type("reload", do_reload, merc.POS_DEAD, merc.ML, merc.LOG_NORMAL, 1)
)
