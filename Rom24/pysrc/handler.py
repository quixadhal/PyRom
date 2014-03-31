
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
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                        *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""

from merc import *

def check_immune(ch,dam_type):
    immune = -1
    defence = IS_NORMAL

    if dam_type is DAM_NONE:
        return immune

    if dam_type <= 3:
        if IS_SET(ch.imm_flags,IMM_WEAPON):
            defence = IS_IMMUNE
        elif IS_SET(ch.res_flags,RES_WEAPON):
            defence = IS_RESISTANT
        elif IS_SET(ch.vuln_flags,VULN_WEAPON):
            defence = IS_VULNERABLE
    else: # magical attack */
        if IS_SET(ch.imm_flags,IMM_MAGIC):
            defence = IS_IMMUNE
        elif IS_SET(ch.res_flags,RES_MAGIC):
            defence = IS_RESISTANT
        elif IS_SET(ch.vuln_flags,VULN_MAGIC):
            defence = IS_VULNERABLE

    bit = {  DAM_BASH:IMM_BASH,
             DAM_PIERCE:IMM_PIERCE,
             DAM_SLASH:IMM_SLASH,
             DAM_FIRE:IMM_FIRE,
             DAM_COLD:IMM_COLD,
             DAM_LIGHTNING:IMM_LIGHTNING,
             DAM_ACID:IMM_ACID,
             DAM_POISON:IMM_POISON,
             DAM_NEGATIVE:IMM_NEGATIVE,
             DAM_HOLY:IMM_HOLY,
             DAM_ENERGY:IMM_ENERGY,
             DAM_MENTAL:IMM_MENTAL,
             DAM_DISEASE:IMM_DISEASE,
             DAM_DROWNING:IMM_DROWNING,
             DAM_LIGHT:IMM_LIGHT,
             DAM_CHARM:IMM_CHARM,
             DAM_SOUND:IMM_SOUND }
    if dam_type not in bit:
        return defence
    bit = bit[dam_type]

    if IS_SET(ch.imm_flags,bit):
        immune = IS_IMMUNE
    elif IS_SET(ch.res_flags,bit) and immune is not IS_IMMUNE:
        immune = IS_RESISTANT
    elif IS_SET(ch.vuln_flags,bit):
        if immune == IS_IMMUNE:
            immune = IS_RESISTANT
        elif immune == IS_RESISTANT:
            immune = IS_NORMAL
    else:
        immune = IS_VULNERABLE

    if immune == -1:
        return defence
    else:
        return immune    



#* Retrieve a character's trusted level for permission checking.
def get_trust( ch ):
    if ch.desc and ch.desc.original:
        ch = ch.desc.original

    if ch.trust:
        return ch.trust

    if IS_NPC(ch) and ch.level >= LEVEL_HERO:
        return LEVEL_HERO - 1
    else:
        return ch.level


# used to de-screw characters */
def reset_char(ch):
    if IS_NPC(ch):
        return

    if ch.pcdata.perm_hit == 0 \
    or  ch.pcdata.perm_mana == 0 \
    or  ch.pcdata.perm_move == 0 \
    or  ch.pcdata.last_level == 0:
        # do a FULL reset */
        for loc in range(MAX_WEAR):
            obj = get_eq_char(ch,loc)
            if not obj:
                continue
            affected = obj.affected
            if not obj.enchanted:
                affected.extend(obj.pIndexData.affected)
            for af in affected:
                mod = af.modifier
                if af.location == APPLY_SEX:
                    ch.sex -= mod
                    if ch.sex < 0 or ch.sex > 2:
                        ch.sex = 0 if IS_NPC(ch) else ch.pcdata.true_sex
                elif af.location == APPLY_MANA:    
                    ch.max_mana -= mod     
                elif af.location == APPLY_HIT: 
                    ch.max_hit -= mod     
                elif af.location == APPLY_MOVE:    
                    ch.max_move -= mod
        # now reset the permanent stats */
        ch.pcdata.perm_hit    = ch.max_hit
        ch.pcdata.perm_mana   = ch.max_mana
        ch.pcdata.perm_move   = ch.max_move
        ch.pcdata.last_level  = ch.played/3600
        if ch.pcdata.true_sex < 0 or ch.pcdata.true_sex > 2:
            if ch.sex > 0 and ch.sex < 3:
                ch.pcdata.true_sex = ch.sex
            else:
                ch.pcdata.true_sex = 0

    # now restore the character to his/her true condition */
    for stat in range(MAX_STATS):
        ch.mod_stat[stat] = 0

    if ch.pcdata.true_sex < 0 or ch.pcdata.true_sex > 2:
        ch.pcdata.true_sex = 0 
    ch.sex     = ch.pcdata.true_sex
    ch.max_hit     = ch.pcdata.perm_hit
    ch.max_mana    = ch.pcdata.perm_mana
    ch.max_move    = ch.pcdata.perm_move
   
    for i in range(4):
        ch.armor[i] = 100

    ch.hitroll = 0
    ch.damroll = 0
    ch.saving_throw = 0

    # now start adding back the effects */
    for loc in range(MAX_WEAR):
        obj = get_eq_char(ch,loc)
        if not obj:
            continue
        for i in range(4):
            ch.armor[i] -= apply_ac( obj, loc, i )
        affected = obj.affected
        if not obj.enchanted:
            affected.extend(obj.pIndexData.affected)

        for af in affected:
            mod = af.modifier
            if af.location == APPLY_STR: ch.mod_stat[STAT_STR] += mod
            elif af.location == APPLY_DEX: ch.mod_stat[STAT_DEX] += mod
            elif af.location == APPLY_INT: ch.mod_stat[STAT_INT] += mod
            elif af.location == APPLY_WIS: ch.mod_stat[STAT_WIS] += mod
            elif af.location == APPLY_CON: ch.mod_stat[STAT_CON] += mod
            elif af.location == APPLY_SEX: ch.sex += mod
            elif af.location == APPLY_MANA: ch.max_mana += mod
            elif af.location == APPLY_HIT: ch.max_hit += mod
            elif af.location == APPLY_MOVE: ch.max_move += mod
            elif af.location == APPLY_AC: ch.armor = [ i+mod for i in ch.armor]
            elif af.location == APPLY_HITROLL: ch.hitroll     += mod
            elif af.location == APPLY_DAMROLL: ch.damroll     += mod
            elif af.location == APPLY_SAVES: ch.saving_throw += mod
            elif af.location == APPLY_SAVING_ROD: ch.saving_throw += mod
            elif af.location == APPLY_SAVING_PETRI: ch.saving_throw += mod
            elif af.location == APPLY_SAVING_BREATH: ch.saving_throw += mod
            elif af.location == APPLY_SAVING_SPELL: ch.saving_throw += mod

   
    # now add back spell effects */
    for af in ch.affected:
        mod = af.modifier
        if af.location == APPLY_STR: ch.mod_stat[STAT_STR] += mod
        elif af.location == APPLY_DEX: ch.mod_stat[STAT_DEX] += mod
        elif af.location == APPLY_INT: ch.mod_stat[STAT_INT] += mod
        elif af.location == APPLY_WIS: ch.mod_stat[STAT_WIS] += mod
        elif af.location == APPLY_CON: ch.mod_stat[STAT_CON] += mod
        elif af.location == APPLY_SEX: ch.sex += mod
        elif af.location == APPLY_MANA: ch.max_mana += mod
        elif af.location == APPLY_HIT: ch.max_hit += mod
        elif af.location == APPLY_MOVE: ch.max_move += mod
        elif af.location == APPLY_AC: ch.armor = [ i+mod for i in ch.armor]
        elif af.location == APPLY_HITROLL: ch.hitroll     += mod
        elif af.location == APPLY_DAMROLL: ch.damroll     += mod
        elif af.location == APPLY_SAVES: ch.saving_throw += mod
        elif af.location == APPLY_SAVING_ROD: ch.saving_throw += mod
        elif af.location == APPLY_SAVING_PETRI: ch.saving_throw += mod
        elif af.location == APPLY_SAVING_BREATH: ch.saving_throw += mod
        elif af.location == APPLY_SAVING_SPELL: ch.saving_throw += mod
    # make sure sex is RIGHT!!!! */
    if ch.sex < 0 or ch.sex > 2:
        ch.sex = ch.pcdata.true_sex


# * Find the ac value of an obj, including position effect.
def apply_ac( obj, iWear, type ):
    if obj.item_type != ITEM_ARMOR:
        return 0

    multi = { WEAR_BODY:3, WEAR_HEAD:2, WEAR_LEGS:2, WEAR_ABOUT:2 }
    if iWear in multi:
        return multi[iWear] * obj.value[type]
    else:
        return obj.value[type]

# Find a piece of eq on a character.
 
def get_eq_char( ch, iWear ):
    if not ch:
        return None
    objs = [ obj for obj in ch.carrying if obj.wear_loc == iWear ]
    if not objs:
        return None
    return objs[0]


# * Give an obj to a char.
def obj_to_char( obj, ch ):
    ch.carrying.append(obj)
    obj.carried_by  = ch
    obj.in_room     = None
    obj.in_obj      = None
    ch.carry_number    += get_obj_number( obj )
    ch.carry_weight    += get_obj_weight( obj )



# * Return # of objects which an object counts as.
# * Thanks to Tony Chamberlain for the correct recursive code here.

def get_obj_number( obj ):
    noweight = [ITEM_CONTAINER, ITEM_MONEY, ITEM_GEM, ITEM_JEWELRY]
    if obj.item_type in noweight:
        number = 0
    else:
        number = 1
 
    for o in obj.contains:
        number += get_obj_number( o )
 
    return number

# * Return weight of an object, including weight of contents.

def get_obj_weight( obj ):
    weight = obj.weight
    for tobj in obj.contains:
        weight += get_obj_weight( tobj ) * WEIGHT_MULT(obj) / 100

    return weight

def get_true_weight(obj):
    weight = obj.weight
    for o in obj.contains:
        weight += get_obj_weight( o )
 
    return weight



# * Equip a char with an obj.
def equip_char( ch, obj, iWear ):
    if get_eq_char( ch, iWear ):
        print "Equip_char: already equipped (%d)." % iWear
        return
    
    if ( IS_OBJ_STAT(obj, ITEM_ANTI_EVIL) and IS_EVIL(ch) ) \
    or ( IS_OBJ_STAT(obj, ITEM_ANTI_GOOD) and IS_GOOD(ch) ) \
    or ( IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) and IS_NEUTRAL(ch) ):
        # Thanks to Morgenes for the bug fix here!
        act( "You are zapped by $p and drop it.", ch, obj, None, TO_CHAR )
        act( "$n is zapped by $p and drops it.",  ch, obj, None, TO_ROOM )
        obj_from_char( obj )
        obj_to_room( obj, ch.in_room )
        return

    for i in range(4):
        ch.armor[i]        -= apply_ac( obj, iWear,i )
    obj.wear_loc    = iWear

    if not obj.enchanted:
        for paf in obj.pIndexData.affected:
            if paf.location != APPLY_SPELL_AFFECT:
                affect_modify( ch, paf, True )
    
    for paf in obj.affected:
        if paf.location == APPLY_SPELL_AFFECT:
            affect_to_char ( ch, paf )
        else:
            affect_modify( ch, paf, True )

    if obj.item_type == ITEM_LIGHT and   obj.value[2] != 0 and   ch.in_room != None:
        ch.in_room.light += 1
    return

# * Unequip a char with an obj.
def unequip_char( ch, obj ):
    if obj.wear_loc == WEAR_NONE:
        print "Unequip_char: already unequipped."
        return

    for i in range(4):
        ch.armor[i]    += apply_ac( obj, obj.wear_loc,i )
    obj.wear_loc    = -1

    if not obj.enchanted:
        for paf in obj.pIndexData.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                for lpaf in ch.affected[:]:
                    if (lpaf.type == paf.type) and (lpaf.level == paf.level) and (lpaf.location == APPLY_SPELL_AFFECT):
                        affect_remove( ch, lpaf )
                        break
            else:
                affect_modify( ch, paf, False )
                affect_check(ch,paf.where,paf.bitvector)

    for paf in obj.affected:
        if paf.location == APPLY_SPELL_AFFECT:
            print "Norm-Apply: %d" % paf.location
            for lpaf in ch.affected:
                if (lpaf.type == paf.type) and (lpaf.level == paf.level) and (lpaf.location == APPLY_SPELL_AFFECT):
                    print ( "location = %d" % lpaf.location )
                    print ( "type = %d" % lpaf.type )
                    affect_remove( ch, lpaf )
                    break
        else:
            affect_modify( ch, paf, False )
            affect_check(ch,paf.where,paf.bitvector) 
        
    if obj.item_type == ITEM_LIGHT and   obj.value[2] != 0 and   ch.in_room != None and   ch.in_room.light > 0:
        --ch.in_room.light
    return

# * Move a char into a room.
def char_to_room( ch, pRoomIndex ):
    if not pRoomIndex:
        print "Char_to_room: NULL."
        room = room_index_hash[ROOM_VNUM_TEMPLE]
        char_to_room(ch,room)
        return

    ch.in_room = pRoomIndex
    pRoomIndex.people.append(ch)

    if not IS_NPC(ch):
        if ch.in_room.area.empty:
            ch.in_room.area.empty = False
            ch.in_room.area.age = 0
        
        ch.in_room.area.nplayer += 1

    obj = get_eq_char(ch, WEAR_LIGHT)

    if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
        ch.in_room.light += 1
    
    if IS_AFFECTED(ch,AFF_PLAGUE):
        af = [af for af in ch.affected if af.type == 'plague']
        if not af:
            REMOVE_BIT(ch.affected_by,AFF_PLAGUE)
            return
        af = af[0]
        
        if af.level == 1:
            return
        plague = AFFECT_DATA()
        plague.where        = TO_AFFECTS
        plague.type         = gsn_plague
        plague.level        = af.level - 1 
        plague.duration     = random.randint(1,2 * plague.level)
        plague.location     = APPLY_STR
        plague.modifier     = -5
        plague.bitvector    = AFF_PLAGUE
        
        for vch in ch.in_room.people[:]:
            if not saves_spell(plague.level - 2,vch,DAM_DISEASE) and not IS_IMMORTAL(vch) and not IS_AFFECTED(vch,AFF_PLAGUE) and random.randint(0,5) == 0:
                send_to_char("You feel hot and feverish.\n\r",vch)
                act("$n shivers and looks very ill.",vch,None,None,TO_ROOM)
                affect_join(vch,plague)
    return


# True if room is dark.
def room_is_dark( pRoomIndex ):
    if pRoomIndex.light > 0:
        return False

    if IS_SET(pRoomIndex.room_flags, ROOM_DARK):
        return True

    if pRoomIndex.sector_type == SECT_INSIDE or pRoomIndex.sector_type == SECT_CITY:
        return False

    if weather_info.sunlight == SUN_SET or weather_info.sunlight == SUN_DARK:
        return True

    return False
