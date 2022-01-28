import random
import logging

logger = logging.getLogger(__name__)

from rom24 import state_checks
from rom24 import merc
from rom24 import fight
from rom24 import const
from rom24 import interp


def do_kick(ch, argument):
    if (
        not ch.is_npc()
        and ch.level < const.skill_table["kick"].skill_level[ch.guild.name]
    ):
        ch.send("You better leave the martial arts to fighters.\n")
        return
    if ch.is_npc() and not ch.off_flags.is_set(merc.OFF_KICK):
        return
    victim = ch.fighting
    if not victim:
        ch.send("You aren't fighting anyone.\n")
        return

    state_checks.WAIT_STATE(ch, const.skill_table["kick"].beats)
    if ch.get_skill("kick") > random.randint(1, 99):
        fight.damage(
            ch, victim, random.randint(1, ch.level), "kick", merc.DAM_BASH, True
        )
        if ch.is_pc:
            ch.check_improve("kick", True, 1)
    else:
        fight.damage(ch, victim, 0, "kick", merc.DAM_BASH, True)
        if ch.is_pc:
            ch.check_improve("kick", False, 1)
    fight.check_killer(ch, victim)
    return


interp.register_command(
    interp.cmd_type("kick", do_kick, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)
)
