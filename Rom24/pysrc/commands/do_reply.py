import logging

logger = logging.getLogger()

import merc
import interp
import handler_game
import state_checks


def do_reply(ch, argument):
    if ch.comm.is_set(merc.COMM_NOTELL):
        ch.send("Your message didn't get through.\n")
        return
    if not ch.reply:
        ch.send("They aren't here.\n")
        return
    victim = ch
    if not victim.desc and not victim.is_npc():
        handler_game.act("$N seems to have misplaced $S link...try again later.", ch, None, victim, merc.TO_CHAR)
        buf = "%s tells you '%s'\n" % (state_checks.PERS(ch, victim), argument)
        victim.buffer.append(buf)
        return
    if not ch.is_immortal() and not state_checks.IS_AWAKE(victim):
        handler_game.act("$E can't hear you.", ch, 0, victim, merc.TO_CHAR)
        return

    if (victim.comm.is_set(merc.COMM_QUIET) or victim.comm.is_set(merc.COMM_DEAF)) \
            and not ch.is_immortal() and not state_checks.IS_IMMORTAL(victim):
        handler_game.act("$E is not receiving tells.", ch, None, victim, merc.TO_CHAR, merc.POS_DEAD)
        return
    if not state_checks.IS_IMMORTAL(victim) and not ch.is_awake():
        ch.send("In your dreams, or what?\n")
        return
    if victim.comm.is_set(merc.COMM_AFK):
        if victim.is_npc():
            handler_game.act("$E is AFK, and not receiving tells.", ch, None, victim, merc.TO_CHAR, merc.POS_DEAD)
            return
        handler_game.act("$E is AFK, but your tell will go through when $E returns.", ch, None, victim, merc.TO_CHAR,
                         merc.POS_DEAD)
        buf = "%s tells you '%s'\n" % (state_checks.PERS(ch, victim), argument)
        victim.buffer.append(buf)
        return
    handler_game.act("You tell $N '$t'", ch, argument, victim, merc.TO_CHAR, merc.POS_DEAD)
    handler_game.act("$n tells you '$t'", ch, argument, victim, merc.TO_VICT, merc.POS_DEAD)
    victim.reply = ch
    return


interp.register_command(interp.cmd_type('reply', do_reply, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
