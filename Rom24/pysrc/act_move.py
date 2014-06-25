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
from handler import *
import const


def move_char(ch, door, follow):
    if door < 0 or door > 5:
        print("BUG: Do_move: bad door %d." % door)
        return
    in_room = ch.in_room
    pexit = in_room.exit[door]
    if not pexit or not pexit.to_room or not ch.can_see_room(pexit.to_room):
        ch.send("Alas, you cannot go that way.\n")
        return
    to_room = pexit.to_room
    if IS_SET(pexit.exit_info, EX_CLOSED) \
            and (not IS_AFFECTED(ch, AFF_PASS_DOOR) or IS_SET(pexit.exit_info, EX_NOPASS)) \
            and not IS_TRUSTED(ch, L7):
        act("The $d is closed.", ch, None, pexit.keyword, TO_CHAR)
        return
    if IS_AFFECTED(ch, AFF_CHARM) and ch.master and in_room == ch.master.in_room:
        ch.send("What?  And leave your beloved master?\n")
        return
    if not ch.is_room_owner(to_room) and to_room.is_private():
        ch.send("That room is private right now.\n")
        return
    if not IS_NPC(ch):
        for gn, guild in const.guild_table.items():
            for room in guild.guild_rooms:
                if guild != ch.guild and to_room.vnum == room:
                    ch.send("You aren't allowed in there.\n")
                    return
        if in_room.sector_type == SECT_AIR or to_room.sector_type == SECT_AIR:
            if not IS_AFFECTED(ch, AFF_FLYING) and not IS_IMMORTAL(ch):
                ch.send("You can't fly.\n")
                return
        if ( in_room.sector_type == SECT_WATER_NOSWIM or to_room.sector_type == SECT_WATER_NOSWIM ) \
                and not IS_AFFECTED(ch, AFF_FLYING):
            # Look for a boat.
            boats = [obj for obj in ch.carrying if obj.item_type == ITEM_BOAT]
            if not boats and not IS_IMMORTAL(ch):
                ch.send("You need a boat to go there.\n")
                return
        move = movement_loss[min(SECT_MAX - 1, in_room.sector_type)] + movement_loss[
            min(SECT_MAX - 1, to_room.sector_type)]
        move /= 2  # i.e. the average */
        # conditional effects */
        if IS_AFFECTED(ch, AFF_FLYING) or IS_AFFECTED(ch, AFF_HASTE):
            move /= 2
        if IS_AFFECTED(ch, AFF_SLOW):
            move *= 2
        if ch.move < move:
            ch.send("You are too exhausted.\n")
            return
        WAIT_STATE(ch, 1)
        ch.move -= move
    if not IS_AFFECTED(ch, AFF_SNEAK) and ch.invis_level < LEVEL_HERO:
        act("$n leaves $T.", ch, None, dir_name[door], TO_ROOM)
    ch.from_room()
    ch.to_room(to_room)
    if not IS_AFFECTED(ch, AFF_SNEAK) and ch.invis_level < LEVEL_HERO:
        act("$n has arrived.", ch, None, None, TO_ROOM)
    ch.do_look("auto")
    if in_room == to_room:  # no circular follows */
        return

    for fch in in_room.people[:]:
        if fch.master == ch and IS_AFFECTED(fch, AFF_CHARM) and fch.position < POS_STANDING:
            fch.do_stand("")

        if fch.master == ch and fch.position == POS_STANDING and fch.can_see_room(to_room):
            if IS_SET(ch.in_room.room_flags, ROOM_LAW) and (IS_NPC(fch) and IS_SET(fch.act, ACT_AGGRESSIVE)):
                act("You can't bring $N into the city.", ch, None, fch, TO_CHAR)
                act("You aren't allowed in the city.", fch, None, None, TO_CHAR)
                continue

            act("You follow $N.", fch, None, ch, TO_CHAR)
            move_char(fch, door, True)


def find_door(ch, arg):
    door = -1
    if arg == "n" or arg == "north":
        door = 0
    elif arg == "e" or arg == "east":
        door = 1
    elif arg == "s" or arg == "south":
        door = 2
    elif arg == "w" or arg == "west":
        door = 3
    elif arg == "u" or arg == "up":
        door = 4
    elif arg == "d" or arg == "down":
        door = 5
    else:
        for door in range(0,5):
            pexit = ch.in_room.exit[door]
            if pexit and IS_SET(pexit.exit_info, EX_ISDOOR) and pexit.keyword and arg in pexit.keyword:
                return door
        act("I see no $T here.", ch, None, arg, TO_CHAR)
        return -1
    pexit = ch.in_room.exit[door]
    if not pexit:
        act("I see no door $T here.", ch, None, arg, TO_CHAR)
        return -1
    if not IS_SET(pexit.exit_info, EX_ISDOOR):
        ch.send("You can't do that.\n")
        return -1
    return door


def has_key(ch, key):
    for obj in ch.carrying:
        if obj.pIndexData.vnum == key:
            return True
    return False


# TODO: continue from this point after a bit...

def do_pick(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Pick what?\n")
        return
    
    WAIT_STATE(ch, skill_table["pick lock"].beats)

    # look for guards */
    for gch in ch.in_room.people:
        if IS_NPC(gch) and IS_AWAKE(gch) and ch.level + 5 < gch.level:
            act( "$N is standing too close to the lock.", ch, None, gch, TO_CHAR )
            return
        if not IS_NPC(ch) and random.randint(1,99) > ch.get_skill("pick lock"):
            ch.send("You failed.\n")
            check_improve(ch,"pick lock",False,2)
            return
        obj = ch.get_obj_here(arg)
        if obj:
        # portal stuff */
            if obj.item_type == ITEM_PORTAL:
                if not IS_SET(obj.value[1], EX_ISDOOR):
                    ch.send("You can't do that.\n")
                    return
                if not IS_SET(obj.value[1], EX_CLOSED):
                    ch.send("It's not closed.\n")
                    return
                if obj.value[4] < 0:
                    ch.send("It can't be unlocked.\n")
                    return
                if IS_SET(obj.value[1], EX_PICKPROOF):
                    ch.send("You failed.\n")
                    return
                REMOVE_BIT(obj.value[1],EX_LOCKED)
                act("You pick the lock on $p.",ch,obj,None,TO_CHAR)
                act("$n picks the lock on $p.",ch,obj,None,TO_ROOM)
                check_improve(ch,"pick lock",True,2)
                return
          
  
  # 'pick object' */
            if obj.item_type != ITEM_CONTAINER:
                ch.send("That's not a container.\n")
                return
            if not IS_SET(obj.value[1], CONT_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[2] < 0:
                ch.send("It can't be unlocked.\n")
                return
            if not IS_SET(obj.value[1], CONT_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if IS_SET(obj.value[1], CONT_PICKPROOF):
                ch.send("You failed.\n")
                return

            REMOVE_BIT(obj.value[1], CONT_LOCKED)
            act("You pick the lock on $p.",ch,obj,None,TO_CHAR)
            act("$n picks the lock on $p.",ch,obj,None,TO_ROOM)
            check_improve(ch,"pick lock",True,2)
            return
        door = find_door( ch, arg )            
        if  door >= 0:
            # 'pick door' */
            ROOM_INDEX_DATA *to_room
            EXIT_DATA *pexit
            EXIT_DATA *pexit_rev

            pexit = ch.in_room.exit[door]
            if not IS_SET(pexit.exit_info, EX_CLOSED) and not IS_IMMORTAL(ch):
                ch.send("It's not closed.\n")
                return
            if pexit.key < 0 and not IS_IMMORTAL(ch):
                ch.send("It can't be picked.\n")
                return
            if not IS_SET(pexit.exit_info, EX_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if IS_SET(pexit.exit_info, EX_PICKPROOF) and not IS_IMMORTAL(ch):
                ch.send("You failed.\n")
                return
            REMOVE_BIT(pexit.exit_info, EX_LOCKED)
            ch.send("*Click*\n")
            act( "$n picks the $d.", ch, None, pexit.keyword, TO_ROOM )
            check_improve(ch,"pick_lock",True,2)
             # pick the other side */
            to_room   = pexit.u1.to_room
            if to_room and to_room.exit[rev_dir[door]] and to_room.exit[rev_dir[door]].to_room == ch.in_room:
                REMOVE_BIT( pexit_rev.exit_info, EX_LOCKED )
      
def do_stand(self, argument):
    ch=self
    obj = None
    if argument:
        if ch.position == POS_FIGHTING:
            ch.send("Maybe you should finish fighting first?\n")
            return
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        if obj.item_type != ITEM_FURNITURE \
        or  ( not IS_SET(obj.value[2],STAND_AT) \
        and not IS_SET(obj.value[2],STAND_ON) \
        and not IS_SET(obj.value[2],STAND_IN)):
            ch.send("You can't seem to find a place to stand.\n")
            return
        if ch.on != obj and count_users(obj) >= obj.value[0]:
            act_new("There's no room to stand on $p.", ch,obj,None,TO_CHAR,POS_DEAD)
            return
        ch.on = obj
  
    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch, AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake and stand up.\n")
            act( "$n wakes and stands up.", ch, None, None, TO_ROOM )
            ch.on = None
        elif IS_SET(obj.value[2], STAND_AT):
            act_new("You wake and stand at $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and stands at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], STAND_ON):
            act_new("You wake and stand on $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and stands on $p.",ch,obj,None,TO_ROOM)
        else: 
            act("You wake and stand in $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and stands in $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_STANDING
        ch.do_look("auto")
        return
    elif ch.position == POS_RESTING or ch.position == POS_SITTING:
        if not obj:
            ch.send("You stand up.\n")
            act( "$n stands up.", ch, None, None, TO_ROOM )
            ch.on = None
        elif IS_SET(obj.value[2], STAND_AT):
            act("You stand at $p.",ch,obj,None,TO_CHAR)
            act("$n stands at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], STAND_ON):
            act("You stand on $p.",ch,obj,None,TO_CHAR)
            act("$n stands on $p.",ch,obj,None,TO_ROOM)
        else:
            act("You stand in $p.",ch,obj,None,TO_CHAR)
            act("$n stands on $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_STANDING
        return
    elif ch.position == POS_STANDING:
        ch.send("You are already standing.\n")
        return
    elif ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return

def do_rest(self, argument):
    ch=self
    obj = None
    if ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return
     # okay, now that we know we can rest, find an object to rest on */
    if argument:
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        else: obj = ch.on

        if obj:
            if obj.item_type != ITEM_FURNITURE \
            or ( not IS_SET(obj.value[2],REST_ON) \
            and not IS_SET(obj.value[2],REST_IN) \
            and not IS_SET(obj.value[2],REST_AT)):
                ch.send("You can't rest on that.\n")
                return
            if obj and ch.on != obj and count_users(obj) >= obj.value[0]:
                act("There's no more room on $p.",ch,obj,None,TO_CHAR,POS_DEAD)
                return
            ch.on = obj

    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch,AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake up and start resting.\n")
            act ("$n wakes up and starts resting.",ch,None,None,TO_ROOM)
        elif IS_SET(obj.value[2], REST_AT):
            act("You wake up and rest at $p.",ch,obj,None,TO_CHAR,POS_SLEEPING)
            act("$n wakes up and rests at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], REST_ON):
            act("You wake up and rest on $p.",ch,obj,None,TO_CHAR,POS_SLEEPING)
            act("$n wakes up and rests on $p.",ch,obj,None,TO_ROOM)
        else:
            act("You wake up and rest in $p.", ch,obj,None,TO_CHAR,POS_SLEEPING)
            act("$n wakes up and rests in $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_RESTING
        return
    elif ch.position == POS_RESTING:
        ch.send("You are already resting.\n")
        return
    elif ch.position == POS_STANDING:
        if obj == None:
            ch.send("You rest.\n")
            act( "$n sits down and rests.", ch, None, None, TO_ROOM )
        elif IS_SET(obj.value[2], REST_AT):
            act("You sit down at $p and rest.",ch,obj,None,TO_CHAR)
            act("$n sits down at $p and rests.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], REST_ON):
            act("You sit on $p and rest.",ch,obj,None,TO_CHAR)
            act("$n sits on $p and rests.",ch,obj,None,TO_ROOM)
        else:
            act("You rest in $p.",ch,obj,None,TO_CHAR)
            act("$n rests in $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_RESTING
        return
    elif ch.position ==  POS_SITTING:
      if not obj:
          ch.send("You rest.\n")
          act("$n rests.",ch,None,None,TO_ROOM)
      elif IS_SET(obj.value[2], REST_AT):
          act("You rest at $p.",ch,obj,None,TO_CHAR)
          act("$n rests at $p.",ch,obj,None,TO_ROOM)
      elif IS_SET(obj.value[2], REST_ON):
          act("You rest on $p.",ch,obj,None,TO_CHAR)
          act("$n rests on $p.",ch,obj,None,TO_ROOM)
      else:
          act("You rest in $p.",ch,obj,None,TO_CHAR)
          act("$n rests in $p.",ch,obj,None,TO_ROOM)
      ch.position = POS_RESTING
      return
      
def do_sit(self, argument):
    ch=self
    obj=None
    if ch.position == POS_FIGHTING:
        ch.send("Maybe you should finish this fight first?\n")
        return
    # okay, now that we know we can sit, find an object to sit on */
    if argument:
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if obj == None:
            ch.send("You don't see that here.\n")
            return
        else: obj = ch.on

        if obj:
            if obj.item_type != ITEM_FURNITURE \
            or ( not IS_SET(obj.value[2],SIT_ON) \
            and not IS_SET(obj.value[2],SIT_IN) \
            and not IS_SET(obj.value[2],SIT_AT)):
                ch.send("You can't sit on that.\n")
                return
            if ch.on != obj and count_users(obj) >= obj.value[0]:
                act("There's no more room on $p.",ch,obj,None,TO_CHAR,POS_DEAD)
                return
            ch.on = obj
    
    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch,AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
          
        if obj == None:
            ch.send("You wake and sit up.\n")
            act( "$n wakes and sits up.", ch, None, None, TO_ROOM )
        elif IS_SET(obj.value[2], SIT_AT):
            act_new("You wake and sit at $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and sits at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act_new("You wake and sit on $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and sits at $p.",ch,obj,None,TO_ROOM)
        else:
            act("You wake and sit in $p.",ch,obj,None,TO_CHAR,POS_DEAD)
            act("$n wakes and sits in $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_SITTING
        return
    elif ch.position == POS_RESTING:
        if obj == None:
            ch.send("You stop resting.\n")
        elif IS_SET(obj.value[2], SIT_AT):
            act("You sit at $p.",ch,obj,None,TO_CHAR)
            act("$n sits at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act("You sit on $p.",ch,obj,None,TO_CHAR)
            act("$n sits on $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_SITTING
        return
    elif ch.position == POS_SITTING:
        ch.send("You are already sitting down.\n")
        return
    elif ch.position == POS_STANDING:
        if obj == None:
            ch.send("You sit down.\n")
            act("$n sits down on the ground.",ch,None,None,TO_ROOM)
        elif IS_SET(obj.value[2], SIT_AT):
            act("You sit down at $p.",ch,obj,None,TO_CHAR)
            act("$n sits down at $p.",ch,obj,None,TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act("You sit on $p.",ch,obj,None,TO_CHAR)
            act("$n sits on $p.",ch,obj,None,TO_ROOM)
        else:
            act("You sit down in $p.",ch,obj,None,TO_CHAR)
            act("$n sits down in $p.",ch,obj,None,TO_ROOM)
        ch.position = POS_SITTING
    
    
def do_sleep(self, argument):
    ch=self
    obj=None
    if ch.position == POS_SLEEPING:
        ch.send("You are already sleeping.\n")
        return
    elif ch.position == POS_RESTING \
    or ch.position == POS_SITTING \
    or ch.position == POS_STANDING: 
        if not argument and not ch.on:
            ch.send("You go to sleep.\n")
            act( "$n goes to sleep.", ch, None, None, TO_ROOM )
            ch.position = POS_SLEEPING
        else:  # find an object and sleep on it */
            if not argument:
                obj = ch.on
            else:
                obj = ch.get_obj_list(argument, ch.in_room.contents)

            if obj == None:
                ch.send("You don't see that here.\n")
                return
            if obj.item_type != ITEM_FURNITURE \
            or ( not IS_SET(obj.value[2],SLEEP_ON) \
            and not IS_SET(obj.value[2],SLEEP_IN) \
            and not IS_SET(obj.value[2],SLEEP_AT)):
                ch.send("You can't sleep on that!\n")
                return
            if ch.on != obj and count_users(obj) >= obj.value[0]:
                act("There is no room on $p for you.",ch,obj,None,TO_CHAR,POS_DEAD)
                return
            ch.on = obj
            if IS_SET(obj.value[2], SLEEP_AT):
                act("You go to sleep at $p.",ch,obj,None,TO_CHAR)
                act("$n goes to sleep at $p.",ch,obj,None,TO_ROOM)
            elif IS_SET(obj.value[2], SLEEP_ON):
                act("You go to sleep on $p.",ch,obj,None,TO_CHAR)
                act("$n goes to sleep on $p.",ch,obj,None,TO_ROOM)
            else:
                act("You go to sleep in $p.",ch,obj,None,TO_CHAR)
                act("$n goes to sleep in $p.",ch,obj,None,TO_ROOM)
            ch.position = POS_SLEEPING
        return
    elif ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return

def do_wake(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.do_stand("")
        return

    if not IS_AWAKE(ch):
        ch.send( "You are asleep yourself!\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_AWAKE(victim):
        act( "$N is already awake.", ch, None, victim, TO_CHAR )
        return
    if IS_AFFECTED(victim, AFF_SLEEP):
        act( "You can't wake $M!",   ch, None, victim, TO_CHAR )
        return
    act("$n wakes you.", ch, None, victim, TO_VICT,POS_SLEEPING )
    victim.do_stand("")
    return

def do_sneak(self, argument):
    ch=self
    ch.send("You attempt to move silently.\n")
    ch.affect_strip("sneak")

    if IS_AFFECTED(ch,AFF_SNEAK):
        return

    if random.randint(1,99) < ch.get_skill("sneak"):
        check_improve(ch,"sneak",True,3)
        af = AFFECT_DATA()
        af.where     = TO_AFFECTS
        af.type      = "sneak"
        af.level     = ch.level 
        af.duration  = ch.level
        af.location  = APPLY_NONE
        af.modifier  = 0
        af.bitvector = AFF_SNEAK
        ch.affect_add(af)
    else:
        check_improve(ch,"sneak",False,3)
    return

def do_hide(self, argument):
    ch=self
    ch.send("You attempt to hide.\n")

    if IS_AFFECTED(ch, AFF_HIDE):
        REMOVE_BIT(ch.affected_by, AFF_HIDE)

    if random.randint(1,99) < ch.get_skill("hide"):
        SET_BIT(ch.affected_by, AFF_HIDE)
        check_improve(ch,"hide",True,3)
    else:
        check_improve(ch,"hide",False,3)
    return

#
# * Contributed by Alander.
def do_visible(self, argument):
    ch=self
    ch.affect_strip("invis")
    ch.affect_strip("mass invis")
    ch.affect_strip("sneak")
    REMOVE_BIT(ch.affected_by, AFF_HIDE)
    REMOVE_BIT(ch.affected_by, AFF_INVISIBLE)
    REMOVE_BIT(ch.affected_by, AFF_SNEAK)
    ch.send("Ok.\n")
    return

def do_recall(self, argument):
    ch=self

    if IS_NPC(ch) and not IS_SET(ch.act,ACT_PET):
        ch.send("Only players can recall.\n")
        return
    act( "$n prays for transportation!", ch, 0, 0, TO_ROOM )
    location = room_index_hash[ROOM_VNUM_TEMPLE]
    if not location:
        ch.send("You are completely lost.\n")
        return
    if ch.in_room == location:
        return
    if IS_SET(ch.in_room.room_flags, ROOM_NO_RECALL) or IS_AFFECTED(ch, AFF_CURSE):
        ch.send("Mota has forsaken you.\n")
        return
    victim = ch.fighting
    if victim:
        skill = ch.get_skill("recall")
        if random.randint(1,99) < 80 * skill / 100:
            check_improve(ch,"recall",False,6)
            WAIT_STATE( ch, 4 )
            sprintf( buf, "You failed!.\n")
            ch.send(buf)
            return
        lose = 25 if ch.desc else 50
        gain_exp( ch, 0 - lose )
        check_improve(ch,"recall",True,4)
        ch.send("You recall from combat!  You lose %d exps.\n" % lose )
        stop_fighting( ch, True )
    ch.move /= 2
    act( "$n disappears.", ch, None, None, TO_ROOM )
    ch.from_room()
    ch.to_room(location)
    act( "$n appears in the room.", ch, None, None, TO_ROOM )
    ch.do_look("auto" )
   
    if ch.pet != None:
        ch.pet.do_recall("")
    return

def do_train(self, argument):
    ch=self
    stat = -1
    pOutput = ""
    if IS_NPC(ch):
        return

     # Check for trainer.
    trainers = [mob for mob in ch.in_room.people if IS_NPC(mob) and IS_SET(mob.act, ACT_TRAIN)]
    if not trainers:
        ch.send("You can't do that here.\n")
        return
    if not argument:
        ch.send("You have %d training sessions.\n" % ch.train )
        argument = "foo"
    cost = 1
    if argument == "str" :
        if ch.guild.attr_prime == STAT_STR:
            cost = 1
        stat = STAT_STR
        pOutput = "strength"
    elif argument == "int" :
        if ch.guild.attr_prime == STAT_INT:
            cost = 1
        stat = STAT_INT
        pOutput = "intelligence"
    elif argument == "wis" :
        if ch.guild.attr_prime == STAT_WIS:
            cost = 1
        stat = STAT_WIS
        pOutput = "wisdom"
    elif argument == "dex" :
        if ch.guild.attr_prime == STAT_DEX:
            cost = 1
        stat = STAT_DEX
        pOutput = "dexterity"
    elif argument == "con" :
        if ch.guild.attr_prime == STAT_CON:
            cost = 1
        stat = STAT_CON
        pOutput = "constitution"
    elif argument == "hp" :
        cost = 1
    elif argument == "mana":
        cost = 1
    elif "hp" == argument:
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.pcdata.perm_hit += 10
        ch.max_hit += 10
        ch.hit +=10
        act( "Your durability increases!",ch,None,None,TO_CHAR)
        act( "$n's durability increases!",ch,None,None,TO_ROOM)
        return
    elif "mana" == argument:
        if cost > ch.train:
            ch.send("You don't have enough training sessions.\n")
            return
        ch.train -= cost
        ch.pcdata.perm_mana += 10
        ch.max_mana += 10
        ch.mana += 10
        act( "Your power increases!",ch,None,None,TO_CHAR)
        act( "$n's power increases!",ch,None,None,TO_ROOM)
        return
    else:
        ch.send("You can train:")
        if ch.perm_stat[STAT_STR] < ch.get_max_train(STAT_STR): ch.send(" str")
        if ch.perm_stat[STAT_INT] < ch.get_max_train(STAT_INT): ch.send(" int")
        if ch.perm_stat[STAT_WIS] < ch.get_max_train(STAT_WIS): ch.send(" wis")
        if ch.perm_stat[STAT_DEX] < ch.get_max_train(STAT_DEX): ch.send(" dex")
        if ch.perm_stat[STAT_CON] < ch.get_max_train(STAT_CON): ch.send(" con")
        ch.send(" hp mana")
        return
    if ch.perm_stat[stat]  >= ch.get_max_train(stat):
        act( "Your $T is already at maximum.", ch, None, pOutput, TO_CHAR )
        return
    if cost > ch.train:
        ch.send("You don't have enough training sessions.\n")
        return
    ch.train -= cost
    ch.perm_stat[stat]   += 1
    act( "Your $T increases!", ch, None, pOutput, TO_CHAR )
    act( "$n's $T increases!", ch, None, pOutput, TO_ROOM )
    return
