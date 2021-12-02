import logging

logger = logging.getLogger(__name__)

from rom24 import handler_game
from rom24 import merc
from rom24 import interp
from rom24 import instance


def do_train(ch, argument):
    stat = -1
    pOutput = ""
    if ch.is_npc():
        return
    trainer = None
    for mob_id in ch.in_room.people:
        mob = instance.characters[mob_id]
        if mob.is_npc() and mob.act.is_set(merc.ACT_TRAIN):
            trainer = mob

    if not trainer:
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
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.perm_hit += 10
        ch.max_hit += 10
        ch.hit += 10
        handler_game.act("Your durability increases!", ch, None, None, merc.TO_CHAR)
        handler_game.act("$n's durability increases!", ch, None, None, merc.TO_ROOM)
        return
    elif argument == "mana":
        cost = 1
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.perm_mana += 10
        ch.max_mana += 10
        ch.mana += 10
        handler_game.act("Your power increases!", ch, None, None, merc.TO_CHAR)
        handler_game.act("$n's power increases!", ch, None, None, merc.TO_ROOM)
        return
    else:
        ch.send("You can train:")
        if ch.perm_stat[merc.STAT_STR] < ch.get_max_train(merc.STAT_STR):
            ch.send(" str")
        if ch.perm_stat[merc.STAT_INT] < ch.get_max_train(merc.STAT_INT):
            ch.send(" int")
        if ch.perm_stat[merc.STAT_WIS] < ch.get_max_train(merc.STAT_WIS):
            ch.send(" wis")
        if ch.perm_stat[merc.STAT_DEX] < ch.get_max_train(merc.STAT_DEX):
            ch.send(" dex")
        if ch.perm_stat[merc.STAT_CON] < ch.get_max_train(merc.STAT_CON):
            ch.send(" con")
        ch.send(" hp mana")
        return
    if ch.perm_stat[stat] >= ch.get_max_train(stat):
        handler_game.act(
            "Your $T is already at maximum.", ch, None, pOutput, merc.TO_CHAR
        )
        return
    if cost > ch.train:
        ch.send("You don't have enough training sessions.\n")
        return
    ch.train -= cost
    ch.perm_stat[stat] += 1
    handler_game.act("Your $T increases!", ch, None, pOutput, merc.TO_CHAR)
    handler_game.act("$n's $T increases!", ch, None, pOutput, merc.TO_ROOM)
    return


interp.register_command(
    interp.cmd_type("train", do_train, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
