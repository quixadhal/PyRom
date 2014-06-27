import logging

logger = logging.getLogger()

from interp import cmd_type, register_command
from merc import IS_NPC, IS_SET, ACT_TRAIN, STAT_STR, STAT_INT, STAT_WIS, STAT_DEX, STAT_CON, act, TO_CHAR, TO_ROOM, \
    POS_RESTING, LOG_NORMAL


def do_train(ch, argument):
    stat = -1
    pOutput = ""
    if IS_NPC(ch):
        return

        # Check for trainer.
    trainers = [mob for mob in ch.in_room.people if IS_NPC(mob) and IS_SET(mob.act, ACT_TRAIN)]
    if not trainers:
        ch.send("You can't do that here.\n")
        return
    if not argument:
        ch.send("You have %d training sessions.\n" % ch.train)
        argument = "foo"
    cost = 1
    if argument == "str":
        if ch.guild.attr_prime == STAT_STR:
            cost = 1
        stat = STAT_STR
        pOutput = "strength"
    elif argument == "int":
        if ch.guild.attr_prime == STAT_INT:
            cost = 1
        stat = STAT_INT
        pOutput = "intelligence"
    elif argument == "wis":
        if ch.guild.attr_prime == STAT_WIS:
            cost = 1
        stat = STAT_WIS
        pOutput = "wisdom"
    elif argument == "dex":
        if ch.guild.attr_prime == STAT_DEX:
            cost = 1
        stat = STAT_DEX
        pOutput = "dexterity"
    elif argument == "con":
        if ch.guild.attr_prime == STAT_CON:
            cost = 1
        stat = STAT_CON
        pOutput = "constitution"
    elif argument == "hp":
        cost = 1
    elif argument == "mana":
        cost = 1
    elif "hp" == argument:
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.pcdata.perm_hit += 10
        ch.max_hit += 10
        ch.hit += 10
        act("Your durability increases!", ch, None, None, TO_CHAR)
        act("$n's durability increases!", ch, None, None, TO_ROOM)
        return
    elif "mana" == argument:
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.pcdata.perm_mana += 10
        ch.max_mana += 10
        ch.mana += 10
        act("Your power increases!", ch, None, None, TO_CHAR)
        act("$n's power increases!", ch, None, None, TO_ROOM)
        return
    else:
        ch.send("You can train:")
        if ch.perm_stat[STAT_STR] < ch.get_max_train(STAT_STR): ch.send(" str")
        if ch.perm_stat[STAT_INT] < ch.get_max_train(STAT_INT): ch.send(" int")
        if ch.perm_stat[STAT_WIS] < ch.get_max_train(STAT_WIS): ch.send(" wis")
        if ch.perm_stat[STAT_DEX] < ch.get_max_train(STAT_DEX): ch.send(" dex")
        if ch.perm_stat[STAT_CON] < ch.get_max_train(STAT_CON): ch.send(" con")
        ch.send(" hp mana")
        return
    if ch.perm_stat[stat] >= ch.get_max_train(stat):
        act("Your $T is already at maximum.", ch, None, pOutput, TO_CHAR)
        return
    if cost > ch.train:
        ch.send("You don't have enough training sessions.\n")
        return
    ch.train -= cost
    ch.perm_stat[stat] += 1
    act("Your $T increases!", ch, None, pOutput, TO_CHAR)
    act("$n's $T increases!", ch, None, pOutput, TO_ROOM)
    return


register_command(cmd_type('train', do_train, POS_RESTING, 0, LOG_NORMAL, 1))
