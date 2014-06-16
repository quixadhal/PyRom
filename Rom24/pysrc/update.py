"""
#**************************************************************************
 *  Original Diku Mud copyright (C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright (C) 1992, 1993 by Michael          *
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
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
from merc import *
from db import area_update
from handler import *
from comm import act
from save import save_char_obj
from fight import violence_update
import act_move
# * Advancement stuff.

def advance_level( ch, hide ):
    ch.pcdata.last_level = ( ch.played + (int) (current_time - ch.logon) ) / 3600

    buf = "the %s" % ( title_table [ch.guild ] [ch.level] [1 if ch.sex == SEX_FEMALE else 0] )
    set_title( ch, buf )

    add_hp = con_app[get_curr_stat(ch,STAT_CON)].hitp + random.randint( ch.guild.hp_min, ch.guild.hp_max )
    add_mana = random.randint( 2, (2*get_curr_stat(ch,STAT_INT) + get_curr_stat(ch,STAT_WIS))/5)
    if not ch.guild.fMana:
        add_mana /= 2
    add_move    = random.randint( 1, (get_curr_stat(ch,STAT_CON) + get_curr_stat(ch,STAT_DEX))/6 )
    add_prac    = wis_app[get_curr_stat(ch,STAT_WIS)].practice

    add_hp = add_hp * 9/10
    add_mana = add_mana * 9/10
    add_move = add_move * 9/10

    add_hp = max(  2, add_hp   )
    add_mana = max(  2, add_mana )
    add_move = max(  6, add_move )

    ch.max_hit     += add_hp
    ch.max_mana    += add_mana
    ch.max_move    += add_move
    ch.practice    += add_prac
    ch.train       += 1

    ch.pcdata.perm_hit    += add_hp
    ch.pcdata.perm_mana   += add_mana
    ch.pcdata.perm_move   += add_move

    if not hide:
        ch.send("You gain %d hit point%s, %d mana, %d move, and %d practice%s.\n" % ( 
            add_hp, "" if add_hp == 1 else "s", add_mana, add_move, add_prac, "" if add_prac == 1 else "s") )

def gain_exp( ch, gain ):
    if IS_NPC(ch) or ch.level >= LEVEL_HERO:
        return

    ch.exp = max( exp_per_level(ch,ch.pcdata.points), ch.exp + gain )
    while ch.level < LEVEL_HERO and ch.exp >= exp_per_level(ch,ch.pcdata.points) * (ch.level+1):
        ch.send("You raise a level!!  ")
        ch.level += 1
        print ("%s gained level %d\r\n" % (ch.name,ch.level))
        wiznet("$N has attained level %d!" % ch.level,ch,None,WIZ_LEVELS,0,0)
        advance_level(ch,False)
        save_char_obj(ch)

# * Regeneration stuff.
def hit_gain( ch ):
    if not ch.in_room:
        return 0

    if IS_NPC(ch):
        gain = 5 + ch.level
        if IS_AFFECTED(ch,AFF_REGENERATION):
            gain *= 2

        if ch.position == POS_SLEEPING:  gain = 3 * gain/2
        elif ch.position == POS_RESTING: pass
        elif ch.position == POS_FIGHTING:  gain /= 3
        else: gain /= 2
    else:
        gain = max(3,get_curr_stat(ch,STAT_CON) - 3 + ch.level/2) 
        gain += ch.guild.hp_max - 10
        number = random.randint(1,99)
        if number < get_skill(ch,'fast healing'):
            gain += number * gain / 100
            if ch.hit < ch.max_hit:
                check_improve(ch,'fast healing',True,8)

        if ch.position == POS_SLEEPING: pass
        elif ch.position == POS_RESTING: gain /= 2
        elif ch.position == POS_FIGHTING:  gain /= 6
        else: gain /= 4

        if not ch.pcdata.condition[COND_HUNGER]:
            gain /= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain /= 2

    gain = gain * ch.in_room.heal_rate / 100
    
    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[3] / 100

    if IS_AFFECTED(ch, AFF_POISON):
        gain /= 4

    if IS_AFFECTED(ch, AFF_PLAGUE):
        gain /= 8

    if IS_AFFECTED(ch,AFF_HASTE) or IS_AFFECTED(ch,AFF_SLOW):
        gain /=2 

    return min(gain, ch.max_hit - ch.hit)

def mana_gain( ch ):
    if ch.in_room == None:
        return 0

    if IS_NPC(ch):
        gain = 5 + ch.level
        if ch.position == POS_SLEEPING: 3 * gain/2
        elif ch.position == POS_RESTING: pass
        elif ch.position == POS_FIGHTING:  gain /= 3
        else: gain /= 2
    else:
        gain = (get_curr_stat(ch,STAT_WIS) + get_curr_stat(ch,STAT_INT) + ch.level) / 2
        number = random.randint(1,99)
        if number < get_skill(ch,'meditation'):
            gain += number * gain / 100
            if ch.mana < ch.max_mana:
                check_improve(ch,'meditation',True,8)

        if not ch.guild.fMana:
            gain /= 2
        if ch.position == POS_SLEEPING: pass
        elif ch.position == POS_RESTING: gain /= 2
        elif ch.position == POS_FIGHTING:  gain /= 6
        else: gain /= 4

        if not ch.pcdata.condition[COND_HUNGER]:
            gain /= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain /= 2

    gain = gain * ch.in_room.mana_rate / 100

    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[4] / 100

    if IS_AFFECTED( ch, AFF_POISON ):
        gain /= 4

    if IS_AFFECTED(ch, AFF_PLAGUE):
        gain /= 8

    if IS_AFFECTED(ch,AFF_HASTE) or IS_AFFECTED(ch,AFF_SLOW):
        gain /=2 

    return min(gain, ch.max_mana - ch.mana)

def move_gain( ch ):
    if not ch.in_room:
        return 0

    if IS_NPC(ch):
        gain = ch.level
    else:
        gain = max( 15, ch.level )
    
        if ch.position == POS_SLEEPING: gain += get_curr_stat(ch,STAT_DEX)
        elif ch.position == POS_RESTING: gain += get_curr_stat(ch,STAT_DEX) / 2

        if not ch.pcdata.condition[COND_HUNGER]:
            gain /= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain /= 2
    

    gain = gain * ch.in_room.heal_rate/100

    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[3] / 100

    if IS_AFFECTED(ch, AFF_POISON):
        gain /= 4

    if IS_AFFECTED(ch, AFF_PLAGUE):
        gain /= 8

    if IS_AFFECTED(ch,AFF_HASTE) or IS_AFFECTED(ch,AFF_SLOW):
        gain /=2 

    return min(gain, ch.max_move - ch.move)

def gain_condition( ch, iCond, value ):
    if value == 0 or IS_NPC(ch) or ch.level >= LEVEL_IMMORTAL:
        return
    
    condition = ch.pcdata.condition[iCond]
    if condition == -1:
        return
    ch.pcdata.condition[iCond]    = min( 0, max(condition + value, 48 ))

    if ch.pcdata.condition[iCond] == 0:
        if iCond == COND_HUNGER:
            ch.send("You are hungry.\n")
        elif iCond == COND_THIRST:
            ch.send("You are thirsty.\n")
        elif iCond == COND_DRUNK:
            if condition != 0:
                ch.send("You are sober.\n")


# * Mob autonomous action.
# * This function takes 25% to 35% of ALL Merc cpu time.
# * -- Furey
def mobile_update( ):
    # Examine all mobs. */
    for ch in char_list[:]:
        if not IS_NPC(ch) or ch.in_room == None or IS_AFFECTED(ch,AFF_CHARM):
            continue

        if ch.in_room.area.empty and not IS_SET(ch.act,ACT_UPDATE_ALWAYS):
            continue

        # Examine call for special procedure */
        if ch.spec_fun:
            if ch.spec_fun( ch ):
                continue

        if ch.pIndexData.pShop: # give him some gold */
            if (ch.gold * 100 + ch.silver) < ch.pIndexData.wealth:
                ch.gold += ch.pIndexData.wealth * random.randint(1,20)/5000000
                ch.silver += ch.pIndexData.wealth * random.randint(1,20)/50000
     

        # That's all for sleeping / busy monster, and empty zones */
        if ch.position != POS_STANDING:
            continue

        # Scavenge */
        if IS_SET(ch.act, ACT_SCAVENGER) and ch.in_room.contents != None and random.randint(0,6) == 0 :
            top = 1
            obj_best = 0
            for obj in ch.in_room.contents:
                if CAN_WEAR(obj, ITEM_TAKE) and can_loot(ch, obj) and obj.cost > top and obj.cost > 0:
                    obj_best    = obj
                    top = obj.cost

            if obj_best:
                obj_from_room( obj_best )
                obj_to_char( obj_best, ch )
                act( "$n gets $p.", ch, obj_best, None, TO_ROOM )

        # Wander */
        door = random.randint(0,5)
        pexit = ch.in_room.exit[door]

        if not IS_SET(ch.act, ACT_SENTINEL)  \
        and random.randint(0,3) == 0  \
        and pexit \
        and pexit.to_room \
        and  not IS_SET(pexit.exit_info, EX_CLOSED) \
        and  not IS_SET(pexit.to_room.room_flags, ROOM_NO_MOB) \
        and ( not IS_SET(ch.act, ACT_STAY_AREA) or pexit.to_room.area == ch.in_room.area ) \
        and ( not IS_SET(ch.act, ACT_OUTDOORS) or not IS_SET(pexit.to_room.room_flags,ROOM_INDOORS)) \
        and ( not IS_SET(ch.act, ACT_INDOORS) \
        or IS_SET(pexit.to_room.room_flags,ROOM_INDOORS)):
            act_move.move_char( ch, door, False )
      
#
# * Update the weather.
def weather_update( ):
    buf = ""
    time_info.hour += 1
    if time_info.hour == 5:
        weather_info.sunlight = SUN_LIGHT
        buf = "The day has begun.\n"
    elif time_info.hour == 6:
        weather_info.sunlight = SUN_RISE
        buf = "The sun rises in the east.\n"
    elif time_info.hour == 19:
        weather_info.sunlight = SUN_SET
        buf = "The sun slowly disappears in the west.\n"
    elif time_info.hour == 20:
        weather_info.sunlight = SUN_DARK
        buf = "The night has begun.\n"
    elif time_info.hour == 24:
        time_info.hour = 0
        time_info.day += 1

    if time_info.day   >= 35:
        time_info.day = 0
        time_info.month += 1
    if time_info.month >= 17:
        time_info.month = 0
        time_info.year += 1
    

    #
     #* Weather change.
    if time_info.month >= 9 and time_info.month <= 16:
        diff = -2 if weather_info.mmhg >  985 else 2
    else:
        diff = -2 if weather_info.mmhg > 1015 else 2

    weather_info.change += diff * dice(1, 4) + dice(2, 6) - dice(2, 6)
    weather_info.change = max(weather_info.change, -12)
    weather_info.change = min(weather_info.change,  12)

    weather_info.mmhg += weather_info.change
    weather_info.mmhg  = max(weather_info.mmhg,  960)
    weather_info.mmhg  = min(weather_info.mmhg, 1040)

    if weather_info.sky == SKY_CLOUDLESS:
        if weather_info.mmhg <  990 or ( weather_info.mmhg < 1010 and random.randint(0,  2 ) == 0 ):
            buf += "The sky is getting cloudy.\n"
            weather_info.sky = SKY_CLOUDY
    elif weather_info.sky == SKY_CLOUDY:
        if weather_info.mmhg <  970 or ( weather_info.mmhg <  990 and random.randint(0, 2 ) == 0 ):
            buf += "It starts to rain.\n"
            weather_info.sky = SKY_RAINING
        if weather_info.mmhg > 1030 and random.randint(0, 2 ) == 0:
            buf += "The clouds disappear.\n"
            weather_info.sky = SKY_CLOUDLESS
    elif weather_info.sky == SKY_RAINING:
        if weather_info.mmhg <  970 and number_bits( 2 ) == 0:
            strcat( buf, "Lightning flashes in the sky.\n" )
            weather_info.sky = SKY_LIGHTNING
        if weather_info.mmhg > 1030 or ( weather_info.mmhg > 1010 and random.randint(0, 2) == 0 ):
            strcat( buf, "The rain stopped.\n" )
            weather_info.sky = SKY_CLOUDY
    elif weather_info.sky == SKY_LIGHTNING:
        if weather_info.mmhg > 1010 or ( weather_info.mmhg >  990 and random.randint(0, 2 ) == 0 ):
            strcat( buf, "The lightning has stopped.\n" )
            weather_info.sky = SKY_RAINING
    else:
        print ("Bug: Weather_update: bad sky %d." % weather_info.sky)
        weather_info.sky = SKY_CLOUDLESS

    if buf:
        for d in descriptor_list:
            if d.connected == con_playing and IS_OUTSIDE(d.character) and IS_AWAKE(d.character):
                ch.send(buf)
    return

save_number = 0
#
# * Update all chars, including mobs.
def char_update( ):
    # update save counter */
    global save_number
    save_number += 1

    if save_number > 29:
        save_number = 0
    ch_quit = []
    for ch in char_list[:]:
        if ch.timer > 30:
            ch_quit.append(ch)

        if ch.position >= POS_STUNNED:
        # check to see if we need to go home */
            if IS_NPC(ch) and ch.zone and ch.zone != ch.in_room.area  \
            and not ch.desc and not ch.fighting and not IS_AFFECTED(ch,AFF_CHARM) and random.randint(1,99) < 5:
                act("$n wanders on home.",ch,None,None,TO_ROOM)
                extract_char(ch,True)
                continue

        if ch.hit  < ch.max_hit:
            ch.hit += hit_gain(ch)
        else:
            ch.hit = ch.max_hit

        if ch.mana < ch.max_mana:
            ch.mana += mana_gain(ch)
        else:
            ch.mana = ch.max_mana

        if ch.move < ch.max_move:
            ch.move += move_gain(ch)
        else:
            ch.move = ch.max_move


        if ch.position == POS_STUNNED:
            update_pos( ch )

        if not IS_NPC(ch) and ch.level < LEVEL_IMMORTAL:
            obj = get_eq_char(ch, WEAR_LIGHT)
            if obj and obj.item_type == ITEM_LIGHT and obj.value[2] > 0:
                obj.value[2] -= 1
                if obj.value[2] == 0 and ch.in_room != None:
                    ch.in_room.light -= 1
                    act( "$p goes out.", ch, obj, None, TO_ROOM )
                    act( "$p flickers and goes out.", ch, obj, None, TO_CHAR )
                    extract_obj( obj )
                elif obj.value[2] <= 5 and ch.in_room:
                    act("$p flickers.",ch,obj,None,TO_CHAR)

            if IS_IMMORTAL(ch):
                ch.timer = 0
            ch.timer += 1
            if ch.timer >= 12:
                if not ch.was_in_room and ch.in_room:
                    ch.was_in_room = ch.in_room
                    if ch.fighting:
                        stop_fighting( ch, True )
                    act( "$n disappears into the void.", ch, None, None, TO_ROOM )
                    ch.send("You disappear into the void.\n") 
                    if ch.level > 1:
                        save_char_obj( ch )
                    char_from_room( ch )
                    char_to_room( ch, room_index_hash[ROOM_VNUM_LIMBO] )



            gain_condition( ch, COND_DRUNK, -1 )
            gain_condition( ch, COND_FULL, -4 if ch.size > SIZE_MEDIUM else -2 )
            gain_condition( ch, COND_THIRST, -1 )
            gain_condition( ch, COND_HUNGER, -2 if ch.size > SIZE_MEDIUM else -1)


        for paf in ch.affected[:]:
            if paf.duration > 0 :
                paf.duration -= 1
                if random.randint(0,4) == 0 and paf.level > 0:
                    paf.level -= 1  # spell strength fades with time */
            elif paf.duration < 0:
                pass
            else:
                #multiple affects. don't send the spelldown msg
                multi = [a for a in ch.affected if a.type == paf.type and a is not paf and a.duration > 0]
                if not multi and paf.type > 0 and skill_table[paf.type].msg_off:
                    ch.send(skill_table[paf.type].msg_off+"\n")
         
                affect_remove( ch, paf )
    #
     #* Careful with the damages here,
     #*   MUST NOT refer to ch after damage taken,
     #*   as it may be lethal damage (on NPC).
     #*/

        if is_affected(ch, 'plague') and ch:
            if ch.in_room == None:
                continue
            
            act("$n writhes in agony as plague sores erupt from $s skin.", ch,None,None,TO_ROOM)
            ch.send("You writhe in agony from the plague.\n")
            af = [a for a in ch.affected if af.type == 'plague'][:1]
            if not af:
                REMOVE_BIT(ch.affected_by,AFF_PLAGUE)
                continue
            if af.level == 1:
                continue
            plague = AFFECT_DATA()    
            plague.where        = TO_AFFECTS
            plague.type         = gsn_plague
            plague.level        = af.level - 1 
            plague.duration     = random.randint(1,2 * plague.level)
            plague.location     = APPLY_STR
            plague.modifier     = -5
            plague.bitvector    = AFF_PLAGUE
        
            for vch in ch.in_room.people:
                if not saves_spell(plague.level - 2,vch,DAM_DISEASE) and not IS_IMMORTAL(vch) \
                and not IS_AFFECTED(vch,AFF_PLAGUE) and random.randint(0,4) == 0:
                    vch.send("You feel hot and feverish.\n")
                    act("$n shivers and looks very ill.",vch,None,None,TO_ROOM)
                    affect_join(vch,plague)
            dam = min(ch.level,af.level/5+1)
            ch.mana -= dam
            ch.move -= dam
            damage( ch, ch, dam, gsn_plague,DAM_DISEASE,False)
        elif IS_AFFECTED(ch, AFF_POISON) and ch and not IS_AFFECTED(ch,AFF_SLOW):
            poison = affect_find(ch.affected,'poison')
            if poison:
                act( "$n shivers and suffers.", ch, None, None, TO_ROOM )
                ch.send("You shiver and suffer.\n")
                damage(ch,ch,poison.level/10 + 1,gsn_poison, DAM_POISON,False)
        elif ch.position == POS_INCAP and random.randint(0,1) == 0:
            damage( ch, ch, 1, TYPE_UNDEFINED, DAM_NONE,False)
        elif ch.position == POS_MORTAL:
            damage( ch, ch, 1, TYPE_UNDEFINED, DAM_NONE,False)

    #
    # * Autosave and autoquit.
    # * Check that these chars still exist.
    # */
    for ch in char_list[:]:
        if ch.desc and save_number == 28:
            save_char_obj(ch)
    for ch in ch_quit[:]:
        ch.do_quit("")

#
 # Update all objs.
 # This function is performance sensitive.
#
def obj_update( ):
    for obj in object_list[:]:
        # go through affects and decrement */
        for paf in obj.affected[:]:
            if paf.duration > 0:
                paf.duration -= 1
                if random.randint(0,4) == 0 and paf.level > 0:
                  paf.level -= 1  # spell strength fades with time */
            elif paf.duration < 0:
                pass
            else:
                multi = [a for a in obj.affected if a.type == paf.type and a is not paf and a.duration > 0]
                if multi and paf.type > 0 and skill_table[paf.type].msg_obj:
                    if obj.carried_by:
                        rch = obj.carried_by
                        act(skill_table[paf.type].msg_obj, rch,obj,None,TO_CHAR)

                    if obj.in_room != None and obj.in_room.people:
                        act(skill_table[paf.type].msg_obj, obj.in_room.people ,obj,None,TO_ALL)
                affect_remove_obj( obj, paf )
        obj.timer -= 1
        if obj.timer <= 0 or obj.timer > 0:
            continue
    
        if obj.item_type == ITEM_FOUNTAIN:   message = "$p dries up."
        elif obj.item_type == ITEM_CORPSE_NPC: message = "$p decays into dust."
        elif obj.item_type == ITEM_CORPSE_PC:  message = "$p decays into dust."
        elif obj.item_type == ITEM_FOOD:       message = "$p decomposes."
        elif obj.item_type == ITEM_POTION:     message = "$p has evaporated from disuse."   
        elif obj.item_type == ITEM_PORTAL:     message = "$p fades out of existence."
        elif obj.item_type == ITEM_CONTAINER:
            if CAN_WEAR(obj,ITEM_WEAR_FLOAT):
                if obj.contains:
                    message = "$p flickers and vanishes, spilling its contents on the floor."
                else:
                    message = "$p flickers and vanishes."
            else:
                message = "$p crumbles into dust."
        else: message = "$p crumbles into dust."

        if obj.carried_by:
            if IS_NPC(obj.carried_by) and  obj.carried_by.pIndexData.pShop:
                obj.carried_by.silver += obj.cost/5
            else:
                act( message, obj.carried_by, obj, None, TO_CHAR )
                if obj.wear_loc == WEAR_FLOAT:
                    act(message,obj.carried_by,obj,None,TO_ROOM)
        elif obj.in_room and obj.in_room.people:
            if not (obj.in_obj and obj.in_obj.pIndexData.vnum == OBJ_VNUM_PIT and not CAN_WEAR(obj.in_obj,ITEM_TAKE)):
                act( message, obj.in_room.people[:1], obj, None, TO_ROOM )
                act( message, obj.in_room.people[:1], obj, None, TO_CHAR )

        if (obj.item_type == ITEM_CORPSE_PC or obj.wear_loc == WEAR_FLOAT) and  obj.contains:
            # save the contents */
            for t_obj in obj.contains[:]:
                obj_from_obj(t_obj)

                if obj.in_obj: # in another object */
                    obj_to_obj(t_obj,obj.in_obj)
                elif obj.carried_by:  # carried */
                    if obj.wear_loc == WEAR_FLOAT:
                        if obj.carried_by.in_room == None:
                            extract_obj(t_obj)
                        else:
                            obj_to_room(t_obj,obj.carried_by.in_room)
                    else:
                        obj_to_char(t_obj,obj.carried_by)
                elif not obj.in_room:  # destroy it */
                    extract_obj(t_obj)
                else: # to a room */
                    obj_to_room(t_obj,obj.in_room)

        extract_obj( obj )
    return
#
# * Aggress.
# *
# * for each mortal PC
# *     for each mob in room
# *         aggress on some random PC
# *
# * This function takes 25% to 35% of ALL Merc cpu time.
# * Unfortunately, checking on each PC move is too tricky,
# *   because we don't the mob to just attack the first PC
# *   who leads the party into the room.
# *
# * -- Furey
# */
def aggr_update( ):
    for wch in char_list[:]:
        if IS_NPC(wch) \
        or wch.level >= LEVEL_IMMORTAL \
        or wch.in_room == None \
        or wch.in_room.area.empty:
            continue

        for ch in wch.in_room.people[:]:
            if not IS_NPC(ch) \
            or not IS_SET(ch.act, ACT_AGGRESSIVE) \
            or IS_SET(ch.in_room.room_flags,ROOM_SAFE) \
            or IS_AFFECTED(ch,AFF_CALM) \
            or ch.fighting != None \
            or IS_AFFECTED(ch, AFF_CHARM) \
            or not IS_AWAKE(ch) \
            or ( IS_SET(ch.act, ACT_WIMPY) and IS_AWAKE(wch) ) \
            or not can_see( ch, wch )  \
            or random.randint(0,1) == 0:
                continue

            #
            #    * Ok we have a 'wch' player character and a 'ch' npc aggressor.
            #    * Now make the aggressor fight a RANDOM pc victim in the room,
            #    *   giving each 'vch' an equal chance of selection.
            count   = 0
            victim = None
            for vch in wch.in_room.people[:]:
                if not IS_NPC(vch) \
                and   vch.level < LEVEL_IMMORTAL \
                and   ch.level >= vch.level - 5  \
                and   ( not IS_SET(ch.act, ACT_WIMPY) or not IS_AWAKE(vch) ) \
                and   can_see( ch, vch ):
                    if random.randint( 0, count ) == 0:
                        victim = vch
                    count += 1

            if not victim:
                continue

            multi_hit( ch, victim, TYPE_UNDEFINED )

#
# * Handle all kinds of updates.
# * Called once per pulse from game loop.
# * Random times to defeat tick-timing clients and players.
# */
pulse_area=0
pulse_mobile=0
pulse_violence=0
pulse_point=0


def update_handler( ):
    global pulse_area
    global pulse_mobile
    global pulse_violence
    global pulse_point

    pulse_area -= 1
    pulse_mobile -= 1
    pulse_violence -= 1
    pulse_point -= 1


    if pulse_area <= 0:
        pulse_area  = PULSE_AREA
        area_update ( )
    if pulse_mobile <= 0:
        pulse_mobile    = PULSE_MOBILE
        mobile_update   ( )
    if pulse_violence <= 0:
        pulse_violence  = PULSE_VIOLENCE
        violence_update ( )
    if pulse_point <= 0:
        wiznet("TICK!",None,None,WIZ_TICKS,0,0)
        pulse_point     = PULSE_TICK
        #weather_update  ( )
        char_update ( )
        obj_update  ( )
    aggr_update( )
