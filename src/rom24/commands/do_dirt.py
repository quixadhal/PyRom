import random
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import handler_game
from rom24 import state_checks
from rom24 import merc
from rom24 import const
from rom24 import interp
from rom24 import fight


def do_dirt(ch, argument):
    arghold, arg = game_utils.read_word(argument)
    chance = ch.get_skill("dirt kicking")
    if (
        chance == 0
        or (ch.is_npc() and not ch.off_flags.is_set(merc.OFF_KICK_DIRT))
        or (
            not ch.is_npc()
            and ch.level < const.skill_table["dirt kicking"].skill_level[ch.guild.name]
        )
    ):
        ch.send("You get your feet dirty.\n")
        return
    if not arg:
        victim = ch.fighting
        if victim is None:
            ch.send("But you aren't in combat!\n")
            return
    else:
        victim = ch.get_char_room(arg)
        if victim is None:
            ch.send("They aren't here.\n")
            return
    if victim.is_affected(merc.AFF_BLIND):
        handler_game.act("$E's already been blinded.", ch, None, victim, merc.TO_CHAR)
        return
    if victim == ch:
        ch.send("Very funny.\n")
        return
    if fight.is_safe(ch, victim):
        return
    if (
        victim.is_npc()
        and victim.fighting is not None
        and not ch.is_same_group(victim.fighting)
    ):
        ch.send("Kill stealing is not permitted.\n")
        return
    if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
        handler_game.act(
            "But $N is such a good friend!", ch, None, victim, merc.TO_CHAR
        )
        return

    # modifiers
    # dexterity
    chance += ch.stat(merc.STAT_DEX)
    chance -= 2 * victim.stat(merc.STAT_DEX)

    # speed
    if (ch.is_npc() and ch.off_flags.is_set(merc.OFF_FAST)) or ch.is_affected(
        merc.AFF_HASTE
    ):
        chance += 10
    if (
        victim.is_npc() and victim.off_flags.is_set(merc.OFF_FAST)
    ) or victim.is_affected(merc.AFF_HASTE):
        chance -= 25
    # level
    chance += (ch.level - victim.level) * 2

    # sloppy hack to prevent false zeroes
    if chance % 5 == 0:
        chance += 1
    # terrain
    nochance = [merc.SECT_WATER_SWIM, merc.SECT_WATER_NOSWIM, merc.SECT_AIR]
    modifiers = {
        merc.SECT_INSIDE: -20,
        merc.SECT_CITY: -10,
        merc.SECT_FIELD: 5,
        merc.SECT_MOUNTAIN: -10,
        merc.SECT_DESERT: 10,
    }
    if ch.in_room.sector_type in nochance:
        chance = 0
    elif ch.in_room.sector_type in modifiers:
        chance += modifiers[ch.in_room.sector_type]

    if chance == 0:
        ch.send("There isn't any dirt to kick.\n")
        return
    # now the attack
    if random.randint(1, 99) < chance:
        handler_game.act(
            "$n is blinded by the dirt in $s eyes!", victim, None, None, merc.TO_ROOM
        )
        handler_game.act("$n kicks dirt in your eyes!", ch, None, victim, merc.TO_VICT)
        fight.damage(
            ch, victim, random.randint(2, 5), "dirt kicking", merc.DAM_NONE, False
        )
        victim.send("You can't see a thing!\n")
        if ch.is_pc:
            ch.check_improve("dirt kicking", True, 2)
        state_checks.WAIT_STATE(ch, const.skill_table["dirt kicking"].beats)
        af = handler_game.AFFECT_DATA()
        af.where = merc.TO_AFFECTS
        af.type = "dirt kicking"
        af.level = ch.level
        af.duration = 0
        af.location = merc.APPLY_HITROLL
        af.modifier = -4
        af.bitvector = merc.AFF_BLIND
        victim.affect_add(af)
    else:
        fight.damage(ch, victim, 0, "dirt kicking", merc.DAM_NONE, True)
        if ch.is_pc:
            ch.check_improve("dirt kicking", False, 2)
        state_checks.WAIT_STATE(ch, const.skill_table["dirt kicking"].beats)
    fight.check_killer(ch, victim)


interp.register_command(
    interp.cmd_type("dirt", do_dirt, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)
)
