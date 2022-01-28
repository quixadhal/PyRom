import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import const
from rom24 import game_utils
from rom24 import state_checks


def do_sset(ch, argument):
    """Set a skill to a specific level.

    Example:

        <26hp 128m 454mv> sset bub dagger 100
        Skill set.

        <26hp 128m 454mv> skill

        Level  1: mace                 1%      trip                 1%
                backstab             1%      wands                1%
                dodge                1%      peek                 1%
                recall              50%      dagger             100%
                sword                1%      scrolls              1%
                staves               1%      hide                 1%
        Level  5: steal                1%
        Level 12: second attack        1%      disarm               1%
        Level  7: pick lock            1%
        Level  4: sneak                1%

        <26hp 128m 454mv>
    """
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    argument, arg3 = game_utils.read_word(argument)

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        ch.send("  set skill <name> all <value>\n")
        ch.send("   (use the name of the skill, not the number)\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    fAll = arg2 == "all"
    sn = state_checks.prefix_lookup(const.skill_table, arg2)
    if not fAll and not sn:
        ch.send("No such skill or spell.\n")
        return

    # Snarf the value.
    if not arg3.isdigit():
        ch.send("Value must be numeric.\n")
        return
    value = int(arg3)
    if value < 0 or value > 100:
        ch.send("Value range is 0 to 100.\n")
        return

    if fAll:
        for sn in const.skill_table.keys():
            victim.learned[sn] = value
    else:
        victim.learned[sn.name] = value
    ch.send("Skill set.\n")


interp.register_command(
    interp.cmd_type("sset", do_sset, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1)
)
