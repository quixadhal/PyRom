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


def say_spell(ch, spell):
    syl_dict = {"ar":"abra", "au":"kada", "bless":"fido", "blind":"nose", "bur":"mosa", "cu":"judi", "de":"oculo", "en":"unso", "light":"dies", 
            "lo":"hi", "mor":"zak", "move":"sido", "ness":"lacri", "ning":"illa", "per":"duda",  "ra":"gru", "fresh":"ima", "re":"candus", 
            "son":"sabru", "tect":"infra", "tri":"cula", "ven":"nofo", "a":"a", "b":"b", "c":"q", "d":"e", "e":"z", "f":"y", "g":"o", 
            "h":"p", "i":"u", "j":"y", "k":"t", "l":"r", "m":"w", "n":"i", "o":"a", "p":"s", "q":"d", "r":"f", "s":"g", "t":"h", "u":"j", 
            "v":"z", "w":"x", "x":"n", "y":"l", "z": "k"}
    incantation = mass_replace(spell.name, syl_dict):

    buf = "$n utters the words, '%s'." % incantation )
    buf2 = "$n utters the words, '%s'." % spell.name )

    for rch in ch.in_room.people:
        send = buf2 if ch.guild==rch.guild else buf
        act(format=send, ch=ch, arg2=rch, TO_VICT)


def saves_spell(level, victim, dam_type):
    save = 50 + ( victim.level - level) * 5 - victim.saving_throw * 2
    if IS_AFFECTED(victim, AFF_BERSERK):
        save += victim.level/2

    immunity = check_immune(victim,dam_type)
    if immunity == IS_IMMUNE:
        return True
    elif immunity == IS_RESISTANT:
        save += 2
    elif immunity == IS_VULNERABLE:
        save -= 2

    if not IS_NPC(victim) and victim.guild.fMana:
        save = 9 * save / 10
    save = max( 5, min(save, 95 )
    return random.randint(1,99) < save

def saves_dispel( dis_level, spell_level, duration):
    if duration == -1:
      spell_level += 5  
      # very hard to dispel permanent effects */

    save = 50 + (spell_level - dis_level) * 5
    save = max( 5, min(save, 95 )
    return random.randint(1,99) < save

def check_dispel( dis_level, victim, skill):
    if is_affected(victim, skill):
        for af in victim.affected:
            if af.type == skill:
                if not saves_dispel(dis_level,af.level,af.duration):
                    victim.affect_strip(sn)
                    if skill.msg_off:
                        victim.send( skill_table[sn].msg_off + "\r\n" )
                    return True
                else
                    af.level -= 1
    return False


# for finding mana costs -- temporary version */
def mana_cost (ch, min_mana, level):
    if ch.level + 2 == level
        return 1000
    return max(min_mana,(100/(2 + ch.level - level)))




# * Spell functions.

def spell_acid_blast( sn, level, ch, victim, target ):
    dam = dice( level, 12 )
    if saves_spell( level, victim, DAM_ACID ):
        dam =  dam/2
    damage( ch, victim, dam, sn, DAM_ACID, True)

def spell_armor( sn, level, ch, victim, target ):
    if is_affected( victim, sn ):
        if victim == ch:
            ch.send("You are already armored.\r\n")
        else:
            act("$N is already armored.",ch,None,victim,TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 24
    af.modifier  = -20
    af.location  = APPLY_AC
    af.bitvector = 0
    affect_to_char( victim, af )
    victim.send( "You feel someone protecting you.\r\n")
    if  ch is not victim:
        act("$N is protected by your magic.",ch,None,victim,TO_CHAR)

def spell_bless( sn, level, ch, victim, target ):
    # deal with the object case first */
    if target == TARGET_OBJ:
        obj = victim
        if IS_OBJ_STAT(obj,ITEM_BLESS):
            act("$p is already blessed.",ch,obj,target=TO_CHAR)
            return
        if IS_OBJ_STAT(obj,ITEM_EVIL):
            paf = affect_find(obj.affected,"curse")
            level = obj.level
            if paf:
                level = paf.level
            if not saves_dispel(level,level,0):
                if paf:
                    affect_remove_obj(obj,paf)
                    act("$p glows a pale blue.",ch,obj,None,TO_ALL)
                    REMOVE_BIT(obj.extra_flags,ITEM_EVIL)
                    return
                else:
                    act("The evil of $p is too powerful for you to overcome.", ch,obj,target=TO_CHAR)
                    return
        af = AFFECT_DATA()
        af.where    = TO_OBJECT
        af.type     = sn
        af.level    = level
        af.duration = 6 + level
        af.location = APPLY_SAVES
        af.modifier = -1
        af.bitvector    = ITEM_BLESS
        affect_to_obj(obj,af)

        act("$p glows with a holy aura.",ch,obj,target=TO_ALL)

        if (obj.wear_loc != WEAR_NONE)
            ch.saving_throw = ch.saving_throw-1
        return


    # character target */
    if victim.position == POS_FIGHTING or is_affected( victim, sn ):
        if (victim == ch):
            ch.send("You are already blessed.\r\n")
        else:
            act("$N already has divine favor.",ch,None,victim,TO_CHAR)
        return
    
    af = AFFECT_DATA()
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 6+level
    af.location  = APPLY_HITROLL
    af.modifier  = level / 8
    af.bitvector = 0
    affect_to_char( victim, af )

    af.location  = APPLY_SAVING_SPELL
    af.modifier  = 0 - level / 8
    affect_to_char( victim, af )
    victim.send( "You feel righteous.\r\n")
    if  ch is not victim:
        act("You grant $N the favor of your god.",ch,None,victim,TO_CHAR)

def spell_blindness( sn, level, ch, victim, target ):
    if IS_AFFECTED(victim, AFF_BLIND) or saves_spell(level,victim,DAM_OTHER):
        return

    af = AFFECT_DATA()
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.location  = APPLY_HITROLL
    af.modifier  = -4
    af.duration  = 1+level
    af.bitvector = AFF_BLIND
    affect_to_char( victim, af )
    victim.send( "You are blinded!\r\n")
    act("$n appears to be blinded.",victim,target=TO_ROOM)

def spell_burning_hands( sn, level, ch, victim, target ):
    dam_each = [     0,
     0,  0,  0,  0, 14, 17, 20, 23, 26, 29,
    29, 29, 30, 30, 31, 31, 32, 32, 33, 33,
    34, 34, 35, 35, 36, 36, 37, 37, 38, 38,
    39, 39, 40, 40, 41, 41, 42, 42, 43, 43,
    44, 44, 45, 45, 46, 46, 47, 47, 48, 48
    ]
    
    level   = min(level, len(dam_each)-1)
    level   = max(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if saves_spell( level, victim,DAM_FIRE):
        dam = dam / 2
    damage( ch, victim, dam, sn, DAM_FIRE,True)


def spell_call_lightning( sn, level, ch, victim, target ):
    if !IS_OUTSIDE(ch):
        ch.send("You must be out of doors.\r\n")
        return

    if weather_info.sky < SKY_RAINING:
        ch.send("You need bad weather.\r\n")
        return

    dam = dice(level/2, 8)

    ch.send("Mota's lightning strikes your foes!\r\n")
    act( "$n calls Mota's lightning to strike $s foes!", ch, None, None, TO_ROOM )

    for vch in char_list:
        if vch.in_room == None:
            continue
        if vch.in_room == ch.in_room:
            if vch is not ch and ( !IS_NPC(vch) if IS_NPC(ch) else IS_NPC(vch) ):
                damage( ch, vch, dam/2 if saves_spell( level,vch,DAM_LIGHTNING) else dam, sn,DAM_LIGHTNING,True)
            continue
    
        if vch.in_room.area == ch.in_room.area and IS_OUTSIDE(vch) and IS_AWAKE(vch):
            vch.send("Lightning flashes in the sky.\r\n")

# RT calm spell stops all fighting in the room */

def spell_calm( sn, level, ch, victim, target ):
    # get sum of all mobile levels in the room */
    count=0
    mlevel=0
    for vch in ch.in_room.people:
        if vch.position == POS_FIGHTING:
            count=count+1
        if IS_NPC(vch):
            mlevel += vch.level
        else:
            mlevel += vch.level/2
        high_level = max(high_level,vch.level)

    # compute chance of stopping combat */
    chance = 4 * level - high_level + 2 * count

    if IS_IMMORTAL(ch): # always works */
      mlevel = 0

    if random.randint(0, chance) >= mlevel: # hard to stop large fights */
        for vch in ch.in_room.people:
            if IS_NPC(vch) and (IS_SET(vch.imm_flags,IMM_MAGIC) or IS_SET(vch.act,ACT_UNDEAD)):
                return

            if IS_AFFECTED(vch,AFF_CALM) or IS_AFFECTED(vch,AFF_BERSERK) or  is_affected(vch,skill_table['frenzy']):
                return
            
            vch.send("A wave of calm passes over you.\r\n")

            if vch.fighting or vch.position == POS_FIGHTING:
                stop_fighting(vch,False)


            af.where = TO_AFFECTS
            af.type = sn
            af.level = level
            af.duration = level/4
            af.location = APPLY_HITROLL
            if !IS_NPC(vch):
              af.modifier = -5
            else:
              af.modifier = -2
            af.bitvector = AFF_CALM
            affect_to_char(vch,af)

            af.location = APPLY_DAMROLL
            affect_to_char(vch,af)

def spell_cancellation( sn, level, ch, victim, target ):
    
    found = False
    level += 2

    if (!IS_NPC(ch) and IS_NPC(victim) and not (IS_AFFECTED(ch, AFF_CHARM) and ch.master == victim) ) or (IS_NPC(ch) and !IS_NPC(victim)):
        ch.send("You failed, try dispel magic.\r\n")
        return

    # unlike dispel magic, the victim gets NO save */
    # begin running through the spells */
 
    spells = { 'armor':None,
               'bless':None,
               'blindness': '$n is no longer blinded',
               'calm': '$n no longer looks so peaceful...',
               'change sex': '$n looks more like $mself again.',
               'charm person': '$n regains $s free will.',
               'chill touch': '$n looks warmer',
               'curse':None,
               'detect evil':None,
               'detect good':None,
               'detect hidden':None,
               'detect invis':None,
               'detect magic':None,
               'faerie fire':"$n's outline fades",
               'fly':'$n falls to the ground!',
               'frenzy': "$n no longer looks so wild.",
               'giant strength': "$n no longer looks so mighty.",
               'haste': '$n is no longer moving so quickly',
               'infravision':None,
               'invis':'$n fades into existence.',
               'mass invis': '$n fades into existence',
               'pass door': None,
               'protection evil': None,
               'protection good': None,
               'sanctuary': "The white aura around $n's body vanishes.",
               'shield': 'The shield protecting $n vanishes',
               'sleep': None,
               'slow': '$n is no longer moving so slowly.',
               'stone skin': "$n's skin regains its normal texture.",
               'weaken': "$n looks stronger." }

    for k,v in spells.iteritems():
        if check_dispel(level,victim,skill_table[k]):
            if v:
                act(v,victim,None,None,TO_ROOM)
            found = True
    
    if found:
        ch.send("Ok.\r\n")
    else:
        ch.send("Spell failed.\r\n")

def spell_cause_light( sn, level, ch, victim, target ):
    damage( ch,victim, dice(1, 8) + level / 3, sn,DAM_HARM,True)
    return

def spell_cause_critical( sn, level, ch, victim, target ):
    damage( ch, victim, dice(3, 8) + level - 6, sn,DAM_HARM,True)
    return

def spell_cause_serious( sn, level, ch, victim, target ):
    damage( ch, victim, dice(2, 8) + level / 2, sn,DAM_HARM,True)
    return

def spell_chain_lightning( sn, level, ch, victim, target ):
    #H first strike */
    act("A lightning bolt leaps from $n's hand and arcs to $N.",ch,None,victim,TO_ROOM)
    act("A lightning bolt leaps from your hand and arcs to $N.",ch,None,victim,TO_CHAR)
    act("A lightning bolt leaps from $n's hand and hits you!",ch,None,victim,TO_VICT)  

    dam = dice(level,6)
    if saves_spell(level,victim,DAM_LIGHTNING):
        dam = dam/3
    damage(ch,victim,dam,sn,DAM_LIGHTNING,True)
    last_vict = victim
    level = level-4   # decrement damage */

    # new targets */
    while level > 0:
        found = False
        for tmp_vict in ch.in_room.people:
            if  not is_safe_spell(ch,tmp_vict,True) and tmp_vict is not last_vict:
                found = True
                last_vict = tmp_vict
                act("The bolt arcs to $n!",tmp_vict,None,None,TO_ROOM)
                act("The bolt hits you!",tmp_vict,None,None,TO_CHAR)
                dam = dice(level,6)
                if saves_spell(level,tmp_vict,DAM_LIGHTNING):
                    dam = dam/3
                damage(ch,tmp_vict,dam,sn,DAM_LIGHTNING,True)
                level = level-4  # decrement damage */
        
        if not found: # no target found, hit the caster */
            if ch == None:
                return

            if (last_vict == ch) # no double hits */
                act("The bolt seems to have fizzled out.",ch,None,None,TO_ROOM)
                act("The bolt grounds out through your body.", ch,None,None,TO_CHAR)
                return
    

            last_vict = ch
            act("The bolt arcs to $n...whoops!",ch,None,None,TO_ROOM)
            ch.send("You are struck by your own lightning!\r\n")
            dam = dice(level,6)
            if (saves_spell(level,ch,DAM_LIGHTNING):
                dam = dam / 3
            damage(ch,ch,dam,sn,DAM_LIGHTNING,True)
            level = level-4  # decrement damage */
            if ch == None:
                return
   
def spell_change_sex( sn, level, ch, victim, target ):
    if is_affected( victim, sn ):
        if victim == ch:
            ch.send("You've already been changed.\r\n")
        else:
            act("$N has already had $s(?) sex changed.",ch,None,victim,TO_CHAR)
        return

    if saves_spell(level , victim,DAM_OTHER):
        return 
    af = AFFECT_DATA()
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 2 * level
    af.location  = APPLY_SEX

    while af.modifier == 0:
        af.modifier = random.randint( 0, 2 ) - victim.sex
    
    af.bitvector = 0
    affect_to_char( victim, &af )
    victim.send("You feel different.\r\n")
    act("$n doesn't look like $mself anymore...",victim,None,None,TO_ROOM)

def spell_charm_person( sn, level, ch, victim, target ):
    if is_safe(ch,victim):
        return

    if victim == ch:
        ch.send("You like yourself even better!\r\n")
        return

    if ( IS_AFFECTED(victim, AFF_CHARM)
    or   IS_AFFECTED(ch, AFF_CHARM)
    or   level < victim.level
    or   IS_SET(victim.imm_flags,IMM_CHARM)
    or   saves_spell( level, victim,DAM_CHARM) ):
        return


    if IS_SET(victim.in_room.room_flags,ROOM_LAW):
        ch.send("The mayor does not allow charming in the city limits.\r\n")
        return
  
    if victim.master:
        stop_follower( victim )
    add_follower( victim, ch )
    victim.leader = ch
    af = AFFECT_DATA()
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = number_fuzzy( level / 4 )
    af.location  = 0
    af.modifier  = 0
    af.bitvector = AFF_CHARM
    affect_to_char( victim, af )
    act( "Isn't $n just so nice?", ch, None, victim, TO_VICT )
    if ch is not victim:
        act("$N looks at you with adoring eyes.",ch,None,victim,TO_CHAR)

def spell_chill_touch( sn, level, ch, victim, target ):
    dam_each=[     0,
     0,  0,  6,  7,  8,  9, 12, 13, 13, 13,
    14, 14, 14, 15, 15, 15, 16, 16, 16, 17,
    17, 17, 18, 18, 18, 19, 19, 19, 20, 20,
    20, 21, 21, 21, 22, 22, 22, 23, 23, 23,
    24, 24, 24, 25, 25, 25, 26, 26, 26, 27 ]

    level   = min(level, len(dam_each)-1)
    level   = max(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if not saves_spell( level, victim,DAM_COLD ):
        act("$n turns blue and shivers.",victim,None,None,TO_ROOM)
        af.where     = TO_AFFECTS
        af.type      = sn
        af.level     = level
        af.duration  = 6
        af.location  = APPLY_STR
        af.modifier  = -1
        af.bitvector = 0
        affect_join( victim, af )
    else:
        dam = dam/2
    damage( ch, victim, dam, sn, DAM_COLD,True )
    
def spell_colour_spray( sn, level, ch, victim, target ):
    dam_each = [ 0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    30, 35, 40, 45, 50, 55, 55, 55, 56, 57,
    58, 58, 59, 60, 61, 61, 62, 63, 64, 64,
    65, 66, 67, 67, 68, 69, 70, 70, 71, 72,
    73, 73, 74, 75, 76, 76, 77, 78, 79, 79 ]
    
    level   = min(level, len(dam_each)-1)
    level   = max(0, level)
    dam     = random.randint( dam_each[level] / 2,  dam_each[level] * 2 )
    if saves_spell( level, victim,DAM_LIGHT):
        dam = dam/2
    else:
        spell_blindness(skill_table["blindness"], level/2,ch,victim,TARGET_CHAR)

    damage( ch, victim, dam, sn, DAM_LIGHT,True )
    return

def spell_continual_light( sn, level, ch, victim, target ):
{
    OBJ_DATA *light

    if (target_name[0] != '\0')  # do a glow on some object */
    {
    light = get_obj_carry(ch,target_name,ch)
    
    if (light == None)
    {
        ch.send("You don't see that here.\r\n")
        return
    }

    if (IS_OBJ_STAT(light,ITEM_GLOW))
    {
        act("$p is already glowing.",ch,light,None,TO_CHAR)
        return
    }

    SET_BIT(light.extra_flags,ITEM_GLOW)
    act("$p glows with a white light.",ch,light,None,TO_ALL)
    return
    }

    light = create_object( get_obj_index( OBJ_VNUM_LIGHT_BALL ), 0 )
    obj_to_room( light, ch.in_room )
    act( "$n twiddles $s thumbs and $p appears.",   ch, light, None, TO_ROOM )
    act( "You twiddle your thumbs and $p appears.", ch, light, None, TO_CHAR )
    return
}



def spell_control_weather( sn, level, ch, victim, target ): 
{
    if ( !str_cmp( target_name, "better" ) )
    weather_info.change += dice( level / 3, 4 )
    else if ( !str_cmp( target_name, "worse" ) )
    weather_info.change -= dice( level / 3, 4 )
    else
    send_to_char ("Do you want it to get better or worse?\r\n", ch )

    ch.send("Ok.\r\n")
    return
}



def spell_create_food( sn, level, ch, victim, target ):
{
    OBJ_DATA *mushroom

    mushroom = create_object( get_obj_index( OBJ_VNUM_MUSHROOM ), 0 )
    mushroom.value[0] = level / 2
    mushroom.value[1] = level
    obj_to_room( mushroom, ch.in_room )
    act( "$p suddenly appears.", ch, mushroom, None, TO_ROOM )
    act( "$p suddenly appears.", ch, mushroom, None, TO_CHAR )
    return
}

def spell_create_rose( sn, level, ch, victim, target ):
{
    OBJ_DATA *rose
    rose = create_object(get_obj_index(OBJ_VNUM_ROSE), 0)
    act("$n has created a beautiful red rose.",ch,rose,None,TO_ROOM)
    ch.send("You create a beautiful red rose.\r\n")
    obj_to_char(rose,ch)
    return
}

def spell_create_spring( sn, level, ch, victim, target ):
{
    OBJ_DATA *spring

    spring = create_object( get_obj_index( OBJ_VNUM_SPRING ), 0 )
    spring.timer = level
    obj_to_room( spring, ch.in_room )
    act( "$p flows from the ground.", ch, spring, None, TO_ROOM )
    act( "$p flows from the ground.", ch, spring, None, TO_CHAR )
    return
}



def spell_create_water( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    int water

    if ( obj.item_type != ITEM_DRINK_CON )
    {
    ch.send("It is unable to hold water.\r\n")
    return
    }

    if ( obj.value[2] != LIQ_WATER and obj.value[1] != 0 )
    {
    ch.send("It contains some other liquid.\r\n")
    return
    }

    water = UMIN(
        level * (weather_info.sky >= SKY_RAINING ? 4 : 2),
        obj.value[0] - obj.value[1]
        )
  
    if ( water > 0 )
    {
    obj.value[2] = LIQ_WATER
    obj.value[1] += water
    if ( !is_name( "water", obj.name ) )
    {
        char buf[MAX_STRING_LENGTH]

        sprintf( buf, "%s water", obj.name )
        free_string( obj.name )
        obj.name = str_dup( buf )
    }
    act( "$p is filled.", ch, obj, None, TO_CHAR )
    }

    return
}



def spell_cure_blindness( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo

    if ( !is_affected( victim, gsn_blindness ) )
    {
        if (victim == ch)
          ch.send("You aren't blind.\r\n")
        else
          act("$N doesn't appear to be blinded.",ch,None,victim,TO_CHAR)
        return
    }
 
    if (check_dispel(level,victim,gsn_blindness))
    {
        victim.send("Your vision returns!\r\n")
        act("$n is no longer blinded.",victim,None,None,TO_ROOM)
    }
    else
        ch.send("Spell failed.\r\n")
}



def spell_cure_critical( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int heal

    heal = dice(3, 8) + level - 6
    victim.hit = UMIN( victim.hit + heal, victim.max_hit )
    update_pos( victim )
    victim.send("You feel better!\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}

# RT added to cure plague */
def spell_cure_disease( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo

    if ( !is_affected( victim, gsn_plague ) )
    {
        if (victim == ch)
          ch.send("You aren't ill.\r\n")
        else
          act("$N doesn't appear to be diseased.",ch,None,victim,TO_CHAR)
        return
    }
    
    if (check_dispel(level,victim,gsn_plague))
    {
    victim.send("Your sores vanish.\r\n")
    act("$n looks relieved as $s sores vanish.",victim,None,None,TO_ROOM)
    }
    else
    ch.send("Spell failed.\r\n")
}



def spell_cure_light( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int heal

    heal = dice(1, 8) + level / 3
    victim.hit = UMIN( victim.hit + heal, victim.max_hit )
    update_pos( victim )
    victim.send("You feel better!\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}



def spell_cure_poison( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
 
    if ( !is_affected( victim, gsn_poison ) )
    {
        if (victim == ch)
          ch.send("You aren't poisoned.\r\n")
        else
          act("$N doesn't appear to be poisoned.",ch,None,victim,TO_CHAR)
        return
    }
 
    if (check_dispel(level,victim,gsn_poison))
    {
        victim.send("A warm feeling runs through your body.\r\n")
        act("$n looks much better.",victim,None,None,TO_ROOM)
    }
    else
        ch.send("Spell failed.\r\n")
}

def spell_cure_serious( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int heal

    heal = dice(2, 8) + level /2 
    victim.hit = UMIN( victim.hit + heal, victim.max_hit )
    update_pos( victim )
    victim.send("You feel better!\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}



def spell_curse( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim
    OBJ_DATA *obj
    AFFECT_DATA af

    # deal with the object case first */
    if (target == TARGET_OBJ)
    {
        obj = (OBJ_DATA *) vo
        if (IS_OBJ_STAT(obj,ITEM_EVIL))
        {
            act("$p is already filled with evil.",ch,obj,None,TO_CHAR)
            return
        }

        if (IS_OBJ_STAT(obj,ITEM_BLESS))
        {
            AFFECT_DATA *paf

            paf = affect_find(obj.affected,skill_lookup("bless"))
            if (!saves_dispel(level,paf != None ? paf.level : obj.level,0))
            {
                if (paf != None)
                    affect_remove_obj(obj,paf)
                act("$p glows with a red aura.",ch,obj,None,TO_ALL)
                REMOVE_BIT(obj.extra_flags,ITEM_BLESS)
                return
            }
            else
            {
                act("The holy aura of $p is too powerful for you to overcome.",
                    ch,obj,None,TO_CHAR)
                return
            }
        }

        af.where        = TO_OBJECT
        af.type         = sn
        af.level        = level
        af.duration     = 2 * level
        af.location     = APPLY_SAVES
        af.modifier     = +1
        af.bitvector    = ITEM_EVIL
        affect_to_obj(obj,&af)

        act("$p glows with a malevolent aura.",ch,obj,None,TO_ALL)

    if (obj.wear_loc != WEAR_NONE)
        ch.saving_throw += 1
        return
    }

    # character curses */
    victim = (CHAR_DATA *) vo

    if (IS_AFFECTED(victim,AFF_CURSE) or saves_spell(level,victim,DAM_NEGATIVE))
    return
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 2*level
    af.location  = APPLY_HITROLL
    af.modifier  = -1 * (level / 8)
    af.bitvector = AFF_CURSE
    affect_to_char( victim, &af )

    af.location  = APPLY_SAVING_SPELL
    af.modifier  = level / 8
    affect_to_char( victim, &af )

    victim.send("You feel unclean.\r\n")
    if ( ch != victim )
    act("$N looks very uncomfortable.",ch,None,victim,TO_CHAR)
    return
}

# RT replacement demonfire spell */

def spell_demonfire( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam

    if ( !IS_NPC(ch) and !IS_EVIL(ch) )
    {
        victim = ch
    ch.send("The demons turn upon you!\r\n")
    }

    ch.alignment = UMAX(-1000, ch.alignment - 50)

    if (victim != ch)
    {
    act("$n calls forth the demons of Hell upon $N!",
        ch,None,victim,TO_ROOM)
        act("$n has assailed you with the demons of Hell!",
        ch,None,victim,TO_VICT)
    ch.send("You conjure forth the demons of hell!\r\n")
    }
    dam = dice( level, 10 )
    if ( saves_spell( level, victim,DAM_NEGATIVE) )
        dam /= 2
    damage( ch, victim, dam, sn, DAM_NEGATIVE ,True)
    spell_curse(gsn_curse, 3 * level / 4, ch, (void *) victim,TARGET_CHAR)
}

def spell_detect_evil( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_DETECT_EVIL) )
    {
    if (victim == ch)
      ch.send("You can already sense evil.\r\n")
    else
      act("$N can already detect evil.",ch,None,victim,TO_CHAR)
    return
    }
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.modifier  = 0
    af.location  = APPLY_NONE
    af.bitvector = AFF_DETECT_EVIL
    affect_to_char( victim, &af )
    victim.send("Your eyes tingle.\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}


def spell_detect_good( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
 
    if ( IS_AFFECTED(victim, AFF_DETECT_GOOD) )
    {
        if (victim == ch)
          ch.send("You can already sense good.\r\n")
        else
          act("$N can already detect good.",ch,None,victim,TO_CHAR)
        return
    }
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.modifier  = 0
    af.location  = APPLY_NONE
    af.bitvector = AFF_DETECT_GOOD
    affect_to_char( victim, &af )
    victim.send("Your eyes tingle.\r\n")
    if ( ch != victim )
        ch.send("Ok.\r\n")
    return
}



def spell_detect_hidden( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_DETECT_HIDDEN) )
    {
        if (victim == ch)
          ch.send("You are already as alert as you can be. \r\n")
        else
          act("$N can already sense hidden lifeforms.",ch,None,victim,TO_CHAR)
        return
    }
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_DETECT_HIDDEN
    affect_to_char( victim, &af )
    victim.send("Your awareness improves.\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}



def spell_detect_invis( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_DETECT_INVIS) )
    {
        if (victim == ch)
          ch.send("You can already see invisible.\r\n")
        else
          act("$N can already see invisible things.",ch,None,victim,TO_CHAR)
        return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.modifier  = 0
    af.location  = APPLY_NONE
    af.bitvector = AFF_DETECT_INVIS
    affect_to_char( victim, &af )
    victim.send("Your eyes tingle.\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}



def spell_detect_magic( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_DETECT_MAGIC) )
    {
        if (victim == ch)
          ch.send("You can already sense magical auras.\r\n")
        else
          act("$N can already detect magic.",ch,None,victim,TO_CHAR)
        return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.modifier  = 0
    af.location  = APPLY_NONE
    af.bitvector = AFF_DETECT_MAGIC
    affect_to_char( victim, &af )
    victim.send("Your eyes tingle.\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}



def spell_detect_poison( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo

    if ( obj.item_type == ITEM_DRINK_CON or obj.item_type == ITEM_FOOD )
    {
    if ( obj.value[3] != 0 )
        ch.send("You smell poisonous fumes.\r\n")
    else
        ch.send("It looks delicious.\r\n")
    }
    else
    {
    ch.send("It doesn't look poisoned.\r\n")
    }

    return
}



def spell_dispel_evil( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam
  
    if ( !IS_NPC(ch) and IS_EVIL(ch) )
    victim = ch
  
    if ( IS_GOOD(victim) )
    {
    act( "Mota protects $N.", ch, None, victim, TO_ROOM )
    return
    }

    if ( IS_NEUTRAL(victim) )
    {
    act( "$N does not seem to be affected.", ch, None, victim, TO_CHAR )
    return
    }

    if (victim.hit > (ch.level * 4))
      dam = dice( level, 4 )
    else
      dam = UMAX(victim.hit, dice(level,4))
    if ( saves_spell( level, victim,DAM_HOLY) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_HOLY ,True)
    return
}


def spell_dispel_good( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam
 
    if ( !IS_NPC(ch) and IS_GOOD(ch) )
        victim = ch
 
    if ( IS_EVIL(victim) )
    {
        act( "$N is protected by $S evil.", ch, None, victim, TO_ROOM )
        return
    }
 
    if ( IS_NEUTRAL(victim) )
    {
        act( "$N does not seem to be affected.", ch, None, victim, TO_CHAR )
        return
    }
 
    if (victim.hit > (ch.level * 4))
      dam = dice( level, 4 )
    else
      dam = UMAX(victim.hit, dice(level,4))
    if ( saves_spell( level, victim,DAM_NEGATIVE) )
        dam /= 2
    damage( ch, victim, dam, sn, DAM_NEGATIVE ,True)
    return
}


# modified for enhanced use */

def spell_dispel_magic( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    bool found = False

    if (saves_spell(level, victim,DAM_OTHER))
    {
    victim.send("You feel a brief tingling sensation.\r\n")
    ch.send("You failed.\r\n")
    return
    }

    # begin running through the spells */ 

    if (check_dispel(level,victim,skill_lookup("armor")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("bless")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("blindness")))
    {
        found = True
        act("$n is no longer blinded.",victim,None,None,TO_ROOM)
    }
 
    if (check_dispel(level,victim,skill_lookup("calm")))
    {
        found = True
        act("$n no longer looks so peaceful...",victim,None,None,TO_ROOM)
    }
 
    if (check_dispel(level,victim,skill_lookup("change sex")))
    {
        found = True
        act("$n looks more like $mself again.",victim,None,None,TO_ROOM)
    }
 
    if (check_dispel(level,victim,skill_lookup("charm person")))
    {
        found = True
        act("$n regains $s free will.",victim,None,None,TO_ROOM)
    }
 
    if (check_dispel(level,victim,skill_lookup("chill touch")))
    {
        found = True
        act("$n looks warmer.",victim,None,None,TO_ROOM)
    }
 
    if (check_dispel(level,victim,skill_lookup("curse")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("detect evil")))
        found = True

    if (check_dispel(level,victim,skill_lookup("detect good")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("detect hidden")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("detect invis")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("detect magic")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("faerie fire")))
    {
        act("$n's outline fades.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("fly")))
    {
        act("$n falls to the ground!",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("frenzy")))
    {
        act("$n no longer looks so wild.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("giant strength")))
    {
        act("$n no longer looks so mighty.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("haste")))
    {
        act("$n is no longer moving so quickly.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("infravision")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("invis")))
    {
        act("$n fades into existance.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("mass invis")))
    {
        act("$n fades into existance.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("pass door")))
        found = True
 

    if (check_dispel(level,victim,skill_lookup("protection evil")))
        found = True

    if (check_dispel(level,victim,skill_lookup("protection good")))
        found = True
 
    if (check_dispel(level,victim,skill_lookup("sanctuary")))
    {
        act("The white aura around $n's body vanishes.",
            victim,None,None,TO_ROOM)
        found = True
    }

    if (IS_AFFECTED(victim,AFF_SANCTUARY) 
    and !saves_dispel(level, victim.level,-1)
    and !is_affected(victim,skill_lookup("sanctuary")))
    {
    REMOVE_BIT(victim.affected_by,AFF_SANCTUARY)
        act("The white aura around $n's body vanishes.",
            victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("shield")))
    {
        act("The shield protecting $n vanishes.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("sleep")))
        found = True

    if (check_dispel(level,victim,skill_lookup("slow")))
    {
        act("$n is no longer moving so slowly.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("stone skin")))
    {
        act("$n's skin regains its normal texture.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (check_dispel(level,victim,skill_lookup("weaken")))
    {
        act("$n looks stronger.",victim,None,None,TO_ROOM)
        found = True
    }
 
    if (found)
        ch.send("Ok.\r\n")
    else
        ch.send("Spell failed.\r\n")
    return
}

def spell_earthquake( sn, level, ch, victim, target ):
{
    CHAR_DATA *vch
    CHAR_DATA *vch_next

    ch.send("The earth trembles beneath your feet!\r\n")
    act( "$n makes the earth tremble and shiver.", ch, None, None, TO_ROOM )

    for vch in char_list:
    {
    vch_next    = vch.next
    if ( vch.in_room == None )
        continue
    if ( vch.in_room == ch.in_room )
    {
        if ( vch != ch and !is_safe_spell(ch,vch,True))
        {   if (IS_AFFECTED(vch,AFF_FLYING))
            damage(ch,vch,0,sn,DAM_BASH,True)
        else
            damage( ch,vch,level + dice(2, 8), sn, DAM_BASH,True)
        }
        continue
    }

    if ( vch.in_room.area == ch.in_room.area )
        vch.send("The earth trembles and shivers.\r\n")
    }

    return
}

def spell_enchant_armor( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    AFFECT_DATA *paf 
    int result, fail
    int ac_bonus, added
    bool ac_found = False

    if (obj.item_type != ITEM_ARMOR)
    {
    ch.send("That isn't an armor.\r\n")
    return
    }

    if (obj.wear_loc != -1)
    {
    ch.send("The item must be carried to be enchanted.\r\n")
    return
    }

    # this means they have no bonus */
    ac_bonus = 0
    fail = 25  # base 25% chance of failure */

    # find the bonuses */

    if (!obj.enchanted)
        for paf in obj:
        {
            if ( paf.location == APPLY_AC )
            {
            ac_bonus = paf.modifier
        ac_found = True
            fail += 5 * (ac_bonus * ac_bonus)
        }

        else  # things get a little harder */
            fail += 20
        }
 
    for paf in obj:
    {
    if ( paf.location == APPLY_AC )
    {
        ac_bonus = paf.modifier
        ac_found = True
        fail += 5 * (ac_bonus * ac_bonus)
    }

    else # things get a little harder */
        fail += 20
    }

    # apply other modifiers */
    fail -= level

    if (IS_OBJ_STAT(obj,ITEM_BLESS))
    fail -= 15
    if (IS_OBJ_STAT(obj,ITEM_GLOW))
    fail -= 5

    fail = URANGE(5,fail,85)

    result = number_percent()

    # the moment of truth */
    if (result < (fail / 5))  # item destroyed */
    {
    act("$p flares blindingly... and evaporates!",ch,obj,None,TO_CHAR)
    act("$p flares blindingly... and evaporates!",ch,obj,None,TO_ROOM)
    extract_obj(obj)
    return
    }

    if (result < (fail / 3)) # item disenchanted */
    {
    AFFECT_DATA *paf_next

    act("$p glows brightly, then fades...oops.",ch,obj,None,TO_CHAR)
    act("$p glows brightly, then fades.",ch,obj,None,TO_ROOM)
    obj.enchanted = True

    # remove all affects */
    for paf in obj:
    {
        paf_next = paf.next 
        free_affect(paf)
    }
    obj.affected = None

    # clear all flags */
    obj.extra_flags = 0
    return
    }

    if ( result <= fail )  # failed, no bad result */
    {
    ch.send("Nothing seemed to happen.\r\n")
    return
    }

    # okay, move all the old flags into new vectors if we have to */
    if (!obj.enchanted)
    {
    AFFECT_DATA *af_new
    obj.enchanted = True

    for paf in obj:
    {
        af_new = new_affect()
    
        af_new.next = obj.affected
        obj.affected = af_new

        af_new.where   = paf.where
        af_new.type    = UMAX(0,paf.type)
        af_new.level   = paf.level
        af_new.duration    = paf.duration
        af_new.location    = paf.location
        af_new.modifier    = paf.modifier
        af_new.bitvector   = paf.bitvector
    }
    }

    if (result <= (90 - level/5))  # success! */
    {
    act("$p shimmers with a gold aura.",ch,obj,None,TO_CHAR)
    act("$p shimmers with a gold aura.",ch,obj,None,TO_ROOM)
    SET_BIT(obj.extra_flags, ITEM_MAGIC)
    added = -1
    }
    
    else  # exceptional enchant */
    {
    act("$p glows a brillant gold!",ch,obj,None,TO_CHAR)
    act("$p glows a brillant gold!",ch,obj,None,TO_ROOM)
    SET_BIT(obj.extra_flags,ITEM_MAGIC)
    SET_BIT(obj.extra_flags,ITEM_GLOW)
    added = -2
    }
        
    # now add the enchantments */ 

    if (obj.level < LEVEL_HERO)
    obj.level = UMIN(LEVEL_HERO - 1,obj.level + 1)

    if (ac_found)
    {
    for paf in obj:
    {
        if ( paf.location == APPLY_AC)
        {
        paf.type = sn
        paf.modifier += added
        paf.level = UMAX(paf.level,level)
        }
    }
    }
    else # add a new affect */
    {
    paf = new_affect()

    paf.where  = TO_OBJECT
    paf.type   = sn
    paf.level  = level
    paf.duration   = -1
    paf.location   = APPLY_AC
    paf.modifier   =  added
    paf.bitvector  = 0
        paf.next   = obj.affected
        obj.affected   = paf
    }

}




def spell_enchant_weapon( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    AFFECT_DATA *paf 
    int result, fail
    int hit_bonus, dam_bonus, added
    bool hit_found = False, dam_found = False

    if (obj.item_type != ITEM_WEAPON)
    {
    ch.send("That isn't a weapon.\r\n")
    return
    }

    if (obj.wear_loc != -1)
    {
    ch.send("The item must be carried to be enchanted.\r\n")
    return
    }

    # this means they have no bonus */
    hit_bonus = 0
    dam_bonus = 0
    fail = 25  # base 25% chance of failure */

    # find the bonuses */

    if (!obj.enchanted)
        for paf in obj:
        {
            if ( paf.location == APPLY_HITROLL )
            {
            hit_bonus = paf.modifier
        hit_found = True
            fail += 2 * (hit_bonus * hit_bonus)
        }

        else if (paf.location == APPLY_DAMROLL )
        {
            dam_bonus = paf.modifier
        dam_found = True
            fail += 2 * (dam_bonus * dam_bonus)
        }

        else  # things get a little harder */
            fail += 25
        }
 
    for paf in obj:
    {
    if ( paf.location == APPLY_HITROLL )
    {
        hit_bonus = paf.modifier
        hit_found = True
        fail += 2 * (hit_bonus * hit_bonus)
    }

    else if (paf.location == APPLY_DAMROLL )
    {
        dam_bonus = paf.modifier
        dam_found = True
        fail += 2 * (dam_bonus * dam_bonus)
    }

    else # things get a little harder */
        fail += 25
    }

    # apply other modifiers */
    fail -= 3 * level/2

    if (IS_OBJ_STAT(obj,ITEM_BLESS))
    fail -= 15
    if (IS_OBJ_STAT(obj,ITEM_GLOW))
    fail -= 5

    fail = URANGE(5,fail,95)

    result = number_percent()

    # the moment of truth */
    if (result < (fail / 5))  # item destroyed */
    {
    act("$p shivers violently and explodes!",ch,obj,None,TO_CHAR)
    act("$p shivers violently and explodeds!",ch,obj,None,TO_ROOM)
    extract_obj(obj)
    return
    }

    if (result < (fail / 2)) # item disenchanted */
    {
    AFFECT_DATA *paf_next

    act("$p glows brightly, then fades...oops.",ch,obj,None,TO_CHAR)
    act("$p glows brightly, then fades.",ch,obj,None,TO_ROOM)
    obj.enchanted = True

    # remove all affects */
    for paf in obj:
    {
        paf_next = paf.next 
        free_affect(paf)
    }
    obj.affected = None

    # clear all flags */
    obj.extra_flags = 0
    return
    }

    if ( result <= fail )  # failed, no bad result */
    {
    ch.send("Nothing seemed to happen.\r\n")
    return
    }

    # okay, move all the old flags into new vectors if we have to */
    if (!obj.enchanted)
    {
    AFFECT_DATA *af_new
    obj.enchanted = True

    for paf in obj:
    {
        af_new = new_affect()
    
        af_new.next = obj.affected
        obj.affected = af_new

        af_new.where   = paf.where
        af_new.type    = UMAX(0,paf.type)
        af_new.level   = paf.level
        af_new.duration    = paf.duration
        af_new.location    = paf.location
        af_new.modifier    = paf.modifier
        af_new.bitvector   = paf.bitvector
    }
    }

    if (result <= (100 - level/5))  # success! */
    {
    act("$p glows blue.",ch,obj,None,TO_CHAR)
    act("$p glows blue.",ch,obj,None,TO_ROOM)
    SET_BIT(obj.extra_flags, ITEM_MAGIC)
    added = 1
    }
    
    else  # exceptional enchant */
    {
    act("$p glows a brillant blue!",ch,obj,None,TO_CHAR)
    act("$p glows a brillant blue!",ch,obj,None,TO_ROOM)
    SET_BIT(obj.extra_flags,ITEM_MAGIC)
    SET_BIT(obj.extra_flags,ITEM_GLOW)
    added = 2
    }
        
    # now add the enchantments */ 

    if (obj.level < LEVEL_HERO - 1)
    obj.level = UMIN(LEVEL_HERO - 1,obj.level + 1)

    if (dam_found)
    {
    for paf in obj:
    {
        if ( paf.location == APPLY_DAMROLL)
        {
        paf.type = sn
        paf.modifier += added
        paf.level = UMAX(paf.level,level)
        if (paf.modifier > 4)
            SET_BIT(obj.extra_flags,ITEM_HUM)
        }
    }
    }
    else # add a new affect */
    {
    paf = new_affect()

    paf.where  = TO_OBJECT
    paf.type   = sn
    paf.level  = level
    paf.duration   = -1
    paf.location   = APPLY_DAMROLL
    paf.modifier   =  added
    paf.bitvector  = 0
        paf.next   = obj.affected
        obj.affected   = paf
    }

    if (hit_found)
    {
        for paf in obj:
    {
            if ( paf.location == APPLY_HITROLL)
            {
        paf.type = sn
                paf.modifier += added
                paf.level = UMAX(paf.level,level)
                if (paf.modifier > 4)
                    SET_BIT(obj.extra_flags,ITEM_HUM)
            }
    }
    }
    else # add a new affect */
    {
        paf = new_affect()
 
        paf.type       = sn
        paf.level      = level
        paf.duration   = -1
        paf.location   = APPLY_HITROLL
        paf.modifier   =  added
        paf.bitvector  = 0
        paf.next       = obj.affected
        obj.affected   = paf
    }

}



#
 * Drain XP, MANA, HP.
 * Caster gains HP.
 */
def spell_energy_drain( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam

    if (victim != ch)
        ch.alignment = UMAX(-1000, ch.alignment - 50)

    if ( saves_spell( level, victim,DAM_NEGATIVE) )
    {
    victim.send("You feel a momentary chill.\r\n")     
    return
    }


    if ( victim.level <= 2 )
    {
    dam      = ch.hit + 1
    }
    else
    {
    gain_exp( victim, 0 - random.randint( level/2, 3 * level / 2 ) )
    victim.mana    /= 2
    victim.move    /= 2
    dam      = dice(1, level)
    ch.hit     += dam
    }

    victim.send("You feel your life slipping away!\r\n")
    ch.send("Wow....what a rush!\r\n")
    damage( ch, victim, dam, sn, DAM_NEGATIVE ,True)

    return
}



def spell_fireball( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    static const sh_int dam_each[] = 
    {
      0,
      0,   0,   0,   0,   0,      0,   0,   0,   0,   0,
      0,   0,   0,   0,  30,     35,  40,  45,  50,  55,
     60,  65,  70,  75,  80,     82,  84,  86,  88,  90,
     92,  94,  96,  98, 100,    102, 104, 106, 108, 110,
    112, 114, 116, 118, 120,    122, 124, 126, 128, 130
    }
    int dam

    level   = min(level, len(dam_each)-1)
    level   = UMAX(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if ( saves_spell( level, victim, DAM_FIRE) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_FIRE ,True)
    return
}


def spell_fireproof( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    AFFECT_DATA af
 
    if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF))
    {
        act("$p is already protected from burning.",ch,obj,None,TO_CHAR)
        return
    }
 
    af.where     = TO_OBJECT
    af.type      = sn
    af.level     = level
    af.duration  = number_fuzzy(level / 4)
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = ITEM_BURN_PROOF
 
    affect_to_obj(obj,&af)
 
    act("You protect $p from fire.",ch,obj,None,TO_CHAR)
    act("$p is surrounded by a protective aura.",ch,obj,None,TO_ROOM)
}



def spell_flamestrike( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam

    dam = dice(6 + level / 2, 8)
    if ( saves_spell( level, victim,DAM_FIRE) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_FIRE ,True)
    return
}



def spell_faerie_fire( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_FAERIE_FIRE) )
    return
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.location  = APPLY_AC
    af.modifier  = 2 * level
    af.bitvector = AFF_FAERIE_FIRE
    affect_to_char( victim, &af )
    victim.send("You are surrounded by a pink outline.\r\n")
    act( "$n is surrounded by a pink outline.", victim, None, None, TO_ROOM )
    return
}



def spell_faerie_fog( sn, level, ch, victim, target ):
{
    CHAR_DATA *ich

    act( "$n conjures a cloud of purple smoke.", ch, None, None, TO_ROOM )
    ch.send("You conjure a cloud of purple smoke.\r\n")

    for ich in ch:
    {
    if (ich.invis_level > 0)
        continue

    if ( ich == ch or saves_spell( level, ich,DAM_OTHER) )
        continue

    affect_strip ( ich, gsn_invis           )
    affect_strip ( ich, gsn_mass_invis      )
    affect_strip ( ich, gsn_sneak           )
    REMOVE_BIT   ( ich.affected_by, AFF_HIDE   )
    REMOVE_BIT   ( ich.affected_by, AFF_INVISIBLE  )
    REMOVE_BIT   ( ich.affected_by, AFF_SNEAK  )
    act( "$n is revealed!", ich, None, None, TO_ROOM )
    ich.send("You are revealed!\r\n")
    }

    return
}

def spell_floating_disc( sn, level, ch, victim, target ):
{
    OBJ_DATA *disc, *floating

    floating = get_eq_char(ch,WEAR_FLOAT)
    if (floating != None and IS_OBJ_STAT(floating,ITEM_NOREMOVE))
    {
    act("You can't remove $p.",ch,floating,None,TO_CHAR)
    return
    }

    disc = create_object(get_obj_index(OBJ_VNUM_DISC), 0)
    disc.value[0]  = ch.level * 10 # 10 pounds per level capacity */
    disc.value[3]  = ch.level * 5 # 5 pounds per level max per item */
    disc.timer     = ch.level * 2 - random.randint(0,level / 2) 

    act("$n has created a floating black disc.",ch,None,None,TO_ROOM)
    ch.send("You create a floating disc.\r\n")
    obj_to_char(disc,ch)
    wear_obj(ch,disc,True)
    return
}


def spell_fly( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_FLYING) )
    {
    if (victim == ch)
      ch.send("You are already airborne.\r\n")
    else
      act("$N doesn't need your help to fly.",ch,None,victim,TO_CHAR)
    return
    }
    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level + 3
    af.location  = 0
    af.modifier  = 0
    af.bitvector = AFF_FLYING
    affect_to_char( victim, &af )
    victim.send("Your feet rise off the ground.\r\n")
    act( "$n's feet rise off the ground.", victim, None, None, TO_ROOM )
    return
}

# RT clerical berserking spell */

def spell_frenzy( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if (is_affected(victim,sn) or IS_AFFECTED(victim,AFF_BERSERK))
    {
    if (victim == ch)
      ch.send("You are already in a frenzy.\r\n")
    else
      act("$N is already in a frenzy.",ch,None,victim,TO_CHAR)
    return
    }

    if (is_affected(victim,skill_lookup("calm")))
    {
    if (victim == ch)
      ch.send("Why don't you just relax for a while?\r\n")
    else
      act("$N doesn't look like $e wants to fight anymore.",
          ch,None,victim,TO_CHAR)
    return
    }

    if ((IS_GOOD(ch) and !IS_GOOD(victim)) or
    (IS_NEUTRAL(ch) and !IS_NEUTRAL(victim)) or
    (IS_EVIL(ch) and !IS_EVIL(victim))
       )
    {
    act("Your god doesn't seem to like $N",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level / 3
    af.modifier  = level / 6
    af.bitvector = 0

    af.location  = APPLY_HITROLL
    affect_to_char(victim,&af)

    af.location  = APPLY_DAMROLL
    affect_to_char(victim,&af)

    af.modifier  = 10 * (level / 12)
    af.location  = APPLY_AC
    affect_to_char(victim,&af)

    victim.send("You are filled with holy wrath!\r\n")
    act("$n gets a wild look in $s eyes!",victim,None,None,TO_ROOM)
}

# RT ROM-style gate */
    
def spell_gate( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim
    bool gate_pet

    if ( ( victim = get_char_world( ch, target_name ) ) == None
    or   victim == ch
    or   victim.in_room == None
    or   !can_see_room(ch,victim.in_room) 
    or   IS_SET(victim.in_room.room_flags, ROOM_SAFE)
    or   IS_SET(victim.in_room.room_flags, ROOM_PRIVATE)
    or   IS_SET(victim.in_room.room_flags, ROOM_SOLITARY)
    or   IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL)
    or   IS_SET(ch.in_room.room_flags, ROOM_NO_RECALL)
    or   victim.level >= level + 3
    or   (is_clan(victim) and !is_same_clan(ch,victim))
    or   (!IS_NPC(victim) and victim.level >= LEVEL_HERO)  # NOT trust */ 
    or   (IS_NPC(victim) and IS_SET(victim.imm_flags,IMM_SUMMON))
    or   (IS_NPC(victim) and saves_spell( level, victim,DAM_OTHER) ) )
    {
        ch.send("You failed.\r\n")
        return
    }   
    if (ch.pet != None and ch.in_room == ch.pet.in_room)
    gate_pet = True
    else
    gate_pet = False
    
    act("$n steps through a gate and vanishes.",ch,None,None,TO_ROOM)
    ch.send("You step through a gate and vanish.\r\n")
    char_from_room(ch)
    char_to_room(ch,victim.in_room)

    act("$n has arrived through a gate.",ch,None,None,TO_ROOM)
    do_function(ch, &do_look, "auto")

    if (gate_pet)
    {
    act("$n steps through a gate and vanishes.",ch.pet,None,None,TO_ROOM)
    send_to_char("You step through a gate and vanish.\r\n",ch.pet)
    char_from_room(ch.pet)
    char_to_room(ch.pet,victim.in_room)
    act("$n has arrived through a gate.",ch.pet,None,None,TO_ROOM)
    do_function(ch.pet, &do_look, "auto")
    }
}



def spell_giant_strength( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( is_affected( victim, sn ) )
    {
    if (victim == ch)
      ch.send("You are already as strong as you can get!\r\n")
    else
      act("$N can't get any stronger.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.location  = APPLY_STR
    af.modifier  = 1 + (level >= 18) + (level >= 25) + (level >= 32)
    af.bitvector = 0
    affect_to_char( victim, &af )
    victim.send("Your muscles surge with heightened power!\r\n")
    act("$n's muscles surge with heightened power.",victim,None,None,TO_ROOM)
    return
}



def spell_harm( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam

    dam = UMAX(  20, victim.hit - dice(1,4) )
    if ( saves_spell( level, victim,DAM_HARM) )
    dam = UMIN( 50, dam / 2 )
    dam = UMIN( 100, dam )
    damage( ch, victim, dam, sn, DAM_HARM ,True)
    return
}

# RT haste spell */

def spell_haste( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
 
    if ( is_affected( victim, sn ) or IS_AFFECTED(victim,AFF_HASTE)
    or   IS_SET(victim.off_flags,OFF_FAST))
    {
    if (victim == ch)
      ch.send("You can't move any faster!\r\n")
    else
      act("$N is already moving as fast as $E can.",
          ch,None,victim,TO_CHAR)
        return
    }

    if (IS_AFFECTED(victim,AFF_SLOW))
    {
    if (!check_dispel(level,victim,skill_lookup("slow")))
    {
        if (victim != ch)
            ch.send("Spell failed.\r\n")
        victim.send("You feel momentarily faster.\r\n")
        return
    }
        act("$n is moving less slowly.",victim,None,None,TO_ROOM)
        return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    if (victim == ch)
      af.duration  = level/2
    else
      af.duration  = level/4
    af.location  = APPLY_DEX
    af.modifier  = 1 + (level >= 18) + (level >= 25) + (level >= 32)
    af.bitvector = AFF_HASTE
    affect_to_char( victim, &af )
    victim.send("You feel yourself moving more quickly.\r\n")
    act("$n is moving more quickly.",victim,None,None,TO_ROOM)
    if ( ch != victim )
        ch.send("Ok.\r\n")
    return
}



def spell_heal( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    victim.hit = UMIN( victim.hit + 100, victim.max_hit )
    update_pos( victim )
    victim.send("A warm feeling fills your body.\r\n")
    if ( ch != victim )
    ch.send("Ok.\r\n")
    return
}

def spell_heat_metal( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    OBJ_DATA *obj_lose, *obj_next
    int dam = 0
    bool fail = True
 
   if (!saves_spell(level + 2,victim,DAM_FIRE) 
   and  !IS_SET(victim.imm_flags,IMM_FIRE))
   {
        for obj_lose in victim:
          obj_lose != None 
          obj_lose = obj_next)
        {
        obj_next = obj_lose.next_content
            if ( random.randint(1,2 * level) > obj_lose.level 
        and   !saves_spell(level,victim,DAM_FIRE)
        and   !IS_OBJ_STAT(obj_lose,ITEM_NONMETAL)
        and   !IS_OBJ_STAT(obj_lose,ITEM_BURN_PROOF))
            {
                switch ( obj_lose.item_type )
                {
                case ITEM_ARMOR:
        if (obj_lose.wear_loc != -1) # remove the item */
        {
            if (can_drop_obj(victim,obj_lose)
            and  (obj_lose.weight / 10) < 
            random.randint(1,2 * get_curr_stat(victim,STAT_DEX))
            and  remove_obj( victim, obj_lose.wear_loc, True ))
            {
                act("$n yelps and throws $p to the ground!",
                victim,obj_lose,None,TO_ROOM)
                act("You remove and drop $p before it burns you.",
                victim,obj_lose,None,TO_CHAR)
            dam += (random.randint(1,obj_lose.level) / 3)
                        obj_from_char(obj_lose)
                        obj_to_room(obj_lose, victim.in_room)
                        fail = False
                    }
            else # stuck on the body! ouch! */
            {
            act("Your skin is seared by $p!",
                victim,obj_lose,None,TO_CHAR)
            dam += (random.randint(1,obj_lose.level))
            fail = False
            }

        }
        else # drop it if we can */
        {
            if (can_drop_obj(victim,obj_lose))
            {
                        act("$n yelps and throws $p to the ground!",
                            victim,obj_lose,None,TO_ROOM)
                        act("You and drop $p before it burns you.",
                            victim,obj_lose,None,TO_CHAR)
                        dam += (random.randint(1,obj_lose.level) / 6)
                        obj_from_char(obj_lose)
                        obj_to_room(obj_lose, victim.in_room)
            fail = False
                    }
            else # cannot drop */
            {
                        act("Your skin is seared by $p!",
                            victim,obj_lose,None,TO_CHAR)
                        dam += (random.randint(1,obj_lose.level) / 2)
            fail = False
                    }
        }
                break
                case ITEM_WEAPON:
        if (obj_lose.wear_loc != -1) # try to drop it */
        {
            if (IS_WEAPON_STAT(obj_lose,WEAPON_FLAMING))
            continue

            if (can_drop_obj(victim,obj_lose) 
            and  remove_obj(victim,obj_lose.wear_loc,True))
            {
            act("$n is burned by $p, and throws it to the ground.",
                victim,obj_lose,None,TO_ROOM)
            send_to_char(
                "You throw your red-hot weapon to the ground!\r\n",
                victim)
            dam += 1
            obj_from_char(obj_lose)
            obj_to_room(obj_lose,victim.in_room)
            fail = False
            }
            else # YOWCH! */
            {
            send_to_char("Your weapon sears your flesh!\r\n",
                victim)
            dam += random.randint(1,obj_lose.level)
            fail = False
            }
        }
                else # drop it if we can */
                {
                    if (can_drop_obj(victim,obj_lose))
                    {
                        act("$n throws a burning hot $p to the ground!",
                            victim,obj_lose,None,TO_ROOM)
                        act("You and drop $p before it burns you.",
                            victim,obj_lose,None,TO_CHAR)
                        dam += (random.randint(1,obj_lose.level) / 6)
                        obj_from_char(obj_lose)
                        obj_to_room(obj_lose, victim.in_room)
                        fail = False
                    }
                    else # cannot drop */
                    {
                        act("Your skin is seared by $p!",
                            victim,obj_lose,None,TO_CHAR)
                        dam += (random.randint(1,obj_lose.level) / 2)
                        fail = False
                    }
                }
                break
        }
        }
    }
    } 
    if (fail)
    {
        ch.send("Your spell had no effect.\r\n")
    victim.send("You feel momentarily warmer.\r\n")
    }
    else # damage! */
    {
    if (saves_spell(level,victim,DAM_FIRE))
        dam = 2 * dam / 3
    damage(ch,victim,dam,sn,DAM_FIRE,True)
    }
}

# RT really nasty high-level attack spell */
def spell_holy_word( sn, level, ch, victim, target ):
{
    CHAR_DATA *vch
    CHAR_DATA *vch_next
    int dam
    int bless_num, curse_num, frenzy_num
   
    bless_num = skill_lookup("bless")
    curse_num = skill_lookup("curse") 
    frenzy_num = skill_lookup("frenzy")

    act("$n utters a word of divine power!",ch,None,None,TO_ROOM)
    ch.send("You utter a word of divine power.\r\n")
 
    for vch in ch:
    {
        vch_next = vch.next_in_room

    if ((IS_GOOD(ch) and IS_GOOD(vch)) or
        (IS_EVIL(ch) and IS_EVIL(vch)) or
        (IS_NEUTRAL(ch) and IS_NEUTRAL(vch)) )
    {
      vch.send("You feel full more powerful.\r\n")
      spell_frenzy(frenzy_num,level,ch,(void *) vch,TARGET_CHAR) 
      spell_bless(bless_num,level,ch,(void *) vch,TARGET_CHAR)
    }

    else if ((IS_GOOD(ch) and IS_EVIL(vch)) or
         (IS_EVIL(ch) and IS_GOOD(vch)) )
    {
      if (!is_safe_spell(ch,vch,True))
      {
            spell_curse(curse_num,level,ch,(void *) vch,TARGET_CHAR)
        vch.send("You are struck down!\r\n")
        dam = dice(level,6)
        damage(ch,vch,dam,sn,DAM_ENERGY,True)
      }
    }

        else if (IS_NEUTRAL(ch))
    {
      if (!is_safe_spell(ch,vch,True))
      {
            spell_curse(curse_num,level/2,ch,(void *) vch,TARGET_CHAR)
        vch.send("You are struck down!\r\n")
        dam = dice(level,4)
        damage(ch,vch,dam,sn,DAM_ENERGY,True)
      }
    }
    }  
    
    ch.send("You feel drained.\r\n")
    ch.move = 0
    ch.hit /= 2
}
 
def spell_identify( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    char buf[MAX_STRING_LENGTH]
    AFFECT_DATA *paf

    sprintf( buf,
    "Object '%s' is type %s, extra flags %s.\r\nWeight is %d, value is %d, level is %d.\r\n",

    obj.name,
    item_name(obj.item_type),
    extra_bit_name( obj.extra_flags ),
    obj.weight / 10,
    obj.cost,
    obj.level
    )
    send_to_char( buf, ch )

    switch ( obj.item_type )
    {
    case ITEM_SCROLL: 
    case ITEM_POTION:
    case ITEM_PILL:
    sprintf( buf, "Level %d spells of:", obj.value[0] )
    send_to_char( buf, ch )

    if ( obj.value[1] >= 0 and obj.value[1] < MAX_SKILL )
    {
        ch.send(" '")
        send_to_char( skill_table[obj.value[1]].name, ch )
        ch.send("'")
    }

    if ( obj.value[2] >= 0 and obj.value[2] < MAX_SKILL )
    {
        ch.send(" '")
        send_to_char( skill_table[obj.value[2]].name, ch )
        ch.send("'")
    }

    if ( obj.value[3] >= 0 and obj.value[3] < MAX_SKILL )
    {
        ch.send(" '")
        send_to_char( skill_table[obj.value[3]].name, ch )
        ch.send("'")
    }

    if (obj.value[4] >= 0 and obj.value[4] < MAX_SKILL)
    {
        ch.send(" '")
        send_to_char(skill_table[obj.value[4]].name,ch)
        ch.send("'")
    }

    ch.send(".\r\n")
    break

    case ITEM_WAND: 
    case ITEM_STAFF: 
    sprintf( buf, "Has %d charges of level %d",
        obj.value[2], obj.value[0] )
    send_to_char( buf, ch )
      
    if ( obj.value[3] >= 0 and obj.value[3] < MAX_SKILL )
    {
        ch.send(" '")
        send_to_char( skill_table[obj.value[3]].name, ch )
        ch.send("'")
    }

    ch.send(".\r\n")
    break

    case ITEM_DRINK_CON:
        sprintf(buf,"It holds %s-colored %s.\r\n",
            liq_table[obj.value[2]].liq_color,
            liq_table[obj.value[2]].liq_name)
        send_to_char(buf,ch)
        break

    case ITEM_CONTAINER:
    sprintf(buf,"Capacity: %d#  Maximum weight: %d#  flags: %s\r\n",
        obj.value[0], obj.value[3], cont_bit_name(obj.value[1]))
    send_to_char(buf,ch)
    if (obj.value[4] != 100)
    {
        sprintf(buf,"Weight multiplier: %d%%\r\n",
        obj.value[4])
        send_to_char(buf,ch)
    }
    break
        
    case ITEM_WEAPON:
    ch.send("Weapon type is ")
    switch (obj.value[0])
    {
        case(WEAPON_EXOTIC) : ch.send("exotic.\r\n")   break
        case(WEAPON_SWORD)  : ch.send("sword.\r\n")    break  
        case(WEAPON_DAGGER) : ch.send("dagger.\r\n")   break
        case(WEAPON_SPEAR)  : ch.send("spear/staff.\r\n")  break
        case(WEAPON_MACE)   : ch.send("mace/club.\r\n")    break
        case(WEAPON_AXE)    : ch.send("axe.\r\n")      break
        case(WEAPON_FLAIL)  : ch.send("flail.\r\n")    break
        case(WEAPON_WHIP)   : ch.send("whip.\r\n")     break
        case(WEAPON_POLEARM): ch.send("polearm.\r\n")  break
        default     : ch.send("unknown.\r\n")  break
    }
    if (obj.pIndexData.new_format)
        sprintf(buf,"Damage is %dd%d (average %d).\r\n",
        obj.value[1],obj.value[2],
        (1 + obj.value[2]) * obj.value[1] / 2)
    else
        sprintf( buf, "Damage is %d to %d (average %d).\r\n",
            obj.value[1], obj.value[2],
            ( obj.value[1] + obj.value[2] ) / 2 )
    send_to_char( buf, ch )
        if (obj.value[4])  # weapon flags */
        {
            sprintf(buf,"Weapons flags: %s\r\n",weapon_bit_name(obj.value[4]))
            send_to_char(buf,ch)
        }
    break

    case ITEM_ARMOR:
    sprintf( buf, 
    "Armor class is %d pierce, %d bash, %d slash, and %d vs. magic.\r\n", 
        obj.value[0], obj.value[1], obj.value[2], obj.value[3] )
    send_to_char( buf, ch )
    break
    }

    if (!obj.enchanted)
    for paf in obj:
    {
    if ( paf.location != APPLY_NONE and paf.modifier != 0 )
    {
        sprintf( buf, "Affects %s by %d.\r\n",
        affect_loc_name( paf.location ), paf.modifier )
        send_to_char(buf,ch)
            if (paf.bitvector)
            {
                switch(paf.where)
                {
                    case TO_AFFECTS:
                        sprintf(buf,"Adds %s affect.\n",
                            affect_bit_name(paf.bitvector))
                        break
                    case TO_OBJECT:
                        sprintf(buf,"Adds %s object flag.\n",
                            extra_bit_name(paf.bitvector))
                        break
                    case TO_IMMUNE:
                        sprintf(buf,"Adds immunity to %s.\n",
                            imm_bit_name(paf.bitvector))
                        break
                    case TO_RESIST:
                        sprintf(buf,"Adds resistance to %s.\r\n",
                            imm_bit_name(paf.bitvector))
                        break
                    case TO_VULN:
                        sprintf(buf,"Adds vulnerability to %s.\r\n",
                            imm_bit_name(paf.bitvector))
                        break
                    default:
                        sprintf(buf,"Unknown bit %d: %d\r\n",
                            paf.where,paf.bitvector)
                        break
                }
            send_to_char( buf, ch )
        }
    }
    }

    for paf in obj:
    {
    if ( paf.location != APPLY_NONE and paf.modifier != 0 )
    {
        sprintf( buf, "Affects %s by %d",
            affect_loc_name( paf.location ), paf.modifier )
        send_to_char( buf, ch )
            if ( paf.duration > -1)
                sprintf(buf,", %d hours.\r\n",paf.duration)
            else
                sprintf(buf,".\r\n")
        send_to_char(buf,ch)
            if (paf.bitvector)
            {
                switch(paf.where)
                {
                    case TO_AFFECTS:
                        sprintf(buf,"Adds %s affect.\n",
                            affect_bit_name(paf.bitvector))
                        break
                    case TO_OBJECT:
                        sprintf(buf,"Adds %s object flag.\n",
                            extra_bit_name(paf.bitvector))
                        break
            case TO_WEAPON:
            sprintf(buf,"Adds %s weapon flags.\n",
                weapon_bit_name(paf.bitvector))
            break
                    case TO_IMMUNE:
                        sprintf(buf,"Adds immunity to %s.\n",
                            imm_bit_name(paf.bitvector))
                        break
                    case TO_RESIST:
                        sprintf(buf,"Adds resistance to %s.\r\n",
                            imm_bit_name(paf.bitvector))
                        break
                    case TO_VULN:
                        sprintf(buf,"Adds vulnerability to %s.\r\n",
                            imm_bit_name(paf.bitvector))
                        break
                    default:
                        sprintf(buf,"Unknown bit %d: %d\r\n",
                            paf.where,paf.bitvector)
                        break
                }
                send_to_char(buf,ch)
            }
    }
    }

    return
}



def spell_infravision( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_INFRARED) )
    {
    if (victim == ch)
      ch.send("You can already see in the dark.\r\n")
    else
      act("$N already has infravision.\r\n",ch,None,victim,TO_CHAR)
    return
    }
    act( "$n's eyes glow red.\r\n", ch, None, None, TO_ROOM )

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 2 * level
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_INFRARED
    affect_to_char( victim, &af )
    victim.send("Your eyes glow red.\r\n")
    return
}



def spell_invis( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim
    OBJ_DATA *obj
    AFFECT_DATA af

    # object invisibility */
    if (target == TARGET_OBJ)
    {
    obj = (OBJ_DATA *) vo  

    if (IS_OBJ_STAT(obj,ITEM_INVIS))
    {
        act("$p is already invisible.",ch,obj,None,TO_CHAR)
        return
    }
    
    af.where    = TO_OBJECT
    af.type     = sn
    af.level    = level
    af.duration = level + 12
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector    = ITEM_INVIS
    affect_to_obj(obj,&af)

    act("$p fades out of sight.",ch,obj,None,TO_ALL)
    return
    }

    # character invisibility */
    victim = (CHAR_DATA *) vo

    if ( IS_AFFECTED(victim, AFF_INVISIBLE) )
    return

    act( "$n fades out of existence.", victim, None, None, TO_ROOM )

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level + 12
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_INVISIBLE
    affect_to_char( victim, &af )
    victim.send("You fade out of existence.\r\n")
    return
}



def spell_know_alignment( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    char *msg
    int ap

    ap = victim.alignment

         if ( ap >  700 ) msg = "$N has a pure and good aura."
    else if ( ap >  350 ) msg = "$N is of excellent moral character."
    else if ( ap >  100 ) msg = "$N is often kind and thoughtful."
    else if ( ap > -100 ) msg = "$N doesn't have a firm moral commitment."
    else if ( ap > -350 ) msg = "$N lies to $S friends."
    else if ( ap > -700 ) msg = "$N is a black-hearted murderer."
    else msg = "$N is the embodiment of pure evil!."

    act( msg, ch, None, victim, TO_CHAR )
    return
}



def spell_lightning_bolt( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    static const sh_int dam_each[] = 
    {
     0,
     0,  0,  0,  0,  0,  0,  0,  0, 25, 28,
    31, 34, 37, 40, 40, 41, 42, 42, 43, 44,
    44, 45, 46, 46, 47, 48, 48, 49, 50, 50,
    51, 52, 52, 53, 54, 54, 55, 56, 56, 57,
    58, 58, 59, 60, 60, 61, 62, 62, 63, 64
    }
    int dam

    level   = min(level, len(dam_each)-1)
    level   = UMAX(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if ( saves_spell( level, victim,DAM_LIGHTNING) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_LIGHTNING ,True)
    return
}



def spell_locate_object( sn, level, ch, victim, target ):
{
    char buf[MAX_INPUT_LENGTH]
    BUFFER *buffer
    OBJ_DATA *obj
    OBJ_DATA *in_obj
    bool found
    int number = 0, max_found

    found = False
    number = 0
    max_found = IS_IMMORTAL(ch) ? 200 : 2 * level

    buffer = new_buf()
 
    for obj in object_list:
    {
    if ( !can_see_obj( ch, obj ) or !is_name( target_name, obj.name ) 
        or   IS_OBJ_STAT(obj,ITEM_NOLOCATE) or number_percent() > 2 * level
    or   ch.level < obj.level)
        continue

    found = True
        number=number+1

    for in_obj in obj:
        

    if ( in_obj.carried_by != None and can_see(ch,in_obj.carried_by))
    {
        sprintf( buf, "one is carried by %s\r\n",
        PERS(in_obj.carried_by, ch) )
    }
    else
    {
        if (IS_IMMORTAL(ch) and in_obj.in_room != None)
        sprintf( buf, "one is in %s [Room %d]\r\n",
            in_obj.in_room.name, in_obj.in_room.vnum)
        else 
            sprintf( buf, "one is in %s\r\n",
            in_obj.in_room == None
                ? "somewhere" : in_obj.in_room.name )
    }

    buf[0] = UPPER(buf[0])
    add_buf(buffer,buf)

        if (number >= max_found)
        break
    }

    if ( !found )
    ch.send("Nothing like that in heaven or earth.\r\n")
    else
    page_to_char(buf_string(buffer),ch)

    free_buf(buffer)

    return
}



def spell_magic_missile( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    static const sh_int dam_each[] = 
    {
     0,
     3,  3,  4,  4,  5,  6,  6,  6,  6,  6,
     7,  7,  7,  7,  7,  8,  8,  8,  8,  8,
     9,  9,  9,  9,  9, 10, 10, 10, 10, 10,
    11, 11, 11, 11, 11, 12, 12, 12, 12, 12,
    13, 13, 13, 13, 13, 14, 14, 14, 14, 14
    }
    int dam

    level   = min(level, len(dam_each)-1)
    level   = UMAX(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if ( saves_spell( level, victim,DAM_ENERGY) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_ENERGY ,True)
    return
}

def spell_mass_healing( sn, level, ch, victim, target ):
{
    CHAR_DATA *gch
    int heal_num, refresh_num
    
    heal_num = skill_lookup("heal")
    refresh_num = skill_lookup("refresh") 

    for gch in ch:
    {
    if ((IS_NPC(ch) and IS_NPC(gch)) or
        (!IS_NPC(ch) and !IS_NPC(gch)))
    {
        spell_heal(heal_num,level,ch,(void *) gch,TARGET_CHAR)
        spell_refresh(refresh_num,level,ch,(void *) gch,TARGET_CHAR)  
    }
    }
}
        

def spell_mass_invis( sn, level, ch, victim, target ):
{
    AFFECT_DATA af
    CHAR_DATA *gch

    for gch in ch:
    {
    if ( !is_same_group( gch, ch ) or IS_AFFECTED(gch, AFF_INVISIBLE) )
        continue
    act( "$n slowly fades out of existence.", gch, None, None, TO_ROOM )
    gch.send("You slowly fade out of existence.\r\n")

    af.where     = TO_AFFECTS
    af.type      = sn
        af.level     = level/2
    af.duration  = 24
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_INVISIBLE
    affect_to_char( gch, &af )
    }
    ch.send("Ok.\r\n")

    return
}



def spell_null( sn, level, ch, victim, target ):
{
    ch.send("That's not a spell!\r\n")
    return
}



def spell_pass_door( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_PASS_DOOR) )
    {
    if (victim == ch)
      ch.send("You are already out of phase.\r\n")
    else
      act("$N is already shifted out of phase.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = number_fuzzy( level / 4 )
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_PASS_DOOR
    affect_to_char( victim, &af )
    act( "$n turns translucent.", victim, None, None, TO_ROOM )
    victim.send("You turn translucent.\r\n")
    return
}

# RT plague spell, very nasty */

def spell_plague( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if (saves_spell(level,victim,DAM_DISEASE) or 
        (IS_NPC(victim) and IS_SET(victim.act,ACT_UNDEAD)))
    {
    if (ch == victim)
      ch.send("You feel momentarily ill, but it passes.\r\n")
    else
      act("$N seems to be unaffected.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type       = sn
    af.level      = level * 3/4
    af.duration  = level
    af.location  = APPLY_STR
    af.modifier  = -5 
    af.bitvector = AFF_PLAGUE
    affect_join(victim,&af)
   
    send_to_char
      ("You scream in agony as plague sores erupt from your skin.\r\n",victim)
    act("$n screams in agony as plague sores erupt from $s skin.",
    victim,None,None,TO_ROOM)
}

def spell_poison( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim
    OBJ_DATA *obj
    AFFECT_DATA af


    if (target == TARGET_OBJ)
    {
    obj = (OBJ_DATA *) vo

    if (obj.item_type == ITEM_FOOD or obj.item_type == ITEM_DRINK_CON)
    {
        if (IS_OBJ_STAT(obj,ITEM_BLESS) or IS_OBJ_STAT(obj,ITEM_BURN_PROOF))
        {
        act("Your spell fails to corrupt $p.",ch,obj,None,TO_CHAR)
        return
        }
        obj.value[3] = 1
        act("$p is infused with poisonous vapors.",ch,obj,None,TO_ALL)
        return
    }

    if (obj.item_type == ITEM_WEAPON)
    {
        if (IS_WEAPON_STAT(obj,WEAPON_FLAMING)
        or  IS_WEAPON_STAT(obj,WEAPON_FROST)
        or  IS_WEAPON_STAT(obj,WEAPON_VAMPIRIC)
        or  IS_WEAPON_STAT(obj,WEAPON_SHARP)
        or  IS_WEAPON_STAT(obj,WEAPON_VORPAL)
        or  IS_WEAPON_STAT(obj,WEAPON_SHOCKING)
        or  IS_OBJ_STAT(obj,ITEM_BLESS) or IS_OBJ_STAT(obj,ITEM_BURN_PROOF))
        {
        act("You can't seem to envenom $p.",ch,obj,None,TO_CHAR)
        return
        }

        if (IS_WEAPON_STAT(obj,WEAPON_POISON))
        {
        act("$p is already envenomed.",ch,obj,None,TO_CHAR)
        return
        }

        af.where     = TO_WEAPON
        af.type  = sn
        af.level     = level / 2
        af.duration  = level/8
        af.location  = 0
        af.modifier  = 0
        af.bitvector = WEAPON_POISON
        affect_to_obj(obj,&af)

        act("$p is coated with deadly venom.",ch,obj,None,TO_ALL)
        return
    }

    act("You can't poison $p.",ch,obj,None,TO_CHAR)
    return
    }

    victim = (CHAR_DATA *) vo

    if ( saves_spell( level, victim,DAM_POISON) )
    {
    act("$n turns slightly green, but it passes.",victim,None,None,TO_ROOM)
    victim.send("You feel momentarily ill, but it passes.\r\n")
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.location  = APPLY_STR
    af.modifier  = -2
    af.bitvector = AFF_POISON
    affect_join( victim, &af )
    victim.send("You feel very sick.\r\n")
    act("$n looks very ill.",victim,None,None,TO_ROOM)
    return
}



def spell_protection_evil( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
 
    if ( IS_AFFECTED(victim, AFF_PROTECT_EVIL) 
    or   IS_AFFECTED(victim, AFF_PROTECT_GOOD))
    {
        if (victim == ch)
          ch.send("You are already protected.\r\n")
        else
          act("$N is already protected.",ch,None,victim,TO_CHAR)
        return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 24
    af.location  = APPLY_SAVING_SPELL
    af.modifier  = -1
    af.bitvector = AFF_PROTECT_EVIL
    affect_to_char( victim, &af )
    victim.send("You feel holy and pure.\r\n")
    if ( ch != victim )
        act("$N is protected from evil.",ch,None,victim,TO_CHAR)
    return
}
 
def spell_protection_good( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
 
    if ( IS_AFFECTED(victim, AFF_PROTECT_GOOD) 
    or   IS_AFFECTED(victim, AFF_PROTECT_EVIL))
    {
        if (victim == ch)
          ch.send("You are already protected.\r\n")
        else
          act("$N is already protected.",ch,None,victim,TO_CHAR)
        return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 24
    af.location  = APPLY_SAVING_SPELL
    af.modifier  = -1
    af.bitvector = AFF_PROTECT_GOOD
    affect_to_char( victim, &af )
    victim.send("You feel aligned with darkness.\r\n")
    if ( ch != victim )
        act("$N is protected from good.",ch,None,victim,TO_CHAR)
    return
}


void spell_ray_of_truth (int sn, int level, CHAR_DATA *ch, void *vo,int target)
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam, align
 
    if (IS_EVIL(ch) )
    {
        victim = ch
        ch.send("The energy explodes inside you!\r\n")
    }
 
    if (victim != ch)
    {
        act("$n raises $s hand, and a blinding ray of light shoots forth!",
            ch,None,None,TO_ROOM)
        send_to_char(
       "You raise your hand and a blinding ray of light shoots forth!\r\n",
       ch)
    }

    if (IS_GOOD(victim))
    {
    act("$n seems unharmed by the light.",victim,None,victim,TO_ROOM)
    victim.send("The light seems powerless to affect you.\r\n")
    return
    }

    dam = dice( level, 10 )
    if ( saves_spell( level, victim,DAM_HOLY) )
        dam /= 2

    align = victim.alignment
    align -= 350

    if (align < -1000)
    align = -1000 + (align + 1000) / 3

    dam = (dam * align * align) / 1000000

    damage( ch, victim, dam, sn, DAM_HOLY ,True)
    spell_blindness(gsn_blindness, 
    3 * level / 4, ch, (void *) victim,TARGET_CHAR)
}


def spell_recharge( sn, level, ch, victim, target ):
{
    OBJ_DATA *obj = (OBJ_DATA *) vo
    int chance, percent

    if (obj.item_type != ITEM_WAND and obj.item_type != ITEM_STAFF)
    {
    ch.send("That item does not carry charges.\r\n")
    return
    }

    if (obj.value[3] >= 3 * level / 2)
    {
    ch.send("Your skills are not great enough for that.\r\n")
    return
    }

    if (obj.value[1] == 0)
    {
    ch.send("That item has already been recharged once.\r\n")
    return
    }

    chance = 40 + 2 * level

    chance -= obj.value[3] # harder to do high-level spells */
    chance -= (obj.value[1] - obj.value[2]) *
          (obj.value[1] - obj.value[2])

    chance = UMAX(level/2,chance)

    percent = number_percent()

    if (percent < chance / 2)
    {
    act("$p glows softly.",ch,obj,None,TO_CHAR)
    act("$p glows softly.",ch,obj,None,TO_ROOM)
    obj.value[2] = UMAX(obj.value[1],obj.value[2])
    obj.value[1] = 0
    return
    }

    else if (percent <= chance)
    {
    int chargeback,chargemax

    act("$p glows softly.",ch,obj,None,TO_CHAR)
    act("$p glows softly.",ch,obj,None,TO_CHAR)

    chargemax = obj.value[1] - obj.value[2]
    
    if (chargemax > 0)
        chargeback = UMAX(1,chargemax * percent / 100)
    else
        chargeback = 0

    obj.value[2] += chargeback
    obj.value[1] = 0
    return
    }   

    else if (percent <= UMIN(95, 3 * chance / 2))
    {
    ch.send("Nothing seems to happen.\r\n")
    if (obj.value[1] > 1)
        obj.value[1]--
    return
    }

    else # whoops! */
    {
    act("$p glows brightly and explodes!",ch,obj,None,TO_CHAR)
    act("$p glows brightly and explodes!",ch,obj,None,TO_ROOM)
    extract_obj(obj)
    }
}

def spell_refresh( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    victim.move = UMIN( victim.move + level, victim.max_move )
    if (victim.max_move == victim.move)
        victim.send("You feel fully refreshed!\r\n")
    else
        victim.send("You feel less tired.\r\n")
    if ( ch != victim )
        ch.send("Ok.\r\n")
    return
}

def spell_remove_curse( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim
    OBJ_DATA *obj
    bool found = False

    # do object cases first */
    if (target == TARGET_OBJ)
    {
    obj = (OBJ_DATA *) vo

    if (IS_OBJ_STAT(obj,ITEM_NODROP) or IS_OBJ_STAT(obj,ITEM_NOREMOVE))
    {
        if (!IS_OBJ_STAT(obj,ITEM_NOUNCURSE)
        and  !saves_dispel(level + 2,obj.level,0))
        {
        REMOVE_BIT(obj.extra_flags,ITEM_NODROP)
        REMOVE_BIT(obj.extra_flags,ITEM_NOREMOVE)
        act("$p glows blue.",ch,obj,None,TO_ALL)
        return
        }

        act("The curse on $p is beyond your power.",ch,obj,None,TO_CHAR)
        return
    }
    act("There doesn't seem to be a curse on $p.",ch,obj,None,TO_CHAR)
    return
    }

    # characters */
    victim = (CHAR_DATA *) vo

    if (check_dispel(level,victim,gsn_curse))
    {
    victim.send("You feel better.\r\n")
    act("$n looks more relaxed.",victim,None,None,TO_ROOM)
    }

   for obj in victim:
   {
        if ((IS_OBJ_STAT(obj,ITEM_NODROP) or IS_OBJ_STAT(obj,ITEM_NOREMOVE))
    and  !IS_OBJ_STAT(obj,ITEM_NOUNCURSE))
        {   # attempt to remove curse */
            if (!saves_dispel(level,obj.level,0))
            {
                found = True
                REMOVE_BIT(obj.extra_flags,ITEM_NODROP)
                REMOVE_BIT(obj.extra_flags,ITEM_NOREMOVE)
                act("Your $p glows blue.",victim,obj,None,TO_CHAR)
                act("$n's $p glows blue.",victim,obj,None,TO_ROOM)
            }
         }
    }
}

def spell_sanctuary( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( IS_AFFECTED(victim, AFF_SANCTUARY) )
    {
    if (victim == ch)
      ch.send("You are already in sanctuary.\r\n")
    else
      act("$N is already in sanctuary.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level / 6
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_SANCTUARY
    affect_to_char( victim, &af )
    act( "$n is surrounded by a white aura.", victim, None, None, TO_ROOM )
    victim.send("You are surrounded by a white aura.\r\n")
    return
}



def spell_shield( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( is_affected( victim, sn ) )
    {
    if (victim == ch)
      ch.send("You are already shielded from harm.\r\n")
    else
      act("$N is already protected by a shield.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 8 + level
    af.location  = APPLY_AC
    af.modifier  = -20
    af.bitvector = 0
    affect_to_char( victim, &af )
    act( "$n is surrounded by a force shield.", victim, None, None, TO_ROOM )
    victim.send("You are surrounded by a force shield.\r\n")
    return
}



def spell_shocking_grasp( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    static const int dam_each[] = 
    {
     0,
     0,  0,  0,  0,  0,  0, 20, 25, 29, 33,
    36, 39, 39, 39, 40, 40, 41, 41, 42, 42,
    43, 43, 44, 44, 45, 45, 46, 46, 47, 47,
    48, 48, 49, 49, 50, 50, 51, 51, 52, 52,
    53, 53, 54, 54, 55, 55, 56, 56, 57, 57
    }
    int dam

    level   = min(level, len(dam_each)-1)
    level   = UMAX(0, level)
    dam     = random.randint( dam_each[level] / 2, dam_each[level] * 2 )
    if ( saves_spell( level, victim,DAM_LIGHTNING) )
    dam /= 2
    damage( ch, victim, dam, sn, DAM_LIGHTNING ,True)
    return
}



def spell_sleep( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
  
    if ( IS_AFFECTED(victim, AFF_SLEEP)
    or   (IS_NPC(victim) and IS_SET(victim.act,ACT_UNDEAD))
    or   (level + 2) < victim.level
    or   saves_spell( level-4, victim,DAM_CHARM) )
    return

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = 4 + level
    af.location  = APPLY_NONE
    af.modifier  = 0
    af.bitvector = AFF_SLEEP
    affect_join( victim, &af )

    if ( IS_AWAKE(victim) )
    {
    victim.send("You feel very sleepy ..... zzzzzz.\r\n")
    act( "$n goes to sleep.", victim, None, None, TO_ROOM )
    victim.position = POS_SLEEPING
    }
    return
}

def spell_slow( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af
 
    if ( is_affected( victim, sn ) or IS_AFFECTED(victim,AFF_SLOW))
    {
        if (victim == ch)
          ch.send("You can't move any slower!\r\n")
        else
          act("$N can't get any slower than that.",
              ch,None,victim,TO_CHAR)
        return
    }
 
    if (saves_spell(level,victim,DAM_OTHER) 
    or  IS_SET(victim.imm_flags,IMM_MAGIC))
    {
    if (victim != ch)
            ch.send("Nothing seemed to happen.\r\n")
        victim.send("You feel momentarily lethargic.\r\n")
        return
    }
 
    if (IS_AFFECTED(victim,AFF_HASTE))
    {
        if (!check_dispel(level,victim,skill_lookup("haste")))
        {
        if (victim != ch)
                ch.send("Spell failed.\r\n")
            victim.send("You feel momentarily slower.\r\n")
            return
        }

        act("$n is moving less quickly.",victim,None,None,TO_ROOM)
        return
    }
 

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level/2
    af.location  = APPLY_DEX
    af.modifier  = -1 - (level >= 18) - (level >= 25) - (level >= 32)
    af.bitvector = AFF_SLOW
    affect_to_char( victim, &af )
    victim.send("You feel yourself slowing d o w n...\r\n")
    act("$n starts to move in slow motion.",victim,None,None,TO_ROOM)
    return
}




def spell_stone_skin( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( is_affected( ch, sn ) )
    {
    if (victim == ch)
      ch.send("Your skin is already as hard as a rock.\r\n") 
    else
      act("$N is already as hard as can be.",ch,None,victim,TO_CHAR)
    return
    }

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level
    af.location  = APPLY_AC
    af.modifier  = -40
    af.bitvector = 0
    affect_to_char( victim, &af )
    act( "$n's skin turns to stone.", victim, None, None, TO_ROOM )
    victim.send("Your skin turns to stone.\r\n")
    return
}



def spell_summon( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim

    if ( ( victim = get_char_world( ch, target_name ) ) == None
    or   victim == ch
    or   victim.in_room == None
    or   IS_SET(ch.in_room.room_flags, ROOM_SAFE)
    or   IS_SET(victim.in_room.room_flags, ROOM_SAFE)
    or   IS_SET(victim.in_room.room_flags, ROOM_PRIVATE)
    or   IS_SET(victim.in_room.room_flags, ROOM_SOLITARY)
    or   IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL)
    or   (IS_NPC(victim) and IS_SET(victim.act,ACT_AGGRESSIVE))
    or   victim.level >= level + 3
    or   (!IS_NPC(victim) and victim.level >= LEVEL_IMMORTAL)
    or   victim.fighting != None
    or   (IS_NPC(victim) and IS_SET(victim.imm_flags,IMM_SUMMON))
    or   (IS_NPC(victim) and victim.pIndexData.pShop != None)
    or   (!IS_NPC(victim) and IS_SET(victim.act,PLR_NOSUMMON))
    or   (IS_NPC(victim) and saves_spell( level, victim,DAM_OTHER)) )

    {
    ch.send("You failed.\r\n")
    return
    }

    act( "$n disappears suddenly.", victim, None, None, TO_ROOM )
    char_from_room( victim )
    char_to_room( victim, ch.in_room )
    act( "$n arrives suddenly.", victim, None, None, TO_ROOM )
    act( "$n has summoned you!", ch, None, victim,   TO_VICT )
    do_function(victim, &do_look, "auto" )
    return
}



def spell_teleport( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    ROOM_INDEX_DATA *pRoomIndex

    if ( victim.in_room == None
    or   IS_SET(victim.in_room.room_flags, ROOM_NO_RECALL)
    or ( victim != ch and IS_SET(victim.imm_flags,IMM_SUMMON))
    or ( !IS_NPC(ch) and victim.fighting != None )
    or ( victim != ch
    and ( saves_spell( level - 5, victim,DAM_OTHER))))
    {
    ch.send("You failed.\r\n")
    return
    }

    pRoomIndex = get_random_room(victim)

    if (victim != ch)
    victim.send("You have been teleported!\r\n")

    act( "$n vanishes!", victim, None, None, TO_ROOM )
    char_from_room( victim )
    char_to_room( victim, pRoomIndex )
    act( "$n slowly fades into existence.", victim, None, None, TO_ROOM )
    do_function(victim, &do_look, "auto" )
    return
}



def spell_ventriloquate( sn, level, ch, victim, target ):
{
    char buf1[MAX_STRING_LENGTH]
    char buf2[MAX_STRING_LENGTH]
    char speaker[MAX_INPUT_LENGTH]
    CHAR_DATA *vch

    target_name = one_argument( target_name, speaker )

    sprintf( buf1, "%s says '%s'.\r\n",              speaker, target_name )
    sprintf( buf2, "Someone makes %s say '%s'.\r\n", speaker, target_name )
    buf1[0] = UPPER(buf1[0])

    for vch in ch:
    {
    if (!is_exact_name( speaker, vch.name) and IS_AWAKE(vch))
        send_to_char( saves_spell(level,vch,DAM_OTHER) ? buf2 : buf1, vch )
    }

    return
}



def spell_weaken( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    AFFECT_DATA af

    if ( is_affected( victim, sn ) or saves_spell( level, victim,DAM_OTHER) )
    return

    af.where     = TO_AFFECTS
    af.type      = sn
    af.level     = level
    af.duration  = level / 2
    af.location  = APPLY_STR
    af.modifier  = -1 * (level / 5)
    af.bitvector = AFF_WEAKEN
    affect_to_char( victim, &af )
    victim.send("You feel your strength slip away.\r\n")
    act("$n looks tired and weak.",victim,None,None,TO_ROOM)
    return
}



# RT recall spell is back */

def spell_word_of_recall( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    ROOM_INDEX_DATA *location
    
    if (IS_NPC(victim))
      return
   
    if ((location = get_room_index( ROOM_VNUM_TEMPLE)) == None)
    {
    victim.send("You are completely lost.\r\n")
    return
    } 

    if (IS_SET(victim.in_room.room_flags,ROOM_NO_RECALL) or
    IS_AFFECTED(victim,AFF_CURSE))
    {
    victim.send("Spell failed.\r\n")
    return
    }

    if (victim.fighting != None)
    stop_fighting(victim,True)
    
    ch.move /= 2
    act("$n disappears.",victim,None,None,TO_ROOM)
    char_from_room(victim)
    char_to_room(victim,location)
    act("$n appears in the room.",victim,None,None,TO_ROOM)
    do_function(victim, &do_look, "auto")
}

#
 * NPC spells.
 */
def spell_acid_breath( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam,hp_dam,dice_dam,hpch

    act("$n spits acid at $N.",ch,None,victim,TO_NOTVICT)
    act("$n spits a stream of corrosive acid at you.",ch,None,victim,TO_VICT)
    act("You spit acid at $N.",ch,None,victim,TO_CHAR)

    hpch = UMAX(12,ch.hit)
    hp_dam = random.randint(hpch/11 + 1, hpch/6)
    dice_dam = dice(level,16)

    dam = UMAX(hp_dam + dice_dam/10,dice_dam + hp_dam/10)
    
    if (saves_spell(level,victim,DAM_ACID))
    {
    acid_effect(victim,level/2,dam/4,TARGET_CHAR)
    damage(ch,victim,dam/2,sn,DAM_ACID,True)
    }
    else
    {
    acid_effect(victim,level,dam,TARGET_CHAR)
    damage(ch,victim,dam,sn,DAM_ACID,True)
    }
}



def spell_fire_breath( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    CHAR_DATA *vch, *vch_next
    int dam,hp_dam,dice_dam
    int hpch

    act("$n breathes forth a cone of fire.",ch,None,victim,TO_NOTVICT)
    act("$n breathes a cone of hot fire over you!",ch,None,victim,TO_VICT)
    act("You breath forth a cone of fire.",ch,None,None,TO_CHAR)

    hpch = UMAX( 10, ch.hit )
    hp_dam  = random.randint( hpch/9+1, hpch/5 )
    dice_dam = dice(level,20)

    dam = UMAX(hp_dam + dice_dam /10, dice_dam + hp_dam / 10)
    fire_effect(victim.in_room,level,dam/2,TARGET_ROOM)

    for vch in victim:
    {
    vch_next = vch.next_in_room

    if (is_safe_spell(ch,vch,True) 
    or  (IS_NPC(vch) and IS_NPC(ch) 
    and   (ch.fighting != vch or vch.fighting != ch)))
        continue

    if (vch == victim) # full damage */
    {
        if (saves_spell(level,vch,DAM_FIRE))
        {
        fire_effect(vch,level/2,dam/4,TARGET_CHAR)
        damage(ch,vch,dam/2,sn,DAM_FIRE,True)
        }
        else
        {
        fire_effect(vch,level,dam,TARGET_CHAR)
        damage(ch,vch,dam,sn,DAM_FIRE,True)
        }
    }
    else # partial damage */
    {
        if (saves_spell(level - 2,vch,DAM_FIRE))
        {
        fire_effect(vch,level/4,dam/8,TARGET_CHAR)
        damage(ch,vch,dam/4,sn,DAM_FIRE,True)
        }
        else
        {
        fire_effect(vch,level/2,dam/4,TARGET_CHAR)
        damage(ch,vch,dam/2,sn,DAM_FIRE,True)
        }
    }
    }
}

def spell_frost_breath( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    CHAR_DATA *vch, *vch_next
    int dam,hp_dam,dice_dam, hpch

    act("$n breathes out a freezing cone of frost!",ch,None,victim,TO_NOTVICT)
    act("$n breathes a freezing cone of frost over you!",
    ch,None,victim,TO_VICT)
    act("You breath out a cone of frost.",ch,None,None,TO_CHAR)

    hpch = UMAX(12,ch.hit)
    hp_dam = random.randint(hpch/11 + 1, hpch/6)
    dice_dam = dice(level,16)

    dam = UMAX(hp_dam + dice_dam/10,dice_dam + hp_dam/10)
    cold_effect(victim.in_room,level,dam/2,TARGET_ROOM) 

    for vch in victim:
    {
    vch_next = vch.next_in_room

    if (is_safe_spell(ch,vch,True)
    or  (IS_NPC(vch) and IS_NPC(ch) 
    and   (ch.fighting != vch or vch.fighting != ch)))
        continue

    if (vch == victim) # full damage */
    {
        if (saves_spell(level,vch,DAM_COLD))
        {
        cold_effect(vch,level/2,dam/4,TARGET_CHAR)
        damage(ch,vch,dam/2,sn,DAM_COLD,True)
        }
        else
        {
        cold_effect(vch,level,dam,TARGET_CHAR)
        damage(ch,vch,dam,sn,DAM_COLD,True)
        }
    }
    else
    {
        if (saves_spell(level - 2,vch,DAM_COLD))
        {
        cold_effect(vch,level/4,dam/8,TARGET_CHAR)
        damage(ch,vch,dam/4,sn,DAM_COLD,True)
        }
        else
        {
        cold_effect(vch,level/2,dam/4,TARGET_CHAR)
        damage(ch,vch,dam/2,sn,DAM_COLD,True)
        }
    }
    }
}

    
def spell_gas_breath( sn, level, ch, victim, target ):
{
    CHAR_DATA *vch
    CHAR_DATA *vch_next
    int dam,hp_dam,dice_dam,hpch

    act("$n breathes out a cloud of poisonous gas!",ch,None,None,TO_ROOM)
    act("You breath out a cloud of poisonous gas.",ch,None,None,TO_CHAR)

    hpch = UMAX(16,ch.hit)
    hp_dam = random.randint(hpch/15+1,8)
    dice_dam = dice(level,12)

    dam = UMAX(hp_dam + dice_dam/10,dice_dam + hp_dam/10)
    poison_effect(ch.in_room,level,dam,TARGET_ROOM)

    for vch in ch:
    {
    vch_next = vch.next_in_room

    if (is_safe_spell(ch,vch,True)
    or  (IS_NPC(ch) and IS_NPC(vch) 
    and   (ch.fighting == vch or vch.fighting == ch)))
        continue

    if (saves_spell(level,vch,DAM_POISON))
    {
        poison_effect(vch,level/2,dam/4,TARGET_CHAR)
        damage(ch,vch,dam/2,sn,DAM_POISON,True)
    }
    else
    {
        poison_effect(vch,level,dam,TARGET_CHAR)
        damage(ch,vch,dam,sn,DAM_POISON,True)
    }
    }
}

def spell_lightning_breath( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam,hp_dam,dice_dam,hpch

    act("$n breathes a bolt of lightning at $N.",ch,None,victim,TO_NOTVICT)
    act("$n breathes a bolt of lightning at you!",ch,None,victim,TO_VICT)
    act("You breathe a bolt of lightning at $N.",ch,None,victim,TO_CHAR)

    hpch = UMAX(10,ch.hit)
    hp_dam = random.randint(hpch/9+1,hpch/5)
    dice_dam = dice(level,20)

    dam = UMAX(hp_dam + dice_dam/10,dice_dam + hp_dam/10)

    if (saves_spell(level,victim,DAM_LIGHTNING))
    {
    shock_effect(victim,level/2,dam/4,TARGET_CHAR)
    damage(ch,victim,dam/2,sn,DAM_LIGHTNING,True)
    }
    else
    {
    shock_effect(victim,level,dam,TARGET_CHAR)
    damage(ch,victim,dam,sn,DAM_LIGHTNING,True) 
    }
}

#
 * Spells for mega1.are from Glop/Erkenbrand.
 */
def spell_general_purpose( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam
 
    dam = random.randint( 25, 100 )
    if ( saves_spell( level, victim, DAM_PIERCE) )
        dam /= 2
    damage( ch, victim, dam, sn, DAM_PIERCE ,True)
    return
}

def spell_high_explosive( sn, level, ch, victim, target ):
{
    CHAR_DATA *victim = (CHAR_DATA *) vo
    int dam
 
    dam = random.randint( 30, 120 )
    if ( saves_spell( level, victim, DAM_PIERCE) )
        dam /= 2
    damage( ch, victim, dam, sn, DAM_PIERCE ,True)
    return
}

