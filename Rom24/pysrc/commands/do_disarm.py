import random
import merc
import const
import interp
import skills
import fight


def do_disarm(ch, argument):
    hth = 0
    chance = ch.get_skill('disarm')
    if chance == 0:
        ch.send("You don't know how to disarm opponents.\n\r")
        return
    hth = ch.get_skill('hand to hand')
    if not ch.get_eq(merc.WEAR_WIELD) \
    and hth == 0 or (merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, merc.OFF_DISARM)):
        ch.send("You must wield a weapon to disarm.\n\r")
        return
    victim = ch.fighting
    if not victim:
        ch.send("You aren't fighting anyone.\n\r")
        return
    obj = victim.get_eq(merc.WEAR_WIELD)
    if not obj:
        ch.send("Your opponent is not wielding a weapon.\n\r")
        return

    # find weapon skills */
    ch_weapon = ch.get_weapon_skill(ch.get_weapon_sn())
    vict_weapon = victim.get_weapon_skill(victim.get_weapon_sn())
    ch_vict_weapon = ch.get_weapon_skill(victim.get_weapon_sn())

    # modifiers */

    # skill */
    if ch.get_eq(merc.WEAR_WIELD) == None:
        chance = chance * hth // 150
    else:
        chance = chance * ch_weapon // 100

    chance += (ch_vict_weapon // 2 - vict_weapon) // 2

    # dex vs. strength */
    chance += ch.get_curr_stat(merc.STAT_DEX)
    chance -= 2 * victim.get_curr_stat(merc.STAT_STR)

    # level */
    chance += (ch.level - victim.level) * 2

    # and now the attack */
    if random.randint(1,99) < chance:
        merc.WAIT_STATE( ch, const.skill_table['disarm'].beats )
        fight.disarm(ch, victim)
        skills.check_improve(ch,'disarm',True,1)
    else:
        merc.WAIT_STATE(ch,const.skill_table['disarm'].beats)
        merc.act("You fail to disarm $N.",ch,None,victim, merc.TO_CHAR)
        merc.act("$n tries to disarm you, but fails.",ch,None,victim, merc.TO_VICT)
        merc.act("$n tries to disarm $N, but fails.",ch,None,victim, merc.TO_NOTVICT)
        skills.check_improve(ch,'disarm',False,1)
    fight.check_killer(ch,victim)
    return

interp.cmd_table['disarm'] = interp.cmd_type('disarm', do_disarm, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)