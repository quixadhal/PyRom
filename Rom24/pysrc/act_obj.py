"""
/***************************************************************************
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

/***************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""

from merc import *

def can_loot(ch, obj):
    if IS_IMMORTAL(ch):
        return True
    if not obj.owner or obj.owner == None:
        return True
    owner = None
    for wch in char_list:
        if wch.name == obj.owner:
            owner = wch
    if owner == None:
        return True
    if ch.name == owner.name:
        return True
    if not IS_NPC(owner) and IS_SET(owner.act,PLR_CANLOOT):
        return True
    if is_same_group(ch,owner):
        return True
    return False

def get_obj(ch, obj, container):
    # variables for AUTOSPLIT */
    if not CAN_WEAR(obj, ITEM_TAKE):
        ch.send("You can't take that.\n\r")
        return
    if ch.carry_number + get_obj_number( obj ) > can_carry_n( ch ):
        act( "$d: you can't carry that many items.", ch, None, obj.name, TO_CHAR )
        return
    if ( not obj.in_obj or obj.in_obj.carried_by != ch) \
    and (get_carry_weight(ch) + get_obj_weight(obj) > can_carry_w(ch)):
        act( "$d: you can't carry that much weight.", ch, None, obj.name, TO_CHAR )
        return
    if not can_loot(ch,obj):
        act("Corpse looting is not permitted.",ch,None,None,TO_CHAR )
        return
    if obj.in_room != None:
        for gch in obj.in_room.people:
            if gch.on == obj:
                act("$N appears to be using $p.", ch,obj,gch,TO_CHAR)
                return
    if container:
        if container.pIndexData.vnum == OBJ_VNUM_PIT and get_trust(ch) < obj.level:
            ch.send("You are not powerful enough to use it.\n\r")
            return
    if container.pIndexData.vnum == OBJ_VNUM_PIT \
    and not CAN_WEAR(container, ITEM_TAKE) \
    and not IS_OBJ_STAT(obj,ITEM_HAD_TIMER):
        obj.timer = 0 
        act( "You get $p from $P.", ch, obj, container, TO_CHAR )
        act( "$n gets $p from $P.", ch, obj, container, TO_ROOM )
        REMOVE_BIT(obj.extra_flags,ITEM_HAD_TIMER)
        obj_from_obj( obj )
    else:
        act( "You get $p.", ch, obj, container, TO_CHAR )
        act( "$n gets $p.", ch, obj, container, TO_ROOM )
        obj_from_room( obj )
    if obj.item_type == ITEM_MONEY:
        ch.silver += obj.value[0]
        ch.gold += obj.value[1]
        if IS_SET(ch.act, PLR_AUTOSPLIT):
            # AUTOSPLIT code */
            members = len([gch for gch in ch.in_room.people if not IS_AFFECTED(gch,AFF_CHARM) and is_same_group( gch, ch )])
            if members > 1 and (obj.value[0] > 1 or obj.value[1]):
                ch.do_split("%d %d" % (obj.value[0],obj.value[1]))
        extract_obj( obj )
    else:
        obj_to_char( obj, ch )
    return

def do_get(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    if arg2 == "from":
        argument, arg2 = read_word(argument)
    found = False
    # Get type. */
    if not arg1:
        ch.send("Get what?\n\r")
        return
    if not arg2:
        if not arg1.startswith('all'):
            # 'get obj' */
            obj = get_obj_list( ch, arg1, ch.in_room.contents )
            if not obj:
                act( "I see no $T here.", ch, None, arg1, TO_CHAR )
                return
            get_obj( ch, obj, None )
        else:
            # 'get all' or 'get all.obj' */
            for obj in ch.in_room.contents[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and can_see_obj( ch, obj ):
                    found = True
                    get_obj( ch, obj, None )
            if not found:
              if len(arg1) == 3:
                  ch.send("I see nothing here.\n\r")
              else:
                  act( "I see no $T here.", ch, None, arg1[4:], TO_CHAR )
    else:
        # 'get ... container' */
        if arg2.startswith("all"):
            ch.send("You can't do that.\n\r")
            return
        container = get_obj_here( ch, arg2 )
        if not container:
            act( "I see no $T here.", ch, None, arg2, TO_CHAR )
            return
        if container.item_type == ITEM_CONTAINER \
        or container.item_type == ITEM_CORPSE_NPC:
            pass
        elif container.item_type == ITEM_CORPSE_PC:
          if not can_loot(ch,container):
              ch.send("You can't do that.\n\r")
              return
        else:
            ch.send("That's not a container.\n\r")
            return
        if IS_SET(container.value[1], CONT_CLOSED):
            act( "The $d is closed.", ch, None, container.name, TO_CHAR )
            return
        if not arg1.startswith('all'):
            # 'get obj container' */
            obj = get_obj_list( ch, arg1, container.contains )
            if not obj == None:
                act( "I see nothing like that in the $T.",ch, None, arg2, TO_CHAR )
                return
            get_obj( ch, obj, container )
        else:
            # 'get all container' or 'get all.obj container' */
            found = False
            for obj in container.contains[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and can_see_obj(ch, obj):
                    found = True
                    if container.pIndexData.vnum == OBJ_VNUM_PIT and not IS_IMMORTAL(ch):
                        ch.send("Don't be so greedy!\n\r")
                        return
                    get_obj( ch, obj, container )
            if not found:
                if len(arg1) == 3:
                    act( "I see nothing in the $T.", ch, None, arg2, TO_CHAR )
                else:
                    act( "I see nothing like that in the $T.",ch, None, arg2, TO_CHAR )

def do_put(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if arg2 == "in" or arg2 == "on":
        argument, arg2 = read_word(argument)
    if not arg1 or not arg2:
        ch.send("Put what in what?\n\r")
        return
    if arg2.startswith("all") or "all" == arg2:
        ch.send("You can't do that.\n\r")
        return
    container = get_obj_here( ch, arg2 )
    if not container:
        act( "I see no $T here.", ch, None, arg2, TO_CHAR )
        return
    if container.item_type != ITEM_CONTAINER:
        ch.send("That's not a container.\n\r")
        return
    if IS_SET(container.value[1], CONT_CLOSED):
        act( "The $d is closed.", ch, None, container.name, TO_CHAR )
        return
    if arg1 != "all" and not arg1.startswith("all."):
        # 'put obj container' */
        obj = get_obj_carry( ch, arg1, ch )
        if not obj:
            ch.send("You do not have that item.\n\r")
            return
        if obj == container:
            ch.send("You can't fold it into itself.\n\r")
            return
        if not can_drop_obj( ch, obj ):
            ch.send("You can't let go of it.\n\r")
            return
        if WEIGHT_MULT(obj) != 100:
            ch.send("You have a feeling that would be a bad idea.\n\r")
            return
        if get_obj_weight( obj ) + get_true_weight( container ) > (container.value[0] * 10) \
        or get_obj_weight(obj) > (container.value[3] * 10):
            ch.send("It won't fit.\n\r")
            return
        if container.pIndexData.vnum == OBJ_VNUM_PIT \
        and not CAN_WEAR(container,ITEM_TAKE):
            if obj.timer:
                SET_BIT(obj.extra_flags,ITEM_HAD_TIMER)
            else:
                obj.timer = random.randint(100,200)
        obj_from_char( obj )
        obj_to_obj( obj, container )

        if IS_SET(container.value[1], CONT_PUT_ON):
            act("$n puts $p on $P.",ch,obj,container, TO_ROOM)
            act("You put $p on $P.",ch,obj,container, TO_CHAR)
        else:
            act( "$n puts $p in $P.", ch, obj, container, TO_ROOM )
            act( "You put $p in $P.", ch, obj, container, TO_CHAR )
    else:
        # 'put all container' or 'put all.obj container' */
        for obj in ch.carrying[:]:
            if ( len(arg1) == 3 or arg1[4:] in obj.name ) \
            and can_see_obj( ch, obj ) and WEIGHT_MULT(obj) == 100 \
            and obj.wear_loc == WEAR_NONE and obj != container \
            and can_drop_obj( ch, obj )  \
            and get_obj_weight( obj ) + get_true_weight( container ) <= (container.value[0] * 10) \
            and get_obj_weight(obj) < (container.value[3] * 10):
                if container.pIndexData.vnum == OBJ_VNUM_PIT and  not CAN_WEAR(obj, ITEM_TAKE):
                    if obj.timer:
                        SET_BIT(obj.extra_flags,ITEM_HAD_TIMER)
                    else:
                        obj.timer = random.randint(100,200)
                obj_from_char( obj )
                obj_to_obj( obj, container )
                if IS_SET(container.value[1], CONT_PUT_ON):
                    act("$n puts $p on $P.",ch,obj,container, TO_ROOM)
                    act("You put $p on $P.",ch,obj,container, TO_CHAR)
                else:
                    act( "$n puts $p in $P.", ch, obj, container, TO_ROOM )
                    act( "You put $p in $P.", ch, obj, container, TO_CHAR )

def do_drop(self, argument):
    ch=self
    found = False

    argument, arg  = read_word(argument)

    if not arg:
        ch.send("Drop what?\n\r")
        return
    if arg.is_digit():
        # 'drop NNNN coins' */
        gold = 0
        silver = 0
        amount   = int(arg)
        argument, arg  = read_word(argument)
        if amount <= 0 or ( arg != "coins" and arg != "coin" and arg != "gold" and arg != "silver"):
            ch.send("Sorry, you can't do that.\n\r")
            return
        if arg == "coins" or arg == "coin" or arg == "silver":
            if ch.silver < amount:
                ch.send("You don't have that much silver.\n\r")
                return
            ch.silver -= amount
            silver = amount
        else:
            if ch.gold < amount:
                ch.send("You don't have that much gold.\n\r")
                return
            ch.gold -= amount
            gold = amount
        for obj in ch.in_room.contents[:]:
            if obj.pIndexData.vnum == OBJ_VNUM_SILVER_ONE:
                silver += 1
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_GOLD_ONE:
                gold += 1
                extract_obj( obj )
            elif obj.pIndexData.vnum == OBJ_VNUM_SILVER_SOME:
                silver += obj.value[0]
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_GOLD_SOME:
                gold += obj.value[1]
                extract_obj( obj )
            elif obj.pIndexData.vnum == OBJ_VNUM_COINS:
                silver += obj.value[0]
                gold += obj.value[1]
                extract_obj(obj)
        obj_to_room( create_money( gold, silver ), ch.in_room )
        act( "$n drops some coins.", ch, None, None, TO_ROOM )
        ch.send("OK.\n\r")
        return
    if not arg.startswith("all"):
        # 'drop obj' */
        obj = get_obj_carry( ch, arg, ch )
        if not obj:
            ch.send("You do not have that item.\n\r")
            return
        if not can_drop_obj( ch, obj ):
            ch.send("You can't let go of it.\n\r")
            return
    obj_from_char( obj )
    obj_to_room( obj, ch.in_room )
    act( "$n drops $p.", ch, obj, None, TO_ROOM )
    act( "You drop $p.", ch, obj, None, TO_CHAR )
    if IS_OBJ_STAT(obj,ITEM_MELT_DROP):
        act("$p dissolves into smoke.",ch,obj,None,TO_ROOM)
        act("$p dissolves into smoke.",ch,obj,None,TO_CHAR)
        extract_obj(obj)
    else:
        # 'drop all' or 'drop all.obj' */
        found = False
        for obj in ch.carrying[:]:
            if (len(arg) == 3 or arg[4:] in obj.name) \
            and can_see_obj( ch, obj ) \
            and obj.wear_loc == WEAR_NONE \
            and can_drop_obj( ch, obj ):
                found = True
                obj_from_char( obj )
                obj_to_room( obj, ch.in_room )
                act( "$n drops $p.", ch, obj, None, TO_ROOM )
                act( "You drop $p.", ch, obj, None, TO_CHAR )
                if IS_OBJ_STAT(obj,ITEM_MELT_DROP):
                    act("$p dissolves into smoke.",ch,obj,None,TO_ROOM)
                    act("$p dissolves into smoke.",ch,obj,None,TO_CHAR)
                    extract_obj(obj)
        if not found:
            if arg == 'all':
                act( "You are not carrying anything.", ch, None, arg, TO_CHAR )
            else:
                act( "You are not carrying any $T.", ch, None, arg[4:], TO_CHAR )

def do_give(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1 or not arg2:
        ch.send("Give what to whom?\n\r")
        return
    if arg1.is_digit():
        # 'give NNNN coins victim' */
        amount   = int(arg1)
        if amount <= 0 or (arg2 != "coins" and arg2 != "coin" and arg2 != "gold" and arg2 != "silver"):
            ch.send("Sorry, you can't do that.\n\r")
            return
        silver = arg2 != "gold"
        argument, arg2  = read_word(argument)
        if not arg2:
            ch.send("Give what to whom?\n\r")
            return
        victim = get_char_room( ch, arg2 )
        if not victim:
            ch.send("They aren't here.\n\r")
            return
        if ( not silver and ch.gold < amount) or (silver and ch.silver < amount):
            ch.send("You haven't got that much.\n\r")
            return
        if silver:
            ch.silver    -= amount
            victim.silver  += amount
        else:
            ch.gold    -= amount
            victim.gold  += amount
        
        act("$n gives you %d %s." % (amount, "silver" if silver else "gold"), ch, None, victim, TO_VICT)
        act("$n gives $N some coins.",  ch, None, victim, TO_NOTVICT)
        act("You give $N %d %s." % (amount, "silver" if silver else "gold"), ch, None, victim, TO_CHAR)

        if IS_NPC(victim) and IS_SET(victim.act,ACT_IS_CHANGER):
            change = 95 * amount / 100 / 100 if silver else 95 * amount
            if not silver and change > victim.silver:
                victim.silver += change
            if silver and change > victim.gold:
                victim.gold += change
            if change < 1 and can_see(victim,ch):
                act("$n tells you 'I'm sorry, you did not give me enough to change.'",victim,None,ch,TO_VICT)
                ch.reply = victim
                victim.do_give("%d %s %s" % (amount, "silver" if silver else "gold",ch.name))
        elif can_see(victim,ch):
            victim.do_give("%d %s %s" % (change, "gold" if silver else "silver",ch.name))
            if silver:
                victim.do_give("%d silver %s" % ((95 * amount / 100 - change * 100),ch.name))
            act("$n tells you 'Thank you, come again.'", victim,None,ch,TO_VICT)
            ch.reply = victim
        return
    obj = get_obj_carry( ch, arg1, ch )
    if not obj:
        ch.send("You do not have that item.\n\r")
        return
    if obj.wear_loc != WEAR_NONE:
        ch.send("You must remove it first.\n\r")
        return
    victim = get_char_room(ch, arg2)
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if IS_NPC(victim) and victim.pIndexData.pShop != None:
        act("$N tells you 'Sorry, you'll have to sell that.'",ch,None,victim,TO_CHAR)
        ch.reply = victim
        return
    if not can_drop_obj( ch, obj ):
        ch.send("You can't let go of it.\n\r")
        return
    if victim.carry_number + get_obj_number( obj ) > can_carry_n( victim ):
        act( "$N has $S hands full.", ch, None, victim, TO_CHAR )
        return
    if get_carry_weight(victim) + get_obj_weight(obj) > can_carry_w( victim ):
        act( "$N can't carry that much weight.", ch, None, victim, TO_CHAR )
        return
    if not can_see_obj( victim, obj ):
        act( "$N can't see it.", ch, None, victim, TO_CHAR )
        return
    obj_from_char( obj )
    obj_to_char( obj, victim )
    act( "$n gives $p to $N.", ch, obj, victim, TO_NOTVICT )
    act( "$n gives you $p.",   ch, obj, victim, TO_VICT    )
    act( "You give $p to $N.", ch, obj, victim, TO_CHAR    )
    return

# for poisoning weapons and food/drink */
def do_envenom(self, argument):
    ch=self
    # find out what */
    if not argument:
        ch.send("Envenom what item?\n\r")
        return
    obj = get_obj_list(ch,argument,ch.carrying)
    if not obj:
        ch.send("You don't have that item.\n\r")
        return
    skill = get_skill(ch, 'envenom')
    if skill < 1:
        ch.send("Are you crazy? You'd poison yourself!\n\r")
        return
    if obj.item_type == ITEM_FOOD or obj.item_type == ITEM_DRINK_CON:
        if IS_OBJ_STAT(obj,ITEM_BLESS) or IS_OBJ_STAT(obj,ITEM_BURN_PROOF):
            act("You fail to poison $p.",ch,obj,None,TO_CHAR)
            return
        if random.randint(1,99) < skill:  # success! */
            act("$n treats $p with deadly poison.",ch,obj,None,TO_ROOM)
            act("You treat $p with deadly poison.",ch,obj,None,TO_CHAR)
            if not obj.value[3]:
                obj.value[3] = 1
                check_improve(ch,"envenom",True,4)
            WAIT_STATE(ch,skill_table["envenom"].beats)
            return
        act("You fail to poison $p.",ch,obj,None,TO_CHAR)
        if not obj.value[3]:
            check_improve(ch,"envenom",False,4)
            WAIT_STATE(ch,skill_table["envenom"].beats)
            return
    if obj.item_type == ITEM_WEAPON:
        if IS_WEAPON_STAT(obj,WEAPON_FLAMING) \
        or  IS_WEAPON_STAT(obj,WEAPON_FROST) \
        or  IS_WEAPON_STAT(obj,WEAPON_VAMPIRIC) \
        or  IS_WEAPON_STAT(obj,WEAPON_SHARP) \
        or  IS_WEAPON_STAT(obj,WEAPON_VORPAL) \
        or  IS_WEAPON_STAT(obj,WEAPON_SHOCKING) \
        or  IS_OBJ_STAT(obj,ITEM_BLESS) or IS_OBJ_STAT(obj,ITEM_BURN_PROOF):
            act("You can't seem to envenom $p.",ch,obj,None,TO_CHAR)
            return
        if obj.value[3] < 0 or attack_table[obj.value[3]].damage == DAM_BASH:
            ch.send("You can only envenom edged weapons.\n\r")
            return
        if IS_WEAPON_STAT(obj,WEAPON_POISON):
            act("$p is already envenomed.",ch,obj,None,TO_CHAR)
            return
        percent = random.randint(1,99)
        if percent < skill:
            af = AFFECT_DATA()
            af.where     = TO_WEAPON
            af.type      = "poison"
            af.level     = ch.level * percent / 100
            af.duration  = ch.level/2 * percent / 100
            af.location  = 0
            af.modifier  = 0
            af.bitvector = WEAPON_POISON
            affect_to_obj(obj,af)
 
            act("$n coats $p with deadly venom.",ch,obj,None,TO_ROOM)
            act("You coat $p with venom.",ch,obj,None,TO_CHAR)
            check_improve(ch,"envenom",True,3)
            WAIT_STATE(ch,skill_table["envenom"].beats)
            return
        else:
            act("You fail to envenom $p.",ch,obj,None,TO_CHAR)
            check_improve(ch,"envenom",False,3)
            WAIT_STATE(ch,skill_table["envenom"].beats)
            return
    act("You can't poison $p.",ch,obj,None,TO_CHAR)
    return

def do_fill(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Fill what?\n\r")
        return
    obj = get_obj_carry(ch, arg, ch)
    if not obj:
        ch.send("You do not have that item.\n\r")
        return
    fountain = [f for f in ch.in_room.contents if f.item_type == ITEM_FOUNTAIN][:1]
    if not fountain:
        ch.send("There is no fountain here!\n\r")
        return
    fountain = fountain[0]
    if obj.item_type != ITEM_DRINK_CON:
        ch.send("You can't fill that.\n\r")
        return
    if obj.value[1] != 0 and obj.value[2] != fountain.value[2]:
        ch.send("There is already another liquid in it.\n\r")
        return
    if obj.value[1] >= obj.value[0]:
        ch.send("Your container is full.\n\r")
        return
    act("You fill $p with %s from $P." % (liq_table[fountain.value[2]].liq_name), ch, obj,fountain, TO_CHAR )
    act("$n fills $p with %s from $P." % (liq_table[fountain.value[2]].liq_name),ch,obj,fountain,TO_ROOM)
    obj.value[2] = fountain.value[2]
    obj.value[1] = obj.value[0]
    return

def do_pour(self, argument):
    ch=self
    argument, arg = read_word(argument)
    
    if not arg or not argument:
        ch.send("Pour what into what?\n\r")
        return
    out = get_obj_carry(ch,arg, ch)
    if not out:
        ch.send("You don't have that item.\n\r")
        return
    if out.item_type != ITEM_DRINK_CON:
        ch.send("That's not a drink container.\n\r")
        return
    if argument == "out":
        if out.value[1] == 0:
            ch.send("It's already empty.\n\r")
            return
        out.value[1] = 0
        out.value[3] = 0
        act("You invert $p, spilling %s all over the ground." % (liq_table[out.value[2]].liq_name),ch,out,None,TO_CHAR)
        act("$n inverts $p, spilling %s all over the ground." % (liq_table[out.value[2]].liq_name),ch,out,None,TO_ROOM)
        return
    into = get_obj_here(ch,argument)
    vch = None
    if not into:
        vch = get_char_room(ch,argument)

        if vch == None:
            ch.send("Pour into what?\n\r")
            return
        into = get_eq_char(vch,WEAR_HOLD)
        if not into:
            ch.send("They aren't holding anything.")

    if into.item_type != ITEM_DRINK_CON:
        ch.send("You can only pour into other drink containers.\n\r")
        return
    if into == out:
        ch.send("You cannot change the laws of physics!\n\r")
        return
    if into.value[1] != 0 and into.value[2] != out.value[2]:
        ch.send("They don't hold the same liquid.\n\r")
        return
    if out.value[1] == 0:
        act("There's nothing in $p to pour.",ch,out,None,TO_CHAR)
        return
    if into.value[1] >= into.value[0]:
        act("$p is already filled to the top.",ch,into,None,TO_CHAR)
        return
    amount = min(out.value[1],into.value[0] - into.value[1])

    into.value[1] += amount
    out.value[1] -= amount
    into.value[2] = out.value[2]
    
    if not vch:
        act("You pour %s from $p into $P." % (liq_table[out.value[2]].liq_name),ch,out,into,TO_CHAR)
        act("$n pours %s from $p into $P." % (liq_table[out.value[2]].liq_name),ch,out,into,TO_ROOM)
    else:
        act("You pour some %s for $N." % (liq_table[out.value[2]].liq_name),ch,None,vch,TO_CHAR)
        act("$n pours you some %s." % (liq_table[out.value[2]].liq_name),ch,None,vch,TO_VICT)
        act("$n pours some %s for $N." % (liq_table[out.value[2]].liq_name),ch,None,vch,TO_NOTVICT)
  
def do_drink(self, argument):
    ch=self
    argument, arg = read_word(argument)
    obj = None
    if not arg:
        obj = [f for f in ch.in_room.contents if f.item_type == ITEM_FOUNTAIN][:1]
        if obj:
            obj = obj[0]
        if not obj:
            ch.send("Drink what?\n\r")
            return
    else:
        obj = get_obj_here(ch,arg)
        if not obj:
            ch.send("You can't find it.\n\r")
            return

    if not IS_NPC(ch) and ch.pcdata.condition[COND_DRUNK] > 10:
        ch.send("You fail to reach your mouth.  *Hic*\n\r")
        return
    amount = 0
    liquid = -1
    if obj.item_type == ITEM_FOUNTAIN:
        liquid = obj.value[2]
        if liquid < 0:
            print "BUG: Do_drink: bad liquid number %s." % liquid
            liquid = obj.value[2] = 0
        amount = liq_table[liquid].liq_affect[4] * 3
    elif obj.item_type == ITEM_DRINK_CON:
        if obj.value[1] <= 0:
            ch.send("It is already empty.\n\r")
            return
        liquid = obj.value[2]
        if liquid < 0:
            print "BUG: Do_drink: bad liquid number %s." % liquid
            liquid = obj.value[2] = 0
        amount = liq_table[liquid].liq_affect[4]
        amount = min(amount, obj.value[1])
    else:
        ch.send("You can't drink from that.\n\r")
        return
    if not IS_NPC(ch) and not IS_IMMORTAL(ch) and ch.pcdata.condition[COND_FULL] > 45:
        ch.send("You're too full to drink more.\n\r")
        return
    act( "$n drinks $T from $p.", ch, obj, liq_table[liquid].liq_name, TO_ROOM )
    act( "You drink $T from $p.", ch, obj, liq_table[liquid].liq_name, TO_CHAR )
    gain_condition( ch, COND_DRUNK, amount * liq_table[liquid].liq_affect[COND_DRUNK] / 36 )
    gain_condition( ch, COND_FULL, amount * liq_table[liquid].liq_affect[COND_FULL] / 4 )
    gain_condition( ch, COND_THIRST,amount * liq_table[liquid].liq_affect[COND_THIRST] / 10 )
    gain_condition(ch, COND_HUNGER, amount * liq_table[liquid].liq_affect[COND_HUNGER] / 2 )
    if not IS_NPC(ch) and ch.pcdata.condition[COND_DRUNK] > 10:
        ch.send("You feel drunk.\n\r")
    if not IS_NPC(ch) and ch.pcdata.condition[COND_FULL] > 40:
        ch.send("You are full.\n\r")
    if not IS_NPC(ch) and ch.pcdata.condition[COND_THIRST] > 40:
        ch.send("Your thirst is quenched.\n\r")
    if obj.value[3] != 0:
        # The drink was poisoned ! */
        af = AFFECT_DATA()
        act("$n chokes and gags.", ch, None, None, TO_ROOM)
        ch.send("You choke and gag.\n\r")
        af.where = TO_AFFECTS
        af.type = "poison"
        af.level = number_fuzzy(amount) 
        af.duration = 3 * amount
        af.location = APPLY_NONE
        af.modifier = 0
        af.bitvector = AFF_POISON
        affect_join(ch,af)
    if obj.value[0] > 0:
        obj.value[1] -= amount
    return

def do_eat(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Eat what?\n\r")
        return
    obj = get_obj_carry(ch, arg, ch)
    if not obj:
        ch.send("You do not have that item.\n\r")
        return
    if not IS_IMMORTAL(ch):
        if obj.item_type != ITEM_FOOD and obj.item_type != ITEM_PILL:
            ch.send("That's not edible.\n\r")
            return
        if not IS_NPC(ch) and ch.pcdata.condition[COND_FULL] > 40:
            ch.send("You are too full to eat more.\n\r")
            return
    act( "$n eats $p.",  ch, obj, None, TO_ROOM )
    act( "You eat $p.", ch, obj, None, TO_CHAR )
    if obj.item_type == ITEM_FOOD:
        if not IS_NPC(ch):
            condition = ch.pcdata.condition[COND_HUNGER]
            gain_condition( ch, COND_FULL, obj.value[0] )
            gain_condition( ch, COND_HUNGER, obj.value[1])
            if condition == 0 and ch.pcdata.condition[COND_HUNGER] > 0:
                ch.send("You are no longer hungry.\n\r")
            elif ch.pcdata.condition[COND_FULL] > 40:
                ch.send("You are full.\n\r")
        if obj.value[3] != 0:
            # The food was poisoned! */
            af = AFFECT_DATA()
            act( "$n chokes and gags.", ch, 0, 0, TO_ROOM )
            ch.send("You choke and gag.\n\r")
            af.where = TO_AFFECTS
            af.type = "poison"
            af.level = number_fuzzy(obj.value[0])
            af.duration = 2 * obj.value[0]
            af.location = APPLY_NONE
            af.modifier = 0
            af.bitvector = AFF_POISON
            affect_join(ch, af)
    elif obj.item_type == ITEM_PILL:
        obj_cast_spell( obj.value[1], obj.value[0], ch, ch, None )
        obj_cast_spell( obj.value[2], obj.value[0], ch, ch, None )
        obj_cast_spell( obj.value[3], obj.value[0], ch, ch, None )
    extract_obj( obj )
    return

# * Remove an object.
def remove_obj( ch, iWear, fReplace ):
    obj = get_eq_char( ch, iWear )
    if not obj:
        return True
    if not fReplace:
        return False
    if IS_SET(obj.extra_flags, ITEM_NOREMOVE):
        act( "You can't remove $p.", ch, obj, None, TO_CHAR )
        return False
    unequip_char( ch, obj )
    act( "$n stops using $p.", ch, obj, None, TO_ROOM )
    act( "You stop using $p.", ch, obj, None, TO_CHAR )
    return True

#
# * Wear one object.
# * Optional replacement of existing objects.
# * Big repetitive code, ick.
def wear_obj( ch, obj, fReplace ):
    if ch.level < obj.level:
        ch.send("You must be level %d to use this object.\n\r" % obj.level)
        act( "$n tries to use $p, but is too inexperienced.", ch, obj, None, TO_ROOM )
        return
    if obj.item_type == ITEM_LIGHT:
        if not remove_obj( ch, WEAR_LIGHT, fReplace ):
            return
        act( "$n lights $p and holds it.", ch, obj, None, TO_ROOM )
        act( "You light $p and hold it.",  ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_LIGHT )
        return
    if CAN_WEAR(obj, ITEM_WEAR_FINGER):
        if get_eq_char(ch, WEAR_FINGER_L) and get_eq_char(ch, WEAR_FINGER_R) \
        and not remove_obj(ch, WEAR_FINGER_L, fReplace) and not remove_obj(ch, WEAR_FINGER_R, fReplace):
            return
        if not get_eq_char( ch, WEAR_FINGER_L ):
            act( "$n wears $p on $s left finger.",    ch, obj, None, TO_ROOM )
            act( "You wear $p on your left finger.",  ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_FINGER_L )
            return
        if not get_eq_char( ch, WEAR_FINGER_R ):
            act( "$n wears $p on $s right finger.",   ch, obj, None, TO_ROOM )
            act( "You wear $p on your right finger.", ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_FINGER_R )
            return
        print "BUG: Wear_obj: no free finger."
        ch.send("You already wear two rings.\n\r")
        return
    if CAN_WEAR(obj, ITEM_WEAR_NECK):
        if get_eq_char(ch, WEAR_NECK_1) and get_eq_char(ch, WEAR_NECK_2) \
        and not remove_obj(ch, WEAR_NECK_1, fReplace) and not remove_obj(ch, WEAR_NECK_2, fReplace):
            return
        if not get_eq_char(ch, WEAR_NECK_1):
            act( "$n wears $p around $s neck.",   ch, obj, None, TO_ROOM )
            act( "You wear $p around your neck.", ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_NECK_1 )
            return
        if not get_eq_char(ch, WEAR_NECK_2):
            act( "$n wears $p around $s neck.",   ch, obj, None, TO_ROOM )
            act( "You wear $p around your neck.", ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_NECK_2 )
            return
        print "BUG: Wear_obj: no free neck."
        ch.send("You already wear two neck items.\n\r")
        return
    if CAN_WEAR(obj, ITEM_WEAR_BODY):
        if not remove_obj( ch, WEAR_BODY, fReplace ):
            return
        act( "$n wears $p on $s torso.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your torso.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_BODY )
        return
    if CAN_WEAR(obj, ITEM_WEAR_HEAD):
        if not remove_obj(ch, WEAR_HEAD, fReplace):
            return
        act( "$n wears $p on $s head.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your head.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_HEAD )
        return
    if CAN_WEAR( obj, ITEM_WEAR_LEGS):
        if not remove_obj( ch, WEAR_LEGS, fReplace):
            return
        act( "$n wears $p on $s legs.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your legs.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_LEGS )
        return
    if CAN_WEAR(obj, ITEM_WEAR_FEET):
        if not remove_obj( ch, WEAR_FEET, fReplace ):
            return
        act( "$n wears $p on $s feet.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your feet.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_FEET )
        return
    if CAN_WEAR(obj, ITEM_WEAR_HANDS):
        if not remove_obj( ch, WEAR_HANDS, fReplace ):
            return
        act( "$n wears $p on $s hands.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your hands.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_HANDS )
        return
    if CAN_WEAR( obj, ITEM_WEAR_ARMS ):
        if not remove_obj( ch, WEAR_ARMS, fReplace ):
            return
        act( "$n wears $p on $s arms.",   ch, obj, None, TO_ROOM )
        act( "You wear $p on your arms.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_ARMS )
        return
    if CAN_WEAR( obj, ITEM_WEAR_ABOUT ):
        if not remove_obj( ch, WEAR_ABOUT, fReplace ):
            return
        act( "$n wears $p about $s torso.",   ch, obj, None, TO_ROOM )
        act( "You wear $p about your torso.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_ABOUT )
        return
    if CAN_WEAR( obj, ITEM_WEAR_WAIST ):
        if not remove_obj( ch, WEAR_WAIST, fReplace ):
            return
        act( "$n wears $p about $s waist.",   ch, obj, None, TO_ROOM )
        act( "You wear $p about your waist.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_WAIST )
        return
    if CAN_WEAR( obj, ITEM_WEAR_WRIST ):
        if get_eq_char(ch, WEAR_WRIST_L) and get_eq_char(ch, WEAR_WRIST_R) \
        and not remove_obj(ch, WEAR_WRIST_L, fReplace) and not remove_obj( ch, WEAR_WRIST_R, fReplace ):
            return
        if not get_eq_char(ch, WEAR_WRIST_L):
            act( "$n wears $p around $s left wrist.",ch, obj, None, TO_ROOM )
            act( "You wear $p around your left wrist.",ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_WRIST_L )
            return
        if not get_eq_char(ch, WEAR_WRIST_R):
            act( "$n wears $p around $s right wrist.",ch, obj, None, TO_ROOM )
            act( "You wear $p around your right wrist.",ch, obj, None, TO_CHAR )
            equip_char( ch, obj, WEAR_WRIST_R )
            return
    
        print "BUG: Wear_obj: no free wrist."
        ch.send("You already wear two wrist items.\n\r")
        return
    if CAN_WEAR(obj, ITEM_WEAR_SHIELD):
        if not remove_obj(ch, WEAR_SHIELD, fReplace):
            return
        weapon = get_eq_char(ch,WEAR_WIELD)
        if weapon and ch.size < SIZE_LARGE and IS_WEAPON_STAT(weapon,WEAPON_TWO_HANDS):
            ch.send("Your hands are tied up with your weapon!\n\r")
            return
        act( "$n wears $p as a shield.", ch, obj, None, TO_ROOM )
        act( "You wear $p as a shield.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_SHIELD )
        return
    if CAN_WEAR( obj, ITEM_WIELD ):
        if not remove_obj( ch, WEAR_WIELD, fReplace ):
            return
        if not IS_NPC(ch) and get_obj_weight(obj) > (str_app[get_curr_stat(ch,STAT_STR)].wield * 10):
            ch.send("It is too heavy for you to wield.\n\r")
            return
        if not IS_NPC(ch) and ch.size < SIZE_LARGE \
        and IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS) \
        and get_eq_char(ch,WEAR_SHIELD) != None:
            ch.send("You need two hands free for that weapon.\n\r")
            return
        act( "$n wields $p.", ch, obj, None, TO_ROOM )
        act( "You wield $p.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_WIELD )

        sn = get_weapon_sn(ch)

        if sn == "hand to hand":
            return

        skill = get_weapon_skill(ch,sn)
 
        if skill >= 100: act("$p feels like a part of you!",ch,obj,None,TO_CHAR)
        elif skill > 85: act("You feel quite confident with $p.",ch,obj,None,TO_CHAR)
        elif skill > 70: act("You are skilled with $p.",ch,obj,None,TO_CHAR)
        elif skill > 50: act("Your skill with $p is adequate.",ch,obj,None,TO_CHAR)
        elif skill > 25: act("$p feels a little clumsy in your hands.",ch,obj,None,TO_CHAR)
        elif skill > 1: act("You fumble and almost drop $p.",ch,obj,None,TO_CHAR)
        else: act("You don't even know which end is up on $p.",ch,obj,None,TO_CHAR)
        return
    if CAN_WEAR( obj, ITEM_HOLD ):
        if not remove_obj( ch, WEAR_HOLD, fReplace ):
            return
        act( "$n holds $p in $s hand.",   ch, obj, None, TO_ROOM )
        act( "You hold $p in your hand.", ch, obj, None, TO_CHAR )
        equip_char( ch, obj, WEAR_HOLD )
        return
    if CAN_WEAR(obj,ITEM_WEAR_FLOAT):
        if not remove_obj(ch,WEAR_FLOAT, fReplace):
            return
        act("$n releases $p to float next to $m.",ch,obj,None,TO_ROOM)
        act("You release $p and it floats next to you.",ch,obj,None,TO_CHAR)
        equip_char(ch,obj,WEAR_FLOAT)
        return
    if fReplace:
        ch.send("You can't wear, wield, or hold that.\n\r")
    return



def do_wear(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Wear, wield, or hold what?\n\r")
        return
    if arg == "all" :
        for obj in ch.carrying[:]:
            if obj.wear_loc == WEAR_NONE and can_see_obj( ch, obj ):
                wear_obj( ch, obj, False )
        return
    else:
        obj = get_obj_carry( ch, arg, ch )
        if not obj:
            ch.send("You do not have that item.\n\r")
            return
        wear_obj( ch, obj, True )
    return

def do_remove(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Remove what?\n\r")
        return
    obj = get_obj_wear( ch, arg )
    if not obj:
        ch.send("You do not have that item.\n\r")
        return
    remove_obj( ch, obj.wear_loc, True )
    return

def do_sacrifice(self, argument):
    ch=self
    read_word( argument, arg )

    if not arg or arg == ch.name.lower():
        act("$n offers $mself to Mota, who graciously declines.",ch, None, None, TO_ROOM )
        ch.send("Mota appreciates your offer and may accept it later.\n\r")
        return
    obj = get_obj_list( ch, arg, ch.in_room.contents )
    if obj == None:
        ch.send("You can't find it.\n\r")
        return
    if obj.item_type == ITEM_CORPSE_PC:
        if obj.contains:
            ch.send( "Mota wouldn't like that.\n\r")
            return
    if not CAN_WEAR(obj, ITEM_TAKE) or CAN_WEAR(obj, ITEM_NO_SAC):
        act( "$p is not an acceptable sacrifice.", ch, obj, 0, TO_CHAR )
        return
    if obj.in_room:
        for gch in obj.in_room.people:
            if gch.on == obj:
                act("$N appears to be using $p.",ch,obj,gch,TO_CHAR)
                return
    
    silver = max(1,obj.level * 3)
    if obj.item_type != ITEM_CORPSE_NPC and obj.item_type != ITEM_CORPSE_PC:
        silver = min(silver,obj.cost)

    if silver == 1:
        ch.send("Mota gives you one silver coin for your sacrifice.\n\r")
    else:
        ch.send("Mota gives you %d silver coins for your sacrifice.\n\r" % silver)
    ch.silver += silver
    if IS_SET(ch.act, PLR_AUTOSPLIT):
        # AUTOSPLIT code */
        members = len([gch for gch in ch.in_room.people if is_same_group( gch, ch )])
        if members > 1 and silver > 1:
            ch.do_split("%d"%silver)
    act("$n sacrifices $p to Mota.", ch, obj, None, TO_ROOM)
    wiznet("$N sends up $p as a burnt offering.",ch,obj,WIZ_SACCING,0,0)
    extract_obj( obj )
    return

def do_quaff(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Quaff what?\n\r")
        return
    obj = get_obj_carry( ch, arg, ch )
    if not obj:
        ch.send("You do not have that potion.\n\r")
        return
    if obj.item_type != ITEM_POTION:
        ch.send("You can quaff only potions.\n\r")
        return
    if ch.level < obj.level:
        ch.send("This liquid is too powerful for you to drink.\n\r")
        return
    act( "$n quaffs $p.", ch, obj, None, TO_ROOM )
    act( "You quaff $p.", ch, obj, None ,TO_CHAR )

    obj_cast_spell( obj.value[1], obj.value[0], ch, ch, None )
    obj_cast_spell( obj.value[2], obj.value[0], ch, ch, None )
    obj_cast_spell( obj.value[3], obj.value[0], ch, ch, None )

    extract_obj( obj )
    return

def do_recite(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    scroll = get_obj_carry( ch, arg1, ch )
    if not scroll:
        ch.send("You do not have that scroll.\n\r")
        return
    if scroll.item_type != ITEM_SCROLL:
        ch.send("You can recite only scrolls.\n\r")
        return
    if ch.level < scroll.level:
        ch.send("This scroll is too complex for you to comprehend.\n\r")
        return
    obj = None
    victim = None
    if not arg2:
        victim = ch
    else:
        victim = get_char_room(ch, arg2)
        obj = get_obj_here(ch, arg2)
        if not victim and not obj:
            ch.send("You can't find it.\n\r")
            return
        act( "$n recites $p.", ch, scroll, None, TO_ROOM )
        act( "You recite $p.", ch, scroll, None, TO_CHAR )

    if random.randint(1,99) >= 20 + get_skill(ch,"scrolls") * 4/5:
        ch.send("You mispronounce a syllable.\n\r")
        check_improve(ch,"scrolls",False,2)
    else:
        obj_cast_spell(scroll.value[1], scroll.value[0], ch, victim, obj)
        obj_cast_spell(scroll.value[2], scroll.value[0], ch, victim, obj)
        obj_cast_spell(scroll.value[3], scroll.value[0], ch, victim, obj)
        check_improve(ch,"scrolls",True,2)
    extract_obj( scroll )
    return

def do_brandish(self, argument):
    ch=self
    staff = get_eq_char(ch, WEAR_HOLD)
    if not staff:
        ch.send("You hold nothing in your hand.\n\r")
        return
    if staff.item_type != ITEM_STAFF:
        ch.send("You can brandish only with a staff.\n\r")
        return
    sn = staff.value[3]
    if sn < 0 or not skill_table[sn].spell_fun:
        print "BUG: Do_brandish: bad sn %s." % sn
        return
    WAIT_STATE( ch, 2 * PULSE_VIOLENCE )

    if staff.value[2] > 0:
        act( "$n brandishes $p.", ch, staff, None, TO_ROOM )
        act( "You brandish $p.",  ch, staff, None, TO_CHAR )
        if ch.level < staff.level or random.randint(1,99) >= 20 + get_skill(ch,"staves") * 4/5:
            act ("You fail to invoke $p.",ch,staff,None,TO_CHAR)
            act ("...and nothing happens.",ch,None,None,TO_ROOM)
            check_improve(ch,"staves",False,2)
      
        else:
            for vch in ch.in_room.people[:]:
                target = skill_table[sn].target
                if target == TAR_IGNORE:
                    if vch != ch:
                        continue
                elif target == TAR_CHAR_OFFENSIVE:
                    if ( IS_NPC(vch) if IS_NPC(ch) else not IS_NPC(vch) ):
                        continue
                elif target == TAR_CHAR_DEFENSIVE:
                    if ( not IS_NPC(vch) if IS_NPC(ch) else IS_NPC(vch) ):
                        continue
                elif target == TAR_CHAR_SELF:
                    if vch != ch:
                        continue
                else:
                    print "BUG: Do_brandish: bad target for sn %s." % sn
                    return
                obj_cast_spell( staff.value[3], staff.value[0], ch, vch, None )
                check_improve(ch,"staves",True,2)
    staff.value[2] -= 1
    if staff.value[2] <= 0:
        act( "$n's $p blazes bright and is gone.", ch, staff, None, TO_ROOM )
        act( "Your $p blazes bright and is gone.", ch, staff, None, TO_CHAR )
        extract_obj( staff )
    
def do_zap(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg and not ch.fighting:
        ch.send("Zap whom or what?\n\r")
        return
    wand = get_eq_char(ch, WEAR_HOLD)
    if not wand:
        ch.send("You hold nothing in your hand.\n\r")
        return
    if wand.item_type != ITEM_WAND:
        ch.send("You can zap only with a wand.\n\r")
        return
    obj = None
    victim = None
    if not arg:
        if ch.fighting:
            victim = ch.fighting
        else:
            ch.send("Zap whom or what?\n\r")
            return
    else:
        victim = get_char_room ( ch, arg )
        obj = get_obj_here  ( ch, arg )
        if not victim or not obj:   
            ch.send("You can't find it.\n\r")
            return
        WAIT_STATE( ch, 2 * PULSE_VIOLENCE )

    if wand.value[2] > 0:
        if victim:
            act( "$n zaps $N with $p.", ch, wand, victim, TO_NOTVICT )
            act( "You zap $N with $p.", ch, wand, victim, TO_CHAR )
            act( "$n zaps you with $p.",ch, wand, victim, TO_VICT )
        else:
            act( "$n zaps $P with $p.", ch, wand, obj, TO_ROOM )
            act( "You zap $P with $p.", ch, wand, obj, TO_CHAR )
        if ch.level < wand.level \
        or random.randint(1,99) >= 20 + get_skill(ch,"wands") * 4/5:
            act( "Your efforts with $p produce only smoke and sparks.", ch,wand,None,TO_CHAR)
            act( "$n's efforts with $p produce only smoke and sparks.", ch,wand,None,TO_ROOM)
            check_improve(ch,"wands",False,2)
        else:
            obj_cast_spell( wand.value[3], wand.value[0], ch, victim, obj )
            check_improve(ch,"wands",True,2)
    want.value[2] -= 1
    if wand.value[2] <= 0:
        act( "$n's $p explodes into fragments.", ch, wand, None, TO_ROOM )
        act( "Your $p explodes into fragments.", ch, wand, None, TO_CHAR )
        extract_obj( wand )

def do_steal(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1 or not arg2:
        ch.send("Steal what from whom?\n\r")
        return
    victim = get_char_room( ch, arg2 )        
    if not victim:
        ch.send("They aren't here.\n\r")
        return
    if victim == ch:
        ch.send("That's pointless.\n\r")
        return
    if is_safe(ch,victim):
        return

    if IS_NPC(victim) and victim.position == POS_FIGHTING:
        ch.send("Kill stealing is not permitted.\n\rYou'd better not -- you might get hit.\n\r")
        return
    WAIT_STATE( ch, skill_table["steal"].beats )
    percent  = random.randint(1,99)

    if not IS_AWAKE(victim):
        percent -= 10
    elif not can_see(victim,ch):
        percent += 25
    else: 
        percent += 50

    if ((ch.level + 7 < victim.level or ch.level -7 > victim.level) \
    and not IS_NPC(victim) and not IS_NPC(ch) ) \
    or (not IS_NPC(ch) and percent > get_skill(ch,"steal")) \
    or (not IS_NPC(ch) and not is_clan(ch)):
        # Failure.
        ch.send("Oops.\n\r")
        affect_strip(ch,"sneak")
        REMOVE_BIT(ch.affected_by,AFF_SNEAK)
        act( "$n tried to steal from you.\n\r", ch, None, victim, TO_VICT    )
        act( "$n tried to steal from $N.\n\r",  ch, None, victim, TO_NOTVICT )
        outcome = random.randint(0,3)
        buf = ''
        if outcome == 0:
            buf = "%s is a lousy thief!" % ch.name
        elif outcome == 1:
            buf = "%s couldn't rob %s way out of a paper bag!" & (ch.name, ("her" if ch.sex == 2 else "his"))
        elif outcome == 2:
            buf = "%s tried to rob me!" % ch.name
        elif outcome == 3:
            buf = "Keep your hands out of there, %s!" % ch.name
        if not IS_AWAKE(victim):
            victim.do_wake("")
        if IS_AWAKE(victim):
            victim.do_yell(buf)
        if not IS_NPC(ch):
            if IS_NPC(victim):
                check_improve(ch,"steal",False,2)
                multi_hit( victim, ch, TYPE_UNDEFINED )
            else:
                wiznet("$N tried to steal from %s." % victim.name,ch,None,WIZ_FLAGS,0,0)
                if not IS_SET(ch.act, PLR_THIEF):
                    SET_BIT(ch.act, PLR_THIEF)
                    ch.send("*** You are now a THIEF!! ***\n\r")
                    save_char_obj( ch )
        return
    currency = ['coins', 'coin', 'gold', 'silver']
    if arg1 in currency:
        gold = victim.gold * random.randint(1, ch.level) / MAX_LEVEL
        silver = victim.silver * random.randint(1,ch.level) / MAX_LEVEL
        if gold <= 0 and silver <= 0:
            ch.send("You couldn't get any coins.\n\r")
            return
        ch.gold += gold
        ch.silver += silver
        victim.silver -= silver
        victim.gold -= gold
        if silver <= 0:
            ch.send("Bingo!  You got %d gold coins.\n\r" % gold)
        elif gold <= 0:
            ch.send("Bingo!  You got %d silver coins.\n\r" % silver)
        else:
            ch.send("Bingo!  You got %d silver and %d gold coins.\n\r" % (silver,gold))
        ch.send(buf)
        check_improve(ch,"steal",True,2)
        return

    obj = get_obj_carry( victim, arg1, ch )
    if not obj:
        ch.send("You can't find it.\n\r")
        return
    if not can_drop_obj( ch, obj ) or IS_SET(obj.extra_flags, ITEM_INVENTORY) or obj.level > ch.level:
        ch.send("You can't pry it away.\n\r")
        return
    if ch.carry_number + get_obj_number( obj ) > can_carry_n( ch ):
        ch.send("You have your hands full.\n\r")
        return
    if ch.carry_weight + get_obj_weight( obj ) > can_carry_w( ch ):
        ch.send("You can't carry that much weight.\n\r")
        return
    obj_from_char( obj )
    obj_to_char( obj, ch )
    act("You pocket $p.",ch,obj,None,TO_CHAR)
    check_improve(ch,"steal",True,2)
    ch.send("Got it!\n\r")
    return

#
 #* Shopping commands.
def find_keeper( ch ):
    #char buf[MAX_STRING_LENGTH]*/
    pShop = None
    for keeper in ch.in_room.people:
        if IS_NPC(keeper) and keeper.pIndexData.pShop:
            pShop = keeper.pIndexData.pShop
            break
    if not pShop:
        ch.send("You can't do that here.\n\r")
        return None
    #* Undesirables.
    #if not IS_NPC(ch) and IS_SET(ch.act, PLR_KILLER):
    #    keeper.do_say("Killers are not welcome!")
    #    keeper.do_yell("%s the KILLER is over here!\n\r" % ch.name)
    #    return None
    #if not IS_NPC(ch) and IS_SET(ch.act, PLR_THIEF):
    #    keeper.do_say("Thieves are not welcome!")
    #    keeper.do_yell("%s the THIEF is over here!\n\r" % ch.name)
    #    return None
    #* Shop hours.
    if time_info.hour < pShop.open_hour:
        keeper.do_say("Sorry, I am closed. Come back later.")
        return None
    if time_info.hour > pShop.close_hour:
        keeper.do_say("Sorry, I am closed. Come back tomorrow.")
        return None
    #* Invisible or hidden people.
    if not can_see( keeper, ch ):
        keeper.do_say("I don't trade with folks I can't see.")
        return None
    
    return keeper

# insert an object at the right spot for the keeper */
def obj_to_keeper(obj, ch):
    # see if any duplicates are found */
    n_obj = None
    spot = -1
    for i, t_obj in enumerate(ch.carrying):
        if obj.pIndexData == t_obj.pIndexData \
        and obj.short_descr == t_obj.short_descr:
            # if this is an unlimited item, destroy the new one */
            if IS_OBJ_STAT(t_obj,ITEM_INVENTORY):
                extract_obj(obj)
                return
            obj.cost = t_obj.cost # keep it standard */
            n_obj = t_obj
            spot = i
            break

    if n_obj == None or spot == -1:
        ch.carrying.remove(obj)
    else:
        ch.carrying.insert(spot, t_obj)
    obj.carried_by      = ch
    obj.in_room         = None
    obj.in_obj          = None
    ch.carry_number    += get_obj_number( obj )
    ch.carry_weight    += get_obj_weight( obj )

# get an object from a shopkeeper's list */
def get_obj_keeper(ch, keeper, argument):
    number, arg = number_argument(argument)
    for count, obj in enumerate(keeper.carrying, 1):
        if obj.wear_loc == WEAR_NONE and can_see_obj( keeper, obj ) and can_see_obj(ch,obj) and arg in obj.name.lower():
            if count == number:
                return obj
  
    return None

def get_cost(keeper, obj, fBuy):
    if not obj or not keeper.pIndexData.pShop:
        return 0
    pShop = keeper.pIndexData.pShop
    cost = 0
    if fBuy:
        cost = obj.cost * pShop.profit_buy  / 100
    else:
        cost = 0
        for itype in pShop.buy_type:
            if obj.item_type == itype:
                cost = obj.cost * pShop.profit_sell / 100
                break
        
        if not IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT):
            for obj2 in keeper.carrying:
                if obj.pIndexData == obj2.pIndexData and obj.short_descr == obj2.short_descr:
                    if IS_OBJ_STAT(obj2,ITEM_INVENTORY):
                        cost /= 2
                    else:
                        cost = cost * 3 / 4
    if obj.item_type == ITEM_STAFF or obj.item_type == ITEM_WAND:
        if obj.value[1] == 0:
            cost /= 4
        else:
            cost = cost * obj.value[2] / obj.value[1]
    return cost

def do_buy(self, argument):
    ch=self
    if not argument:
        ch.send("Buy what?\n\r")
        return
    if IS_SET(ch.in_room.room_flags, ROOM_PET_SHOP):
        if IS_NPC(ch):
            return
        argument, arg = read_word(argument)
        pRoomIndexNext = None
  # hack to make new thalos pets work */
        if ch.in_room.vnum == 9621:
            if 9706 in room_index_hash:
                pRoomIndexNext = room_index_hash(9706)
        else:
            if ch.in_room.vnum+1 in room_index_hash:
                pRoomIndexNext = room_index_hash(ch.in_room.vnum+1)
        if not pRoomIndexNext:
            print "BUG: Do_buy: bad pet shop at vnum %d." % ch.in_room.vnum
            ch.send("Sorry, you can't buy that here.\n\r")
            return
        in_room     = ch.in_room
        ch.in_room = pRoomIndexNext
        pet         = get_char_room( ch, arg )
        ch.in_room = in_room

        if not pet or not IS_SET(pet.act, ACT_PET):
            ch.send("Sorry, you can't buy that here.\n\r")
            return
        if ch.pet:
            ch.send("You already own a pet.\n\r")
            return
        cost = 10 * pet.level * pet.level

        if (ch.silver+100*ch.gold) < cost:
            ch.send("You can't afford it.\n\r")
            return
        if ch.level < pet.level:
            ch.send(    "You're not powerful enough to master this pet.\n\r")
            return
        # haggle */
        roll = random.randint(1,99)
        if roll < get_skill(ch,"haggle"):
            cost -= cost / 2 * roll / 100
            ch.send("You haggle the price down to %d coins.\n\r" % cost)
            check_improve(ch,"haggle",True,4)
        deduct_cost(ch,cost)
        pet = create_mobile( pet.pIndexData )
        SET_BIT(pet.act, ACT_PET)
        SET_BIT(pet.affected_by, AFF_CHARM)
        pet.comm = COMM_NOTELL|COMM_NOSHOUT|COMM_NOCHANNELS

        argument, arg  = read_word(argument)
        if arg:
            pet.name = "%s %s" % (pet.name, arg)
        pet.description = "%sA neck tag says 'I belong to %s'.\n\r" % (pet.description, ch.name)
        char_to_room( pet, ch.in_room )
        add_follower( pet, ch )
        pet.leader = ch
        ch.pet = pet
        ch.send("Enjoy your pet.\n\r")
        act( "$n bought $N as a pet.", ch, None, pet, TO_ROOM )
        return
    else:
        keeper = find_keeper(ch)
        if not keeper:
            return
        number, arg = mult_argument(argument)
        obj = get_obj_keeper( ch,keeper, arg )
        cost = get_cost( keeper, obj, True )
        if number < 1 or number > 99:
            act("$n tells you 'Get real!",keeper,None,ch,TO_VICT)
            return
        if cost <= 0 or not can_see_obj( ch, obj ):
            act( "$n tells you 'I don't sell that -- try 'list''.", keeper, None, ch, TO_VICT )
            ch.reply = keeper
            return
        items = None
        if not IS_OBJ_STAT(obj,ITEM_INVENTORY):
            items = [t_obj for t_obj in keeper.carrying if t_obj.pIndexData == obj.pIndexData and t_obj.short_descr == obj.short_descr][:number]
            count = len(items)
            if count < number:
                act("$n tells you 'I don't have that many in stock.", keeper,None,ch,TO_VICT)
                ch.reply = keeper
                return
        if (ch.silver + ch.gold * 100) < cost * number:
            if number > 1:
                act("$n tells you 'You can't afford to buy that many.",keeper,obj,ch,TO_VICT)
            else:
                act( "$n tells you 'You can't afford to buy $p'.", keeper, obj, ch, TO_VICT )
            ch.reply = keeper
            return
        if obj.level > ch.level:
            act( "$n tells you 'You can't use $p yet'.", keeper, obj, ch, TO_VICT )
            ch.reply = keeper
            return
        if ch.carry_number +  number * get_obj_number(obj) > can_carry_n(ch):
            ch.send("You can't carry that many items.\n\r")
            return
        if ch.carry_weight + number * get_obj_weight(obj) > can_carry_w(ch):
            ch.send("You can't carry that much weight.\n\r")
            return
        # haggle */
        roll = random.randint(1,99)
        if not IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT) and roll < get_skill(ch,"haggle"):
            cost -= obj.cost / 2 * roll / 100
            act("You haggle with $N.",ch,None,keeper,TO_CHAR)
            check_improve(ch,"haggle",True,4)
          
        if number > 1:
            act("$n buys $p[%d]." % number,ch,obj,None,TO_ROOM)
            act("You buy $p[%d] for %d silver." % (number,cost * number),ch,obj,None,TO_CHAR)
        else:
            act("$n buys $p.", ch, obj, None, TO_ROOM )
            act("You buy $p for %d silver." %cost, ch, obj, None, TO_CHAR )
  
        deduct_cost(ch,cost * number)
        keeper.gold += cost * number/100
        keeper.silver += cost * number - (cost * number/100) * 100
        t_obj = None
        if IS_SET(obj.extra_flags, ITEM_INVENTORY ):
            items = []
            for count in range(number):
                t_obj = create_object( obj.pIndexData, obj.level )
                items.append(t_obj)
        for t_obj in items[:]:
            if not IS_SET(obj.extra_flags, ITEM_INVENTORY):
                obj_from_char( t_obj )

            if t_obj.timer > 0 and not IS_OBJ_STAT(t_obj,ITEM_HAD_TIMER):
                t_obj.timer = 0
            REMOVE_BIT(t_obj.extra_flags,ITEM_HAD_TIMER)
            obj_to_char( t_obj, ch )
            if cost < t_obj.cost:
                t_obj.cost = cost
  
def do_list(self, argument):
    ch=self
    if IS_SET(ch.in_room.room_flags, ROOM_PET_SHOP):
        # hack to make new thalos pets work */
        pRoomIndexNext = None
        if ch.in_room.vnum == 9621:
            if 9706 in room_index_hash:
                pRoomIndexNext = room_index_hash[9706]
        else:
            if ch.in_room.vnum+1 in room_index_hash:
                pRoomIndexNext = room_index_hash[ch.in_room.vnum+1]
        if not pRoomIndexNext:
            print "BUG: Do_list: bad pet shop at vnum %d." % ch.in_room.vnum
            ch.send("You can't do that here.\n\r")
            return
        found = False
        for pet in pRoomIndexNext.people:
            if IS_SET(pet.act, ACT_PET):
                if not found:
                    found = True
                    ch.send("Pets for sale:\n\r")
                ch.send("[%2d] %8d - %s\n\r" % (pet.level, 10 * pet.level * pet.level, pet.short_descr))
        if not found:
            ch.send("Sorry, we're out of pets right now.\n\r")
        return
    else:
        keeper = find_keeper( ch )
        if not keeper:
            return
        argument, arg = read_word(argument)
        found = False
        
        items = OrderedDict()
        for obj in keeper.carrying:
            cost = get_cost( keeper, obj, True )
            if obj.wear_loc == WEAR_NONE and can_see_obj( ch, obj ) and cost > 0 \
            and ( not arg or arg in obj.name.lower()):
                if IS_OBJ_STAT(obj,ITEM_INVENTORY):
                    items[(obj.pIndexData, obj.short_descr)] = (obj, -1)
                else:
                    k = (obj.pIndexData, obj.short_descr)
                    if k not in items:
                        items[k] = (obj, 1)
                    else:
                        items[k][1] += 1


        if not items:
            ch.send("You can't buy anything here.\n\r")
            return
        ch.send("[Lv Price Qty] Item\n\r")      
        for k, p in items.iteritems():
            obj, count = p
            cost = get_cost( keeper, obj, True )
            ch.send("[%2d %5d %2s ] %s\n\r" % (obj.level,cost, ("--" if count == -1 else count),obj.short_descr))

def do_sell(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Sell what?\n\r")
        return
    keeper = find_keeper(ch)
    if not keeper:
        return
    obj = get_obj_carry( ch, arg, ch )
    if not obj:
        act( "$n tells you 'You don't have that item'.", keeper, None, ch, TO_VICT )
        ch.reply = keeper
        return
    if not can_drop_obj( ch, obj ):
        ch.send("You can't let go of it.\n\r")
        return
    if not can_see_obj(keeper,obj):
        act("$n doesn't see what you are offering.",keeper,None,ch,TO_VICT)
        return
    cost = get_cost( keeper, obj, False )        
    if cost <= 0:
        act( "$n looks uninterested in $p.", keeper, obj, ch, TO_VICT )
        return
    if cost > (keeper. silver + 100 * keeper.gold):
        act("$n tells you 'I'm afraid I don't have enough wealth to buy $p.", keeper,obj,ch,TO_VICT)
        return
    act( "$n sells $p.", ch, obj, None, TO_ROOM )
    # haggle */
    roll = random.randint(1,99)
    if not IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT) and roll < get_skill(ch,"haggle"):
        ch.send("You haggle with the shopkeeper.\n\r")
        cost += obj.cost / 2 * roll / 100
        cost = min(cost,95 * get_cost(keeper,obj,True) / 100)
        cost = min(cost,(keeper.silver + 100 * keeper.gold))
        check_improve(ch,"haggle",True,4)
    ch.send("You sell $p for %d silver and %d gold piece%s." % (cost - (cost/100) * 100, cost/100, ("" if cost == 1 else "s" ) ) )
    act( buf, ch, obj, None, TO_CHAR )
    ch.gold     += cost/100
    ch.silver   += cost - (cost/100) * 100

    deduct_cost(keeper,cost)
    if keeper.gold < 0:
        keeper.gold = 0
    if keeper.silver < 0:
        keeper.silver = 0
    if obj.item_type == ITEM_TRASH or IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT):
        extract_obj( obj )
    else:
        obj_from_char( obj )
        if obj.timer:
            SET_BIT(obj.extra_flags,ITEM_HAD_TIMER)
        else:
            obj.timer = random.randint(50,100)
        obj_to_keeper( obj, keeper )
    return


def do_value(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Value what?\n\r")
        return
    keeper = find_keeper( ch )
    if not keeper:
        return
    obj = get_obj_carry(ch, arg, ch)
    if not obj:
        act( "$n tells you 'You don't have that item'.", keeper, None, ch, TO_VICT )
        ch.reply = keeper
        return
    if not can_see_obj(keeper,obj):
        act("$n doesn't see what you are offering.",keeper,None,ch,TO_VICT)
        return
    if not can_drop_obj( ch, obj ):
        ch.send("You can't let go of it.\n\r")
        return
    cost = get_cost( keeper, obj, False )
    if cost <= 0:
        act( "$n looks uninterested in $p.", keeper, obj, ch, TO_VICT )
        return
    act("$n tells you 'I'll give you %d silver and %d gold coins for $p'." % (cost - (cost/100) * 100, cost/100 ), 
      keeper, obj, ch, TO_VICT )
    ch.reply = keeper
    return
