import merc
import interp
import fight


def do_slay(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Slay whom?\n\r")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if ch == victim:
        ch.send("Suicide is a mortal sin.\n\r")
        return
    if not merc.IS_NPC(victim) and victim.level >= ch.get_trust():
        ch.send("You failed.\n\r")
        return
    merc.act( "You slay $M in cold blood!", ch, None, victim, merc.TO_CHAR)
    merc.act( "$n slays you in cold blood!", ch, None, victim, merc.TO_VICT)
    merc.act( "$n slays $N in cold blood!", ch, None, victim, merc.TO_NOTVICT)
    fight.raw_kill(victim)
    return

interp.cmd_type('slay', do_slay, merc.POS_DEAD, merc.L3, merc.LOG_ALWAYS, 1)