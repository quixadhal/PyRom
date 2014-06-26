import random
import merc
import const
import interp
import fight
import skills


def do_trip(ch, argument):
    arghold, arg = merc.read_word(argument)
    chance = ch.get_skill('trip')
    if chance == 0 or (merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, merc.OFF_TRIP)) \
    or ( not merc.IS_NPC(ch) and ch.level < const.skill_table['trip'].skill_level[ch.guild.name]):
        ch.send("Tripping?  What's that?\n\r")
        return
    if not arg:
        victim = ch.fighting
        if victim == None:
            ch.send("But you aren't fighting anyone!\n\r")
            return
    else:
        victim = ch.get_char_room(arg)
        if victim == None:
            ch.send("They aren't here.\n\r")
            return
    if fight.is_safe(ch,victim):
        return
    if merc.IS_NPC(victim) and victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if merc.IS_AFFECTED(victim,merc.AFF_FLYING):
        merc.act("$S feet aren't on the ground.",ch,None,victim,merc.TO_CHAR)
        return
    if victim.position < merc.POS_FIGHTING:
        merc.act("$N is already down.",ch,None,victim,merc.TO_CHAR)
        return
    if victim == ch:
        ch.send("You fall flat on your face!\n\r")
        merc.WAIT_STATE(ch,2 * const.skill_table['trip'].beats)
        merc.act("$n trips over $s own feet!",ch,None,None, merc.TO_ROOM)
        return

    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
        merc.act("$N is your beloved master.",ch,None,victim,merc.TO_CHAR)
        return
    # modifiers */
    # size */
    if ch.size < victim.size:
        chance += (ch.size - victim.size) * 10  # bigger = harder to trip */

    # dex */
    chance += ch.get_curr_stat(merc.STAT_DEX)
    chance -= victim.get_curr_stat(merc.STAT_DEX) * 3 // 2

    # speed */
    if merc.IS_SET(ch.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(ch, merc.AFF_HASTE):
        chance += 10
    if merc.IS_SET(victim.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(victim, merc.AFF_HASTE):
        chance -= 20
    # level */
    chance += (ch.level - victim.level) * 2
    # now the attack */
    if random.randint(1,99) < chance:
        merc.act("$n trips you and you go down!",ch,None,victim,merc.TO_VICT)
        merc.act("You trip $N and $N goes down!",ch,None,victim,merc.TO_CHAR)
        merc.act("$n trips $N, sending $M to the ground.",ch,None,victim,merc.TO_NOTVICT)
        skills.check_improve(ch,'trip',True,1)

        merc.DAZE_STATE(victim,2 * merc.PULSE_VIOLENCE)
        merc.WAIT_STATE(ch,const.skill_table['trip'].beats)
        victim.position = merc.POS_RESTING
        fight.damage(ch,victim,random.randint(2, 2 +  2 * victim.size),'trip', merc.DAM_BASH,True)
    else:
        fight.damage(ch,victim,0,'trip',merc.DAM_BASH,True)
        merc.WAIT_STATE(ch,const.skill_table['trip'].beats*2 // 3)
        skills.check_improve(ch,'trip',False,1)
    fight.check_killer(ch,victim)

interp.cmd_table['trip'] = interp.cmd_type('trip', do_trip, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)