import logging

logger = logging.getLogger()

import merc
import interp


def do_tell(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_NOTELL) or merc.IS_SET(ch.comm, merc.COMM_DEAF):
        ch.send("Your message didn't get through.\n")
        return
    if merc.IS_SET(ch.comm, merc.COMM_QUIET):
        ch.send("You must turn off quiet mode first.\n")
        return
    if merc.IS_SET(ch.comm, merc.COMM_DEAF):
        ch.send("You must turn off deaf mode first.\n")
        return
    argument, arg = merc.read_word(argument)

    if not arg or not argument:
        ch.send("Tell whom what?\n")
        return
        # Can tell to PC's anywhere, but NPC's only in same room.
        # -- Furey
    victim = ch.get_char_world(arg)
    if not victim or ( merc.IS_NPC(victim) and victim.in_room != ch.in_room ):
        ch.send("They aren't here.\n")
        return
    if victim.desc is None and not merc.IS_NPC(victim):
        merc.act("$N seems to have misplaced $S link...try again later.", ch, None, victim, merc.TO_CHAR)
        buf = "%s tells you '%s'\n" % (merc.PERS(ch, victim), argument)
        victim.pcdata.buffer.append(buf)
        return

    if not (merc.IS_IMMORTAL(ch) and ch.level > merc.LEVEL_IMMORTAL) and not merc.IS_AWAKE(victim):
        merc.act("$E can't hear you.", ch, 0, victim, merc.TO_CHAR)
        return

    if (merc.IS_SET(victim.comm, merc.COMM_QUIET) or merc.IS_SET(victim.comm, merc.COMM_DEAF)) and not merc.IS_IMMORTAL(
            ch):
        merc.act("$E is not receiving tells.", ch, 0, victim, merc.TO_CHAR)
        return

    if merc.IS_SET(victim.comm, merc.COMM_AFK):
        if merc.IS_NPC(victim):
            merc.act("$E is AFK, and not receiving tells.", ch, None, victim, merc.TO_CHAR)
            return
        merc.act("$E is AFK, but your tell will go through when $E returns.", ch, None, victim, merc.TO_CHAR)
        buf = "%s tells you '%s'\n" % (merc.PERS(ch, victim), argument)
        victim.pcdata.buffer.append(buf)
        return
    merc.act("You tell $N '$t'", ch, argument, victim, merc.TO_CHAR)
    merc.act("$n tells you '$t'", ch, argument, victim, merc.TO_VICT, merc.POS_DEAD)
    victim.reply = ch
    return


interp.register_command(interp.cmd_type('tell', do_tell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
