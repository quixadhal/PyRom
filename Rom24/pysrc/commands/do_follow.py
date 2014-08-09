import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_ch
import handler_game


def do_follow(ch, argument):
    # RT changed to allow unlimited following and follow the NOFOLLOW rules
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Follow whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if ch.is_affected(merc.AFF_CHARM) and ch.master:
        handler_game.act("But you'd rather follow $N!", ch, None, ch.master, merc.TO_CHAR)
        return
    if victim == ch:
        if ch.master is None:
            ch.send("You already follow yourself.\n")
            return
        handler_ch.stop_follower(ch)
        return
    if not victim.is_npc() \
            and victim.act.is_set(merc.PLR_NOFOLLOW) \
            and not ch.is_immortal():
        handler_game.act("$N doesn't seem to want any followers.\n", ch, None, victim, merc.TO_CHAR)
        return
    ch.act.rem_bit(merc.PLR_NOFOLLOW)
    if ch.master:
        handler_ch.stop_follower(ch)
    handler_ch.add_follower(ch, victim)
    return


interp.register_command(interp.cmd_type('follow', do_follow, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
