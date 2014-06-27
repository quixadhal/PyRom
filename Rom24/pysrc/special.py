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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import random
import handler_room
from merc import *
import magic
import const
import fight
import handler_game
import state_checks



def spec_troll_member( ch ):
    if not state_checks.IS_AWAKE(ch) or state_checks.IS_AFFECTED(ch,AFF_CALM) or ch.in_room == None  \
    or  state_checks.IS_AFFECTED(ch,AFF_CHARM) or ch.fighting != None:
        return False
    count = 0
    # find an ogre to beat up */
    for vch in ch.in_room.people:
        if not state_checks.IS_NPC(vch) or ch == vch:
            continue

        if vch.pIndexData.vnum == MOB_VNUM_PATROLMAN:
            return False

        if vch.pIndexData.group == GROUP_VNUM_OGRES and ch.level > vch.level - 2 and not fight.is_safe(ch,vch):
            if random.randint(0,count) == 0:
                victim = vch
                count += 1

    if victim == None:
        return False

    # say something, then raise hell */
    messages = [ "$n yells 'I've been looking for you, punk!'",
                 "With a scream of rage, $n attacks $N.",
                 "$n says 'What's slimy Ogre trash like you doing around here?'",
                 "$n cracks his knuckles and says 'Do ya feel lucky?'",
                 "$n says 'There's no cops to save you this time!'",
                 "$n says 'Time to join your brother, spud.'",  
                 "$n says 'Let's rock.'"]
    message = random.choice(messages)
    handler_game.act(message,ch,None,victim,TO_ALL)
    fight.multi_hit( ch, victim, TYPE_UNDEFINED )
    return True

def spec_ogre_member( ch ):
    if not state_checks.IS_AWAKE(ch) or state_checks.IS_AFFECTED(ch,AFF_CALM) or not ch.in_room or state_checks.IS_AFFECTED(ch,AFF_CHARM) or ch.fighting:
        return False
    count = 0
    victim = None
    # find an troll to beat up */
    for vch in ch.in_room.people:
        if not state_checks.IS_NPC(vch) or ch == vch:
            continue
 
        if vch.pIndexData.vnum == MOB_VNUM_PATROLMAN:
            return False
 
        if vch.pIndexData.group == GROUP_VNUM_TROLLS and ch.level > vch.level - 2 and not fight.is_safe(ch,vch):
            if random.randint(0,count) == 0:
                victim = vch
            count += 1

    if victim == None:
        return False
 
    messages = ["$n yells 'I've been looking for you, punk!'",
                "With a scream of rage, $n attacks $N.'",
                "$n says 'What's Troll filth like you doing around here?'",
                "$n cracks his knuckles and says 'Do ya feel lucky?'",
                "$n says 'There's no cops to save you this time!'",
                "$n says 'Time to join your brother, spud.'",
                "$n says 'Let's rock.'" ]
    message = random.choice(messages)
    handler_game.act(message,ch,None,victim,TO_ALL)
    fight.multi_hit( ch, victim, TYPE_UNDEFINED )
    return True

def spec_patrolman(ch):
    if not state_checks.IS_AWAKE(ch) or state_checks.IS_AFFECTED(ch,AFF_CALM) or not ch.in_room or state_checks.IS_AFFECTED(ch,AFF_CHARM) or ch.fighting:
        return False
    victim = None
    # look for a fight in the room */
    for vch in ch.in_room.people:
        if vch == ch:
            continue

        if vch.fighting != None:  # break it up! */
            if random.randint(0, count) == 0:
                victim = vch if (vch.level > vch.fighting.level) else vch.fighting
                count += 1

    if victim == None or (state_checks.IS_NPC(victim) and victim.spec_fun == ch.spec_fun):
        return False
    neck1 = ch.get_eq(WEAR_NECK_1)
    neck2 = ch.get_eq(WEAR_NECK_2)
    if (neck1 and neck1.pIndexData.vnum == OBJ_VNUM_WHISTLE) or ( neck2 and neck2.pIndexData.vnum == OBJ_VNUM_WHISTLE):
        handler_game.act("You blow down hard on $p.",ch,obj,None,TO_CHAR)
        handler_game.act("$n blows on $p, ***WHEEEEEEEEEEEET***",ch,obj,None,TO_ROOM)

        for vch in char_list:
            if vch.in_room == None:
                continue
            if vch.in_room != ch.in_room and vch.in_room.area == ch.in_room.area:
                vch.send("You hear a shrill whistling sound.\n")

    messages = ["$n yells 'All roit! All roit! break it up!'",
                "$n says 'Society's to blame, but what's a bloke to do?'",
                "$n mumbles 'bloody kids will be the death of us all.'",
                "$n shouts 'Stop that! Stop that!' and attacks.",
                "$n pulls out his billy and goes to work.",
                "$n sighs in resignation and proceeds to break up the fight.",
                "$n says 'Settle down, you hooligans!'" ]
    message = random.choice(messages)
    handler_game.act(message,ch,None,None,TO_ALL)
    fight.multi_hit(ch,victim,TYPE_UNDEFINED)
    return True

def spec_nasty( ch ):
    if not state_checks.IS_AWAKE(ch):
       return False

    if ch.position != POS_FIGHTING:
        for victim in ch.in_room.people[:]:
            if not state_checks.IS_NPC(victim) and (victim.level > ch.level) and (victim.level < ch.level + 10):
                ch.do_backstab(victim.name)
            if ch.position != POS_FIGHTING:
                ch.do_murder(victim.name)
              # should steal some coins right away? :) */
                return True
        return False    #  No one to attack */
 
    # okay, we must be fighting.... steal some coins and flee */
    if not ch.fighting:
        return False   # let's be paranoid.... */
    victim = ch.fighting
    num = random.randint(0,2)
    if num == 0: 
        handler_game.act( "$n rips apart your coin purse, spilling your gold!", ch, None, victim, TO_VICT)
        handler_game.act( "You slash apart $N's coin purse and gather his gold.", ch, None, victim, TO_CHAR)
        handler_game.act( "$N's coin purse is ripped apart!", ch, None, victim, TO_NOTVICT)
        gold = victim.gold / 10  # steal 10% of his gold */
        victim.gold -= gold
        ch.gold += gold
        return True
    elif num == 1:
        ch.do_flee("")
        return True
 
    else: return False

#
# Core procedure for dragons.
def dragon( ch, spell_name ):
    if ch.position != POS_FIGHTING:
        return False
    victim = None
    for vch in ch.in_room.people[:]:
        if vch.fighting == ch and random.randint(0,3) == 0:
            victim = vch
            break


    if victim == None:
        return False
    if spell_name not in const.skill_table:
        return False
    const.skill_table[spell_name].spell_fun( sn, ch.level, ch, victim, TARGET_CHAR)
    return True
# Special procedures for mobiles.

def spec_breath_any( ch ):
    if ch.position != POS_FIGHTING:
        return False

    breaths = [ spec_breath_fire, spec_breath_lightning, spec_breath_gas, spec_breath_acid, spec_breath_frost ]
    breath = random.randint(0, len(breaths)+3)
    if breath < len(breaths):
        return breaths[breath](ch)
    return False

def spec_breath_acid( ch ):
    return dragon( ch, "acid breath" )

def spec_breath_fire( ch ):
    return dragon( ch, "fire breath" )

def spec_breath_frost( ch ):
    return dragon( ch, "frost breath" )

def spec_breath_gas( ch ):
    if ch.position != POS_FIGHTING:
        return False

    if "gas breath" not in const.skill_table:
        return False
    const.skill_table["gas breath"].spell_fun( sn, ch.level, ch, None,TARGET_CHAR)
    return True

def spec_breath_lightning( ch ):
    return dragon( ch, "lightning breath" )

def spec_cast_adept( ch ):
    if not state_checks.IS_AWAKE(ch):
        return False
    victim = None
    for vch in ch.in_room.people[:]:
        if vch != ch and ch.can_see(vch) and random.randint(0, 1 ) == 0 and not state_checks.IS_NPC(vch) and vch.level < 11:
            victim = vch
            break

    if victim == None:
        return False
    
    num = random.randint(1,15)
    if num ==  0:
        handler_game.act( "$n utters the word 'abrazak'.", ch, None, None, TO_ROOM )
        magic.spell_armor( const.skill_table["armor"], ch.level,ch,victim,TARGET_CHAR)
        return True
    elif num ==   1:
        handler_game.act( "$n utters the word 'fido'.", ch, None, None, TO_ROOM )
        magic.spell_bless( const.skill_table["bless"], ch.level,ch,victim,TARGET_CHAR)
        return True
    elif num == 2:
        handler_game.act("$n utters the words 'judicandus noselacri'.",ch,None,None,TO_ROOM)
        magic.spell_cure_blindness( const.skill_table["cure blindness"], ch.level, ch, victim,TARGET_CHAR)
        return True
    elif num == 3:
        handler_game.act("$n utters the words 'judicandus dies'.", ch,None, None, TO_ROOM )
        magic.spell_cure_light( const.skill_table["cure light"], ch.level, ch, victim,TARGET_CHAR)
        return True
    elif num == 4:
        handler_game.act( "$n utters the words 'judicandus sausabru'.",ch,None,None,TO_ROOM)
        magic.spell_cure_poison( const.skill_table["cure poison"], ch.level, ch, victim,TARGET_CHAR)
        return True
    elif num == 5:
        handler_game.act("$n utters the word 'candusima'.", ch, None, None, TO_ROOM )
        magic.spell_refresh( const.skill_table["refresh"],ch.level,ch,victim,TARGET_CHAR)
        return True
    elif num == 6:
        handler_game.act("$n utters the words 'judicandus eugzagz'.",ch,None,None,TO_ROOM)
        magic.spell_cure_disease( const.skill_table["cure disease"], ch.level,ch,victim,TARGET_CHAR)
        return False

def spec_cast_cleric( ch ):
    if ch.position != POS_FIGHTING:
        return False
    victim = None
    for vch in ch.in_room.people[:]:
        if vch.fighting == ch and random.randint(0,3) == 0:
            victim = vch
            break

    if victim == None:
        return False

    while True:
        num = random.randint(0,16)
        if num == 0: 
            min_level =  0 
            spell = "blindness"
        elif num == 1: 
            min_level =  3 
            spell = "cause serious"
        elif num == 2:
            min_level =  7 
            spell = "earthquake"
        elif num == 3: 
            min_level =  9 
            spell = "cause critical"
        elif num == 4:
            min_level = 10
            spell = "dispel evil"
        elif num == 5:
            min_level = 12
            spell = "curse"
        elif num == 6:
            min_level = 12
            spell = "change sex"
        elif num == 7:
            min_level = 13
            spell = "flamestrike"
        elif num in [8, 9, 10]:
            min_level = 15
            spell = "harm"
        elif num == 11:
            min_level = 15
            spell = "plague"
        else:
            min_level = 16
            spell = "dispel magic"

        if ch.level >= min_level:
            break

    if spell not in const.skill_table:
        return False
    const.skill_table[spell].spell_fun( sn, ch.level, ch, victim,TARGET_CHAR)
    return True

def spec_cast_judge( ch ):
    if ch.position != POS_FIGHTING:
        return False
 
    victim = None
    for vch in ch.in_room.people:
        if vch.fighting == ch and random.randint(0, 3 ) == 0:
            victim = vch
            break

    if victim == None:
        return False
 
    spell = "high explosive"
    if spell not in const.skill_table:
        return False
    const.skill_table[spell].spell_fun( sn, ch.level, ch, victim,TARGET_CHAR)
    return True

def spec_cast_mage( ch ):
    if ch.position != POS_FIGHTING:
        return False
    victim = None
    for vch in ch.in_room.people[:]:
        if vch.fighting == ch and random.randint(0,2) == 0:
            victim = vch
            break
    
    if victim == None:
        return False

    while True:
        num = random.randint(0,16)
        if num == 0:
            min_level = 0 
            spell = "blindness"
        elif num == 1:
            min_level = 3
            spell = "chill touch"
        elif num == 2:
            min_level = 7
            spell = "weaken"
        elif num == 3:
            min_level = 8
            spell = "teleport"
        elif num == 4:
            min_level = 11
            spell = "colour spray"
        elif num == 5:
            min_level = 12
            spell = "change sex"
        elif num == 6:
            min_level = 13
            spell = "energy drain"
        elif num in [7,8,9]:
            min_level = 15
            spell = "fireball"
        elif num == 10:
            min_level = 20
            spell = "plague"
        else:
            min_level = 20
            spell = "acid blast"

        if ch.level >= min_level:
            break

    if spell not in const.skill_table:
        return False
    const.skill_table[spell].spell_fun( sn, ch.level, ch, victim,TARGET_CHAR)
    return True

def spec_cast_undead( ch ):
    if ch.position != POS_FIGHTING:
        return False

    for vch in ch.in_room.people[:]:
        if vch.fighting == ch and random.randint(0,3) == 0:
            victim = vch
            break
    if victim == None:
        return False

    while True:
        num = random.randint(0,16)
        if num == 0:
            min_level =  0
            spell = "curse"
        elif num == 1:
            min_level =  3
            spell = "weaken"
        elif num == 2:
            min_level =  6
            spell = "chill touch"
        elif num == 3:
            min_level =  9
            spell = "blindness"
        elif num == 4:
            min_level = 12
            spell = "poison"
        elif num == 5:
            min_level = 15
            spell = "energy drain"
        elif num == 6:
            min_level = 18
            spell = "harm"
        elif num == 7:
            min_level = 21
            spell = "teleport"
        elif num == 8:
            min_level = 20
            spell = "plague"
        else:
            min_level = 18
            spell = "harm"

        if ch.level >= min_level:
            break
    if spell not in const.skill_table:
        return False
    const.skill_table[spell].spell_fun( sn, ch.level, ch, victim,TARGET_CHAR)
    return True

def spec_executioner( ch ):
    if not state_checks.IS_AWAKE(ch) or ch.fighting != None:
        return False

    crime = ""
    victim = None
    for vch in ch.in_room.people[:]:
        if not state_checks.IS_NPC(vch) and state_checks.IS_SET(vch.act, PLR_KILLER) and ch.can_see(vch):
            victim = vch
            crime = "KILLER"

        if not state_checks.IS_NPC(vch) and state_checks.IS_SET(vch.act, PLR_THIEF) and ch.can_see(vch):
            victim = vch
            crime = "THIEF"

    if victim == None:
        return False
 
    state_checks.REMOVE_BIT(ch.comm,COMM_NOSHOUT)
    ch.do_yell("%s is a %s!  PROTECT THE INNOCENT!  MORE BLOOOOD!!!" % (victim.name, crime))
    fight.multi_hit( ch, victim, TYPE_UNDEFINED )
    return True            

def spec_fido( ch ):
    if not state_checks.IS_AWAKE(ch):
        return False

    for corpse in ch.in_room.contents:
        if corpse.item_type != ITEM_CORPSE_NPC:
            continue
        handler_game.act( "$n savagely devours a corpse.", ch, None, None, TO_ROOM )
        for obj in corpse.contains[:]:
            obj.from_obj()
            obj.to_room(ch.in_room)

        corpse.extract()
        return True
    return False

def spec_guard( ch ):
    if not state_checks.IS_AWAKE(ch) or ch.fighting != None:
        return False

    max_evil = 300
    ech = None
    crime = ""
    victim = None
    for vch in ch.in_room.people:
        if not state_checks.IS_NPC(vch) and state_checks.IS_SET(vch.act, PLR_KILLER) and ch.can_see(vch):
            victim = vch
            crime = "KILLER"
            break

        if not state_checks.IS_NPC(vch) and state_checks.IS_SET(vch.act, PLR_THIEF) and ch.can_see(vch):
            crime = "THIEF" 
            victim = vch
            break

        if vch.fighting and vch.fighting != ch and vch.alignment < max_evil:
            max_evil = vch.alignment
            ech = vch

    if victim:
        buf = "%s is a %s!  PROTECT THE INNOCENT!!  BANZAI!!" % ( victim.name, crime )
        state_checks.REMOVE_BIT(ch.comm,COMM_NOSHOUT)
        ch.do_yell(buf)
        fight.multi_hit( ch, victim, TYPE_UNDEFINED )
        return True

    if ech:
        handler_game.act( "$n screams 'PROTECT THE INNOCENT!!  BANZAI!!", ch, None, None, TO_ROOM )
        fight.multi_hit( ch, ech, TYPE_UNDEFINED )
        return True
    return False

def spec_janitor( ch ):
    if not state_checks.IS_AWAKE(ch):
        return False

    for trash in ch.in_room.contents:
        if not state_checks.IS_SET( trash.wear_flags, ITEM_TAKE ) or not ch.can_loot(trash):
            continue
        if trash.item_type == ITEM_DRINK_CON or trash.item_type == ITEM_TRASH or trash.cost < 10:
            handler_game.act( "$n picks up some trash.", ch, None, None, TO_ROOM )
            trash.from_room()
            trash.to_char(ch)
            return True
    return False

pos=0
move=False
path=""
def spec_mayor( ch ):
    open_path = "W3a3003b33000c111d0d111Oe333333Oe22c222112212111a1S."

    close_path = "W3a3003b33000c111d0d111CE333333CE22c222112212111a1S."

    global pos,move,path


    if not move:
        if handler_game.time_info.hour ==  6:
            path = open_path
            move = True
            pos  = 0

        if handler_game.time_info.hour == 20:
            path = close_path
            move = True
            pos  = 0

    if ch.fighting != None:
        return spec_cast_mage( ch )
    if not move or ch.position < POS_SLEEPING:
        return False

    if path[pos] == '0' or path[pos] =='1' or path[pos] =='2' or path[pos] =='3':
        move_char( ch, int(path[pos]), False )
    elif path[pos] == 'W':
        ch.position = POS_STANDING
        handler_game.act( "$n awakens and groans loudly.", ch, None, None, TO_ROOM )
    elif path[pos] ==  'S':
        ch.position = POS_SLEEPING
        handler_game.act( "$n lies down and falls asleep.", ch, None, None, TO_ROOM )
    elif path[pos] == 'a':
        handler_game.act( "$n says 'Hello Honey!'", ch, None, None, TO_ROOM )
    elif path[pos] ==  'b':
        handler_game.act( "$n says 'What a view!  I must do something about that dump!'", ch, None, None, TO_ROOM )
    elif path[pos] == 'c':
        handler_game.act( "$n says 'Vandals!  Youngsters have no respect for anything!'", ch, None, None, TO_ROOM )
    elif path[pos] == 'd':
        handler_game.act( "$n says 'Good day, citizens!'", ch, None, None, TO_ROOM )
    elif path[pos] == 'e':
        handler_game.act( "$n says 'I hereby declare the city of Midgaard open!'", ch, None, None, TO_ROOM )
    elif path[pos] == 'E':
        handler_game.act( "$n says 'I hereby declare the city of Midgaard closed!'", ch, None, None, TO_ROOM )
    elif path[pos] == 'O':
        #  do_function(ch, &do_unlock, "gate" ) */
        ch.do_open("gate")
    elif 'C':
        ch.do_close("gate")
        #  do_function(ch, &do_lock, "gate" ) */
    elif path[pos] == '.' :
        move = False
    pos += 1
    return False

def spec_poison( ch ):
    if ch.position != POS_FIGHTING or not ch.fighting or random.randint(1,99) > 2 * ch.level:
        return False
    victim = ch.fighting
    handler_game.act( "You bite $N!",  ch, None, victim, TO_CHAR    )
    handler_game.act( "$n bites $N!",  ch, None, victim, TO_NOTVICT )
    handler_game.act( "$n bites you!", ch, None, victim, TO_VICT    )
    magic.spell_poison( const.skill_table['poison'], ch.level, ch, victim,TARGET_CHAR)
    return True

def spec_thief( ch ):
    if ch.position != POS_STANDING:
        return False

    for victim in ch.in_room.people:
        if state_checks.IS_NPC(victim) or victim.level >= LEVEL_IMMORTAL or random.randint(0,31) != 0 or not ch.can_see(victim):
            continue

        if state_checks.IS_AWAKE(victim) and random.randint( 0, ch.level ) == 0:
            handler_game.act( "You discover $n's hands in your wallet!", ch, None, victim, TO_VICT )
            handler_game.act( "$N discovers $n's hands in $S wallet!", ch, None, victim, TO_NOTVICT )
            return True
        else:
            gold = victim.gold * min(random.randint(1,20),ch.level / 2) / 100
            gold = min(gold, ch.level * ch.level * 10 )
            ch.gold     += gold
            victim.gold -= gold
            silver = victim.silver * min(random.randint(1,20),ch.level/2)/100
            silver = min(silver,ch.level*ch.level * 25)
            ch.silver  += silver
            victim.silver -= silver
            return True
    return False

spec_table = {}
spec_table["spec_breath_any"] = spec_breath_any
spec_table["spec_breath_acid"] = spec_breath_acid
spec_table["spec_breath_fire"] = spec_breath_fire
spec_table["spec_breath_frost"] = spec_breath_frost
spec_table["spec_breath_gas"] = spec_breath_gas
spec_table["spec_breath_lightning"] = spec_breath_lightning  
spec_table["spec_cast_adept"] = spec_cast_adept
spec_table["spec_cast_cleric"] = spec_cast_cleric
spec_table["spec_cast_judge"] = spec_cast_judge
spec_table["spec_cast_mage"] = spec_cast_mage
spec_table["spec_cast_undead"] = spec_cast_undead
spec_table["spec_executioner"] = spec_executioner
spec_table["spec_fido"] = spec_fido
spec_table["spec_guard"] = spec_guard
spec_table["spec_janitor"] = spec_janitor
spec_table["spec_mayor"] = spec_mayor
spec_table["spec_poison"] = spec_poison
spec_table["spec_thief"] = spec_thief
spec_table["spec_nasty"] = spec_nasty
spec_table["spec_troll_member"] = spec_troll_member
spec_table["spec_ogre_member"] = spec_ogre_member
spec_table["spec_patrolman"] = spec_patrolman
