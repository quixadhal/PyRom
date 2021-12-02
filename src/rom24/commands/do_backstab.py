import random
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import merc
from rom24 import fight
from rom24 import const
from rom24 import state_checks
from rom24 import interp
from rom24 import handler_game


def do_backstab(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Backstab whom?\n")
        return
    victim = None
    if ch.fighting:
        ch.send("You're facing the wrong end.\n")
        return
    else:
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("How can you sneak up on yourself?\n")
            return
        if fight.is_safe(ch, victim):
            return
        if (
            victim.is_npc()
            and victim.fighting
            and not ch.is_same_group(victim.fighting)
        ):
            ch.send("Kill stealing is not permitted.\n")
            return
        item = ch.get_eq("main_hand")
        if not item:
            ch.send("You need to wield a weapon to backstab.\n")
            return
        if victim.hit < victim.max_hit // 3:
            handler_game.act(
                "$N is hurt and suspicious ... you can't sneak up.",
                ch,
                None,
                victim,
                merc.TO_CHAR,
            )
            return
        fight.check_killer(ch, victim)
        state_checks.WAIT_STATE(ch, const.skill_table["backstab"].beats)
        if random.randint(1, 99) < ch.get_skill("backstab") or (
            ch.get_skill("backstab") >= 2 and not state_checks.IS_AWAKE(victim)
        ):
            if ch.is_pc:
                ch.check_improve("backstab", True, 1)
            fight.multi_hit(ch, victim, "backstab")
        else:
            if ch.is_pc:
                ch.check_improve("backstab", False, 1)
            fight.damage(ch, victim, 0, "backstab", merc.DAM_NONE, True)
    return


interp.register_command(
    interp.cmd_type("backstab", do_backstab, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)
)
interp.register_command(
    interp.cmd_type("bs", do_backstab, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0)
)
