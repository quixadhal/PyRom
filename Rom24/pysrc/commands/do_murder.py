import merc
import interp
import fight


def do_murder(ch, argument):
    argument, arg = merc.read_word(argument)

    if not arg:
        ch.send("Murder whom?\n\r")
        return

    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) or (merc.IS_NPC(ch) and merc.IS_SET(ch.act, merc.ACT_PET)):
        return
    victim = ch.get_char_room(arg)
    if victim == None:
        ch.send("They aren't here.\n\r")
        return
    if victim == ch:
        ch.send("Suicide is a mortal sin.\n\r")
        return
    if fight.is_safe(ch, victim):
        return
    if merc.IS_NPC(victim) and victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
        act( "$N is your beloved master.", ch, None, victim, TO_CHAR )
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("You do the best you can!\n\r")
        return

    merc.WAIT_STATE(ch, 1 * merc.PULSE_VIOLENCE)
    if merc.IS_NPC(ch):
        buf = "Help! I am being attacked by %s!" % ch.short_descr
    else:
        buf = "Help!  I am being attacked by %s!" % ch.name
    victim.do_yell(buf)
    fight.check_killer(ch, victim)
    fight.multi_hit(ch, victim, merc.TYPE_UNDEFINED)
    return

interp.cmd_table['murder'] = interp.cmd_type('murder', do_murder, merc.POS_FIGHTING, 5, merc.LOG_ALWAYS, 1)