"""
#**************************************************************************
 *  Original Diku Mud copyright=C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright=C) 1992, 1993 by Michael          *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

#**************************************************************************
*    ROM 2.4 is copyright 1993-1998 Russ Taylor                           *
*    ROM has been brought to you by the ROM consortium                    *
*        Russ Taylor=rtaylor@hypercube.org)                               *
*        Gabrielle Taylor=gtaylor@hypercube.org)                          *
*        Brian Moore=zump@rom.org)                                        *
*    By using this code, you have agreed to follow the terms of the       *
*    ROM license, in the file Rom24/doc/rom.license                       *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
from merc import *
from handler import *
from skills import check_improve, exp_per_level
import const

# * Control the fights going on.
# * Called periodically by update_handler.
def violence_update( ):
    for ch in char_list[:]:
        if not ch.fighting or not ch.in_room:
            continue
        victim = ch.fighting
        if IS_AWAKE(ch) and ch.in_room == victim.in_room:
            multi_hit( ch, victim, TYPE_UNDEFINED )
        else:
            stop_fighting( ch, False )
        if not ch.fighting:
            continue
        victim = ch.fighting
        #
        #* Fun for the whole family!
        #*/
        check_assist(ch,victim)
    return

# for auto assisting */
def check_assist( ch, victim):
    for rch in ch.in_room.people[:]:
        if IS_AWAKE(rch) and rch.fighting == None:
            # quick check for ASSIST_PLAYER */
            if not IS_NPC(ch) and IS_NPC(rch) and IS_SET(rch.off_flags,ASSIST_PLAYERS) and rch.level + 6 > victim.level:
                rch.do_emote("screams and attacks!")
                multi_hit(rch,victim,TYPE_UNDEFINED)
                continue
        # PCs next */
        if not IS_NPC(ch) or IS_AFFECTED(ch,AFF_CHARM):
            if( (not IS_NPC(rch) and IS_SET(rch.act,PLR_AUTOASSIST)) \
            or IS_AFFECTED(rch,AFF_CHARM)) \
            and is_same_group(ch,rch) \
            and not is_safe(rch, victim):
                multi_hit (rch,victim,TYPE_UNDEFINED)
                continue
   
        # now check the NPC cases */
        if IS_NPC(ch) and not IS_AFFECTED(ch,AFF_CHARM):
            if (IS_NPC(rch) and IS_SET(rch.off_flags,ASSIST_ALL)) \
            or (IS_NPC(rch) and rch.group and rch.group == ch.group) \
            or (IS_NPC(rch) and rch.race == ch.race and IS_SET(rch.off_flags,ASSIST_RACE)) \
            or (IS_NPC(rch) and IS_SET(rch.off_flags,ASSIST_ALIGN) \
                and ((IS_GOOD(rch) and IS_GOOD(ch)) or (IS_EVIL(rch) and IS_EVIL(ch)) \
                or (IS_NEUTRAL(rch) and IS_NEUTRAL(ch)))) \
            or (rch.pIndexData == ch.pIndexData and IS_SET(rch.off_flags,ASSIST_VNUM)):
                if random.randint(0,1) == 0:
                    continue
        
                target = None
                number = 0
                for vch in ch.in_room.people:
                    if can_see(rch,vch) and is_same_group(vch,victim) and random.randint(0,number) == 0:
                        target = vch
                        number += 1
                if target:
                    rch.do_emote("screams and attacks!")
                    multi_hit(rch,target,TYPE_UNDEFINED)


# * Do one group of attacks.
def multi_hit( ch, victim, dt ):
    # decrement the wait */
    if ch.desc == None:
        ch.wait = max(0,ch.wait - PULSE_VIOLENCE)

    if ch.desc == None:
        ch.daze = max(0,ch.daze - PULSE_VIOLENCE) 


    # no attacks for stunnies -- just a check */
    if ch.position < POS_RESTING:
        return

    if IS_NPC(ch):
        mob_hit(ch,victim,dt)
        return

    one_hit( ch, victim, dt )

    if ch.fighting != victim:
        return

    if IS_AFFECTED(ch,AFF_HASTE):
        one_hit(ch,victim,dt)

    if ch.fighting != victim or dt == 'backstab':
        return

    chance = get_skill(ch,'second attack')/2

    if IS_AFFECTED(ch,AFF_SLOW):
        chance /= 2

    if random.randint(1,99) < chance:
        one_hit( ch, victim, dt )
        check_improve(ch,'second_attack',True,5)
        if ch.fighting != victim:
            return
    
    chance = get_skill(ch,'third attack')/4

    if IS_AFFECTED(ch,AFF_SLOW):
        chance = 0

    if random.randint(1,99) < chance:
        one_hit( ch, victim, dt )
        check_improve(ch,'third attack',True,6)
        if ch.fighting != victim:
            return
    return
# procedure for all mobile attacks */
def mob_hit (ch, victim, dt):
    one_hit(ch,victim,dt)
    if ch.fighting != victim:
        return
    # Area attack -- BALLS nasty! */
    if IS_SET(ch.off_flags,OFF_AREA_ATTACK):
        for vch in ch.in_room.people[:]:
            if vch != victim and vch.fighting == ch:
                one_hit(ch,vch,dt)

    if IS_AFFECTED(ch,AFF_HASTE) or (IS_SET(ch.off_flags,OFF_FAST) and not IS_AFFECTED(ch,AFF_SLOW)):
        one_hit(ch,victim,dt)

    if ch.fighting != victim or dt == 'backstab':
        return

    chance = get_skill(ch,"second attack")/2

    if IS_AFFECTED(ch,AFF_SLOW) and not IS_SET(ch.off_flags,OFF_FAST):
        chance /= 2

    if random.randint(1,99) < chance:
        one_hit(ch,victim,dt)
        if ch.fighting != victim:
            return
    chance = get_skill(ch,'third attack')/4

    if IS_AFFECTED(ch,AFF_SLOW) and not IS_SET(ch.off_flags,OFF_FAST):
        chance = 0

    if random.randint(1,99) < chance:
        one_hit(ch,victim,dt)
        if ch.fighting != victim:
            return

    # oh boy!  Fun stuff! */
    if ch.wait > 0:
        return

    number = random.randint(0,2)

    if number == 1 and IS_SET(ch.act,ACT_MAGE):
        pass
        #  { mob_cast_mage(ch,victim) return } */ 

    if number == 2 and IS_SET(ch.act,ACT_CLERIC):
        pass
        # { mob_cast_cleric(ch,victim) return } */ 

    # now for the skills */

    number = random.randint(0,8)

    if number == 0:
       if IS_SET(ch.off_flags,OFF_BASH):
            ch.do_bash("")
    elif number == 1:
        if IS_SET(ch.off_flags,OFF_BERSERK) and not IS_AFFECTED(ch,AFF_BERSERK):
            ch.do_berserk("")
    elif number == 2:
        if IS_SET(ch.off_flags,OFF_DISARM) \
        or (get_weapon_sn(ch) != 'hand_to_hand' \
        and (IS_SET(ch.act,ACT_WARRIOR) \
        or  IS_SET(ch.act,ACT_THIEF))):
            ch.do_disarm("")
    elif number == 3:
        if IS_SET(ch.off_flags,OFF_KICK):
            ch.do_kick("")
    elif number == 4:
        if IS_SET(ch.off_flags,OFF_KICK_DIRT):
            ch.do_dirt("")
    elif number == 5:
        if IS_SET(ch.off_flags,OFF_TAIL):
            pass  # do_function(ch, &do_tail, "") */ 
    elif number == 6:
        if IS_SET(ch.off_flags,OFF_TRIP):
            ch.do_trip("")
    elif number == 7:
        if IS_SET(ch.off_flags,OFF_CRUSH):
            pass # do_function(ch, &do_crush, "") */ 
    elif number == 8:
        if IS_SET(ch.off_flags,OFF_BACKSTAB):
            ch.do_backstab("")

# * Hit one guy once.
# */
def one_hit( ch, victim, dt ):
    sn = -1
    # just in case */
    if victim == ch or ch == None or victim == None:
        return
    #* Can't beat a dead char!
    #* Guard against weird room-leavings.
    if victim.position == POS_DEAD or ch.in_room != victim.in_room:
        return

     #* Figure out the type of damage message.
    wield = get_eq_char( ch, WEAR_WIELD )
    if dt == TYPE_UNDEFINED:
        dt = TYPE_HIT
        if wield and wield.item_type == ITEM_WEAPON:
            dt += wield.value[3]
        else :
            dt += ch.dam_type

    if dt < TYPE_HIT:
        if wield:
            dam_type = const.attack_table[wield.value[3]].damage
        else:
            dam_type = const.attack_table[ch.dam_type].damage
    else:
        dam_type = const.attack_table[dt - TYPE_HIT].damage

    if dam_type == -1:
        dam_type = DAM_BASH

    # get the weapon skill */
    sn = get_weapon_sn(ch)
    skill = 20 + get_weapon_skill(ch,sn)

    #* Calculate to-hit-armor-guild-0 versus armor.
    if IS_NPC(ch):
        thac0_00 = 20
        thac0_32 = -4   # as good as a thief */ 
        if IS_SET(ch.act,ACT_WARRIOR):
            thac0_32 = -10
        elif IS_SET(ch.act,ACT_THIEF):
            thac0_32 = -4
        elif IS_SET(ch.act,ACT_CLERIC):
            thac0_32 = 2
        elif IS_SET(ch.act,ACT_MAGE):
            thac0_32 = 6
    else:
        thac0_00 = ch.guild.thac0_00
        thac0_32 = ch.guild.thac0_32
    
    thac0  = interpolate( ch.level, thac0_00, thac0_32 )

    if thac0 < 0:
        thac0 = thac0/2

    if thac0 < -5:
        thac0 = -5 + (thac0 + 5) / 2

    thac0 -= GET_HITROLL(ch) * skill/100
    thac0 += 5 * (100 - skill) / 100

    if dt == 'backstab':
        thac0 -= 10 * (100 - get_skill(ch,'backstab'))

    if dam_type == DAM_PIERCE: victim_ac = GET_AC(victim,AC_PIERCE)/10
    elif dam_type == DAM_BASH: victim_ac = GET_AC(victim,AC_BASH)/10
    elif dam_type == DAM_SLASH: victim_ac = GET_AC(victim,AC_SLASH)/10
    else: victim_ac = GET_AC(victim,AC_EXOTIC)/10
    
    if victim_ac < -15:
        victim_ac = (victim_ac + 15) / 5 - 15
     
    if not can_see( ch, victim ):
        victim_ac -= 4

    if victim.position < POS_FIGHTING:
        victim_ac += 4
 
    if victim.position < POS_RESTING:
        victim_ac += 6

     #* The moment of excitement!
    diceroll = random.randint(0,20)
    if diceroll == 0 or ( diceroll != 19 and diceroll < thac0 - victim_ac ):
        # Miss. */
        damage( ch, victim, 0, dt, dam_type, True )
        return
     # Hit.
     # Calc damage.
    if IS_NPC(ch) and (not ch.pIndexData.new_format or wield == None):
        if not ch.pIndexData.new_format:
            dam = random.randint( ch.level / 2, ch.level * 3 / 2 )
            if wield != None:
                dam += dam / 2
        else:
            dam = dice(ch.damage[DICE_NUMBER],ch.damage[DICE_TYPE])
    else:
        if sn != -1:
            check_improve(ch,sn,True,5)
        if wield:
            if wield.pIndexData.new_format:
                dam = dice(wield.value[1],wield.value[2]) * skill/100
            else:
                dam = random.randint( wield.value[1] * skill/100, wield.value[2] * skill/100)

            if get_eq_char(ch,WEAR_SHIELD) == None:  # no shield = more */
                dam = dam * 11/10
            # sharpness! */
            if IS_WEAPON_STAT(wield,WEAPON_SHARP):
                percent = random.randint(1,99)
                if percent <= (skill / 8):
                    dam = 2 * dam + (dam * 2 * percent / 100)
        else:
            dam = random.randint( 1 + 4 * skill/100, 2 * ch.level/3 * skill/100)
    #
    # * Bonuses.
    if get_skill(ch,'enhanced damage') > 0:
        diceroll = random.randint(1,99)
        if diceroll <= get_skill(ch,'enhanced_damage'):
            check_improve(ch,'enhanced damage',True,6)
            dam += 2 * ( dam * diceroll/300)
    if not IS_AWAKE(victim):
        dam *= 2
    elif victim.position < POS_FIGHTING:
        dam = dam * 3 / 2

    if dt == 'backstab' and wield:
        if wield.value[0] != 2:
            dam *= 2 + (ch.level / 10) 
        else:
            dam *= 2 + (ch.level / 8)
    dam += GET_DAMROLL(ch) * min(100,skill) /100

    if dam <= 0:
        dam = 1

    result = damage( ch, victim, dam, dt, dam_type, True )
    
    # but do we have a funky weapon? */
    if result and wield != None:

        if ch.fighting == victim and IS_WEAPON_STAT(wield,WEAPON_POISON):
            poison = affect_find(wield.affected,'poison')
            if poison:
                level = wield.level
            else:
                level = poison.level
            if not saves_spell(level / 2,victim,DAM_POISON):
                victim.send("You feel poison coursing through your veins.")
                act("$n is poisoned by the venom on $p.", victim,wield,None,TO_ROOM)
                af = AFFECT_DATA()
                af.where     = TO_AFFECTS
                af.type      = 'poison'
                af.level     = level * 3/4
                af.duration  = level / 2
                af.location  = APPLY_STR
                af.modifier  = -1
                af.bitvector = AFF_POISON
                affect_join( victim, af )

            # weaken the poison if it's temporary */
            if poison:
                poison.level = max(0,poison.level - 2)
                poison.duration = max(0,poison.duration - 1)
                if poison.level == 0 or poison.duration == 0:
                    act("The poison on $p has worn off.",ch,wield,None,TO_CHAR)

            if ch.fighting == victim and IS_WEAPON_STAT(wield,WEAPON_VAMPIRIC):
                dam = random.randint(1, wield.level / 5 + 1)
                act("$p draws life from $n.",victim,wield,None,TO_ROOM)
                act("You feel $p drawing your life away.", victim,wield,None,TO_CHAR)
                damage(ch,victim,dam,0,DAM_NEGATIVE,False)
                ch.alignment = max(-1000,ch.alignment - 1)
                ch.hit += dam/2
            if ch.fighting == victim and IS_WEAPON_STAT(wield,WEAPON_FLAMING):
                dam = random.randint(1,wield.level / 4 + 1)
                act("$n is burned by $p.",victim,wield,None,TO_ROOM)
                act("$p sears your flesh.",victim,wield,None,TO_CHAR)
                fire_effect(victim,wield.level/2,dam,TARGET_CHAR)
                damage(ch,victim,dam,0,DAM_FIRE,False)
            if ch.fighting == victim and IS_WEAPON_STAT(wield,WEAPON_FROST):
                dam = random.randint(1,wield.level / 6 + 2)
                act("$p freezes $n.",victim,wield,None,TO_ROOM)
                act("The cold touch of $p surrounds you with ice.",
                victim,wield,None,TO_CHAR)
                cold_effect(victim,wield.level/2,dam,TARGET_CHAR)
                damage(ch,victim,dam,0,DAM_COLD,False)
            if ch.fighting == victim and IS_WEAPON_STAT(wield,WEAPON_SHOCKING):
                dam = random.randint(1,wield.level/5 + 2)
                act("$n is struck by lightning from $p.",victim,wield,None,TO_ROOM)
                act("You are shocked by $p.",victim,wield,None,TO_CHAR)
                shock_effect(victim,wield.level/2,dam,TARGET_CHAR)
                damage(ch,victim,dam,0,DAM_LIGHTNING,False)
    return

# * Inflict damage from a hit.
def damage(ch,victim,dam,dt,dam_type,show):
    if victim.position == POS_DEAD:
        return False

    #Stop up any residual loopholes.
    if dam > 1200 and dt >= TYPE_HIT:
        print ("BUG: Damage: %d: more than 1200 points!" % dam)
        dam = 1200
        if not IS_IMMORTAL(ch):
            obj = get_eq_char( ch, WEAR_WIELD )
            ch.send("You really shouldn't cheat.\n\r")
            if obj:
                extract_obj(obj)
    
    # damage reduction */
    if dam > 35:
        dam = (dam - 35)/2 + 35
    if dam > 80:
        dam = (dam - 80)/2 + 80 
  
    if victim != ch:
        # Certain attacks are forbidden.
        # Most other attacks are returned.
        if is_safe( ch, victim ):
            return False
        check_killer( ch, victim )

        if victim.position > POS_STUNNED:
            if not victim.fighting:
                set_fighting( victim, ch )
            if victim.timer <= 4:
                victim.position = POS_FIGHTING

        if victim.position > POS_STUNNED:
            if not ch.fighting:
                set_fighting( ch, victim )
        # More charm stuff.
        if victim.master == ch:
            stop_follower( victim )
    # * Inviso attacks ... not.
    if IS_AFFECTED(ch, AFF_INVISIBLE):
        affect_strip( ch, "invis" )
        affect_strip( ch, "mass invis" )
        REMOVE_BIT( ch.affected_by, AFF_INVISIBLE )
        act( "$n fades into existence.", ch, None, None, TO_ROOM )

     # Damage modifiers.
    if dam > 1 and not IS_NPC(victim) and victim.pcdata.condition[COND_DRUNK] > 10:
        dam = 9 * dam / 10
    if dam > 1 and IS_AFFECTED(victim, AFF_SANCTUARY):
        dam /= 2

    if dam > 1 and ((IS_AFFECTED(victim, AFF_PROTECT_EVIL) and IS_EVIL(ch)) \
    or (IS_AFFECTED(victim, AFF_PROTECT_GOOD) and IS_GOOD(ch) )):
        dam -= dam / 4

    immune = False
     # Check for parry, and dodge.
    if dt >= TYPE_HIT and ch != victim:
        if check_parry( ch, victim ):
            return False
        if check_dodge( ch, victim ):
            return False
        if check_shield_block(ch,victim):
            return False
    imm = check_immune(victim, dam_type)

    if imm == IS_IMMUNE:
        immune = True
        dam = 0
    elif imm == IS_RESISTANT:
        dam -= dam/3
    elif imm == IS_VULNERABLE:
        dam += dam/2
    dam = int(dam)
    if show:
        dam_message( ch, victim, dam, dt, immune )

    if dam == 0:
        return False
     # Hurt the victim.
     # Inform the victim of his new state.
    victim.hit -= dam
    if not IS_NPC(victim) and victim.level >= LEVEL_IMMORTAL and victim.hit < 1:
        victim.hit = 1
    update_pos( victim )

    if victim.position == POS_MORTAL:
        act( "$n is mortally wounded, and will die soon, if not aided.", victim, None, None, TO_ROOM )
        victim.send("You are mortally wounded, and will die soon, if not aided.\n\r")
    elif victim.position == POS_INCAP:
        act( "$n is incapacitated and will slowly die, if not aided.", victim, None, None, TO_ROOM )
        victim.send("You are incapacitated and will slowly die, if not aided.\n\r")
    elif victim.position == POS_STUNNED:
        act( "$n is stunned, but will probably recover.", victim, None, None, TO_ROOM )
        victim.send("You are stunned, but will probably recover.\n\r")
    elif victim.position == POS_DEAD:
        act( "$n is DEAD!!", victim, 0, 0, TO_ROOM )
        victim.send("You have been KILLED!!\n\r\n\r")
    else:
        if dam > victim.max_hit / 4:
            victim.send("That really did HURT!\n\r")
        if victim.hit < victim.max_hit / 4:
            victim.send("You sure are BLEEDING!\n\r")
    # Sleep spells and extremely wounded folks.
    if not IS_AWAKE(victim):
        stop_fighting( victim, False )

    # Payoff for killing things.
    if victim.position == POS_DEAD:
        group_gain( ch, victim )

        if not IS_NPC(victim):
            print ("%s killed by %s at %d" % ( victim.name, ch.short_descr if IS_NPC(ch) else ch.name, ch.in_room.vnum ))
            # Dying penalty:
            # 2/3 way back to previous level.
            if victim.exp > exp_per_level(victim,victim.pcdata.points) * victim.level:
                gain_exp( victim, (2 * (exp_per_level(victim,victim.pcdata.points) * victim.level - victim.exp)/3) + 50 )

        log_buf = "%s got toasted by %s at %s [room %d]" % ( victim.short_descr if IS_NPC(victim) else victim.name,
            ch.short_descr if IS_NPC(ch) else ch.name, ch.in_room.name, ch.in_room.vnum)
 
        if IS_NPC(victim):
            wiznet(log_buf,None,None,WIZ_MOBDEATHS,0,0)
        else:
            wiznet(log_buf,None,None,WIZ_DEATHS,0,0)

        raw_kill( victim )
        # dump the flags */
        if ch != victim and not IS_NPC(ch) and not is_same_clan(ch,victim):
            if IS_SET(victim.act,PLR_KILLER):
                REMOVE_BIT(victim.act,PLR_KILLER)
            else:
                REMOVE_BIT(victim.act,PLR_THIEF)
            # RT new auto commands */
        corpse = get_obj_list(ch,"corpse",ch.in_room.contents)
        if not IS_NPC(ch) and corpse and corpse.item_type == ITEM_CORPSE_NPC and can_see_obj(ch,corpse):
            if IS_SET(ch.act, PLR_AUTOLOOT) and corpse and corpse.contains: # exists and not empty */
                ch.do_get("all corpse")
            
            if IS_SET(ch.act,PLR_AUTOGOLD) and corpse and corpse.contains and not IS_SET(ch.act,PLR_AUTOLOOT):
                coins = get_obj_list(ch,"gcash",corpse.contains)
                if coins: ch.do_get("all.gcash corpse")
            
            if IS_SET(ch.act, PLR_AUTOSAC):
                if IS_SET(ch.act,PLR_AUTOLOOT) and corpse and corpse.contains:
                    return True  # leave if corpse has treasure */
                else:
                    ch.do_sacrifice("corpse")
        return True
    
    if victim == ch:
        return True

     #* Take care of link dead people.
    if not IS_NPC(victim) and victim.desc == None:
        if random.randint( 0, victim.wait ) == 0:
            victim.do_recall("")
            return True

    # * Wimp out?
    if IS_NPC(victim) and dam > 0 and victim.wait < PULSE_VIOLENCE / 2:
        if (IS_SET(victim.act, ACT_WIMPY) and random.randint(0,4) == 0 \
        and victim.hit < victim.max_hit / 5) \
        or ( IS_AFFECTED(victim, AFF_CHARM) and victim.master \
        and victim.master.in_room != victim.in_room ):
            victim.do_flee("")

    if not IS_NPC(victim) and victim.hit > 0 and victim.hit <= victim.wimpy and victim.wait < PULSE_VIOLENCE / 2:
        victim.do_flee("")
    return True

def is_safe(ch, victim):
    if victim.in_room == None or ch.in_room == None:
        return True
    if victim.fighting == ch or victim == ch:
        return False
    if IS_IMMORTAL(ch) and ch.level > LEVEL_IMMORTAL:
        return False
    # killing mobiles */
    if IS_NPC(victim):
        # safe room? */
        if IS_SET(victim.in_room.room_flags,ROOM_SAFE):
            ch.send("Not in this room.\n\r")
            return True
        if victim.pIndexData.pShop:
            ch.send("The shopkeeper wouldn't like that.\n\r")
            return True
        # no killing healers, trainers, etc */
        if IS_SET(victim.act,ACT_TRAIN) \
        or IS_SET(victim.act,ACT_PRACTICE) \
        or IS_SET(victim.act,ACT_IS_HEALER) \
        or IS_SET(victim.act,ACT_IS_CHANGER):
            ch.send("I don't think Mota would approve.\n\r")
            return True
        if not IS_NPC(ch):
            # no pets */
            if IS_SET(victim.act,ACT_PET):
                act("But $N looks so cute and cuddly...", ch,None,victim,TO_CHAR)
                return True

            # no charmed creatures unless owner */
            if IS_AFFECTED(victim,AFF_CHARM) and ch != victim.master:
                ch.send("You don't own that monster.\n\r")
                return True
    # killing players */
    else:
        # NPC doing the killing */
        if IS_NPC(ch):
            # safe room check */
            if IS_SET(victim.in_room.room_flags,ROOM_SAFE):
                ch.send("Not in this room.\n\r")
                return True

            # charmed mobs and pets cannot attack players while owned */
            if IS_AFFECTED(ch,AFF_CHARM) and ch.master and  ch.master.fighting != victim:
                ch.send("Players are your friends!\n\r")
                return True
        # player doing the killing */
        else:
            if not is_clan(ch):
                ch.send("Join a clan if you want to kill players.\n\r")
                return True

            if IS_SET(victim.act,PLR_KILLER) or IS_SET(victim.act,PLR_THIEF):
                return False

            if not is_clan(victim):
                ch.send("They aren't in a clan, leave them alone.\n\r")
                return True

            if ch.level > victim.level + 8:
                ch.send("Pick on someone your own size.\n\r")
                return True
    return False
 
def is_safe_spell(ch, victim, area ):
    if victim.in_room == None or ch.in_room == None:
        return True
    if victim == ch and area:
        return True
    if victim.fighting == ch or victim == ch:
        return False
    if IS_IMMORTAL(ch) and ch.level > LEVEL_IMMORTAL and not area:
        return False
    # killing mobiles */
    if IS_NPC(victim):
        # safe room? */
        if IS_SET(victim.in_room.room_flags,ROOM_SAFE):
            return True
        if victim.pIndexData.pShop:
            return True
        # no killing healers, trainers, etc */
        if IS_SET(victim.act,ACT_TRAIN) \
        or IS_SET(victim.act,ACT_PRACTICE) \
        or IS_SET(victim.act,ACT_IS_HEALER) \
        or IS_SET(victim.act,ACT_IS_CHANGER):
            return True
        if not IS_NPC(ch):
            # no pets */
            if IS_SET(victim.act,ACT_PET):
                return True
            # no charmed creatures unless owner */
            if IS_AFFECTED(victim,AFF_CHARM) and (area or ch != victim.master):
                return True
            # legal kill? -- cannot hit mob fighting non-group member */
            if victim.fighting != None and not is_same_group(ch,victim.fighting):
                return True
        else:
            # area effect spells do not hit other mobs */
            if area and not is_same_group(victim,ch.fighting):
                return True
    # killing players */
    else:
        if area and IS_IMMORTAL(victim) and victim.level > LEVEL_IMMORTAL:
            return True

        # NPC doing the killing */
        if IS_NPC(ch):
            # charmed mobs and pets cannot attack players while owned */
            if IS_AFFECTED(ch,AFF_CHARM) and ch.master and ch.master.fighting != victim:
                return True
            # safe room? */
            if IS_SET(victim.in_room.room_flags,ROOM_SAFE):
                return True

            # legal kill? -- mobs only hit players grouped with opponent*/
            if ch.fighting and not is_same_group(ch.fighting,victim):
                return True
        # player doing the killing */
        else:
            if not is_clan(ch):
                return True
            if IS_SET(victim.act,PLR_KILLER) or IS_SET(victim.act,PLR_THIEF):
                return False
            if not is_clan(victim):
                return True
            if ch.level > victim.level + 8:
                return True
    return False
#
# * See if an attack justifies a KILLER flag.
def check_killer( ch, victim ):
#     * Follow charm thread to responsible character.
#     * Attacking someone's charmed char is hostile!
    while IS_AFFECTED(victim, AFF_CHARM) and victim.master != None:
        victim = victim.master

     # NPC's are fair game.
     # So are killers and thieves.
    if IS_NPC(victim) or IS_SET(victim.act, PLR_KILLER) or IS_SET(victim.act, PLR_THIEF):
        return

     # Charm-o-rama.
    if IS_SET(ch.affected_by, AFF_CHARM):
        if ch.master == None:
            print ("BUG: Check_killer: %s bad AFF_CHARM" % (ch.short_descr if IS_NPC(ch) else ch.name ))
            affect_strip( ch, 'charm person' )
            REMOVE_BIT( ch.affected_by, AFF_CHARM )
            return
    #    send_to_char( "*** You are now a KILLER!! ***\n\r", ch.master )
    #    SET_BIT(ch.master.act, PLR_KILLER)
        stop_follower( ch )
        return

     # NPC's are cool of course (as long as not charmed).
     # Hitting yourself is cool too (bleeding).
     # So is being immortal (Alander's idea).
     # And current killers stay as they are.
    if IS_NPC(ch) or ch == victim or ch.level >= LEVEL_IMMORTAL \
    or not is_clan(ch) or IS_SET(ch.act, PLR_KILLER) or ch.fighting == victim:
        return

    ch.send("*** You are now a KILLER!! ***\n\r")
    SET_BIT(ch.act, PLR_KILLER)
    wiznet("$N is attempting to murder %s" % victim.name,ch,None,WIZ_FLAGS,0,0)
    save_char_obj( ch )
    return
# Check for parry.
def check_parry( ch, victim ):
    if IS_AWAKE(victim):
        return False
    chance = get_skill(victim,'parry') / 2

    if get_eq_char( victim, WEAR_WIELD ) == None:
        if IS_NPC(victim):
            chance /= 2
        else:
            return False
    if not can_see(ch,victim):
        chance /= 2

    if random.randint(1,99) >= chance + victim.level - ch.level:
        return False

    act( "You parry $n's attack.",  ch, None, victim, TO_VICT    )
    act( "$N parries your attack.", ch, None, victim, TO_CHAR    )
    check_improve(victim,'parry',True,6)
    return True

# Check for shield block.
def check_shield_block( ch, victim ):
    if not IS_AWAKE(victim):
        return False
    chance = get_skill(victim,'shield block') / 5 + 3
    if get_eq_char( victim, WEAR_SHIELD ) == None:
        return False
    if random.randint(1,99) >= chance + victim.level - ch.level:
        return False
    act( "You block $n's attack with your shield.",  ch, None, victim, TO_VICT)
    act( "$N blocks your attack with a shield.", ch, None, victim, TO_CHAR)
    check_improve(victim,'shield block',True,6)
    return True

# Check for dodge.
def check_dodge( ch, victim ):
    if not IS_AWAKE(victim):
        return False
    chance = get_skill(victim,'dodge') / 2
    if not can_see(victim,ch):
        chance /= 2
    if random.randint(1,99) >= chance + victim.level - ch.level:
        return False
    act( "You dodge $n's attack.", ch, None, victim, TO_VICT    )
    act( "$N dodges your attack.", ch, None, victim, TO_CHAR    )
    check_improve(victim,'dodge',True,6)
    return True

# Set position of a victim.
def update_pos(victim):
    if victim.hit > 0:
        if victim.position <= POS_STUNNED:
            victim.position = POS_STANDING
        return
    if IS_NPC(victim) and victim.hit < 1:
        victim.position = POS_DEAD
        return
    if victim.hit <= -11:
        victim.position = POS_DEAD
        return

    if victim.hit <= -6: victim.position = POS_MORTAL
    elif victim.hit <= -3: victim.position = POS_INCAP
    else: victim.position = POS_STUNNED

# Start fights.
def set_fighting( ch, victim ):
    if ch.fighting != None:
        print ("BUG: Set_fighting: already fighting")
        return

    if IS_AFFECTED(ch, AFF_SLEEP):
        affect_strip( ch, 'sleep' )

    ch.fighting = victim
    ch.position = POS_FIGHTING

# Stop fights.
def stop_fighting( ch, fBoth ):
    for fch in char_list:
        if fch == ch or ( fBoth and fch.fighting == ch ):
            fch.fighting = None
            fch.position = fch.default_pos if IS_NPC(fch) else POS_STANDING
            update_pos( fch )
    return
#
# * Make a corpse out of a character.
def make_corpse( ch ):
    from db import create_object
    if IS_NPC(ch):
        name = ch.short_descr
        corpse      = create_object(get_obj_index(OBJ_VNUM_CORPSE_NPC), 0)
        corpse.timer   = random.randint( 3, 6 )
        if ch.gold > 0:
            obj_to_obj( create_money( ch.gold, ch.silver ), corpse )
            ch.gold = 0
            ch.silver = 0
        corpse.cost = 0
    else:
        name = ch.name
        corpse = create_object(obj_index_hash[OBJ_VNUM_CORPSE_PC], 0)
        corpse.timer = random.randint( 25, 40 )
        REMOVE_BIT(ch.act,PLR_CANLOOT)
        if not is_clan(ch):
            corpse.owner = ch.name
        else:
            corpse.owner = ""
            if ch.gold > 1 or ch.silver > 1:
                obj_to_obj(create_money(ch.gold / 2, ch.silver/2), corpse)
                ch.gold -= ch.gold/2
                ch.silver -= ch.silver/2
        corpse.cost = 0
    corpse.level = ch.level
    corpse.short_descr = corpse.short_descr % name
    corpse.description = corpse.description % name

    for obj in ch.carrying[:]:
        floating = False
        if obj.wear_loc == WEAR_FLOAT:
            floating = True
        obj_from_char( obj )
        if obj.item_type == ITEM_POTION:
            obj.timer = random.randint(500,1000)
        if obj.item_type == ITEM_SCROLL:
            obj.timer = random.randint(1000,2500)
        if IS_SET(obj.extra_flags,ITEM_ROT_DEATH) and not floating:
            obj.timer = random.randint(5,10)
            REMOVE_BIT(obj.extra_flags,ITEM_ROT_DEATH)
        REMOVE_BIT(obj.extra_flags,ITEM_VIS_DEATH)

        if IS_SET( obj.extra_flags, ITEM_INVENTORY ):
            extract_obj( obj )
        elif floating:
            if IS_OBJ_STAT(obj,ITEM_ROT_DEATH): # get rid of it! */
                if obj.contains:
                    act("$p evaporates,scattering its contents.", ch,obj,None,TO_ROOM)
                    for o in obj.contains[:]:
                        obj_from_obj(o)
                        obj_to_room(o,ch.in_room)
                else:
                    act("$p evaporates.", ch,obj,None,TO_ROOM)
                extract_obj(obj)
            else:
                act("$p falls to the floor.",ch,obj,None,TO_ROOM)
                obj_to_room(obj,ch.in_room)
        else:
            obj_to_obj( obj, corpse )
    obj_to_room( corpse, ch.in_room )
    return

#
# Improved Death_cry contributed by Diavolo.
def death_cry( ch ):
    from db import create_object
    vnum = 0
    msg = "You hear $n's death cry."
    num = random.randint(0,7)
    if num == 0: msg  = "$n hits the ground ... DEAD."
    elif num == 1: 
        if ch.material == 0:
            msg  = "$n splatters blood on your armor."     
    elif num == 2:                            
        if IS_SET(ch.parts,PART_GUTS):
            msg = "$n spills $s guts all over the floor."
            vnum = OBJ_VNUM_GUTS
    elif num ==  3: 
        if IS_SET(ch.parts,PART_HEAD):
            msg  = "$n's severed head plops on the ground."
            vnum = OBJ_VNUM_SEVERED_HEAD               
    elif num ==  4: 
        if IS_SET(ch.parts,PART_HEART):
            msg  = "$n's heart is torn from $s chest."
            vnum = OBJ_VNUM_TORN_HEART             
    elif num ==  5: 
        if IS_SET(ch.parts,PART_ARMS):
            msg  = "$n's arm is sliced from $s dead body."
            vnum = OBJ_VNUM_SLICED_ARM             
    elif num ==  6: 
        if IS_SET(ch.parts,PART_LEGS):
            msg  = "$n's leg is sliced from $s dead body."
            vnum = OBJ_VNUM_SLICED_LEG             
    elif num == 7:
        if IS_SET(ch.parts,PART_BRAINS):
            msg = "$n's head is shattered, and $s brains splash all over you."
            vnum = OBJ_VNUM_BRAINS
    act( msg, ch, None, None, TO_ROOM )
    if vnum != 0:
        name = ch.short_descr if IS_NPC(ch) else ch.name
        obj = create_object( obj_index_hash[vnum], 0 )
        obj.timer = random.randint( 4, 7 )

        obj.short_descr = obj.short_descr % name
        obj.description = obj.description % name
        if obj.item_type == ITEM_FOOD:
            if IS_SET(ch.form,FORM_POISON):
                obj.value[3] = 1
            elif not IS_SET(ch.form,FORM_EDIBLE):
                obj.item_type = ITEM_TRASH
            obj_to_room( obj, ch.in_room )

    if IS_NPC(ch):
        msg = "You hear something's death cry."
    else:
        msg = "You hear someone's death cry."

    was_in_room = ch.in_room
    for pexit in was_in_room.exit:
        if pexit and pexit.to_room and pexit.to_room != was_in_room:
            ch.in_room = pexit.to_room
            act( msg, ch, None, None, TO_ROOM )
    ch.in_room = was_in_room
    return

def raw_kill( victim ):
    stop_fighting( victim, True )
    death_cry( victim )
    make_corpse( victim )

    if IS_NPC(victim):
        victim.pIndexData.killed += 1
        kill_table[min(0, max(victim.level, MAX_LEVEL-1))].killed += 1
        extract_char( victim, True )
        return

    extract_char( victim, False )
    for af in victim.affected[:]:
        affect_remove( victim, af )
    victim.affected_by = victim.race.aff
    victim.armor = [100 for i in range(4)]
    victim.position = POS_RESTING
    victim.hit = max( 1, victim.hit  )
    victim.mana = max( 1, victim.mana )
    victim.move = max( 1, victim.move )
#  save_char_obj( victim ) we're stable enough to not need this :) */
    return

def group_gain( ch, victim ):
    # Monsters don't get kill xp's or alignment changes.
    # P-killing doesn't help either.
    # Dying of mortal wounds or poison doesn't give xp to anyone!
    if victim == ch:
        return
    members = 0
    group_levels = 0
    for gch in ch.in_room.people:
        if is_same_group( gch, ch ):
            members += 1
            group_levels += gch.level / 2 if IS_NPC(gch) else gch.level

    if members == 0:
        print ("BUG: Group_gain: members. %s" % members)
        members = 1
        group_levels = ch.level 

    lch = ch.leader if ch.leader else ch

    for gch in ch.in_room.people:
        if not is_same_group( gch, ch ) or IS_NPC(gch):
            continue

        #Taken out, add it back if you want it
        if gch.level - lch.level >= 5:
            gch.send("You are too high for this group.\n\r")
            continue
        if gch.level - lch.level <= -5:
            gch.send("You are too low for this group.\n\r")
            continue
        #*/

        xp = xp_compute( gch, victim, group_levels )  
        gch.send("You receive %d experience points.\n\r" % xp)
        gain_exp( gch, xp )
        for obj in ch.carrying[:]:
            if obj.wear_loc == WEAR_NONE:
                continue
            if (IS_OBJ_STAT(obj, ITEM_ANTI_EVIL) and IS_EVIL(ch) ) \
            or (IS_OBJ_STAT(obj, ITEM_ANTI_GOOD) and IS_GOOD(ch) ) \
            or (IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) and IS_NEUTRAL(ch) ):
                act( "You are zapped by $p.", ch, obj, None, TO_CHAR )
                act( "$n is zapped by $p.",   ch, obj, None, TO_ROOM )
                obj_from_char( obj )
                obj_to_room( obj, ch.in_room )

 # Compute xp for a kill.
 # Also adjust alignment of killer.
 # Edit this function to change xp computations.
def xp_compute( gch, victim, total_levels ):
    level_range = victim.level - gch.level
    # compute the base exp */
    if level_range == -9 : base_exp = 1
    elif level_range == -8: base_exp = 2
    elif level_range == -7: base_exp = 5
    elif level_range == -6: base_exp = 9
    elif level_range == -5: base_exp = 11
    elif level_range == -4: base_exp = 22
    elif level_range == -3: base_exp = 33
    elif level_range == -2: base_exp = 50
    elif level_range == -1: base_exp = 66
    elif level_range == 0: base_exp = 83
    elif level_range == 1: base_exp = 99
    elif level_range == 2: base_exp = 121
    elif level_range == 3: base_exp = 143
    elif level_range == 4: base_exp = 165
    else: base_exp = 0
    
    if level_range > 4:
        base_exp = 160 + 20 * (level_range - 4)
    # do alignment computations */
    align = victim.alignment - gch.alignment
    if IS_SET(victim.act,ACT_NOALIGN):
        pass    # no change */
    elif align > 500: # monster is more good than slayer */
        change = (align - 500) * base_exp / 500 * gch.level/total_levels 
        change = max(1,change)
        gch.alignment = max(-1000,gch.alignment - change)
    elif align < -500: # monster is more evil than slayer */
        change =  ( -1 * align - 500) * base_exp/500 * gch.level/total_levels
        change = max(1,change)
        gch.alignment = min(1000,gch.alignment + change)
    else: # improve this someday */
        change =  gch.alignment * base_exp/500 * gch.level/total_levels  
        gch.alignment -= change
    # calculate exp multiplier */
    if IS_SET(victim.act,ACT_NOALIGN):
        xp = base_exp
    elif gch.alignment > 500:  # for goodie two shoes */
        if victim.alignment < -750:
            xp = (base_exp *4)/3
        elif victim.alignment < -500:
            xp = (base_exp * 5)/4
        elif victim.alignment > 750:
            xp = base_exp / 4
        elif victim.alignment > 500:
            xp = base_exp / 2
        elif victim.alignment > 250:
            xp = (base_exp * 3)/4 
        else:
            xp = base_exp
    elif gch.alignment < -500:# for baddies */
        if victim.alignment > 750:
            xp = (base_exp * 5)/4
        elif victim.alignment > 500:
            xp = (base_exp * 11)/10 
        elif victim.alignment < -750:
            xp = base_exp/2
        elif victim.alignment < -500:
            xp = (base_exp * 3)/4
        elif victim.alignment < -250:
            xp = (base_exp * 9)/10
        else:
            xp = base_exp
    elif gch.alignment > 200:  # a little good */
        if victim.alignment < -500:
            xp = (base_exp * 6)/5
        elif victim.alignment > 750:
            xp = base_exp/2
        elif victim.alignment > 0:
            xp = (base_exp * 3)/4 
        else:
            xp = base_exp
    elif gch.alignment < -200: # a little bad */
        if victim.alignment > 500:
            xp = (base_exp * 6)/5
        elif victim.alignment < -750:
            xp = base_exp/2
        elif victim.alignment < 0:
            xp = (base_exp * 3)/4
        else:
            xp = base_exp
    else: # neutral */
        if victim.alignment > 500 or victim.alignment < -500:
            xp = (base_exp * 4)/3
        elif victim.alignment < 200 and victim.alignment > -200:
            xp = base_exp/2
        else:
            xp = base_exp
    # more exp at the low levels */
    if gch.level < 6:
        xp = 10 * xp / (gch.level + 4)

    # less at high */
    if gch.level > 35:
        xp =  15 * xp / (gch.level - 25 )
    # reduce for playing time */
    # compute quarter-hours per level */
    time_per_level = 4 * (gch.played + (int) (current_time - gch.logon))/3600 / gch.level
    time_per_level = min(2,max(time_per_level,12))
    if gch.level < 15:  # make it a curve */
        time_per_level = max(time_per_level,(15 - gch.level))
    xp = xp * time_per_level / 12
    # randomize the rewards */
    xp = random.randint (xp * 3/4, xp * 5/4)
    # adjust for grouping */
    xp = xp * gch.level/( max(1,total_levels -1) )
    return xp

def dam_message( ch, victim, dam, dt, immune ):
    if ch == None or victim == None:
        return

    if dam == 0: msg = {'vs':"miss", 'vp':"misses"}
    elif dam <= 4: msg = {'vs':"scratch", 'vp':"scratches"}
    elif dam <=   8: msg = {'vs':"graze", 'vp':"grazes"}
    elif dam <=  12: msg = {'vs':"hit", 'vp':"hits"}
    elif dam <=  16: msg = {'vs':"injure", 'vp':"injures"}
    elif dam <=  20: msg = {'vs':"wound", 'vp':"wounds"}
    elif dam <=  24: msg = {'vs':"maul", 'vp':"mauls"}
    elif dam <=  28: msg = {'vs':"decimate", 'vp':"decimates"}
    elif dam <=  32: msg = {'vs':"devastate", 'vp':"devastates"}
    elif dam <=  36: msg = {'vs':"maim", 'vp':"maims"}
    elif dam <=  40: msg = {'vs':"MUTILATE", 'vp':"MUTILATES"}
    elif dam <=  44: msg = {'vs':"DISEMBOWEL", 'vp':"DISEMBOWELS"}
    elif dam <=  48: msg = {'vs':"DISMEMBER", 'vp':"DISMEMBERS"}
    elif dam <=  52: msg = {'vs':"MASSACRE", 'vp':"MASSACRES"}
    elif dam <=  56: msg = {'vs':"MANGLE", 'vp':"MANGLES"}
    elif dam <=  60: msg = {'vs':"*** DEMOLISH ***", 'vp':"*** DEMOLISHES ***"}
    elif dam <=  75: msg = {'vs':"*** DEVASTATE ***", 'vp':"*** DEVASTATES ***"}
    elif dam <= 100: msg = {'vs':"=== OBLITERATE ===", 'vp':"=== OBLITERATES ==="}
    elif dam <= 125: msg = {'vs':">>> ANNIHILATE <<<", 'vp':">>> ANNIHILATES <<<"}
    elif dam <= 150: msg = {'vs':"<<< ERADICATE >>>", 'vp':"<<< ERADICATES >>>"}
    else: msg = {'vs':"do UNSPEAKABLE things to", 'vp':"does UNSPEAKABLE things to"}
    vs = msg['vs']
    vp = msg['vp']
    punct = '.' if dam <= 24 else '!'
    if dt == TYPE_HIT:
        if ch == victim:
            buf1 = "$n %s $melf%c" % (vp,punct)
            buf2 = "You %s yourself%c" % (vs, punct)
        else:
            buf1 = "$n %s $N%c" % ( vp, punct )
            buf2 = "You %s $N%c" % ( vs, punct )
            buf3 = "$n %s you%c" % ( vp, punct )
    else:
        if dt >= 0 and dt < MAX_SKILL:
            attack  = skill_table[dt].noun_damage
        elif dt >= TYPE_HIT and dt < TYPE_HIT + len(const.attack_table):
            attack = const.attack_table[dt - TYPE_HIT].noun
        else:
            print ("BUG: Dam_message: bad dt %d.")
            dt = TYPE_HIT
            attack  = const.attack_table[0].name
        if immune:
            if ch == victim:
                buf1 = "$n is unaffected by $s own %s." % attack
                buf2 = "Luckily, you are immune to that."
            else:
                buf1 = "$N is unaffected by $n's %s!" % attack
                buf2 = "$N is unaffected by your %s!" % attack
                buf3 = "$n's %s is powerless against you." % attack
        else:
            if ch == victim:
                buf1 = "$n's %s %s $m%c" % (attack,vp,punct)
                buf2 = "Your %s %s you%c" % (attack,vp,punct)
            else:
                buf1 = "$n's %s %s $N%c" % (attack, vp, punct)
                buf2 = "Your %s %s $N%c" %  (attack, vp, punct)
                buf3 = "$n's %s %s you%c" % (attack, vp, punct)

    if ch == victim:
        act(buf1,ch,None,None,TO_ROOM)
        act(buf2,ch,None,None,TO_CHAR)
    else:
        act( buf1, ch, None, victim, TO_NOTVICT )
        act( buf2, ch, None, victim, TO_CHAR )
        act( buf3, ch, None, victim, TO_VICT )
    return

# * Disarm a creature.
# * Caller must check for successful attack.
def disarm( ch, victim ):
    obj = get_eq_char( victim, WEAR_WIELD )
    if not obj:
        ch.send("I think you're taking disarm a little too literally")
        return

    if IS_OBJ_STAT(obj,ITEM_NOREMOVE):
        act("$S weapon won't budge!",ch,None,victim,TO_CHAR)
        act("$n tries to disarm you, but your weapon won't budge!", ch,None,victim,TO_VICT)
        act("$n tries to disarm $N, but fails.",ch,None,victim,TO_NOTVICT)
        return
    act( "$n DISARMS you and sends your weapon flying!", ch, None, victim, TO_VICT)
    act( "You disarm $N!",  ch, None, victim, TO_CHAR    )
    act( "$n disarms $N!",  ch, None, victim, TO_NOTVICT )
    obj_from_char( obj )
    if IS_OBJ_STAT(obj,ITEM_NODROP) or IS_OBJ_STAT(obj,ITEM_INVENTORY):
        obj_to_char( obj, victim )
    else:
        obj_to_room( obj, victim.in_room )
        if IS_NPC(victim) and victim.wait == 0 and can_see_obj(victim,obj):
            get_obj(victim,obj,None)
    return

def do_berserk( self, argument):
    ch = self
    chance = get_skill(ch, 'berserk')
    if chance== 0 or (IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_BERSERK)) \
    or  (not IS_NPC(ch) and ch.level < skill_table['berserk'].skill_level[ch.guild]):
        ch.send("You turn red in the face, but nothing happens.\n\r")
        return

    if IS_AFFECTED(ch,AFF_BERSERK) or is_affected(ch,'berserk') or is_affected(ch,"frenzy"):
        ch.send("You get a little madder.\n\r")
        return
    if IS_AFFECTED(ch,AFF_CALM):
        ch.send("You're feeling to mellow to berserk.\n\r")
        return
    if ch.mana < 50:
        ch.send("You can't get up enough energy.\n\r")
        return
    # modifiers */
    # fighting */
    if ch.position == POS_FIGHTING:
        chance += 10

    # damage -- below 50% of hp helps, above hurts */
    hp_percent = 100 * ch.hit/ch.max_hit
    chance += 25 - hp_percent/2

    if random.randint(1,99) < chance:
        WAIT_STATE(ch,PULSE_VIOLENCE)
        ch.mana -= 50
        ch.move /= 2
        # heal a little damage */
        ch.hit += ch.level * 2
        ch.hit = min(ch.hit,ch.max_hit)
        ch.send("Your pulse races as you are consumed by rage!\n\r")
        act("$n gets a wild look in $s eyes.",ch,None,None,TO_ROOM)
        check_improve(ch,'berserk',True,2)
        af = AFFECT_DATA()
        af.where    = TO_AFFECTS
        af.type     = 'berserk'
        af.level    = ch.level
        af.duration = number_fuzzy(ch.level / 8)
        af.modifier = max(1,ch.level/5)
        af.bitvector    = AFF_BERSERK

        af.location = APPLY_HITROLL
        affect_to_char(ch,af)

        af.location = APPLY_DAMROLL
        affect_to_char(ch,af)

        af.modifier = max(10,10 * (ch.level/5))
        af.location = APPLY_AC
        affect_to_char(ch,af)
    else:
        WAIT_STATE(ch,3 * PULSE_VIOLENCE)
        ch.mana -= 25
        ch.move /= 2

        ch.send("Your pulse speeds up, but nothing happens.\n\r")
        check_improve(ch,'berserk',False,2)

def do_bash( ch, argument ):
    arghold, arg = read_word(argument)
    chance = get_skill(ch,'bash')
    if chance == 0 or (IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_BASH)) \
    or (not IS_NPC(ch) and ch.level < skill_table['bash'].skill_level[ch.guild.name] ):
        ch.send("Bashing? What's that?\n\r")
        return
    victim = None 
    if not arg:
        victim = ch.fighting
        if not victim:
            ch.send("But you aren't fighting anyone!\n\r")
            return
    else:
        victim = get_char_room(ch,arg)
        if not victim:
            ch.send("They aren't here.\n\r")
            return
    if victim.position < POS_FIGHTING:
        act("You'll have to let $M get back up first.",ch,None,victim,TO_CHAR)
        return
    if victim == ch:
        ch.send("You try to bash your brains out, but fail.\n\r")
        return
    if is_safe(ch,victim):
        return
    if IS_NPC(victim) and victim.fighting and not is_same_group(ch,victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(ch,AFF_CHARM) and ch.master == victim:
        act("But $N is your friend!",ch,None,victim,TO_CHAR)
        return

    # modifiers */
    # size  and weight */
    chance += ch.carry_weight / 250
    chance -= victim.carry_weight / 200
    if ch.size < victim.size:
        chance += (ch.size - victim.size) * 15
    else:
        chance += (ch.size - victim.size) * 10 


    # stats */
    chance += get_curr_stat(ch,STAT_STR)
    chance -= (get_curr_stat(victim,STAT_DEX) * 4)/3
    chance -= GET_AC(victim,AC_BASH) /25
    # speed */
    if IS_SET(ch.off_flags,OFF_FAST) or IS_AFFECTED(ch,AFF_HASTE):
        chance += 10
    if IS_SET(victim.off_flags,OFF_FAST) or IS_AFFECTED(victim,AFF_HASTE):
        chance -= 30
    # level */
    chance += (ch.level - victim.level)
    if not IS_NPC(victim) and chance < get_skill(victim,'dodge'):
        pass
        #act("$n tries to bash you, but you dodge it.",ch,None,victim,TO_VICT)
        #act("$N dodges your bash, you fall flat on your face.",ch,None,victim,TO_CHAR)
        #WAIT_STATE(ch,skill_table['bash'].beats)
        #return*/
        chance -= 3 * (get_skill(victim,'dodge') - chance)
    # now the attack */
    if random.randint(1,99) < chance:
        act("$n sends you sprawling with a powerful bash!", ch,None,victim,TO_VICT)
        act("You slam into $N, and send $M flying!",ch,None,victim,TO_CHAR)
        act("$n sends $N sprawling with a powerful bash.", ch,None,victim,TO_NOTVICT)
        check_improve(ch,'bash',True,1)
        DAZE_STATE(victim, 3 * PULSE_VIOLENCE)
        WAIT_STATE(ch,skill_table['bash'].beats)
        victim.position = POS_RESTING
        damage(ch,victim,random.randint(2,2 + 2 * ch.size + chance/20),'bash', DAM_BASH,False)
    else:
        damage(ch,victim,0,'bash',DAM_BASH,False)
        act("You fall flat on your face!", ch,None,victim,TO_CHAR)
        act("$n falls flat on $s face.", ch,None,victim,TO_NOTVICT)
        act("You evade $n's bash, causing $m to fall flat on $s face.", ch,None,victim,TO_VICT)
        check_improve(ch,'bash',False,1)
        ch.position = POS_RESTING
        WAIT_STATE(ch,skill_table['bash'].beats * 3/2) 
    check_killer(ch,victim)

def do_dirt( self, argument ):
    ch = self
    arghold, arg = read_word(argument)
    chance = get_skill(ch, 'dirt kicking')
    if chance == 0 or (IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_KICK_DIRT)) \
    or ( not IS_NPC(ch) and ch.level < skill_table['dirt kicking'].skill_level[ch.guild]):
        ch.send("You get your feet dirty.\n\r")
        return
    if not arg:
        victim = ch.fighting
        if victim == None:
            ch.send("But you aren't in combat!\n\r")
            return
    else:
        victim = get_char_room(ch,arg)
        if victim == None:
            ch.send("They aren't here.\n\r")
            return
    if IS_AFFECTED(victim,AFF_BLIND):
        act("$E's already been blinded.",ch,None,victim,TO_CHAR)
        return
    if victim == ch:
        ch.send("Very funny.\n\r")
        return
    if is_safe(ch,victim):
        return
    if IS_NPC(victim) and victim.fighting != None and not is_same_group(ch,victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(ch,AFF_CHARM) and ch.master == victim:
        act("But $N is such a good friend!",ch,None,victim,TO_CHAR)
        return

    # modifiers */
    # dexterity */
    chance += get_curr_stat(ch,STAT_DEX)
    chance -= 2 * get_curr_stat(victim,STAT_DEX)

    # speed  */
    if IS_SET(ch.off_flags,OFF_FAST) or IS_AFFECTED(ch,AFF_HASTE):
        chance += 10
    if IS_SET(victim.off_flags,OFF_FAST) or IS_AFFECTED(victim,AFF_HASTE):
        chance -= 25
    # level */
    chance += (ch.level - victim.level) * 2

    # sloppy hack to prevent false zeroes */
    if chance % 5 == 0:
        chance += 1
    # terrain */
    nochance = [ SECT_WATER_SWIM, SECT_WATER_NOSWIM, SECT_AIR ]
    modifiers = { SECT_INSIDE: -20,
                  SECT_CITY: -10,
                  SECT_FIELD: 5,
                  SECT_MOUNTAIN: -10,
                  SECT_DESERT: 10
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
        act("$n is blinded by the dirt in $s eyes!",victim,None,None,TO_ROOM)
        act("$n kicks dirt in your eyes!",ch,None,victim,TO_VICT)
        damage(ch,victim,random.randint(2,5),'dirt kicking',DAM_NONE,False)
        victim.send("You can't see a thing!\n\r")
        check_improve(ch,'dirt kicking',True,2)
        WAIT_STATE(ch,skill_table['dirt kicking'].beats)
        af = AFFECT_DATA()
        af.where    = TO_AFFECTS
        af.type     = 'dirt kicking'
        af.level    = ch.level
        af.duration = 0
        af.location = APPLY_HITROLL
        af.modifier = -4
        af.bitvector    = AFF_BLIND
        affect_to_char(victim,af)
    else:
        damage(ch,victim,0,'dirt kicking',DAM_NONE,True)
        check_improve(ch,'dirt kicking',False,2)
        WAIT_STATE(ch,skill_table['dirt kicking'].beats)
    check_killer(ch,victim)

def do_trip( self, argument ):
    ch = self
    arghold, arg = one_argument(argument)
    chance = get_skill(ch, 'trip')
    if chance == 0 or (IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_TRIP)) \
    or ( not IS_NPC(ch) and ch.level < skill_table['trip'].skill_level[ch.guild]):
        ch.send("Tripping?  What's that?\n\r")
        return
    if not arg:
        victim = ch.fighting
        if victim == None:
            ch.send("But you aren't fighting anyone!\n\r")
            return
    else:
        victim = get_char_room(ch,arg)
        if victim == None:
            ch.send("They aren't here.\n\r")
            return
    if is_safe(ch,victim):
        return
    if IS_NPC(victim) and victim.fighting and not is_same_group(ch,victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(victim,AFF_FLYING):
        act("$S feet aren't on the ground.",ch,None,victim,TO_CHAR)
        return
    if victim.position < POS_FIGHTING:
        act("$N is already down.",ch,None,victim,TO_CHAR)
        return
    if victim == ch:
        ch.send("You fall flat on your face!\n\r")
        WAIT_STATE(ch,2 * skill_table['trip'].beats)
        act("$n trips over $s own feet!",ch,None,None,TO_ROOM)
        return

    if IS_AFFECTED(ch,AFF_CHARM) and ch.master == victim:
        act("$N is your beloved master.",ch,None,victim,TO_CHAR)
        return
    # modifiers */
    # size */
    if ch.size < victim.size:
        chance += (ch.size - victim.size) * 10  # bigger = harder to trip */

    # dex */
    chance += get_curr_stat(ch,STAT_DEX)
    chance -= get_curr_stat(victim,STAT_DEX) * 3 / 2

    # speed */
    if IS_SET(ch.off_flags,OFF_FAST) or IS_AFFECTED(ch,AFF_HASTE):
        chance += 10
    if IS_SET(victim.off_flags,OFF_FAST) or IS_AFFECTED(victim,AFF_HASTE):
        chance -= 20
    # level */
    chance += (ch.level - victim.level) * 2
    # now the attack */
    if random.randint(1,99) < chance:
        act("$n trips you and you go down!",ch,None,victim,TO_VICT)
        act("You trip $N and $N goes down!",ch,None,victim,TO_CHAR)
        act("$n trips $N, sending $M to the ground.",ch,None,victim,TO_NOTVICT)
        check_improve(ch,'trip',True,1)

        DAZE_STATE(victim,2 * PULSE_VIOLENCE)
        WAIT_STATE(ch,skill_table['trip'].beats)
        victim.position = POS_RESTING
        damage(ch,victim,random.randint(2, 2 +  2 * victim.size),'trip', DAM_BASH,True)
    else:
        damage(ch,victim,0,'trip',DAM_BASH,True)
        WAIT_STATE(ch,skill_table['trip'].beats*2/3)
        check_improve(ch,'trip',False,1)
    check_killer(ch,victim)

def do_kill( self, argument ):
    ch = self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Kill whom?\n\r")
        return
    victim = get_char_room( ch, arg )
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
        multi_hit( ch, ch, TYPE_UNDEFINED )
        return
    if is_safe( ch, victim ):
        return
    if victim.fighting and not is_same_group(ch,victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(ch, AFF_CHARM) and ch.master == victim:
        act( "$N is your beloved master.", ch, None, victim, TO_CHAR )
        return
    if ch.position == POS_FIGHTING:
        ch.send("You do the best you can!\n\r")
        return

    WAIT_STATE( ch, 1 * PULSE_VIOLENCE )
    check_killer( ch, victim )
    multi_hit( ch, victim, TYPE_UNDEFINED )
    return

def do_murde( self, argument ):
    self.send("If you want to MURDER, spell it out.\n\r")
    return

def do_murder( self, argument ):
    ch = self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Murder whom?\n\r")
        return

    if IS_AFFECTED(ch,AFF_CHARM) or (IS_NPC(ch) and IS_SET(ch.act,ACT_PET)):
        return
    victim = get_char_room( ch, arg )
    if victim == None:
        ch.send("They aren't here.\n\r")
        return
    if victim == ch:
        ch.send("Suicide is a mortal sin.\n\r")
        return
    if is_safe( ch, victim ):
        return
    if IS_NPC(victim) and victim.fighting and not is_same_group(ch,victim.fighting):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    if IS_AFFECTED(ch, AFF_CHARM) and ch.master == victim:
        act( "$N is your beloved master.", ch, None, victim, TO_CHAR )
        return
    if ch.position == POS_FIGHTING:
        ch.send("You do the best you can!\n\r")
        return

    WAIT_STATE( ch, 1 * PULSE_VIOLENCE )
    if IS_NPC(ch):
        buf = "Help! I am being attacked by %s!" % ch.short_descr
    else:
        buf = "Help!  I am being attacked by %s!" % ch.name
    victim.do_yell(buf)
    check_killer( ch, victim )
    multi_hit( ch, victim, TYPE_UNDEFINED )
    return

def do_backstab( self, argument ):
    ch = self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Backstab whom?\n\r")
        return
    victim = None
    if ch.fighting:
        ch.send("You're facing the wrong end.\n\r")
        return
    else:
        victim = get_char_room(ch,arg)
        if not victim:
            ch.send("They aren't here.\n\r")
            return
        if victim == ch:
            ch.send("How can you sneak up on yourself?\n\r")
            return

        if is_safe( ch, victim ):
            return

        if IS_NPC(victim) and victim.fighting and not is_same_group(ch,victim.fighting):
            ch.send("Kill stealing is not permitted.\n\r")
            return
        obj = get_eq_char( ch, WEAR_WIELD )
        if obj:
            ch.send("You need to wield a weapon to backstab.\n\r")
            return
        if victim.hit < victim.max_hit / 3:
            act( "$N is hurt and suspicious ... you can't sneak up.", ch, None, victim, TO_CHAR )
            return
        check_killer( ch, victim )
        WAIT_STATE( ch, skill_table['backstab'].beats )
        if random.randint(1,99) < get_skill(ch,'backstab') \
        or ( get_skill(ch,'backstab') >= 2 and not IS_AWAKE(victim) ):
            check_improve(ch,'backstab',True,1)
            multi_hit( ch, victim, 'backstab' )
        else:
            check_improve(ch,'backstab',False,1)
            damage( ch, victim, 0, 'backstab',DAM_NONE,True)
    return

def do_flee( ch, argument ):
    victim = ch.fighting
    if not victim:
        if ch.position == POS_FIGHTING:
            ch.position = POS_STANDING
        ch.send("You aren't fighting anyone.\n\r")
        return

    was_in = ch.in_room
    for attempt in range(6):
        door = number_door( )
        pexit = was_in.exit[door]
        if not pexit or not pexit.to_room or IS_SET(pexit.exit_info, EX_CLOSED) or random.randint(0,ch.daze) != 0 \
        or ( IS_NPC(ch) and IS_SET(pexit.u1.to_room.room_flags, ROOM_NO_MOB) ):
            continue

        move_char( ch, door, False )
        now_in = ch.in_room
        if  now_in == was_in:
            continue

        ch.in_room = was_in
        act( "$n has fled!", ch, None, None, TO_ROOM )
        ch.in_room = now_in

        if not IS_NPC(ch):
            ch.send("You flee from combat!\n\r")
            if ch.guild == 2 and (random.randint(1,99) < 3*(ch.level/2) ):
                ch.send("You snuck away safely.\n\r")
            else:
                ch.send("You lost 10 exp.\n\r") 
                gain_exp( ch, -10 )

        stop_fighting( ch, True )
        return
    ch.send("PANIC! You couldn't escape!\n\r")
    return

def do_rescue( self, argument ):
    ch = self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Rescue whom?\n\r")
        return
    victim = get_char_room(ch,arg)
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if victim == ch:
        ch.send("What about fleeing instead?\n\r")
        return
    if not IS_NPC(ch) and IS_NPC(victim):
        ch.send("Doesn't need your help!\n\r")
        return
    if ch.fighting == victim:
        ch.send("Too late.\n\r")
        return
    fch = victim.fighting
    if not fch:
        ch.send("That person is not fighting right now.\n\r")
        return
    if IS_NPC(fch) and not is_same_group(ch,victim):
        ch.send("Kill stealing is not permitted.\n\r")
        return
    WAIT_STATE( ch, skill_table['rescue'].beats )
    if random.randint(1,99) > get_skill(ch,'rescue'):
        ch.send("You fail the rescue.\n\r")
        check_improve(ch,'rescue',False,1)
        return
    act( "You rescue $N!",  ch, None, victim, TO_CHAR    )
    act( "$n rescues you!", ch, None, victim, TO_VICT    )
    act( "$n rescues $N!",  ch, None, victim, TO_NOTVICT )
    check_improve(ch,'rescue',True,1)

    stop_fighting( fch, False )
    stop_fighting( victim, False )

    check_killer( ch, fch )
    set_fighting( ch, fch )
    set_fighting( fch, ch )
    return

def do_kick( self, argument ):
    ch = self
    if not IS_NPC(ch) and ch.level < skill_table['kick'].skill_level[ch.guild]:
        ch.send("You better leave the martial arts to fighters.\n\r")
        return
    if IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_KICK):
        return
    victim = ch.fighting
    if not victim:
        ch.send("You aren't fighting anyone.\n\r")
        return

    WAIT_STATE( ch, skill_table['kick'].beats )
    if get_skill(ch,'kick') > random.randint(1,99):
        damage(ch,victim,random.randint( 1, ch.level ), 'kick',DAM_BASH,True)
        check_improve(ch,'kick',True,1)
    else:
        damage( ch, victim, 0, 'kick',DAM_BASH,True)
        check_improve(ch,'kick',False,1)
    check_killer(ch,victim)
    return

def do_disarm( ch, argument ):
    hth = 0
    chance = get_skill(ch,'disarm')
    if chance == 0:
        ch.send("You don't know how to disarm opponents.\n\r")
        return
    hth = get_skill(ch,'hand to hand')
    if not get_eq_char( ch, WEAR_WIELD ) \
    and hth == 0 or (IS_NPC(ch) and not IS_SET(ch.off_flags,OFF_DISARM)):
        ch.send("You must wield a weapon to disarm.\n\r")
        return
    victim = ch.fighting
    if not victim:
        ch.send("You aren't fighting anyone.\n\r")
        return
    obj = get_eq_char( victim, WEAR_WIELD )
    if not obj:
        ch.send("Your opponent is not wielding a weapon.\n\r")
        return

    # find weapon skills */
    ch_weapon = get_weapon_skill(ch,get_weapon_sn(ch))
    vict_weapon = get_weapon_skill(victim,get_weapon_sn(victim))
    ch_vict_weapon = get_weapon_skill(ch,get_weapon_sn(victim))

    # modifiers */

    # skill */
    if get_eq_char(ch,WEAR_WIELD) == None:
        chance = chance * hth/150
    else:
        chance = chance * ch_weapon/100

    chance += (ch_vict_weapon/2 - vict_weapon) / 2 

    # dex vs. strength */
    chance += get_curr_stat(ch,STAT_DEX)
    chance -= 2 * get_curr_stat(victim,STAT_STR)

    # level */
    chance += (ch.level - victim.level) * 2
 
    # and now the attack */
    if random.randint(1,99) < chance:
        WAIT_STATE( ch, skill_table['disarm'].beats )
        disarm( ch, victim )
        check_improve(ch,'disarm',True,1)
    else:
        WAIT_STATE(ch,skill_table['disarm'].beats)
        act("You fail to disarm $N.",ch,None,victim,TO_CHAR)
        act("$n tries to disarm you, but fails.",ch,None,victim,TO_VICT)
        act("$n tries to disarm $N, but fails.",ch,None,victim,TO_NOTVICT)
        check_improve(ch,'disarm',False,1)
    check_killer(ch,victim)
    return

def do_sla(ch, argument ):
    ch.send("If you want to SLAY, spell it out.\n\r")
    return

def do_slay( ch, argument ):
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Slay whom?\n\r")
        return
    victim = get_char_room( ch, arg )
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if ch == victim:
        ch.send("Suicide is a mortal sin.\n\r")
        return
    if not IS_NPC(victim) and victim.level >= get_trust(ch):
        ch.send("You failed.\n\r")
        return
    act( "You slay $M in cold blood!",  ch, None, victim, TO_CHAR    )
    act( "$n slays you in cold blood!", ch, None, victim, TO_VICT    )
    act( "$n slays $N in cold blood!",  ch, None, victim, TO_NOTVICT )
    raw_kill( victim )
    return
