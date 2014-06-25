import merc
import interp


def do_follow(ch, argument):
# RT changed to allow unlimited following and follow the NOFOLLOW rules */
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Follow whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master:
        merc.act("But you'd rather follow $N!", ch, None, ch.master, merc.TO_CHAR)
        return
    if victim == ch:
        if ch.master == None:
            ch.send("You already follow yourself.\n")
            return
        merc.stop_follower(ch)
        return
    if not merc.IS_NPC(victim) and merc.IS_SET(victim.act, merc.PLR_NOFOLLOW) and not merc.IS_IMMORTAL(ch):
        merc.act("$N doesn't seem to want any followers.\n", ch, None, victim, merc.TO_CHAR)
        return
    ch.act = merc.REMOVE_BIT(ch.act, merc.PLR_NOFOLLOW)
    if ch.master:
        merc.stop_follower(ch)
    merc.add_follower(ch, victim)
    return

interp.cmd_table['follow'] = interp.cmd_type('follow', do_follow, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)