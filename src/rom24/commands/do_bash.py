import random
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import handler_game
from rom24 import merc
from rom24 import const
from rom24 import fight
from rom24 import interp
from rom24 import state_checks


def do_bash(ch, argument):
    arghold, arg = game_utils.read_word(argument)
    chance = ch.get_skill("bash")
    if (
        chance == 0
        or (ch.is_npc() and not ch.off_flags.is_set(merc.OFF_BASH))
        or (
            not ch.is_npc()
            and ch.level < const.skill_table["bash"].skill_level[ch.guild.name]
        )
    ):
        ch.send("Bashing? What's that?\n\r")
        return
    victim = None
    if not arg:
        victim = ch.fighting
        if not victim:
            ch.send("But you aren't fighting anyone!\n")
            return
    else:
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
    if victim.position < merc.POS_FIGHTING:
        handler_game.act(
            "You'll have to let $M get back up first.", ch, None, victim, merc.TO_CHAR
        )
        return
    if victim == ch:
        ch.send("You try to bash your brains out, but fail.\n")
        return
    if fight.is_safe(ch, victim):
        return
    if victim.is_npc() and victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
        handler_game.act("But $N is your friend!", ch, None, victim, merc.TO_CHAR)
        return

    # modifiers
    # size and weight
    chance += ch.carry_weight // 250
    chance -= victim.carry_weight // 200
    if ch.size < victim.size:
        chance += (ch.size - victim.size) * 15
    else:
        chance += (ch.size - victim.size) * 10
    # stats
    chance += ch.stat(merc.STAT_STR)
    chance -= (victim.stat(merc.STAT_DEX) * 4) // 3
    chance -= state_checks.GET_AC(victim, merc.AC_BASH) // 25
    # speed */
    if (ch.is_npc() and ch.off_flags.is_set(merc.OFF_FAST)) or ch.is_affected(
        merc.AFF_HASTE
    ):
        chance += 10
    if (
        victim.is_npc() and victim.off_flags.is_set(merc.OFF_FAST)
    ) or victim.is_affected(merc.AFF_HASTE):
        chance -= 30
    # level
    chance += ch.level - victim.level
    if not victim.is_npc() and chance < victim.get_skill("dodge"):
        pass
        # act("$n tries to bash you, but you dodge it.",ch,None,victim,TO_VICT)
        # act("$N dodges your bash, you fall flat on your face.",ch,None,victim,TO_CHAR)
        # WAIT_STATE(ch,const.skill_table['bash'].beats)
        # return
        chance -= 3 * (victim.get_skill("dodge") - chance)
    # now the attack */
    if random.randint(1, 99) < chance:
        handler_game.act(
            "$n sends you sprawling with a powerful bash!",
            ch,
            None,
            victim,
            merc.TO_VICT,
        )
        handler_game.act(
            "You slam into $N, and send $M flying!", ch, None, victim, merc.TO_CHAR
        )
        handler_game.act(
            "$n sends $N sprawling with a powerful bash.",
            ch,
            None,
            victim,
            merc.TO_NOTVICT,
        )
        if not ch.is_npc():
            if ch.is_pc:
                ch.check_improve("bash", True, 1)
        state_checks.DAZE_STATE(victim, 3 * merc.PULSE_VIOLENCE)
        state_checks.WAIT_STATE(ch, const.skill_table["bash"].beats)
        victim.position = merc.POS_RESTING
        fight.damage(
            ch,
            victim,
            random.randint(2, 2 + 2 * ch.size + chance // 20),
            "bash",
            merc.DAM_BASH,
            False,
        )
    else:
        fight.damage(ch, victim, 0, "bash", merc.DAM_BASH, False)
        handler_game.act("You fall flat on your face!", ch, None, victim, merc.TO_CHAR)
        handler_game.act("$n falls flat on $s face.", ch, None, victim, merc.TO_NOTVICT)
        handler_game.act(
            "You evade $n's bash, causing $m to fall flat on $s face.",
            ch,
            None,
            victim,
            merc.TO_VICT,
        )
        if not ch.is_npc():
            if ch.is_pc:
                ch.check_improve("bash", False, 1)
        ch.position = merc.POS_RESTING
        state_checks.WAIT_STATE(ch, const.skill_table["bash"].beats * 3 // 2)
    fight.check_killer(ch, victim)


interp.register_command(
    interp.cmd_type("bash", do_bash, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)
)
