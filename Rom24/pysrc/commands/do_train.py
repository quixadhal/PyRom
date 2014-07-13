import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_train(ch, argument):
    stat = -1
    pOutput = ""
    if ch.is_npc():
        return

        # Check for trainer.
    trainers = [mob for mob in merc.rooms[ch.in_room].people if state_checks.IS_NPC(mob) and state_checks.IS_SET(mob.act, merc.ACT_TRAIN)]
    if not trainers:
        ch.send("You can't do that here.\n")
        return
    if not argument:
        ch.send("You have %d training sessions.\n" % ch.train)
        argument = "foo"
    cost = 1
    if argument == "str":
        if ch.guild.attr_prime == merc.STAT_STR:
            cost = 1
        stat = merc.STAT_STR
        pOutput = "strength"
    elif argument == "int":
        if ch.guild.attr_prime == merc.STAT_INT:
            cost = 1
        stat = merc.STAT_INT
        pOutput = "intelligence"
    elif argument == "wis":
        if ch.guild.attr_prime == merc.STAT_WIS:
            cost = 1
        stat = merc.STAT_WIS
        pOutput = "wisdom"
    elif argument == "dex":
        if ch.guild.attr_prime == merc.STAT_DEX:
            cost = 1
        stat = merc.STAT_DEX
        pOutput = "dexterity"
    elif argument == "con":
        if ch.guild.attr_prime == merc.STAT_CON:
            cost = 1
        stat = merc.STAT_CON
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
        ch.perm_hit += 10
        ch.max_hit += 10
        ch.hit += 10
        act("Your durability increases!", ch, None, None, merc.TO_CHAR)
        act("$n's durability increases!", ch, None, None, merc.TO_ROOM)
        return
    elif "mana" == argument:
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.perm_mana += 10
        ch.max_mana += 10
        ch.mana += 10
        act("Your power increases!", ch, None, None, merc.TO_CHAR)
        act("$n's power increases!", ch, None, None, merc.TO_ROOM)
        return
    else:
        ch.send("You can train:")
        if ch.perm_stat[merc.STAT_STR] < ch.get_max_train(merc.STAT_STR): ch.send(" str")
        if ch.perm_stat[merc.STAT_INT] < ch.get_max_train(merc.STAT_INT): ch.send(" int")
        if ch.perm_stat[merc.STAT_WIS] < ch.get_max_train(merc.STAT_WIS): ch.send(" wis")
        if ch.perm_stat[merc.STAT_DEX] < ch.get_max_train(merc.STAT_DEX): ch.send(" dex")
        if ch.perm_stat[merc.STAT_CON] < ch.get_max_train(merc.STAT_CON): ch.send(" con")
        ch.send(" hp mana")
        return
    if ch.perm_stat[stat] >= ch.get_max_train(stat):
        act("Your $T is already at maximum.", ch, None, pOutput, merc.TO_CHAR)
        return
    if cost > ch.train:
        ch.send("You don't have enough training sessions.\n")
        return
    ch.train -= cost
    ch.perm_stat[stat] += 1
    act("Your $T increases!", ch, None, pOutput, merc.TO_CHAR)
    act("$n's $T increases!", ch, None, pOutput, merc.TO_ROOM)
    return


interp.register_command(interp.cmd_type('train', do_train, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
