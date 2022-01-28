import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import const
from rom24 import interp
from rom24 import game_utils
from rom24 import state_checks


def do_slookup(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Lookup which skill or spell?\n")
        return
    if arg == "all":
        for sn, skill in const.skill_table.items():
            ch.send(
                "Sn: %15s  Slot: %3d  Skill/spell: '%s'\n"
                % (sn, skill.slot, skill.name)
            )
    else:
        skill = state_checks.prefix_lookup(const.skill_table, arg)
        if not skill:
            ch.send("No such skill or spell.\n")
            return

        ch.send(
            "Sn: %15s  Slot: %3d  Skill/spell: '%s'\n"
            % (skill.name, skill.slot, skill.name)
        )


interp.register_command(
    interp.cmd_type("slookup", do_slookup, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)
)
