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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""

from merc import *
from handler import *

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
        ch.send("You can't take that.\n")
        return
    if ch.carry_number + get_obj_number(obj) > can_carry_n(ch):
        act("$d: you can't carry that many items.", ch, None, obj.name, TO_CHAR)
        return
    if (not obj.in_obj or obj.in_obj.carried_by != ch) \
    and (get_carry_weight(ch) + get_obj_weight(obj) > can_carry_w(ch)):
        act("$d: you can't carry that much weight.", ch, None, obj.name, TO_CHAR)
        return
    if not can_loot(ch,obj):
        act("Corpse looting is not permitted.",ch,None,None,TO_CHAR)
        return
    if obj.in_room != None:
        for gch in obj.in_room.people:
            if gch.on == obj:
                act("$N appears to be using $p.", ch,obj,gch,TO_CHAR)
                return
    if container:
        if container.pIndexData.vnum == OBJ_VNUM_PIT and get_trust(ch) < obj.level:
            ch.send("You are not powerful enough to use it.\n")
            return
    if container.pIndexData.vnum == OBJ_VNUM_PIT \
    and not CAN_WEAR(container, ITEM_TAKE) \
    and not IS_OBJ_STAT(obj,ITEM_HAD_TIMER):
        obj.timer = 0 
        act("You get $p from $P.", ch, obj, container, TO_CHAR)
        act("$n gets $p from $P.", ch, obj, container, TO_ROOM)
        REMOVE_BIT(obj.extra_flags,ITEM_HAD_TIMER)
        obj_from_obj(obj)
    else:
        act("You get $p.", ch, obj, container, TO_CHAR)
        act("$n gets $p.", ch, obj, container, TO_ROOM)
        obj_from_room(obj)
    if obj.item_type == ITEM_MONEY:
        ch.silver += obj.value[0]
        ch.gold += obj.value[1]
        if IS_SET(ch.act, PLR_AUTOSPLIT):
            # AUTOSPLIT code */
            members = len([gch for gch in ch.in_room.people if not IS_AFFECTED(gch,AFF_CHARM) and is_same_group(gch, ch)])
            if members > 1 and (obj.value[0] > 1 or obj.value[1]):
                ch.do_split("%d %d" % (obj.value[0],obj.value[1]))
        extract_obj(obj)
    else:
        obj_to_char(obj, ch)
    return

def do_get(self, argument):
    ch = self
    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)
    if arg2 == "from":
        argument, arg2 = read_word(argument)
    found = False
    # Get type.  */
    if not arg1:
        ch.send("Get what?\n")
        return
    if not arg2:
        if not arg1.startswith('all'):
            # 'get obj' */
            obj = get_obj_list(ch, arg1, ch.in_room.contents)
            if not obj:
                act("I see no $T here.", ch, None, arg1, TO_CHAR)
                return
            get_obj(ch, obj, None)
        else:
            # 'get all' or 'get all.obj' */
            for obj in ch.in_room.contents[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and can_see_obj(ch, obj):
                    found = True
                    get_obj(ch, obj, None)
            if not found:
              if len(arg1) == 3:
                  ch.send("I see nothing here.\n")
              else:
                  act("I see no $T here.", ch, None, arg1[4:], TO_CHAR)
    else:
        # 'get ...  container' */
        if arg2.startswith("all"):
            ch.send("You can't do that.\n")
            return
        container = get_obj_here(ch, arg2)
        if not container:
            act("I see no $T here.", ch, None, arg2, TO_CHAR)
            return
        if container.item_type == ITEM_CONTAINER \
        or container.item_type == ITEM_CORPSE_NPC:
            pass
        elif container.item_type == ITEM_CORPSE_PC:
          if not can_loot(ch,container):
              ch.send("You can't do that.\n")
              return
        else:
            ch.send("That's not a container.\n")
            return
        if IS_SET(container.value[1], CONT_CLOSED):
            act("The $d is closed.", ch, None, container.name, TO_CHAR)
            return
        if not arg1.startswith('all'):
            # 'get obj container' */
            obj = get_obj_list(ch, arg1, container.contains)
            if not obj == None:
                act("I see nothing like that in the $T.",ch, None, arg2, TO_CHAR)
                return
            get_obj(ch, obj, container)
        else:
            # 'get all container' or 'get all.obj container' */
            found = False
            for obj in container.contains[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and can_see_obj(ch, obj):
                    found = True
                    if container.pIndexData.vnum == OBJ_VNUM_PIT and not IS_IMMORTAL(ch):
                        ch.send("Don't be so greedy!\n")
                        return
                    get_obj(ch, obj, container)
            if not found:
                if len(arg1) == 3:
                    act("I see nothing in the $T.", ch, None, arg2, TO_CHAR)
                else:
                    act("I see nothing like that in the $T.",ch, None, arg2, TO_CHAR)

def do_put(self, argument):
    ch = self
    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)

    if arg2 == "in" or arg2 == "on":
        argument, arg2 = read_word(argument)
    if not arg1 or not arg2:
        ch.send("Put what in what?\n")
        return
    if arg2.startswith("all") or "all" == arg2:
        ch.send("You can't do that.\n")
        return
    container = get_obj_here(ch, arg2)
    if not container:
        act("I see no $T here.", ch, None, arg2, TO_CHAR)
        return
    if container.item_type != ITEM_CONTAINER:
        ch.send("That's not a container.\n")
        return
    if IS_SET(container.value[1], CONT_CLOSED):
        act("The $d is closed.", ch, None, container.name, TO_CHAR)
        return
    if arg1 != "all" and not arg1.startswith("all."):
        # 'put obj container' */
        obj = get_obj_carry(ch, arg1, ch)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        if obj == container:
            ch.send("You can't fold it into itself.\n")
            return
        if not can_drop_obj(ch, obj):
            ch.send("You can't let go of it.\n")
            return
        if WEIGHT_MULT(obj) != 100:
            ch.send("You have a feeling that would be a bad idea.\n")
            return
        if get_obj_weight(obj) + get_true_weight(container) > (container.value[0] * 10) \
        or get_obj_weight(obj) > (container.value[3] * 10):
            ch.send("It won't fit.\n")
            return
        if container.pIndexData.vnum == OBJ_VNUM_PIT \
        and not CAN_WEAR(container,ITEM_TAKE):
            if obj.timer:
                SET_BIT(obj.extra_flags,ITEM_HAD_TIMER)
            else:
                obj.timer = random.randint(100,200)
        obj_from_char(obj)
        obj_to_obj(obj, container)

        if IS_SET(container.value[1], CONT_PUT_ON):
            act("$n puts $p on $P.",ch,obj,container, TO_ROOM)
            act("You put $p on $P.",ch,obj,container, TO_CHAR)
        else:
            act("$n puts $p in $P.", ch, obj, container, TO_ROOM)
            act("You put $p in $P.", ch, obj, container, TO_CHAR)
    else:
        # 'put all container' or 'put all.obj container' */
        for obj in ch.carrying[:]:
            if (len(arg1) == 3 or arg1[4:] in obj.name) \
            and can_see_obj(ch, obj) and WEIGHT_MULT(obj) == 100 \
            and obj.wear_loc == WEAR_NONE and obj != container \
            and can_drop_obj(ch, obj)  \
            and get_obj_weight(obj) + get_true_weight(container) <= (container.value[0] * 10) \
            and get_obj_weight(obj) < (container.value[3] * 10):
                if container.pIndexData.vnum == OBJ_VNUM_PIT and not CAN_WEAR(obj, ITEM_TAKE):
                    if obj.timer:
                        SET_BIT(obj.extra_flags,ITEM_HAD_TIMER)
                    else:
                        obj.timer = random.randint(100,200)
                obj_from_char(obj)
                obj_to_obj(obj, container)
                if IS_SET(container.value[1], CONT_PUT_ON):
                    act("$n puts $p on $P.",ch,obj,container, TO_ROOM)
                    act("You put $p on $P.",ch,obj,container, TO_CHAR)
                else:
                    act("$n puts $p in $P.", ch, obj, container, TO_ROOM)
                    act("You put $p in $P.", ch, obj, container, TO_CHAR)

def do_drop(self, argument):
    ch = self
    found = False

    argument, arg = read_word(argument)

    if not arg:
        ch.send("Drop what?\n")
        return
    if arg.isdigit():
        # 'drop NNNN coins' */
        gold = 0
        silver = 0
        amount = int(arg)
        argument, arg = read_word(argument)
        if amount <= 0 or (arg != "coins" and arg != "coin" and arg != "gold" and arg != "silver"):
            ch.send("Sorry, you can't do that.\n")
            return
        if arg == "coins" or arg == "coin" or arg == "silver":
            if ch.silver < amount:
                ch.send("You don't have that much silver.\n")
                return
            ch.silver -= amount
            silver = amount
        else:
            if ch.gold < amount:
                ch.send("You don't have that much gold.\n")
                return
            ch.gold -= amount
            gold = amount
        for obj in ch.in_room.contents[:]:
            if obj.pIndexData.vnum == OBJ_VNUM_SILVER_ONE:
                silver += 1
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_GOLD_ONE:
                gold += 1
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_SILVER_SOME:
                silver += obj.value[0]
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_GOLD_SOME:
                gold += obj.value[1]
                extract_obj(obj)
            elif obj.pIndexData.vnum == OBJ_VNUM_COINS:
                silver += obj.value[0]
                gold += obj.value[1]
                extract_obj(obj)
        obj_to_room(create_money(gold, silver), ch.in_room)
        act("$n drops some coins.", ch, None, None, TO_ROOM)
        ch.send("OK.\n")
        return
    if not arg.startswith("all"):
        # 'drop obj' */
        obj = get_obj_carry(ch, arg, ch)
        if not obj:
            ch.send("You do not have that item.\n")
            return
        if not can_drop_obj(ch, obj):
            ch.send("You can't let go of it.\n")
            return
        obj_from_char(obj)
        obj_to_room(obj, ch.in_room)
        act("$n drops $p.", ch, obj, None, TO_ROOM)
        act("You drop $p.", ch, obj, None, TO_CHAR)
        if IS_OBJ_STAT(obj,ITEM_MELT_DROP):
            act("$p dissolves into smoke.",ch,obj,None,TO_ROOM)
            act("$p dissolves into smoke.",ch,obj,None,TO_CHAR)
            extract_obj(obj)
    else:
        # 'drop all' or 'drop all.obj' */
        found = False
        for obj in ch.carrying[:]:
            if (len(arg) == 3 or arg[4:] in obj.name) \
            and can_see_obj(ch, obj) \
            and obj.wear_loc == WEAR_NONE \
            and can_drop_obj(ch, obj):
                found = True
                obj_from_char(obj)
                obj_to_room(obj, ch.in_room)
                act("$n drops $p.", ch, obj, None, TO_ROOM)
                act("You drop $p.", ch, obj, None, TO_CHAR)
                if IS_OBJ_STAT(obj,ITEM_MELT_DROP):
                    act("$p dissolves into smoke.",ch,obj,None,TO_ROOM)
                    act("$p dissolves into smoke.",ch,obj,None,TO_CHAR)
                    extract_obj(obj)
        if not found:
            if arg == 'all':
                act("You are not carrying anything.", ch, None, arg, TO_CHAR)
            else:
                act("You are not carrying any $T.", ch, None, arg[4:], TO_CHAR)

def do_give(self, argument):
    ch = self
    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)

    if not arg1 or not arg2:
        ch.send("Give what to whom?\n")
        return
    if arg1.is_digit():
        # 'give NNNN coins victim' */
        amount = int(arg1)
        if amount <= 0 or (arg2 != "coins" and arg2 != "coin" and arg2 != "gold" and arg2 != "silver"):
            ch.send("Sorry, you can't do that.\n")
            return
        silver = arg2 != "gold"
        argument, arg2 = read_word(argument)
        if not arg2:
            ch.send("Give what to whom?\n")
            return
        victim = get_char_room(ch, arg2)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if (not silver and ch.gold < amount) or (silver and ch.silver < amount):
            ch.send("You haven't got that much.\n")
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
    obj = get_obj_carry(ch, arg1, ch)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    if obj.wear_loc != WEAR_NONE:
        ch.send("You must remove it first.\n")
        return
    victim = get_char_room(ch, arg2)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim) and victim.pIndexData.pShop != None:
        act("$N tells you 'Sorry, you'll have to sell that.'",ch,None,victim,TO_CHAR)
        ch.reply = victim
        return
    if not can_drop_obj(ch, obj):
        ch.send("You can't let go of it.\n")
        return
    if victim.carry_number + get_obj_number(obj) > can_carry_n(victim):
        act("$N has $S hands full.", ch, None, victim, TO_CHAR)
        return
    if get_carry_weight(victim) + get_obj_weight(obj) > can_carry_w(victim):
        act("$N can't carry that much weight.", ch, None, victim, TO_CHAR)
        return
    if not can_see_obj(victim, obj):
        act("$N can't see it.", ch, None, victim, TO_CHAR)
        return
    obj_from_char(obj)
    obj_to_char(obj, victim)
    act("$n gives $p to $N.", ch, obj, victim, TO_NOTVICT)
    act("$n gives you $p.",   ch, obj, victim, TO_VICT)
    act("You give $p to $N.", ch, obj, victim, TO_CHAR)
    return
