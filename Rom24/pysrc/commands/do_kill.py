import merc
import interp
import fight


def do_kill(ch, argument):
    argument, arg = merc.read_word(argument)

    if not arg:
        ch.send("Kill whom?\n\r")
        return
    victim = ch.get_char_room(arg)
    if victim == None:
        ch.send("They aren't here.\n\r")
        return
    #  Allow player killing
#    if not IS_NPC(victim):
#        if not IS_SET(victim.act, PLR_KILLER) and not IS_SET(victim.act, PLR_THIEF):
#            ch.send("You must MURDER a player.\n\r")
#            return

    if victim == ch:
        ch.send("You hit yourself.  Ouch!\n\r")
        fight.multi_hit(ch, ch, merc.TYPE_UNDEFINED)
        return
    if fight.is_safe(ch, victim):
        return
    if victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
        merc.act( "$N is your beloved master.", ch, None, victim, merc.TO_CHAR)
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("You do the best you can!\n\r")
        return

    merc.WAIT_STATE(ch, 1 * merc.PULSE_VIOLENCE)
    fight.check_killer(ch, victim)
    fight.multi_hit(ch, victim, merc.TYPE_UNDEFINED)
    return

interp.cmd_table['hit'] = interp.cmd_type('hit', do_kill, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0)
interp.cmd_table['kill'] = interp.cmd_type('kill', do_kill, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)