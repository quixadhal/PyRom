import random
import merc
import const
import interp
import skills
import fight


def do_dirt(ch, argument):
    arghold, arg = merc.read_word(argument)
    chance = ch.get_skill('dirt kicking')
    if chance == 0 or (merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, merc.OFF_KICK_DIRT)) \
    or ( not merc.IS_NPC(ch) and ch.level < const.skill_table['dirt kicking'].skill_level[ch.guild.name]):
        ch.send("You get your feet dirty.\n\r")
        return
    if not arg:
        victim = ch.fighting
        if victim == None:
            ch.send("But you aren't in combat!\n\r")
            return
    else:
        victim = ch.get_char_room(arg)
        if victim == None:
            ch.send("They aren't here.\n\r")
            return
    if merc.IS_AFFECTED(victim, merc.AFF_BLIND):
        merc.act("$E's already been blinded.",ch,None,victim,merc.TO_CHAR)
        return
    if victim == ch:
        ch.send("Very funny.\n\r")
        return
    if fight.is_safe(ch,victim):
        return
    if merc.IS_NPC(victim) and victim.fighting != None and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
        act("But $N is such a good friend!",ch,None,victim,merc.TO_CHAR)
        return

    # modifiers */
    # dexterity */
    chance += ch.get_curr_stat(merc.STAT_DEX)
    chance -= 2 * victim.get_curr_stat(merc.STAT_DEX)

    # speed  */
    if merc.IS_SET(ch.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(ch, merc.AFF_HASTE):
        chance += 10
    if merc.IS_SET(victim.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(victim, merc.AFF_HASTE):
        chance -= 25
    # level */
    chance += (ch.level - victim.level) * 2

    # sloppy hack to prevent false zeroes */
    if chance % 5 == 0:
        chance += 1
    # terrain */
    nochance = [ merc.SECT_WATER_SWIM, merc.SECT_WATER_NOSWIM, merc.SECT_AIR ]
    modifiers = { merc.SECT_INSIDE: -20,
                  merc.SECT_CITY: -10,
                  merc.SECT_FIELD: 5,
                  merc.SECT_MOUNTAIN: -10,
                  merc.SECT_DESERT: 10
                }
    if ch.in_room.sector_type in nochance:
        chance = 0
    elif ch.in_room.sector_type in modifiers:
        chance += modifiers[ch.in_room.sector_type]

    if chance == 0:
        ch.send("There isn't any dirt to kick.\n\r")
        return
    # now the attack */
    if random.randint(1,99) < chance:
        merc.act("$n is blinded by the dirt in $s eyes!",victim,None,None, merc.TO_ROOM)
        merc.act("$n kicks dirt in your eyes!",ch,None,victim, merc.TO_VICT)
        fight.damage(ch,victim,random.randint(2,5),'dirt kicking', merc.DAM_NONE,False)
        victim.send("You can't see a thing!\n\r")
        skills.check_improve(ch,'dirt kicking',True,2)
        merc.WAIT_STATE(ch,const.skill_table['dirt kicking'].beats)
        af = merc.AFFECT_DATA()
        af.where = merc.TO_AFFECTS
        af.type = 'dirt kicking'
        af.level = ch.level
        af.duration = 0
        af.location = merc.APPLY_HITROLL
        af.modifier = -4
        af.bitvector = merc.AFF_BLIND
        victim.affect_add(af)
    else:
        fight.damage(ch,victim,0,'dirt kicking',DAM_NONE,True)
        skills.check_improve(ch,'dirt kicking',False,2)
        merc.WAIT_STATE(ch,const.skill_table['dirt kicking'].beats)
    fight.check_killer(ch,victim)

interp.cmd_type('dirt', do_dirt, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)