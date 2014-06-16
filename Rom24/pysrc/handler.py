
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
import time
from merc import *
import const
import fight

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
        print ("Equip_char: already equipped (%d)." % iWear)
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
        print ("Unequip_char: already unequipped.")
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
            print ("Norm-Apply: %d" % paf.location)
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

# enchanted stuff for eq */
def affect_enchant(obj):
    # okay, move all the old flags into new vectors if we have to */
    if not obj.enchanted:
        obj.enchanted = True
        for paf in obj.pIndexData.affected:
            af_new = AFFECT_DATA()
            obj.affected.append(af_new)

            af_new.where   = paf.where
            af_new.type        = max(0,paf.type)
            af_new.level       = paf.level
            af_new.duration    = paf.duration
            af_new.location    = paf.location
            af_new.modifier    = paf.modifier
            af_new.bitvector   = paf.bitvector
depth = 0         
#
# * Apply or remove an affect to a character.
def affect_modify( ch, paf, fAdd ):
    mod = paf.modifier
    if fAdd:
        if paf.where == TO_AFFECTS:
            SET_BIT(ch.affected_by, paf.bitvector)
        elif paf.where == TO_IMMUNE:
            SET_BIT(ch.imm_flags,paf.bitvector)
        elif paf.where == TO_RESIST:
            SET_BIT(ch.res_flags,paf.bitvector)
        elif paf.where == TO_VULN:
            SET_BIT(ch.vuln_flags,paf.bitvector)
    else:

        if paf.where == TO_AFFECTS:
            REMOVE_BIT(ch.affected_by, paf.bitvector)
        elif paf.where == TO_IMMUNE:
            REMOVE_BIT(ch.imm_flags,paf.bitvector)
        elif paf.where == TO_RESIST:
            REMOVE_BIT(ch.res_flags,paf.bitvector)
        elif paf.where == TO_VULN:
            REMOVE_BIT(ch.vuln_flags,paf.bitvector)
        mod = 0 - mod

    
    if paf.location == APPLY_NONE: pass
    elif paf.location == APPLY_STR: ch.mod_stat[STAT_STR] += mod
    elif paf.location == APPLY_DEX: ch.mod_stat[STAT_DEX] += mod
    elif paf.location == APPLY_INT: ch.mod_stat[STAT_INT] += mod
    elif paf.location == APPLY_WIS: ch.mod_stat[STAT_WIS] += mod
    elif paf.location == APPLY_CON: ch.mod_stat[STAT_CON] += mod
    elif paf.location == APPLY_SEX: ch.sex += mod
    elif paf.location == APPLY_CLASS: pass
    elif paf.location == APPLY_LEVEL: pass
    elif paf.location == APPLY_AGE: pass
    elif paf.location == APPLY_HEIGHT: pass
    elif paf.location == APPLY_WEIGHT: pass
    elif paf.location == APPLY_MANA: ch.max_mana += mod
    elif paf.location == APPLY_HIT: ch.max_hit += mod
    elif paf.location == APPLY_MOVE: ch.max_move += mod
    elif paf.location == APPLY_GOLD: pass
    elif paf.location == APPLY_EXP: pass
    elif paf.location == APPLY_AC:
        for i in range(4):
            ch.armor[i] += mod
    elif paf.location == APPLY_HITROLL: ch.hitroll += mod
    elif paf.location == APPLY_DAMROLL: ch.damroll += mod
    elif paf.location == APPLY_SAVES: ch.saving_throw += mod
    elif paf.location == APPLY_SAVING_ROD: ch.saving_throw += mod
    elif paf.location == APPLY_SAVING_PETRI: ch.saving_throw += mod
    elif paf.location == APPLY_SAVING_BREATH: ch.saving_throw += mod
    elif paf.location == APPLY_SAVING_SPELL: ch.saving_throw += mod
    elif paf.location == APPLY_SPELL_AFFECT: pass
    else:
        print ("Affect_modify: unknown location %d." % paf.location)
        return
    #
    # * Check for weapon wielding.
    # * Guard against recursion (for weapons with affects).
    wield = get_eq_char(ch, WEAR_WIELD)
    if not IS_NPC(ch) and wield and get_obj_weight(wield) > (const.str_app[get_curr_stat(ch,STAT_STR)].wield*10):
        global depth

        if depth == 0:
            depth += 1
            act( "You drop $p.", ch, wield, None, TO_CHAR )
            act( "$n drops $p.", ch, wield, None, TO_ROOM )
            obj_from_char( wield )
            obj_to_room( wield, ch.in_room )
            depth -= 1
    return

# find an effect in an affect list */
def affect_find(paf, sn):
    return [paf_find for paf_find in paf if paf_find.type == sn][:1]

# fix object affects when removing one */
def affect_check(ch,where,vector):
    if where == TO_OBJECT or where == TO_WEAPON or vector == 0:
        return

    for paf in ch.affected:
        if paf.where == where and paf.bitvector == vector:
            if where == TO_AFFECTS:
                SET_BIT(ch.affected_by,vector)
            elif where == TO_IMMUNE:
                SET_BIT(ch.imm_flags,vector)   
            elif where == TO_RESIST:
                SET_BIT(ch.res_flags,vector)
            elif where == TO_VULN:
                SET_BIT(ch.vuln_flags,vector)
            return

    for obj in ch.carrying:
        if obj.wear_loc == -1:
            continue

        for paf in obj.affected:
            if paf.where == where and paf.bitvector == vector:
                if where == TO_AFFECTS:
                    SET_BIT(ch.affected_by,vector)
                elif where == TO_IMMUNE:
                    SET_BIT(ch.imm_flags,vector)   
                elif where == TO_RESIST:
                    SET_BIT(ch.res_flags,vector)
                elif where == TO_VULN:
                    SET_BIT(ch.vuln_flags,vector)
                return


        if obj.enchanted:
            continue

        for paf in obj.pIndexData.affected:
            if paf.where == where and paf.bitvector == vector:
                if where == TO_AFFECTS:
                    SET_BIT(ch.affected_by,vector)
                elif where == TO_IMMUNE:
                    SET_BIT(ch.imm_flags,vector)   
                elif where == TO_RESIST:
                    SET_BIT(ch.res_flags,vector)
                elif where == TO_VULN:
                    SET_BIT(ch.vuln_flags,vector)
                return
                

#
# * Give an affect to a char.
def affect_to_char( ch, paf ):
    paf_new = AFFECT_DATA()
    ch.affected.append(paf_new)
    affect_modify( ch, paf_new, True )
    return

# give an affect to an object */
def affect_to_obj( obj, paf):
    paf_new = AFFECT_DATA()
    obj.affected.append(paf_new)
    # apply any affect vectors to the object's extra_flags */
    if paf.bitvector:
        if paf.where == TO_OBJECT:
            SET_BIT(obj.extra_flags,paf.bitvector)
        elif paf.where == TO_WEAPON:
            if obj.item_type == ITEM_WEAPON:
                SET_BIT(obj.value[4],paf.bitvector)

# * Remove an affect from a char.
def affect_remove( ch, paf ):
    if not ch.affected:
        print ("BUG: Affect_remove: no affect.")
        return

    affect_modify( ch, paf, False )
    where = paf.where
    vector = paf.bitvector
    
    if paf not in ch.affected:
        print ("Affect_remove: cannot find paf.")
        return
    ch.affected.remove(paf)
    del paf
    affect_check(ch,where,vector)
    return

def affect_remove_obj(obj, paf):
    if not obj.affected:
        print ("BUG: Affect_remove_object: no affect.")
        return

    if obj.carried_by != None and obj.wear_loc != -1:
        affect_modify( obj.carried_by, paf, False )

    where = paf.where
    vector = paf.bitvector

    # remove flags from the object if needed */
    if paf.bitvector:
        if paf.where == TO_OBJECT:
            REMOVE_BIT(obj.extra_flags,paf.bitvector)
        elif paf.where == TO_WEAPON:
            if obj.item_type == ITEM_WEAPON:
                REMOVE_BIT(obj.value[4],paf.bitvector)

    if paf not in obj.affected:
        print ("BUG: Affect_remove_object: cannot find paf.")
        return
    obj.affected.remove(paf)
    del paf
    if obj.carried_by != None and obj.wear_loc != -1:
        affect_check(obj.carried_by,where,vector)
    return
#
# * Strip all affects of a given sn.
def affect_strip( ch,  sn ):
    [affect_remove(ch, paf) for paf in ch.affected[:] if paf.type == sn]
    return
#
# * Add or enhance an affect.
def affect_join( ch, paf ):
    found = False
    for paf_old in ch.affected:
        if paf_old.type == paf.type:
            paf.level = (paf.level + paf_old.level) / 2
            paf.duration += paf_old.duration
            paf.modifier += paf_old.modifier
            affect_remove( ch, paf_old )
            break
    
    affect_to_char( ch, paf )
    return

# * Move a char out of a room.
def char_from_room( ch ):
    if not ch.in_room:
        print ("BUG: Char_from_room: None.")
        return

    if not IS_NPC(ch):
        ch.in_room.area.nplayer -= 1
    obj = get_eq_char(ch, WEAR_LIGHT)
    if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and ch.in_room.light > 0:
        ch.in_room.light -= 1


    if ch not in ch.in_room.people:
        print ("BUG: Char_from_room: ch not found.")
        return
    ch.in_room.people.remove(ch)
    ch.in_room      = None
    ch.on       = None  # sanity check! */
    return

# * Move a char into a room.
def char_to_room( ch, pRoomIndex ):
    if not pRoomIndex:
        print ("Char_to_room: None.")
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
        plague.type         = "plague"
        plague.level        = af.level - 1 
        plague.duration     = random.randint(1,2 * plague.level)
        plague.location     = APPLY_STR
        plague.modifier     = -5
        plague.bitvector    = AFF_PLAGUE
        
        for vch in ch.in_room.people[:]:
            if not saves_spell(plague.level - 2,vch,DAM_DISEASE) and not IS_IMMORTAL(vch) and not IS_AFFECTED(vch,AFF_PLAGUE) and random.randint(0,5) == 0:
                vch.send("You feel hot and feverish.\n\r")
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


#
# * Unequip a char with an obj.
def unequip_char( ch, obj ):
    if obj.wear_loc == WEAR_NONE:
        print ("Unequip_char: already unequipped.")
        return

    for i in range(4):
        ch.armor[i] += apply_ac( obj, obj.wear_loc,i )
    obj.wear_loc = -1

    if not obj.enchanted:
        for paf in obj.pIndexData.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                for lpaf in ch.affected[:]:
                    if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                        affect_remove( ch, lpaf )
                        break
            else:
                affect_modify( ch, paf, False )
                affect_check(ch,paf.where,paf.bitvector)

    for paf in obj.affected:
        if paf.location == APPLY_SPELL_AFFECT:
            print ("Bug: Norm-Apply")
            for lpaf in ch.affected:
                if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                    print ("bug: location = %d" % lpaf.location)
                    print ("bug: type = %d" % lpaf.type)
                    affect_remove( ch, lpaf )
                    break
        else:
            affect_modify( ch, paf, False )
            affect_check(ch,paf.where,paf.bitvector) 

    if obj.item_type == ITEM_LIGHT \
    and   obj.value[2] != 0 \
    and   ch.in_room \
    and   ch.in_room.light > 0:
        ch.in_room.light -= 1
    return
#
# * Count occurrences of an obj in a list.
def count_obj_list( pObjIndex, list ):
    return len([obj for obj in list if obj.pIndexData == pObjIndex])
#
# * Move an obj out of a room.
# */
def obj_from_room( obj ):
    if not obj.in_room:
        print ("Bug: obj_from_room: None.")
        return
    in_room = obj.in_room
    for ch in in_room.people:
        if ch.on == obj:
            ch.on = None

    if obj not in in_room.contents:
        print ("Bug: Obj_from_room: obj not found.")
        return

    obj.in_room      = None
    in_room.contents.remove(obj)
    return


#
# * Move an obj into a room.
# */
def obj_to_room( obj, pRoomIndex ):
    pRoomIndex.contents.append(obj)
    obj.in_room        = pRoomIndex
    obj.carried_by     = None
    obj.in_obj         = None
    return

#
# * Move an object into an object.
def obj_to_obj( obj, obj_to ):
    obj_to.contains.append(obj)
    obj.in_obj         = obj_to
    obj.in_room        = None
    obj.carried_by     = None
    if obj_to.pIndexData.vnum == OBJ_VNUM_PIT:
        obj.cost = 0 

    while obj_to:
        if obj_to.carried_by:
            obj_to.carried_by.carry_number += get_obj_number( obj )
            obj_to.carried_by.carry_weight += get_obj_weight( obj ) * WEIGHT_MULT(obj_to) / 100
        obj_to = obj_to.in_obj            
    return

#
# * Move an object out of an object.
def obj_from_obj( obj ):
    if not obj.in_obj:
        print ("Bug: Obj_from_obj: null obj_from.")
        return
    obj_from = obj.in_obj

    if obj not in obj_from.contents:
        print ("BUG: Obj_from_obj: obj not found.")
        return
    obj_from.contents.remove(obj)
    obj.in_obj       = None

    while obj_from:
        if obj_from.carried_by:
            obj_from.carried_by.carry_number -= get_obj_number( obj )
            obj_from.carried_by.carry_weight -= get_obj_weight( obj ) * WEIGHT_MULT(obj_from) / 100
    return

#
# * Extract an obj from the world.
def extract_obj( obj ):
    if obj.in_room:
        obj_from_room( obj )
    elif obj.carried_by:
        obj_from_char( obj )
    elif obj.in_obj:
        obj_from_obj( obj )

    for obj_content in obj.contains[:]:
        extract_obj( obj_content )

    if obj not in object_list:
        print ("Extract_obj: obj %d not found." % obj.pIndexData.vnum)
        return
    object_list.remove(obj)
    del obj

#
# * Extract a char from the world.
def extract_char( ch, fPull ):
    # doesn't seem to be necessary
    #if not ch.in_room:
    #    print "Extract_char: None."
    #    return
 
#    nuke_pets(ch)
    ch.pet = None # just in case */

    #if fPull:
    #    die_follower( ch )
    fight.stop_fighting( ch, True )

    for obj in ch.carrying[:]:
        extract_obj( obj )
    
    if ch.in_room:
        char_from_room( ch )

    # Death room is set in the clan tabe now */
    if not fPull:
        char_to_room(ch,room_index_hash[ch.clan.hall])
        return

    if ch.desc and ch.desc.original:
        ch.do_return("")
        ch.desc = None

    for wch in player_list:
        if wch.reply == ch:
            wch.reply = None

    if ch not in char_list:
        print ("Extract_char: char not found.")
        return
    char_list.remove(ch)
    player_list.remove(ch)

    if ch.desc:
        ch.desc.character = None
    del ch
    return
#
# * Find a char in the room.
# */
def get_char_room( ch, argument ):
    number, arg = number_argument( argument )
    count  = 0
    arg = arg.lower()
    if arg == "self":
        return ch
    for rch in ch.in_room.people:
        if not can_see( ch, rch ):
            continue
        if not IS_NPC(rch) and not rch.name.lower().startswith(arg):
            continue
        if IS_NPC(rch) and arg not in rch.name:
            continue
        count += 1
        if count == number:
            return rch
    return None

#
# * Find a char in the world.
def get_char_world( ch, argument ):
    wch = get_char_room(ch,argument)
    if wch:
        return wch

    number, arg = number_argument( argument )
    count  = 0
    for wch in char_list:
        if wch.in_room == None or not can_see( ch, wch ):
            continue
        if not IS_NPC(wch) and not wch.name.lower().startswith(arg):
            continue
        if IS_NPC(wch) and arg not in wch.name:
            continue
        count += 1
        if count == number:
            return wch
    return None

#
# * Find some object with a given index data.
# * Used by area-reset 'P' command.
def get_obj_type( pObjIndex ):
    search = [obj for obj in object_list if obj.pIndexData == pObjIndex][:1]
    return search[0] if search else None

# * Find an obj in a list.
def get_obj_list( ch, argument, list ):
    number, arg = number_argument( argument )
    count  = 0
    for obj in list:
        if can_see_obj( ch, obj ) and arg.lower() in  obj.name.lower():
            count += 1
            if count == number:
                return obj
    return None
#
# * Find an obj in player's inventory.
def get_obj_carry( ch, argument, viewer ):
    number, arg = number_argument( argument )
    count  = 0
    for obj in ch.carrying:
        if obj.wear_loc == WEAR_NONE and can_see_obj( viewer, obj ) and arg.lower() in obj.name.lower():
            count += 1
            if count == number:
                return obj
    return None

# * Find an obj in player's equipment.
def get_obj_wear( ch, argument ):
    number, arg = number_argument(argument)
    count = 0
    for obj in ch.carrying:
        if obj.wear_loc != WEAR_NONE and can_see_obj(ch, obj) and arg.lower() in obj.name.lower():
            count += 1   
            if count == number:
                return obj
    return None

#
# * Find an obj in the room or in inventory.
def get_obj_here( ch, argument ):
    obj = get_obj_list(ch, argument, ch.in_room.contents)
    
    if obj:
        return obj
    obj = get_obj_carry( ch, argument, ch )
    if obj:
        return obj
    obj = get_obj_wear( ch, argument )
    if obj:
        return obj
    return None

#
# * Find an obj in the world.
def get_obj_world( ch, argument ):
    obj = get_obj_here( ch, argument )
    if obj:
        return obj

    number, arg = number_argument( argument )
    count = 0
    arg = arg.lower()
    for obj in object_list:
        if can_see_obj( ch, obj ) and arg in obj.name.lower():
            count += 1
        if count == number:
           return obj
    return None
# deduct cost from a character */
def deduct_cost(ch, cost):
    silver = min(ch.silver,cost) 

    if silver < cost:
        gold = ((cost - silver + 99) / 100)
        silver = cost - 100 * gold
    ch.gold -= gold
    ch.silver -= silver

    if ch.gold < 0:
        print ("Bug: deduct costs: gold %d < 0" % ch.gold)
        ch.gold = 0
    if ch.silver < 0:
        print ("BUG: deduct costs: silver %d < 0" % ch.silver)
        ch.silver = 0
#
# * Create a 'money' obj.
def create_money( gold, silver ):
    if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
        print ("BUG: Create_money: zero or negative money. %d " % min(gold,silver))
        gold = max(1,gold)
        silver = max(1,silver)

    if gold == 0 and silver == 1:
        obj = create_object( obj_index_hash[OBJ_VNUM_SILVER_ONE], 0 )
    elif gold == 1 and silver == 0:
        obj = create_object( obj_index_hash[OBJ_VNUM_GOLD_ONE], 0 )
    elif silver == 0:
        obj = create_object( obj_index_hash[OBJ_VNUM_GOLD_SOME], 0 )
        obj.short_descr        += " %d" % gold
        obj.value[1]           = gold
        obj.cost               = gold
        obj.weight     = gold/5
    elif gold == 0:
        obj = create_object( obj_index_hash[OBJ_VNUM_SILVER_SOME], 0 )
        obj.short_descr        += " %d" % silver
        obj.value[0]           = silver
        obj.cost               = silver
        obj.weight     = silver/20
    else:
        obj = create_object( obj_index_hash[OBJ_VNUM_COINS], 0 )
        obj.short_descr    += " %d %d" % (gold, silver)
        obj.value[0]       = silver
        obj.value[1]       = gold
        obj.cost       = 100 * gold + silver
        obj.weight     = gold / 5 + silver / 20
    return obj


#
 #* Return # of objects which an object counts as.
# * Thanks to Tony Chamberlain for the correct recursive code here.
def get_obj_number( obj ):
    if obj.item_type == ITEM_CONTAINER or obj.item_type == ITEM_MONEY \
    or  obj.item_type == ITEM_GEM or obj.item_type == ITEM_JEWELRY:
        number = 0
    else:
        number = 1
    list = obj.contains[:]
    counted = [obj]
    for o in list:
        number += 1
        if o in counted:
            print ("BUG: Objects contain eachother. %s(%d) - %s(%d)" % (obj.short_descr, obj.pIndexData.vnum, o.short_descr, o.pIndexData.vnum))
            break
        counted.append(o)
        list.extend(o.contains)
 
    return number
#
#* Return weight of an object, including weight of contents.
def get_obj_weight( obj ):
    weight = obj.weight
    list = obj.contains[:]
    counted = [obj]
    for tobj in list:
        if tobj in counted:
            print ("BUG: Objects contain eachother. %s(%d) - %s(%d)" % (obj.short_descr, obj.pIndexData.vnum, tobj.short_descr, tobj.pIndexData.vnum))
            break
        counted.append(tobj)

        weight += tobj.weight * WEIGHT_MULT(obj) / 100
        list.extend(tobj.contains)
    return weight

def get_true_weight(obj):
    weight = obj.weight
    for obj in obj.contains:
        weight += get_obj_weight( obj )
    return weight

def is_room_owner( ch, room):
    if not room.owner:
        return False

    return True if ch.name in room.owner else False
#
# * True if room is private.
def room_is_private( pRoomIndex ):
    if pRoomIndex.owner:
        return True

    count = len(pRoomIndex.people)

    if IS_SET(pRoomIndex.room_flags, ROOM_PRIVATE) and count >= 2:
        return True
    if IS_SET(pRoomIndex.room_flags, ROOM_SOLITARY) and count >= 1:
        return True
    if IS_SET(pRoomIndex.room_flags, ROOM_IMP_ONLY):
        return True
    return False

# visibility on a room -- for entering and exits */
def can_see_room( ch, pRoomIndex ):
    if IS_SET(pRoomIndex.room_flags, ROOM_IMP_ONLY) and  get_trust(ch) < MAX_LEVEL:
        return False
    if IS_SET(pRoomIndex.room_flags, ROOM_GODS_ONLY) and not IS_IMMORTAL(ch):
        return False
    if IS_SET(pRoomIndex.room_flags, ROOM_HEROES_ONLY) and not IS_IMMORTAL(ch):
        return False
    if IS_SET(pRoomIndex.room_flags,ROOM_NEWBIES_ONLY) and ch.level > 5 and not IS_IMMORTAL(ch):
        return False
    if not IS_IMMORTAL(ch) and pRoomIndex.clan and ch.clan != pRoomIndex.clan:
        return False
    return True
#
# * True if char can see victim.
def can_see( ch, victim ):
    # RT changed so that WIZ_INVIS has levels */
    if ch == victim:
        return True
    if get_trust(ch) < victim.invis_level:
        return False
    if get_trust(ch) < victim.incog_level and ch.in_room != victim.in_room:
        return False
    if ( not IS_NPC(ch) and IS_SET(ch.act, PLR_HOLYLIGHT) ) or (IS_NPC(ch) and IS_IMMORTAL(ch)):
        return True
    if IS_AFFECTED(ch, AFF_BLIND):
        return False
    if room_is_dark( ch.in_room ) and not IS_AFFECTED(ch, AFF_INFRARED):
        return False
    if IS_AFFECTED(victim, AFF_INVISIBLE) and not IS_AFFECTED(ch, AFF_DETECT_INVIS):
        return False
    # sneaking */

    if IS_AFFECTED(victim, AFF_SNEAK) and not IS_AFFECTED(ch,AFF_DETECT_HIDDEN) and victim.fighting == None:
        chance = get_skill(victim,"sneak")
        chance += get_curr_stat(victim,STAT_DEX) * 3/2
        chance -= get_curr_stat(ch,STAT_INT) * 2
        chance -= ch.level - victim.level * 3/2

        if random.randint(1,99) < chance:
            return False

    if IS_AFFECTED(victim, AFF_HIDE) and not IS_AFFECTED(ch, AFF_DETECT_HIDDEN) and victim.fighting == None:
        return False

    return True
# * True if char can see obj.
def can_see_obj( ch, obj ):
    if not IS_NPC(ch) and IS_SET(ch.act, PLR_HOLYLIGHT):
        return True
    if IS_SET(obj.extra_flags,ITEM_VIS_DEATH):
        return False
    if IS_AFFECTED( ch, AFF_BLIND ) and obj.item_type != ITEM_POTION:
        return False
    if obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
        return True
    if IS_SET(obj.extra_flags, ITEM_INVIS) and not IS_AFFECTED(ch, AFF_DETECT_INVIS):
        return False
    if IS_OBJ_STAT(obj,ITEM_GLOW):
        return True
    if room_is_dark( ch.in_room ) and not IS_AFFECTED(ch, AFF_DARK_VISION):
        return False
    return True

# * True if char can drop obj.
def can_drop_obj( ch, obj ):
    if not IS_SET(obj.extra_flags, ITEM_NODROP):
        return True
    if not IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
        return True
    return False
#
# * Return ascii name of an affect location.
def affect_loc_name( location ):
    if location == APPLY_NONE: return "none"
    if location == APPLY_STR: return "strength"
    if location == APPLY_DEX: return "dexterity"
    if location == APPLY_INT: return "intelligence"
    if location == APPLY_WIS: return "wisdom"
    if location == APPLY_CON: return "constitution"
    if location == APPLY_SEX: return "sex"
    if location == APPLY_CLASS: return "class"
    if location == APPLY_LEVEL: return "level"
    if location == APPLY_AGE: return "age"
    if location == APPLY_MANA: return "mana"
    if location == APPLY_HIT: return "hp"
    if location == APPLY_MOVE: return "moves"
    if location == APPLY_GOLD: return "gold"
    if location == APPLY_EXP: return "experience"
    if location == APPLY_AC: return "armor class"
    if location == APPLY_HITROLL: return "hit roll"
    if location == APPLY_DAMROLL: return "damage roll"
    if location == APPLY_SAVES: return "saves"
    if location == APPLY_SAVING_ROD: return "save vs rod"
    if location == APPLY_SAVING_PETRI: return "save vs petrification"
    if location == APPLY_SAVING_BREATH: return "save vs breath"
    if location == APPLY_SAVING_SPELL: return "save vs spell"
    if location == APPLY_SPELL_AFFECT: return "none"
    print ("Affect_location_name: unknown location %d." % location)
    return "(unknown)"

# * Return ascii name of an affect bit vector.
def affect_bit_name( vector ):
    buf = ""
    if vector & AFF_BLIND: buf += " blind"
    if vector & AFF_INVISIBLE: buf += " invisible"
    if vector & AFF_DETECT_EVIL: buf += " detect_evil"
    if vector & AFF_DETECT_GOOD: buf += " detect_good"
    if vector & AFF_DETECT_INVIS: buf += " detect_invis"
    if vector & AFF_DETECT_MAGIC: buf += " detect_magic"
    if vector & AFF_DETECT_HIDDEN: buf += " detect_hidden"
    if vector & AFF_SANCTUARY: buf += " sanctuary"
    if vector & AFF_FAERIE_FIRE: buf += " faerie_fire"
    if vector & AFF_INFRARED: buf += " infrared"
    if vector & AFF_CURSE: buf += " curse"
    if vector & AFF_POISON: buf += " poison"
    if vector & AFF_PROTECT_EVIL: buf += " prot_evil"
    if vector & AFF_PROTECT_GOOD: buf += " prot_good"
    if vector & AFF_SLEEP: buf += " sleep"
    if vector & AFF_SNEAK: buf += " sneak"
    if vector & AFF_HIDE: buf += " hide"
    if vector & AFF_CHARM: buf += " charm"
    if vector & AFF_FLYING: buf += " flying"
    if vector & AFF_PASS_DOOR: buf += " pass_door"
    if vector & AFF_BERSERK: buf += " berserk"
    if vector & AFF_CALM: buf += " calm"
    if vector & AFF_HASTE: buf += " haste"
    if vector & AFF_SLOW: buf += " slow"
    if vector & AFF_PLAGUE: buf += " plague"
    if vector & AFF_DARK_VISION: buf += " dark_vision"
    if not buf:
        return "none"
    return buf

#
# * Return ascii name of extra flags vector.
def extra_bit_name( extra_flags ):
    buf = ""
    if extra_flags & ITEM_GLOW: buf += " glow"
    if extra_flags & ITEM_HUM: buf += " hum"
    if extra_flags & ITEM_DARK: buf += " dark"
    if extra_flags & ITEM_LOCK: buf += " lock"
    if extra_flags & ITEM_EVIL: buf += " evil"
    if extra_flags & ITEM_INVIS: buf += " invis"
    if extra_flags & ITEM_MAGIC: buf += " magic"
    if extra_flags & ITEM_NODROP: buf += " nodrop"
    if extra_flags & ITEM_BLESS: buf += " bless"
    if extra_flags & ITEM_ANTI_GOOD: buf += " anti-good"
    if extra_flags & ITEM_ANTI_EVIL: buf += " anti-evil"
    if extra_flags & ITEM_ANTI_NEUTRAL: buf += " anti-neutral"
    if extra_flags & ITEM_NOREMOVE: buf += " noremove"
    if extra_flags & ITEM_INVENTORY: buf += " inventory"
    if extra_flags & ITEM_NOPURGE: buf += " nopurge"
    if extra_flags & ITEM_VIS_DEATH: buf += " vis_death"
    if extra_flags & ITEM_ROT_DEATH: buf += " rot_death"
    if extra_flags & ITEM_NOLOCATE: buf += " no_locate"
    if extra_flags & ITEM_SELL_EXTRACT: buf += " sell_extract"
    if extra_flags & ITEM_BURN_PROOF: buf += " burn_proof"
    if extra_flags & ITEM_NOUNCURSE: buf += " no_uncurse"
    return "none" if not buf else buf

# return ascii name of an act vector */
def act_bit_name( act_flags ):
    buf = ""

    if IS_SET(act_flags,ACT_IS_NPC): 
        buf += " npc"
        if act_flags & ACT_SENTINEL: buf += " sentinel"
        if act_flags & ACT_SCAVENGER: buf += " scavenger"
        if act_flags & ACT_AGGRESSIVE: buf += " aggressive"
        if act_flags & ACT_STAY_AREA: buf += " stay_area"
        if act_flags & ACT_WIMPY: buf += " wimpy"
        if act_flags & ACT_PET: buf += " pet"
        if act_flags & ACT_TRAIN: buf += " train"
        if act_flags & ACT_PRACTICE: buf += " practice"
        if act_flags & ACT_UNDEAD: buf += " undead"
        if act_flags & ACT_CLERIC: buf += " cleric"
        if act_flags & ACT_MAGE: buf += " mage"
        if act_flags & ACT_THIEF: buf += " thief"
        if act_flags & ACT_WARRIOR: buf += " warrior"
        if act_flags & ACT_NOALIGN: buf += " no_align"
        if act_flags & ACT_NOPURGE: buf += " no_purge"
        if act_flags & ACT_IS_HEALER: buf += " healer"
        if act_flags & ACT_IS_CHANGER: buf += " changer"
        if act_flags & ACT_GAIN: buf += " skill_train"
        if act_flags & ACT_UPDATE_ALWAYS: buf += " update_always"
    else:
        buf += " player"
        if act_flags & PLR_AUTOASSIST: buf += " autoassist"
        if act_flags & PLR_AUTOEXIT: buf += " autoexit"
        if act_flags & PLR_AUTOLOOT: buf += " autoloot"
        if act_flags & PLR_AUTOSAC: buf += " autosac"
        if act_flags & PLR_AUTOGOLD: buf += " autogold"
        if act_flags & PLR_AUTOSPLIT: buf += " autosplit"
        if act_flags & PLR_HOLYLIGHT: buf += " holy_light"
        if act_flags & PLR_CANLOOT: buf += " loot_corpse"
        if act_flags & PLR_NOSUMMON: buf += " no_summon"
        if act_flags & PLR_NOFOLLOW: buf += " no_follow"
        if act_flags & PLR_FREEZE: buf += " frozen"
        if act_flags & PLR_THIEF: buf += " thief"
        if act_flags & PLR_KILLER: buf += " killer"
    return "none" if not buf else buf

def comm_bit_name(comm_flags):
    buf = ""
    if comm_flags & COMM_QUIET: buf += " quiet"
    if comm_flags & COMM_DEAF: buf += " deaf"
    if comm_flags & COMM_NOWIZ: buf += " no_wiz"
    if comm_flags & COMM_NOAUCTION: buf += " no_auction"
    if comm_flags & COMM_NOGOSSIP: buf += " no_gossip"
    if comm_flags & COMM_NOQUESTION: buf += " no_question"
    if comm_flags & COMM_NOMUSIC: buf += " no_music"
    if comm_flags & COMM_NOQUOTE: buf += " no_quote"
    if comm_flags & COMM_COMPACT: buf += " compact"
    if comm_flags & COMM_BRIEF: buf += " brief"
    if comm_flags & COMM_PROMPT: buf += " prompt"
    if comm_flags & COMM_COMBINE: buf += " combine"
    if comm_flags & COMM_NOEMOTE: buf += " no_emote"
    if comm_flags & COMM_NOSHOUT: buf += " no_shout"
    if comm_flags & COMM_NOTELL: buf += " no_tell"
    if comm_flags & COMM_NOCHANNELS: buf += " no_channels"
    return "none" if not buf else buf

def imm_bit_name(imm_flags):
    buf = ""
    if imm_flags & IMM_SUMMON: buf += " summon"
    if imm_flags & IMM_CHARM: buf += " charm"
    if imm_flags & IMM_MAGIC: buf += " magic"
    if imm_flags & IMM_WEAPON: buf += " weapon"
    if imm_flags & IMM_BASH: buf += " blunt"
    if imm_flags & IMM_PIERCE: buf += " piercing"
    if imm_flags & IMM_SLASH: buf += " slashing"
    if imm_flags & IMM_FIRE: buf += " fire"
    if imm_flags & IMM_COLD: buf += " cold"
    if imm_flags & IMM_LIGHTNING: buf += " lightning"
    if imm_flags & IMM_ACID: buf += " acid"
    if imm_flags & IMM_POISON: buf += " poison"
    if imm_flags & IMM_NEGATIVE: buf += " negative"
    if imm_flags & IMM_HOLY: buf += " holy"
    if imm_flags & IMM_ENERGY: buf += " energy"
    if imm_flags & IMM_MENTAL: buf += " mental"
    if imm_flags & IMM_DISEASE: buf += " disease"
    if imm_flags & IMM_DROWNING: buf += " drowning"
    if imm_flags & IMM_LIGHT: buf += " light"
    if imm_flags & VULN_IRON: buf += " iron"
    if imm_flags & VULN_WOOD: buf += " wood"
    if imm_flags & VULN_SILVER: buf += " silver"
    return "none" if not buf else buf

def wear_bit_name(wear_flags):
    buf = ""
    if wear_flags & ITEM_TAKE: buf += " take"
    if wear_flags & ITEM_WEAR_FINGER: buf += " finger"
    if wear_flags & ITEM_WEAR_NECK: buf += " neck"
    if wear_flags & ITEM_WEAR_BODY: buf += " torso"
    if wear_flags & ITEM_WEAR_HEAD: buf += " head"
    if wear_flags & ITEM_WEAR_LEGS: buf += " legs"
    if wear_flags & ITEM_WEAR_FEET: buf += " feet"
    if wear_flags & ITEM_WEAR_HANDS: buf += " hands"
    if wear_flags & ITEM_WEAR_ARMS: buf += " arms"
    if wear_flags & ITEM_WEAR_SHIELD: buf += " shield"
    if wear_flags & ITEM_WEAR_ABOUT: buf += " body"
    if wear_flags & ITEM_WEAR_WAIST: buf += " waist"
    if wear_flags & ITEM_WEAR_WRIST: buf += " wrist"
    if wear_flags & ITEM_WIELD: buf += " wield"
    if wear_flags & ITEM_HOLD: buf += " hold"
    if wear_flags & ITEM_NO_SAC: buf += " nosac"
    if wear_flags & ITEM_WEAR_FLOAT: buf += " float"
    return "none" if not buf else buf

def form_bit_name(form_flags):
    buf[0] = ""
    if form_flags & FORM_POISON: buf += " poison"
    elif form_flags & FORM_EDIBLE: buf += " edible"
    if form_flags & FORM_MAGICAL: buf += " magical"
    if form_flags & FORM_INSTANT_DECAY: buf += " instant_rot"
    if form_flags & FORM_OTHER: buf += " other"
    if form_flags & FORM_ANIMAL: buf += " animal"
    if form_flags & FORM_SENTIENT: buf += " sentient"
    if form_flags & FORM_UNDEAD: buf += " undead"
    if form_flags & FORM_CONSTRUCT: buf += " construct"
    if form_flags & FORM_MIST: buf += " mist"
    if form_flags & FORM_INTANGIBLE: buf += " intangible"
    if form_flags & FORM_BIPED: buf += " biped"
    if form_flags & FORM_CENTAUR: buf += " centaur"
    if form_flags & FORM_INSECT: buf += " insect"
    if form_flags & FORM_SPIDER: buf += " spider"
    if form_flags & FORM_CRUSTACEAN: buf += " crustacean"
    if form_flags & FORM_WORM: buf += " worm"
    if form_flags & FORM_BLOB: buf += " blob"
    if form_flags & FORM_MAMMAL: buf += " mammal"
    if form_flags & FORM_BIRD: buf += " bird"
    if form_flags & FORM_REPTILE: buf += " reptile"
    if form_flags & FORM_SNAKE: buf += " snake"
    if form_flags & FORM_DRAGON: buf += " dragon"
    if form_flags & FORM_AMPHIBIAN: buf += " amphibian"
    if form_flags & FORM_FISH: buf += " fish"
    if form_flags & FORM_COLD_BLOOD: buf += " cold_blooded"
    return "none" if not buf else buf

def part_bit_name(part_flags):
    buf = ''
    if part_flags & PART_HEAD: buf += " head"
    if part_flags & PART_ARMS: buf += " arms"
    if part_flags & PART_LEGS: buf += " legs"
    if part_flags & PART_HEART: buf += " heart"
    if part_flags & PART_BRAINS: buf += " brains"
    if part_flags & PART_GUTS: buf += " guts"
    if part_flags & PART_HANDS: buf += " hands"
    if part_flags & PART_FEET: buf += " feet"
    if part_flags & PART_FINGERS: buf += " fingers"
    if part_flags & PART_EAR: buf += " ears"
    if part_flags & PART_EYE: buf += " eyes"
    if part_flags & PART_LONG_TONGUE: buf += " long_tongue"
    if part_flags & PART_EYESTALKS: buf += " eyestalks"
    if part_flags & PART_TENTACLES: buf += " tentacles"
    if part_flags & PART_FINS: buf += " fins"
    if part_flags & PART_WINGS: buf += " wings"
    if part_flags & PART_TAIL: buf += " tail"
    if part_flags & PART_CLAWS: buf += " claws"
    if part_flags & PART_FANGS: buf += " fangs"
    if part_flags & PART_HORNS: buf += " horns"
    if part_flags & PART_SCALES: buf += " scales"
    return "none" if not buf else buf

def weapon_bit_name(weapon_flags):
    buf = ''
    if weapon_flags & WEAPON_FLAMING: buf += " flaming"
    if weapon_flags & WEAPON_FROST: buf += " frost"
    if weapon_flags & WEAPON_VAMPIRIC: buf += " vampiric"
    if weapon_flags & WEAPON_SHARP: buf += " sharp"
    if weapon_flags & WEAPON_VORPAL: buf += " vorpal"
    if weapon_flags & WEAPON_TWO_HANDS: buf += " two-handed"
    if weapon_flags & WEAPON_SHOCKING: buf += " shocking"
    if weapon_flags & WEAPON_POISON: buf += " poison"
    return "none" if not buf else buf

def cont_bit_name(cont_flags):
    buf = ''
    if cont_flags & CONT_CLOSEABLE: buf += " closable"
    if cont_flags & CONT_PICKPROOF: buf += " pickproof"
    if cont_flags & CONT_CLOSED: buf += " closed"
    if cont_flags & CONT_LOCKED: buf += " locked"
    return "none" if not buf else buf

def off_bit_name(off_flags):
    buf = ''
    if off_flags & OFF_AREA_ATTACK: buf += " area attack"
    if off_flags & OFF_BACKSTAB: buf += " backstab"
    if off_flags & OFF_BASH: buf += " bash"
    if off_flags & OFF_BERSERK: buf += " berserk"
    if off_flags & OFF_DISARM: buf += " disarm"
    if off_flags & OFF_DODGE: buf += " dodge"
    if off_flags & OFF_FADE: buf += " fade"
    if off_flags & OFF_FAST: buf += " fast"
    if off_flags & OFF_KICK: buf += " kick"
    if off_flags & OFF_KICK_DIRT: buf += " kick_dirt"
    if off_flags & OFF_PARRY: buf += " parry"
    if off_flags & OFF_RESCUE: buf += " rescue"
    if off_flags & OFF_TAIL: buf += " tail"
    if off_flags & OFF_TRIP: buf += " trip"
    if off_flags & OFF_CRUSH: buf += " crush"
    if off_flags & ASSIST_ALL: buf += " assist_all"
    if off_flags & ASSIST_ALIGN: buf += " assist_align"
    if off_flags & ASSIST_RACE: buf += " assist_race"
    if off_flags & ASSIST_PLAYERS: buf += " assist_players"
    if off_flags & ASSIST_GUARD: buf += " assist_guard"
    if off_flags & ASSIST_VNUM: buf += " assist_vnum"
    return "none" if not buf else buf

# for returning skill information */
def get_skill(ch, sn):
    skill = 0
    if sn == -1: # shorthand for level based skills */
        skill = ch.level * 5 / 2
    elif sn not in const.skill_table:
        print ("BUG: Bad sn %s in get_skill." % sn)
        skill = 0
    elif not IS_NPC(ch):
        if ch.level < const.skill_table[sn].skill_level[ch.guild.name]:
            skill = 0
        else:
            skill = ch.pcdata.learned[sn]
    else: # mobiles */
        if const.skill_table[sn].spell_fun != spell_null:
            skill = 40 + 2 * ch.level;
        elif sn == 'sneak' or sn == 'hide':
            skill = ch.level * 2 + 20
        elif (sn == 'dodge' and IS_SET(ch.off_flags, OFF_DODGE)) \
        or (sn == 'parry' and IS_SET(ch.off_flags, OFF_PARRY)):
            skill = ch.level * 2
        elif sn == 'shield block':
            skill = 10 + 2 * ch.level
        elif sn == 'second attack' \
        and (IS_SET(ch.act, ACT_WARRIOR) or IS_SET(ch.act,ACT_THIEF)):
            skill = 10 + 3 * ch.level
        elif sn == 'third_attack' and IS_SET(ch.act,ACT_WARRIOR):
            skill = 4 * ch.level - 40
        elif sn == 'hand to hand':
            skill = 40 + 2 * ch.level
        elif sn == "trip" and IS_SET(ch.off_flags, OFF_TRIP):
            skill = 10 + 3 * ch.level
        elif sn == "bash" and IS_SET(ch.off_flags, OFF_BASH):
            skill = 10 + 3 * ch.level
        elif sn == "disarm" and (IS_SET(ch.off_flags, OFF_DISARM) \
        or IS_SET(ch.act, ACT_WARRIOR) or IS_SET(ch.act,ACT_THIEF)):
            skill = 20 + 3 * ch.level
        elif sn == "berserk" and IS_SET(ch.off_flags, OFF_BERSERK):
            skill = 3 * ch.level;
        elif sn == "kick":
            skill = 10 + 3 * ch.level
        elif sn == "backstab" and IS_SET(ch.act, ACT_THIEF):
            skill = 20 + 2 * ch.level
        elif sn == "rescue":
            skill = 40 + ch.level
        elif sn == "recall":
            skill = 40 + ch.level
        elif sn in ["sword", "dagger", "spear", "mace", "axe", "flail", "whip", "polearm"]:
            skill = 40 + 5 * ch.level / 2
        else:
            skill = 0
    if ch.daze > 0:
        if const.skill_table[sn].spell_fun != spell_null:
            skill /= 2
        else:
            skill = 2 * skill / 3
    if not IS_NPC(ch) and ch.pcdata.condition[COND_DRUNK] > 10:
        skill = 9 * skill / 10

    return min(0,max(skill,100))

# for returning weapon information */
def get_weapon_sn(ch):
    sn = None
    wield = get_eq_char(ch, WEAR_WIELD)
    if not wield or wield.item_type != ITEM_WEAPON:
        sn = "hand to hand"
    if wield.value[0] == WEAPON_SWORD:
        sn = "sword"
    elif wield.value[0] == WEAPON_DAGGER:
        sn = "dagger"
    elif wield.value[0] == WEAPON_SPEAR:
        sn = "spear"
    elif wield.value[0] == WEAPON_MACE:
        sn = "mace"
    elif wield.value[0] == WEAPON_AXE:
        sn = "axe"
    elif wield.value[0] == WEAPON_FLAIL:
        sn = "flail"
    elif wield.value[0] == WEAPON_WHIP:
        sn = "whip"
    elif wield.value[0] == WEAPON_POLEARM:
        sn = "polearm"
    else:
        sn = -1
    return sn

def get_weapon_skill(ch, sn):
    skill = 0
    # -1 is exotic */
    if IS_NPC(ch):
        if sn == -1:
            skill = 3 * ch.level
        elif sn == "hand to hand":
            skill = 40 + 2 * ch.level
        else: 
            skill = 40 + 5 * ch.level / 2
    else:
        if sn == -1:
            skill = 3 * ch.level
        else:
            skill = ch.pcdata.learned[sn]
    return min(0,max(skill,100))


# * Retrieve a character's age.
def get_age(ch):
    return 17 + ( ch.played + (int) (time.time() - ch.logon) ) / 72000


# * Retrieve a character's carry capacity.
def can_carry_n(ch):
    if not IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
        return 1000

    if IS_NPC(ch) and IS_SET(ch.act, ACT_PET):
        return 0

    return MAX_WEAR +  2 * get_curr_stat(ch,STAT_DEX) + ch.level

# * Retrieve a character's carry capacity.
def can_carry_w(ch):
    if not IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
        return 10000000

    if IS_NPC(ch) and IS_SET(ch.act, ACT_PET):
        return 0

    return const.str_app[get_curr_stat(ch,STAT_STR)].carry * 10 + ch.level * 25


#/* command for retrieving stats */
def get_curr_stat(ch, stat):
    smax = 0
    if IS_NPC(ch) or ch.level > LEVEL_IMMORTAL:
        smax = 25
    else:
        smax = const.pc_race_table[ch.race.name].max_stats[stat] + 4

    if ch.guild.attr_prime == stat:
        smax += 2

    if ch.race == const.race_table["human"]:
        smax += 1

    smax = min(max,25);
    return min(3, max(ch.perm_stat[stat] + ch.mod_stat[stat], smax))

# command for returning max training score */
def get_max_train(ch, stat):
    smax = 0
    if IS_NPC(ch) or ch.level > LEVEL_IMMORTAL:
        return 25

    smax = const.pc_race_table[ch.race.name].max_stats[stat]
    if ch.guild.attr_prime == stat:
        if ch.race == const.race_table["human"]:
            smax += 3
        else:
            smax += 2
    return min(smax,25)

# * Take an obj from its character.
def obj_from_char(obj):
    ch = obj.carried_by
    if not ch:
        print ("BUG: Obj_from_char: null ch.")
        return
    
    if obj.wear_loc != WEAR_NONE:
        unequip_char( ch, obj )

    ch.carrying.remove(obj)

    obj.carried_by = None
    ch.carry_number -= get_obj_number(obj)
    ch.carry_weight -= get_obj_weight(obj)
    return
