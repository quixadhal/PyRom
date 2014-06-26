import random
import merc
import interp
import const
import skills
import fight


def do_kick(ch, argument):
    if not merc.IS_NPC(ch) and ch.level < const.skill_table['kick'].skill_level[ch.guild.name]:
        ch.send("You better leave the martial arts to fighters.\n\r")
        return
    if merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, merc.OFF_KICK):
        return
    victim = ch.fighting
    if not victim:
        ch.send("You aren't fighting anyone.\n\r")
        return

    merc.WAIT_STATE( ch, const.skill_table['kick'].beats )
    if ch.get_skill('kick') > random.randint(1,99):
        fight.damage(ch,victim,random.randint( 1, ch.level ), 'kick',merc.DAM_BASH,True)
        skills.check_improve(ch, 'kick', True, 1)
    else:
        fight.damage(ch, victim, 0, 'kick', merc.DAM_BASH, True)
        skills.check_improve(ch,'kick',False,1)
    fight.check_killer(ch,victim)
    return

interp.cmd_type('kick', do_kick, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)