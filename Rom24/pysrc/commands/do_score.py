import time
import logging

logger = logging.getLogger()

import state_checks
import merc
import interp


def do_score(ch, argument):
    ch.send("You are %s%s, level %d, %d years old (%d hours).\n" % (ch.name, "" if ch.is_npc() else ch.title,
                                                                    ch.level, ch.get_age(), (
    ch.played + (int)(time.time() - ch.logon)) // 3600))

    if ch.trust != ch.level:
        ch.send("You are trusted at level %d.\n" % ch.trust)
    ch.send("Race: %s  Sex: %s  Class: %s\n" % (
    ch.race.name, "sexless" if ch.sex == 0 else "male" if ch.sex == 1 else "female",
    "mobile" if ch.is_npc() else ch.guild.name))
    ch.send("You have %d/%d hit, %d/%d mana, %d/%d movement.\n" % (ch.hit, ch.max_hit,
                                                                   ch.mana, ch.max_mana, ch.move, ch.max_move))
    ch.send("You have %d practices and %d training sessions.\n" % (ch.practice, ch.train))
    ch.send("You are carrying %d/%d items with weight %ld/%d pounds.\n" % (ch.carry_number, ch.can_carry_n(),
                                                                           state_checks.get_carry_weight(ch) // 10,
                                                                           ch.can_carry_w() // 10))
    ch.send("Str: %d(%d)  Int: %d(%d)  Wis: %d(%d)  Dex: %d(%d)  Con: %d(%d)\n" % (
        ch.perm_stat[merc.STAT_STR], ch.stat(merc.STAT_STR),
        ch.perm_stat[merc.STAT_INT], ch.stat(merc.STAT_INT),
        ch.perm_stat[merc.STAT_WIS], ch.stat(merc.STAT_WIS),
        ch.perm_stat[merc.STAT_DEX], ch.stat(merc.STAT_DEX),
        ch.perm_stat[merc.STAT_CON], ch.stat(merc.STAT_CON)))

    ch.send("You have scored %d exp, and have %ld gold and %ld silver coins.\n" % (ch.exp, ch.gold, ch.silver))
    # RT shows exp to level
    if not ch.is_npc() and ch.level < merc.LEVEL_HERO:
        ch.send("You need %d exp to level.\n" % ((ch.level + 1) * ch.exp_per_level(ch.points) - ch.exp))
    ch.send("Wimpy set to %d hit points.\n" % ch.wimpy)
    if not ch.is_npc() and ch.condition[merc.COND_DRUNK] > 10:
        ch.send("You are drunk.\n")
    if not ch.is_npc() and ch.condition[merc.COND_THIRST] == 0:
        ch.send("You are thirsty.\n")
    if not ch.is_npc() and ch.condition[merc.COND_HUNGER] == 0:
        ch.send("You are hungry.\n")

    if ch.position == merc.POS_DEAD:
        ch.send("You are DEAD!!\n")
    elif ch.position == merc.POS_MORTAL:
        ch.send("You are mortally wounded.\n")
    elif ch.position == merc.POS_INCAP:
        ch.send("You are incapacitated.\n")
    elif ch.position == merc.POS_STUNNED:
        ch.send("You are stunned.\n")
    elif ch.position == merc.POS_SLEEPING:
        ch.send("You are sleeping.\n")
    elif ch.position == merc.POS_RESTING:
        ch.send("You are resting.\n")
    elif ch.position == merc.POS_SITTING:
        ch.send("You are sitting.\n")
    elif ch.position == merc.POS_STANDING:
        ch.send("You are standing.\n")
    elif ch.position == merc.POS_FIGHTING:
        ch.send("You are fighting.\n")
    # print AC values
    if ch.level >= 25:
        ch.send("Armor: pierce: %d  bash: %d  slash: %d  magic: %d\n" % (
            state_checks.GET_AC(ch, merc.AC_PIERCE),
            state_checks.GET_AC(ch, merc.AC_BASH),
            state_checks.GET_AC(ch, merc.AC_SLASH),
            state_checks.GET_AC(ch, merc.AC_EXOTIC)))
    for i in range(4):
        temp = ''
        if i == merc.AC_PIERCE:
            temp = "piercing"
        elif i == merc.AC_BASH:
            temp = "bashing"
        elif i == merc.AC_SLASH:
            temp = "slashing"
        elif i == merc.AC_EXOTIC:
            temp = "magic"
        else:
            temp = "error"
        ch.send("You are ")

        if state_checks.GET_AC(ch, i) >= 101:
            ch.send("hopelessly vulnerable to %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= 80:
            ch.send("defenseless against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= 60:
            ch.send("barely protected from %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= 40:
            ch.send("slightly armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= 20:
            ch.send("somewhat armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= 0:
            ch.send("armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= -20:
            ch.send("well-armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= -40:
            ch.send("very well-armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= -60:
            ch.send("heavily armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= -80:
            ch.send("superbly armored against %s.\n" % temp)
        elif state_checks.GET_AC(ch, i) >= -100:
            ch.send("almost invulnerable to %s.\n" % temp)
        else:
            ch.send("divinely armored against %s.\n" % temp)

    # RT wizinvis and holy light
    if ch.is_immortal():
        ch.send("Holy Light: ")
        if ch.act.is_set(merc.PLR_HOLYLIGHT):
            ch.send("on")
        else:
            ch.send("off")

        if ch.invis_level:
            ch.send("  Invisible: level %d" % ch.invis_level)
        if ch.incog_level:
            ch.send("  Incognito: level %d" % ch.incog_level)
        ch.send("\n")

    if ch.level >= 15:
        ch.send("Hitroll: %d  Damroll: %d.\n" % (state_checks.GET_HITROLL(ch), state_checks.GET_DAMROLL(ch)))
    if ch.level >= 10:
        ch.send("Alignment: %d.  " % ch.alignment)
    ch.send("You are ")
    if ch.alignment > 900:
        ch.send("angelic.\n")
    elif ch.alignment > 700:
        ch.send("saintly.\n")
    elif ch.alignment > 350:
        ch.send("good.\n")
    elif ch.alignment > 100:
        ch.send("kind.\n")
    elif ch.alignment > -100:
        ch.send("neutral.\n")
    elif ch.alignment > -350:
        ch.send("mean.\n")
    elif ch.alignment > -700:
        ch.send("evil.\n")
    elif ch.alignment > -900:
        ch.send("demonic.\n")
    else:
        ch.send("satanic.\n")

    if ch.comm.is_set(merc.COMM_SHOW_AFFECTS):
        ch.do_affects("")


interp.register_command(interp.cmd_type('score', do_score, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
