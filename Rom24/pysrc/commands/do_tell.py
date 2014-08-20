import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


def do_tell(ch, argument):
    if ch.comm.is_set(merc.COMM_NOTELL) or ch.comm.is_set(merc.COMM_DEAF):
        ch.send("Your message didn't get through.\n")
        return
    if ch.comm.is_set(merc.COMM_QUIET):
        ch.send("You must turn off quiet mode first.\n")
        return
    if ch.comm.is_set(merc.COMM_DEAF):
        ch.send("You must turn off deaf mode first.\n")
        return
    argument, arg = game_utils.read_word(argument)

    if not arg or not argument:
        ch.send("Tell whom what?\n")
        return
        # Can tell to PC's anywhere, but NPC's only in same room.
        # -- Furey
    victim = ch.get_char_world(arg)
    argument = argument.strip()
    if not victim or ( victim.is_npc() and victim.in_room != ch.in_room ):
        ch.send("They aren't here.\n")
        return
    if victim.desc is None and not victim.is_npc():
        handler_game.act("$N seems to have misplaced $S link...try again later.", ch, None, victim, merc.TO_CHAR)
        buf = "%s tells you '%s'\n" % (state_checks.PERS(ch, victim), argument)
        victim.buffer.append(buf)
        return

    if not (ch.is_immortal() and ch.level > merc.LEVEL_IMMORTAL) and not state_checks.IS_AWAKE(victim):
        handler_game.act("$E can't hear you.", ch, 0, victim, merc.TO_CHAR)
        return

    if (victim.comm.is_set(merc.COMM_QUIET) or state_checks.IS_SET(victim.comm,merc.COMM_DEAF)) and not state_checks.IS_IMMORTAL(ch):
        handler_game.act("$E is not receiving tells.", ch, 0, victim, merc.TO_CHAR)
        return

    if victim.comm.is_set(merc.COMM_AFK):
        if victim.is_npc():
            handler_game.act("$E is AFK, and not receiving tells.", ch, None, victim, merc.TO_CHAR)
            return
        handler_game.act("$E is AFK, but your tell will go through when $E returns.", ch, None, victim, merc.TO_CHAR)
        buf = "%s tells you '%s'\n" % (state_checks.PERS(ch, victim), argument)
        victim.buffer.append(buf)
        return
    handler_game.act("You tell $N '$t'", ch, argument, victim, merc.TO_CHAR)
    handler_game.act("$n tells you '$t'", ch, argument, victim, merc.TO_VICT, merc.POS_DEAD)
    victim.reply = ch
    return


interp.register_command(interp.cmd_type('tell', do_tell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
