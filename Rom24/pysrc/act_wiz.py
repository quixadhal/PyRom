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
from merc import *
import nanny
from handler import get_trust, get_eq_char, obj_to_char, equip_char
from db import create_object
from const import weapon_table
from settings import NEWLOCK

def do_wiznet(self, argument):
    ch=self
    if not argument:
        if IS_SET(ch.wiznet, WIZ_ON):
            ch.send("Signing off of Wiznet.\n")
            REMOVE_BIT(ch.wiznet,WIZ_ON)
        else:
            ch.send("Welcome to Wiznet!\n")
            SET_BIT(ch.wiznet,WIZ_ON)
        return

    if "on".startswith(argument):
        ch.send("Welcome to Wiznet!\n")
        SET_BIT(ch.wiznet,WIZ_ON)
        return
    if "off".startswith(argument):
        ch.send("Signing off of Wiznet.\n")
        REMOVE_BIT(ch.wiznet,WIZ_ON)
        return
    buf = ''
    # show wiznet status */
    if "status".startswith(argument): 
        if not IS_SET(ch.wiznet, WIZ_ON):
          buf += "off "
        for name, flag in wiznet_table.items():
            if IS_SET(ch.wiznet, flag.flag):
                buf += name + " "
            ch.send("Wiznet status:\n%s\n" % buf)
            return
    if "show".startswith(argument):
    # list of all wiznet options */
        buf = ''
        for name, flag in wiznet_table.items():
            if flag.level <= get_trust(ch):
                buf += name + " "
        ch.send("Wiznet options available to you are:\n%s\n" % buf )
        return
    flag = prefix_lookup(wiznet_table, argument)
    if not flag or get_trust(ch) < flag.level:
        ch.send("No such option.\n")
        return
    if IS_SET(ch.wiznet, flag.flag):
        ch.send("You will no longer see %s on wiznet.\n" % flag.name)
        REMOVE_BIT(ch.wiznet,flag.flag)
        return
    else:
        ch.send("You will now see %s on wiznet.\n" % flag.name)
        SET_BIT(ch.wiznet,flag.flag)
        return

def do_guild(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1 or not arg2:
        ch.send("Syntax: guild <char> <cln name>\n")
        return

    victim = get_char_world(ch, arg1)
    if not victim:
        ch.send("They aren't playing.\n")
        return
   
    if "none".startswith(arg2):
        ch.send("They are now clanless.\n")
        victim.send("You are now a member of no clan!\n")
        victim.clan = 0
        return
    clan = prefix_lookup(clan_table, arg2)
    if not clan:
        ch.send("No such clan exists.\n")
        return
    if clan.independent:
        ch.send("They are now a %s.\n" % clan.name)
        victim.send("You are now a %s.\n" % clan.name)
    else:
        ch.send("They are now a member of clan %s.\n" % clan.name.capitalize())
        victim.send("You are now a member of clan %s.\n" % clan.name.capitalize())
    victim.clan = clan

# equips a character */
def do_outfit ( self, argument ):
    ch = self
    if ch.level > 5 or IS_NPC(ch):
        ch.send("Find it yourself!\n")
        return  

    obj = get_eq_char(ch, WEAR_LIGHT)
    if not obj:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_BANNER], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_LIGHT )

    obj = get_eq_char(ch, WEAR_BODY) 
    if not obj:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_VEST], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_BODY )

    # do the weapon thing */
    obj = get_eq_char(ch,WEAR_WIELD)
    if not obj:
        sn = 'dagger'
        vnum = OBJ_VNUM_SCHOOL_SWORD # just in case! */
        for k,weapon in weapon_table.items():
            if sn not in ch.pcdata.learned or (weapon.gsn in ch.pcdata.learned and ch.pcdata.learned[sn] < ch.pcdata.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum

        obj = create_object(obj_index_hash[vnum],0)
        obj_to_char(obj,ch)
        equip_char(ch,obj,WEAR_WIELD)

    obj = get_eq_char(ch,WEAR_WIELD) 
    shield = get_eq_char( ch, WEAR_SHIELD )
    if (not obj or not IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS)) and not shield:
        obj = create_object( obj_index_hash[OBJ_VNUM_SCHOOL_SHIELD], 0 )
        obj.cost = 0
        obj_to_char( obj, ch )
        equip_char( ch, obj, WEAR_SHIELD )

    ch.send("You have been equipped by Mota.\n")

     
# RT nochannels command, for those spammers */
def do_nochannels(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Nochannel whom?")
        return
   
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
        ch.send("You failed.\n")
        return
    
    if IS_SET(victim.comm, COMM_NOCHANNELS):
        REMOVE_BIT(victim.comm, COMM_NOCHANNELS)
        victim.send("The gods have restored your channel priviliges.\n")
        ch.send("NOCHANNELS removed.\n")
        wiznet("$N restores channels to %s" % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOCHANNELS)
        victim.send("The gods have revoked your channel priviliges.\n")
        ch.send("NOCHANNELS set.\n")
        wiznet("$N revokes %s's channels." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return

def do_smote(self, argument):
    ch=self
    matches = 0
    if not IS_NPC(ch) and IS_SET(ch.comm, COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    if ch.name not in argument:
        ch.send("You must include your name in an smote.\n")
        return
  
    ch.send(argument + "\n")
    for vch in ch.in_room.people:
        if vch.desc == None or vch == ch:
            continue
 
        if vch.name not in argument:
            vch.send(argument + "\n")
            continue
        buf = mass_replace({"%s's" % vch.name:'your', vch.name:'you'})
        vch.send(buf + "\n")
    return

def do_bamfin(self, argument):
    ch=self
    if not IS_NPC(ch):
        if not argument:
            ch.send("Your poofin is %s\n" % ch.pcdata.bamfin)
        return
        if ch.name not in argument:
            ch.send("You must include your name.\n")
            return
           
        ch.pcdata.bamfin = argument

        ch.send("Your poofin is now %s\n" % ch.pcdata.bamfin)
    return

def do_bamfout(self, argument):
    ch=self
    if not IS_NPC(ch):
        if not argument:
            ch.send("Your poofout is %s\n" % ch.pcdata.bamfout)
            return
        if ch.name not in argument:
            ch.send("You must include your name.\n")
            return
        ch.pcdata.bamfout = argument
        ch.send("Your poofout is now %s\n" % ch.pcdata.bamfout)
    return

def do_deny(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Deny whom?\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
        ch.send("You failed.\n")
        return
    SET_BIT(victim.act, PLR_DENY)
    victim.send("You are denied access!\n")
    wiznet("$N denies access to %s" % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    ch.send("OK.\n")
    save_char_obj(victim)
    stop_fighting(victim,True)
    victim.do_quit("" )
    return

def do_disconnect(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Disconnect whom?\n")
        return
    if arg.is_digit():
        desc = int(arg)
        for d in descriptor_list:
            if d.descriptor == desc:
                close_socket( d )
                ch.send("Ok.\n")
                return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.desc == None:
        act( "$N doesn't have a descriptor.", ch, None, victim, TO_CHAR )
        return
    for d in descriptor_list:
        if d == victim.desc:
            close_socket( d )
            ch.send("Ok.\n")
            return
    print("BUG: Do_disconnect: desc not found.")
    ch.send("Descriptor not found!\n")
    return

def do_pardon(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    if not arg1 or not arg2:
        ch.send("Syntax: pardon <character> <killer|thief>.\n")
        return
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return

    if arg2 == "killer" :
        if IS_SET(victim.act, PLR_KILLER):
            REMOVE_BIT( victim.act, PLR_KILLER )
            ch.send("Killer flag removed.\n")
            victim.send("You are no longer a KILLER.\n")
        return
    if arg2 == "thief" :
        if IS_SET(victim.act, PLR_THIEF):
            REMOVE_BIT( victim.act, PLR_THIEF )
            ch.send("Thief flag removed.\n")
            victim.send("You are no longer a THIEF.\n")
        return
    ch.send("Syntax: pardon <character> <killer|thief>.\n")
    return

def do_echo(self, argument):
    ch=self
    
    if not argument:
        ch.send("Global echo what?\n")
        return
   
    for d in descriptor_list:
        if d.connected == con_playing:
            if get_trust(d.character) >= get_trust(ch):
                d.send("global> ")
            d.send(argument + "\n")
    return

def do_recho(self, argument):
    ch=self
    if not argument:
        ch.send("Local echo what?\n")
        return

    for d in descriptor_list:
        if d.connected == con_playing and d.character.in_room == ch.in_room:
            if get_trust(d.character) >= get_trust(ch):
                d.send( "local> ")
            d.send( argument + "\n" )

    return

def do_zecho(self, argument):
    ch=self
    if not argument:
        ch.send("Zone echo what?\n")
        return
    for d in descriptor_list:
        if d.connected == con_playing and  d.character.in_room and ch.in_room \
        and d.character.in_room.area == ch.in_room.area:
            if get_trust(d.character) >= get_trust(ch):
                d.send("zone> ")
            d.send(argument +"\n")

def do_pecho(self, argument):
    ch=self
    argument, arg = read_word(argument)
 
    if not argument or not arg:
        ch.send("Personal echo what?\n") 
        return
    
    victim = get_char_world(ch, arg)
    if not victim:
        ch.send("Target not found.\n")
        return
    if get_trust(victim) >= get_trust(ch) and get_trust(ch) != MAX_LEVEL:
        victim.send("personal> ")

    victim.send(argument)
    victim.send("\n")
    ch.send("personal> ")
    ch.send(argument)
    ch.send("\n")

def find_location( ch, arg ):
    if arg.is_digit():
        vnum = int(arg)
        if vnum not in room_index_hash:
            return None
        else:
            return room_index_hash[vnum]
    victim = get_char_world( ch, arg )
    if victim:
        return victim.in_room
    obj = get_obj_world( ch, arg )
    if obj:
        return obj.in_room
    return None

def do_transfer(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1:
        ch.send("Transfer whom (and where)?\n")
        return
    if arg1 == "all" :
        for d in descriptor_list:
            if d.connected == con_playing \
            and d.character != ch \
            and d.character.in_room \
            and can_see( ch, d.character ):
                 ch.do_transfer("%s %s" % d.character.name, arg2 )
        return
    #
    # * Thanks to Grodyn for the optional location parameter.
    if not arg2:
        location = ch.in_room
    else:
        location = find_location( ch, arg2 )
        if not location:
            ch.send("No such location.\n")
            return
        if not is_room_owner(ch,location) and room_is_private( location ) \
        and get_trust(ch) < MAX_LEVEL:
            ch.send("That room is private right now.\n")
            return
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.in_room == None:
        ch.send("They are in limbo.\n")
        return

    if victim.fighting:
        stop_fighting( victim, True )
    act( "$n disappears in a mushroom cloud.", victim, None, None, TO_ROOM )
    char_from_room( victim )
    char_to_room( victim, location )
    act( "$n arrives from a puff of smoke.", victim, None, None, TO_ROOM )
    if ch != victim:
        act( "$n has transferred you.", ch, None, victim, TO_VICT )
    victim.do_look("auto")
    ch.send("Ok.\n")

def do_at(self, argument):
    ch=self
    argument, arg  = read_word(argument)

    if not arg or not argument:
        ch.send("At where what?\n")
        return
    location = find_location( ch, arg )
    if not location:
        ch.send("No such location.\n")
        return
    if not is_room_owner(ch,location) and room_is_private( location ) \
    and get_trust(ch) < MAX_LEVEL:
        ch.send("That room is private right now.\n")
        return
    original = ch.in_room
    on = ch.on
    char_from_room( ch )
    char_to_room( ch, location )
    interpret( ch, argument )

    # * See if 'ch' still exists before continuing!
    # * Handles 'at XXXX quit' case.
    for wch in char_list:
        if wch == ch:
            char_from_room( ch )
            char_to_room( ch, original )
            ch.on = on
            break

def do_goto(self, argument):
    ch=self
    if not argument:
        ch.send("Goto where?\n")
        return
    location = find_location( ch, argument )
    if not location:
        ch.send("No such location.\n")
        return
    count = len(location.people)
    if not is_room_owner(ch,location) and room_is_private(location) \
    and (count > 1 or get_trust(ch) < MAX_LEVEL):
        ch.send("That room is private right now.\n")
        return
    if ch.fighting:
        stop_fighting( ch, True )
    for rch in ch.in_room.people:
        if get_trust(rch) >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfout:
                act("$t",ch,ch.pcdata.bamfout,rch,TO_VICT)
            else:
                act("$n leaves in a swirling mist.",ch,None,rch,TO_VICT)
    char_from_room( ch )
    char_to_room( ch, location )

    for rch in ch.in_room.people:
        if get_trust(rch) >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfin:
                act("$t",ch,ch.pcdata.bamfin,rch,TO_VICT)
            else:
                act("$n appears in a swirling mist.",ch,None,rch,TO_VICT)
    ch.do_look("auto" )
    return

def do_violate(self, argument):
    ch=self
    if not argument:
        ch.send("Goto where?\n")
        return
    location = find_location( ch, argument )
    if not location:
        ch.send("No such location.\n")
        return
    if not room_is_private( location ):
        ch.send("That room isn't private, use goto.\n")
        return
 
    if ch.fighting:
        stop_fighting( ch, True )
 
    for rch in ch.in_room.people:
        if get_trust(rch) >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfout:
                act("$t",ch,ch.pcdata.bamfout,rch,TO_VICT)
            else:
                act("$n leaves in a swirling mist.",ch,None,rch,TO_VICT)
    char_from_room( ch )
    char_to_room( ch, location )
 
    for rch in ch.in_room.people:
        if get_trust(rch) >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfin:
                act("$t",ch,ch.pcdata.bamfin,rch,TO_VICT)
            else:
                act("$n appears in a swirling mist.",ch,None,rch,TO_VICT)
    ch.do_look("auto" )
    return

# RT to replace the 3 stat commands */
def do_stat(self, argument):
    ch=self
    string, arg = read_word(argument)
    if not arg:
        ch.send("Syntax:\n")
        ch.send("  stat <name>\n")
        ch.send("  stat obj <name>\n")
        ch.send("  stat mob <name>\n")
        ch.send("  stat room <number>\n")
        return
    if arg == "room":
        ch.do_rstat(string)
        return
    if arg == "obj":
        ch.do_ostat(string)
        return
    if arg == "char" or arg == "mob":
        ch.do_mstat(string)
        return
  
    # do it the old way */

    obj = get_obj_world(ch,argument)
    if obj:
        ch.do_ostat(argument)
        return
    victim = get_char_world(ch,argument)
    if victim:
        ch.do_mstat(argument)
        return
    location = find_location(ch,argument)
    if location:
        ch.do_rstat(argument)
        return
    ch.send("Nothing by that name found anywhere.\n")

def do_rstat(self, argument):
    ch=self

    argument, arg = read_word( argument )
    location = ch.in_room if not arg else find_location( ch, arg )
    if not location:
        ch.send("No such location.\n")
        return

    if not is_room_owner(ch,location) and ch.in_room != location \
    and room_is_private( location ) and not IS_TRUSTED(ch,IMPLEMENTOR):
        ch.send("That room is private right now.\n")
        return
    ch.send("Name: '%s'\nArea: '%s'\n" % (location.name, location.area.name ) )
    ch.send("Vnum: %d  Sector: %d  Light: %d  Healing: %d  Mana: %d\n" % (
              location.vnum,
              location.sector_type,
              location.light,
              location.heal_rate,
              location.mana_rate ) )
    ch.send("Room flags: %d.\nDescription:\n%s" % ( location.room_flags, location.description ) )
    if location.extra_descr:
        ch.send("Extra description keywords: '")
        [ch.send(ed.keyword + " ") for ed in location.extra_descr]
        ch.send("'.\n")

    ch.send("Characters:")
    for rch in location.people:
        if can_see(ch,rch):
            ch.send("%s " % rch.name if not IS_NPC(rch) else rch.short_descr)
    ch.send(".\nObjects:   ")
    for obj in location.contents:
        ch.send("'%s' " % obj.name )
    ch.send(".\n")
    for pexit in location.exit:
        if pexit:
            ch.send("Door: %d.  To: %d.  Key: %d.  Exit flags: %d.\nKeyword: '%s'.  Description: %s" % (
            door,
            -1 if pexit.u1.to_room == None else pexit.u1.to_room.vnum,
            pexit.key,
            pexit.exit_info,
            pexit.keyword,
            pexit.description if pexit.description else "(none).\n" ) )
    return

def do_ostat(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Stat what?\n")
        return
    obj = get_obj_world( ch, argument )
    if not obj:
        ch.send("Nothing like that in hell, earth, or heaven.\n")
        return

    ch.send("Name(s): %s\n" % obj.name )
    ch.send("Vnum: %d  Format: %s  Type: %s  Resets: %d\n" % (
        obj.pIndexData.vnum, "new" if obj.pIndexData.new_format else "old",
        item_name(obj.item_type), obj.pIndexData.reset_num ) )
    ch.send("Short description: %s\nLong description: %s\n" % (obj.short_descr, obj.description ))
    ch.send("Wear bits: %s\nExtra bits: %s\n" % (wear_bit_name(obj.wear_flags), extra_bit_name( obj.extra_flags ) ) )
    ch.send("Number: 1/%d  Weight: %d/%d/%d (10th pounds)\n" % ( get_obj_number( obj ),
        obj.weight, get_obj_weight( obj ),get_true_weight(obj) ) )
    ch.send("Level: %d  Cost: %d  Condition: %d  Timer: %d\n" % (obj.level, obj.cost, obj.condition, obj.timer ) )

    ch.send( "In room: %d  In object: %s  Carried by: %s  Wear_loc: %d\n" % (
        0 if not obj.in_room else obj.in_room.vnum,
        "(none)" if not obj.in_obj else obj.in_obj.short_descr,
        "(noone)" if not obj.carried_by else "someone" if not can_see(ch,obj.carried_by) else obj.carried_by.name,
        obj.wear_loc ) )
    ch.send("Values: %d %d %d %d %d\n" % (v for v in obj.value))
    # now give out vital statistics as per identify */

    if obj.item_type == ITEM_SCROLL \
    or obj.item_type == ITEM_POTION \
    or obj.item_type == ITEM_PILL:
        ch.send( "Level %d spells of:", obj.value[0] )
        for value in obj.value:
            if value and value in skill_table:
                ch.send(" '%s'" % skill_table[value].name)

        ch.send(".\n")
    elif obj.item_type == ITEM_WAND \
    or obj.item_type == ITEM_STAFF: 
        ch.send("Has %d(%d) charges of level %d" % (obj.value[1], obj.value[2], obj.value[0] ))
        ch.send(buf)
        
        if obj.value[3] and obj.value[3] in skill_table:
              ch.send(" '%s'" %  (skill_table[obj.value[3]].name) )
        ch.send(".\n")
    elif obj.item_type == ITEM_DRINK_CON:
          ch.send("It holds %s-colored %s.\n" % (liq_table[obj.value[2]].liq_color, liq_table[obj.value[2]].liq_name) )
    elif obj.item_type == ITEM_WEAPON:
          ch.send("Weapon type is ")
          weapon_type = { WEAPON_EXOTIC:"exotic", WEAPON_SWORD:"sword",
                          WEAPON_DAGGER:"dagger", WEAPON_SPEAR:"spear/staff",
                          WEAPON_MACE:"mace/club", WEAPON_AXE:"axe", 
                          WEAPON_FLAIL:"flail", WEAPON_WHIP:"whip",
                          WEAPON_POLEARM: "polearm" }
          if obj.value[0] not in weapon_type:
              ch.send("unknown\n")
          else:
              ch.send(weapon_type[obj.value[0]] + "\n")
          if obj.pIndexData.new_format:
              ch.send("Damage is %dd%d (average %d)\n" % (obj.value[1],obj.value[2], (1 + obj.value[2]) * obj.value[1] / 2))
          else:
              ch.send("Damage is %d to %d (average %d)\n" % ( obj.value[1], obj.value[2], ( obj.value[1] + obj.value[2] ) / 2 ) )
          ch.send("Damage noun is %s.\n" % (attack_table[obj.value[3]].noun if obj.value[3] in attack_table else "undefined") )
          if obj.value[4] > 0:  # weapon flags */
              ch.send("Weapons flags: %s\n" % weapon_bit_name(obj.value[4]))
    elif obj.item_type == ITEM_ARMOR:
        ch.send( "Armor class is %d pierce, %d bash, %d slash, and %d vs. magic\n" % (
              obj.value[0], obj.value[1], obj.value[2], obj.value[3] ) )
    elif obj.item_type == ITEM_CONTAINER:
        ch.send("Capacity: %d#  Maximum weight: %d#  flags: %s\n" % (obj.value[0], obj.value[3], cont_bit_name(obj.value[1])))
        if obj.value[4] != 100:
            ch.send("Weight multiplier: %d%%\n" % obj.value[4])

    if obj.extra_descr or obj.pIndexData.extra_descr:
        ch.send("Extra description keywords: '")
        extra_descr = obj.extra_descr
        extra_descr.extend(obj.pIndexData.extra_descr)
        for ed in extra_descr:
            ch.send(ed.keyword)
            ch.send(" ")
    affected = obj.affected
    if not obj.enchanted:
        affected.extend(obj.pIndexData.affected)
    for paf in affected:
        ch.send("Affects %s by %d, level %d" % (affect_loc_name( paf.location ), paf.modifier,paf.level ) )
        if paf.duration > -1:
            ch.send(", %d hours.\n" % paf.duration)
        else:
            ch.send(".\n")
        if paf.bitvector:
            if paf.where == TO_AFFECTS:
                ch.send("Adds %s affect.\n" % affect_bit_name(paf.bitvector))
            elif paf.where == TO_WEAPON:
                ch.send("Adds %s weapon flags.\n" % weapon_bit_name(paf.bitvector))
            elif paf.where == TO_OBJECT:
                ch.send("Adds %s object flag.\n" % extra_bit_name(paf.bitvector))
            elif paf.where == TO_IMMUNE:
                ch.send("Adds immunity to %s.\n" % imm_bit_name(paf.bitvector))
            elif paf.where == TO_RESIST:
                ch.send("Adds resistance to %s.\n" % imm_bit_name(paf.bitvector))
            elif paf.where == TO_VULN:
                ch.send("Adds vulnerability to %s.\n" % imm_bit_name(paf.bitvector))
            else:
                ch.send("Unknown bit %d: %d\n" % paf.where,paf.bitvector)

def do_mstat(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Stat whom?\n")
        return
    victim = get_char_world(ch, argument )
    if not victim:
        ch.send("They aren't here.\n")
        return
    ch.send("Name: %s\n" % victim.name)
    ch.send("Vnum: %d  Format: %s  Race: %s  Group: %d  Sex: %s  Room: %d\n" % (
                0 if not IS_NPC(victim) else victim.pIndexData.vnum,
                "pc" if not IS_NPC(victim) else "new" if victim.pIndexData.new_format else "old",
                victim.race.name,
                0 if not IS_NPC(victim) else victim.group, sex_table[victim.sex].name,
                0 if not victim.in_room else victim.in_room.vnum ) )

    if IS_NPC(victim):
        ch.send("Count: %d  Killed: %d\n" % (victim.pIndexData.count,victim.pIndexData.killed))
    ch.send("Str: %d(%d)  Int: %d(%d)  Wis: %d(%d)  Dex: %d(%d)  Con: %d(%d)\n" % (
                victim.perm_stat[STAT_STR], get_curr_stat(victim,STAT_STR),
                victim.perm_stat[STAT_INT], get_curr_stat(victim,STAT_INT),
                victim.perm_stat[STAT_WIS], get_curr_stat(victim,STAT_WIS),
                victim.perm_stat[STAT_DEX], get_curr_stat(victim,STAT_DEX),
                victim.perm_stat[STAT_CON], get_curr_stat(victim,STAT_CON)))
    ch.send("Hp: %d/%d  Mana: %d/%d  Move: %d/%d  Practices: %d\n" % (
                victim.hit, victim.max_hit,
                victim.mana, victim.max_mana,
                victim.move, victim.max_move,
                0 if IS_NPC(ch) else victim.practice ) )
    ch.send("Lv: %d  Class: %s  Align: %d  Gold: %ld  Silver: %ld  Exp: %d\n" % (
                victim.level,       
                "mobile" if IS_NPC(victim) else victim.guild.name,            
                victim.alignment, victim.gold, victim.silver, victim.exp ) )
    ch.send("Armor: pierce: %d  bash: %d  slash: %d  magic: %d\n" % (
                GET_AC(victim,AC_PIERCE), GET_AC(victim,AC_BASH),
                GET_AC(victim,AC_SLASH),  GET_AC(victim,AC_EXOTIC)))
    ch.send("Hit: %d  Dam: %d  Saves: %d  Size: %s  Position: %s  Wimpy: %d\n" % (
                GET_HITROLL(victim), GET_DAMROLL(victim), victim.saving_throw,
                size_table[victim.size].name, position_table[victim.position].name,
                victim.wimpy ))
    if IS_NPC(victim) and victim.pIndexData.new_format:
        ch.send("Damage: %dd%d  Message:  %s\n" % (
              victim.damage[DICE_NUMBER],victim.damage[DICE_TYPE],
              attack_table[victim.dam_type].noun) )
    ch.send("Fighting: %s\n" % (victim.fighting.name if victim.fighting else "(none)" ))
    if not IS_NPC(victim):
        ch.send( "Thirst: %d  Hunger: %d  Full: %d  Drunk: %d\n" % (
                    victim.pcdata.condition[COND_THIRST],
                    victim.pcdata.condition[COND_HUNGER],
                    victim.pcdata.condition[COND_FULL],
                    victim.pcdata.condition[COND_DRUNK] ))
    ch.send("Carry number: %d  Carry weight: %ld\n" % ( victim.carry_number, get_carry_weight(victim) / 10 ) )
    if not IS_NPC(victim):
        ch.send("Age: %d  Played: %d  Last Level: %d  Timer: %d\n",
                    get_age(victim), (int) (victim.played + current_time - victim.logon) / 3600, 
                    victim.pcdata.last_level, victim.timer )
    ch.send("Act: %s\n" % act_bit_name(victim.act))
    if victim.comm:
        ch.send("Comm: %s\n" % comm_bit_name(victim.comm))
    if IS_NPC(victim) and victim.off_flags:
        ch.send("Offense: %s\n" % off_bit_name(victim.off_flags))
    if victim.imm_flags:
        ch.send("Immune: %s\n" % imm_bit_name(victim.imm_flags))
    if victim.res_flags:
        ch.send("Resist: %s\n" % imm_bit_name(victim.res_flags))
    if victim.vuln_flags:
        ch.send("Vulnerable: %s\n" % imm_bit_name(victim.vuln_flags))
    ch.send("Form: %s\nParts: %s\n" % (form_bit_name(victim.form), part_bit_name(victim.parts)))
    if victim.affected_by:
        ch.send("Affected by %s\n" % affect_bit_name(victim.affected_by))
    ch.send("Master: %s  Leader: %s  Pet: %s\n" % (
                victim.master.name if victim.master else "(none)",
                victim.leader.name if victim.leader else "(none)",
                victim.pet.name if victim.pet else "(none)"))
    ch.send("Short description: %s\nLong  description: %s" % (  victim.short_descr,
                victim.long_descr if victim.long_descr else "(none)\n" ) )
    if IS_NPC(victim) and victim.spec_fun != None:
        ch.send("Mobile has special procedure %s.\n" % victim.spec_fun.__name__)

    for paf in victim.affected:
        ch.send( "Spell: '%s' modifies %s by %d for %d hours with bits %s, level %d.\n" % (
                    paf.type,
                    affect_loc_name( paf.location ),
                    paf.modifier,
                    paf.duration,
                    affect_bit_name( paf.bitvector ),
                    paf.level))
    
# ofind and mfind replaced with vnum, vnum skill also added */
def do_vnum(self, argument):
    ch=self
    string, arg = read_word(argument)
 
    if not arg:
        ch.send("Syntax:\n")
        ch.send("  vnum obj <name>\n")
        ch.send("  vnum mob <name>\n")
        ch.send("  vnum skill <skill or spell>\n")
        return
    if arg == "obj":
        ch.do_ofind(string)
        return

    if arg == "mob" or arg == "char":
        ch.do_mfind(string)
        return

    if arg == "skill" or arg == "spell":
        ch.do_slookup(string)
        return
    # do both */
    ch.do_mfind(argument)
    ch.do_ofind(argument)

def do_mfind(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Find whom?\n")
        return
    fAll  = False # !str_cmp( arg, "all" ) */
    found = False
    nMatch  = 0


     #* Yeah, so iterating over all vnum's takes 10,000 loops.
     #* Get_mob_index is fast, and I don't feel like threading another link.
     #* Do you?
     # -- Furey
    for pMobIndex in mob_index_hash:
        if fAll or argument in pMobIndex.player_name:
            found = True
            ch.send("[%5d] %s\n" % (pMobIndex.vnum, pMobIndex.short_descr))
    if not found:
        ch.send("No mobiles by that name.\n")

    return

def do_ofind(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Find what?\n")
        return

    fAll  = False # !str_cmp( arg, "all" ) */
    found = False
    nMatch  = 0
    
    # * Yeah, so iterating over all vnum's takes 10,000 loops.
    # * Get_obj_index is fast, and I don't feel like threading another link.
    # * Do you?
    # * -- Furey
    for pObjIndex in obj_index_hash:
        if fAll or argument in pObjIndex.name:
            found = True
            ch.send("[%5d] %s\n" % (pObjIndex.vnum, pObjIndex.short_descr))
    if not found:
        ch.send("No objects by that name.\n")
    return

def do_owhere(self, argument):
    ch=self
    found = False
    number = 0
    max_found = 200

    if not argument:
        ch.send("Find what?\n")
        return
    for obj in object_list:
        if not can_see_obj( ch, obj ) or argument not in obj.name or ch.level < obj.level:
            continue
        found = True
        number += 1
        in_obj = obj.in_obj
        while in_obj.in_obj: in_obj = in_obj.in_obj
           
        if in_obj.carried_by and can_see(ch,in_obj.carried_by) and in_obj.carried_by.in_room:
            ch.send("%3d) %s is carried by %s [Room %d]\n" % (
                        number, obj.short_descr,PERS(in_obj.carried_by, ch), in_obj.carried_by.in_room.vnum ) )
        elif in_obj.in_room and can_see_room(ch,in_obj.in_room):
            ch.send("%3d) %s is in %s [Room %d]\n" % (
                        number, obj.short_descr,in_obj.in_room.name, in_obj.in_room.vnum) )
        else:
            ch.send("%3d) %s is somewhere\n" % (number, obj.short_descr))
 
        if number >= max_found:
            break
 
    if not found:
        ch.send("Nothing like that in heaven or earth.\n")

def do_mwhere(self, argument):
    ch=self
    count = 0
    if not argument:
        # show characters logged */
        for d in descriptor_list:
            if d.character and d.connected == con_playing \
            and d.character.in_room and can_see(ch,d.character) \
            and can_see_room(ch,d.character.in_room):
                victim = d.character
                count+=1
            if d.original:
                ch.send("%3d) %s (in the body of %s) is in %s [%d]\n" % (
                            count, d.original.name,victim.short_descr,
                            victim.in_room.name,victim.in_room.vnum))
            else:
                ch.send("%3d) %s is in %s [%d]\n" % (
                            count, victim.name,victim.in_room.name, victim.in_room.vnum) )
        return
    found = False
    for victim in char_list:
        if victim.in_room and  argument in victim.name:
            found = True
            count += 1
            ch.send("%3d) [%5d] %-28s [%5d] %s\n" % (
                        count, 0 if not IS_NPC(victim) else victim.pIndexData.vnum,
                        victim.short_descr if IS_NPC(victim) else victim.name,
                        victim.in_room.vnum,
                        victim.in_room.name ))
    if found:
        act( "You didn't find any $T.", ch, None, argument, TO_CHAR )

def do_reboo(self, argument):
    ch=self
    ch.send("If you want to REBOOT, spell it out.\n")
    return


def do_reboot(self, argument):
    ch=self
    if ch.invis_level < LEVEL_HERO:
        ch.do_echo("Reboot by %s." % ch.name )
    merc_down = True
    for d in descriptor_list[:]:
        vch = CH(d)
        if vch:
            save_char_obj(vch)
            close_socket(d)

def do_shutdow(self, argument):
    ch=self
    ch.send("If you want to SHUTDOWN, spell it out.\n")
    return

def do_shutdown(self, argument):
    ch=self
    ch=self
    if ch.invis_level < LEVEL_HERO:
        ch.do_echo("Shutdown by %s." % ch.name )
    merc_down = True
    for d in descriptor_list[:]:
        vch = CH(d)
        if vch:
            save_char_obj(vch)
            close_socket(d)

def do_protect(self, argument):
    ch=self
    if not argument:
        ch.send("Protect whom from snooping?\n")
        return
    victim = get_char_world(ch, argument)
    if not victim:
        ch.send("You can't find them.\n")
        return
    if IS_SET(victim.comm, COMM_SNOOP_PROOF):
        act("$N is no longer snoop-proof.",ch,None,victim,TO_CHAR,POS_DEAD)
        victim.send("Your snoop-proofing was just removed.\n")
        REMOVE_BIT(victim.comm,COMM_SNOOP_PROOF)
    else:
        act("$N is now snoop-proof.",ch,None,victim,TO_CHAR,POS_DEAD)
        victim.send("You are now immune to snooping.\n")
        SET_BIT(victim.comm,COMM_SNOOP_PROOF)

def do_snoop(self, argument):
    ch=self
    argument, arg = read_word( argument )

    if not arg:
        ch.send("Snoop whom?\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if not victim.desc:
        ch.send("No descriptor to snoop.\n")
        return
    if victim == ch:
        ch.send("Cancelling all snoops.\n")
        wiznet("$N stops being such a snoop.", ch,None,WIZ_SNOOPS,WIZ_SECURE,get_trust(ch))
        for d in descriptor_list:
            if d.snoop_by == ch.desc:
                d.snoop_by = None
        return
    if victim.desc.snoop_by:
        ch.send("Busy already.\n")
        return
    if not is_room_owner(ch,victim.in_room) and ch.in_room != victim.in_room \
    and room_is_private(victim.in_room) and not IS_TRUSTED(ch,IMPLEMENTOR):
        ch.send("That character is in a private room.\n")
        return
    if get_trust( victim ) >= get_trust( ch ) or IS_SET(victim.comm,COMM_SNOOP_PROOF):
        ch.send("You failed.\n")
        return
    if ch.desc:
        d = ch.desc.snoop_by
        while d:
            if d.character == victim or d.original == victim:
                ch.send("No snoop loops.\n")
                return
            d = d.snoop_by
    victim.desc.snoop_by = ch.desc
    buf = "$N starts snooping on %s" % (victim.short_descr if IS_NPC(ch) else victim.name)
    wiznet(buf,ch,None,WIZ_SNOOPS,WIZ_SECURE,get_trust(ch))
    ch.send("Ok.\n")
    return

def do_switch(self, argument):
    ch=self
    argument, arg = read_word( argument )
    
    if not arg:
        ch.send("Switch into whom?\n")
        return
    if not ch.desc == None:
        return
    if ch.desc.original:
        ch.send("You are already switched.\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim == ch:
        ch.send("Ok.\n")
        return
    if not IS_NPC(victim):
        ch.send("You can only switch into mobiles.\n")
        return
    if not is_room_owner(ch,victim.in_room) and ch.in_room != victim.in_room \
    and room_is_private(victim.in_room) and not IS_TRUSTED(ch,IMPLEMENTOR):
        ch.send("That character is in a private room.\n")
        return
    if victim.desc:
        ch.send("Character in use.\n")
        return
    
    wiznet("$N switches into %s" % victim.short_descr,ch,None,WIZ_SWITCHES,WIZ_SECURE,get_trust(ch))

    ch.desc.character = victim
    ch.desc.original  = ch
    victim.desc        = ch.desc
    ch.desc            = None
    # change communications to match */
    if ch.prompt:
        victim.prompt = ch.prompt
    victim.comm = ch.comm
    victim.lines = ch.lines
    victim.send("Ok.\n")
    return

def do_return(self, argument):
    ch=self
    if not ch.desc:
        return
    if not ch.desc.original:
        ch.send("You aren't switched.\n")
        return
    ch.send("You return to your original body. Type replay to see any missed tells.\n")
    if ch.prompt:
        ch.prompt = ''
    wiznet("$N returns from %s." % ch.short_descr,ch.desc.original,0,WIZ_SWITCHES,WIZ_SECURE,get_trust(ch))
    ch.desc.character       = ch.desc.original
    ch.desc.original        = None
    ch.desc.character.desc = ch.desc 
    ch.desc                  = None
    return

# trust levels for load and clone */
def obj_check (ch, obj):
    if IS_TRUSTED(ch,GOD) \
    or (IS_TRUSTED(ch,IMMORTAL) and obj.level <= 20 and obj.cost <= 1000) \
    or (IS_TRUSTED(ch,DEMI)     and obj.level <= 10 and obj.cost <= 500) \
    or (IS_TRUSTED(ch,ANGEL)    and obj.level <=  5 and obj.cost <= 250) \
    or (IS_TRUSTED(ch,AVATAR)   and obj.level ==  0 and obj.cost <= 100):
        return True
    else:
        return False

# for clone, to insure that cloning goes many levels deep */
def recursive_clone(ch, obj, clone):
    for c_obj in obj.contains:
        if obj_check(ch,c_obj):
            t_obj = create_object(c_obj.pIndexData,0)
            clone_object(c_obj,t_obj)
            obj_to_obj(t_obj,clone)
            recursive_clone(ch,c_obj,t_obj)

# command that is similar to load */
def do_clone(self, argument):
    ch=self
    rest,arg = read_word(argument)
    mob = None
    obj = None
    if not arg:
        ch.send("Clone what?\n")
        return
    if "object".startswith(arg):
        mob = None
        obj = get_obj_here(ch,rest)
        if not obj:
            ch.send("You don't see that here.\n")
            return
    elif "character".startswith(arg) or "mobile".startswith(arg):
        obj = None
        mob = get_char_room(ch,rest)
        if not mob:
            ch.send("You don't see that here.\n")
            return
    else: # find both */
        mob = get_char_room(ch,argument)
        obj = get_obj_here(ch,argument)
        if mob == None and obj == None:
            ch.send("You don't see that here.\n")
            return
  
    # clone an object */
    if obj:
        if not obj_check(ch,obj):
            ch.send(    "Your powers are not great enough for such a task.\n")
            return
        clone = create_object(obj.pIndexData,0) 
        clone_object(obj,clone)
        if obj.carried_by:
            obj_to_char(clone,ch)
        else:
            obj_to_room(clone,ch.in_room)
        recursive_clone(ch,obj,clone)

        act("$n has created $p.",ch,clone,None,TO_ROOM)
        act("You clone $p.",ch,clone,None,TO_CHAR)
        wiznet("$N clones $p.",ch,clone,WIZ_LOAD,WIZ_SECURE,get_trust(ch))
        return
    elif mob:
        if not IS_NPC(mob):
            ch.send("You can only clone mobiles.\n")
            return
        if (mob.level > 20 and not IS_TRUSTED(ch,GOD)) \
        or (mob.level > 10 and not IS_TRUSTED(ch,IMMORTAL)) \
        or (mob.level >  5 and not IS_TRUSTED(ch,DEMI)) \
        or (mob.level >  0 and not IS_TRUSTED(ch,ANGEL)) \
        or not IS_TRUSTED(ch,AVATAR):
            ch.send(    "Your powers are not great enough for such a task.\n")
            return
        clone = create_mobile(mob.pIndexData)
        clone_mobile(mob,clone) 
  
        for obj in mob.carrying:
            if obj_check(ch,obj):
                new_obj = create_object(obj.pIndexData,0)
                clone_object(obj,new_obj)
                recursive_clone(ch,obj,new_obj)
                obj_to_char(new_obj,clone)
                new_obj.wear_loc = obj.wear_loc
        char_to_room(clone,ch.in_room)
        act("$n has created $N.",ch,None,clone,TO_ROOM)
        act("You clone $N.",ch,None,clone,TO_CHAR)
        wiznet("$N clones %s." % clone.short_descr,ch,None,WIZ_LOAD,WIZ_SECURE,get_trust(ch))
        return

# RT to replace the two load commands */
def do_load(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Syntax:\n")
        ch.send("  load mob <vnum>\n")
        ch.send("  load obj <vnum> <level>\n")
        return
    if arg == "mob" or arg == "char":
        ch.do_mload(argument)
        return
    if arg == "obj":
        ch.do_oload(argument)
        return
    # echo syntax */
    ch.do_load("")

def do_mload(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg or not arg.is_digit():
        ch.send("Syntax: load mob <vnum>.\n")
        return
    vnum = int(arg)
    if vnum not in mob_index_hash:
        ch.send("No mob has that vnum.\n")
        return
    pMobIndex = mob_index_hash[vnum]
    victim = create_mobile( pMobIndex )
    char_to_room( victim, ch.in_room )
    act( "$n has created $N!", ch, None, victim, TO_ROOM )
    wiznet("$N loads %s." % victim.short_descr,ch,None,WIZ_LOAD,WIZ_SECURE,get_trust(ch))
    ch.send("Ok.\n")
    return

def do_oload(self, argument):
    ch=self
    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)

    if not arg1 or not arg1.is_digit():
        ch.send("Syntax: load obj <vnum> <level>.\n")
        return
    level = get_trust(ch) # default */
  
    if arg2:  # load with a level */
        if not arg2.is_digit():
            ch.send("Syntax: oload <vnum> <level>.\n")
            return
        level = int(arg2)
        if level < 0 or level > get_trust(ch):
            ch.send("Level must be be between 0 and your level.\n")
            return
    vnum = int(arg1)
    if vnum not in obj_index_hash:
        ch.send("No object has that vnum.\n")
        return
    obj = create_object( pObjIndex, level )
    if CAN_WEAR(obj, ITEM_TAKE):
        obj_to_char( obj, ch )
    else:
        obj_to_room( obj, ch.in_room )
    act( "$n has created $p!", ch, obj, None, TO_ROOM )
    wiznet("$N loads $p.",ch,obj,WIZ_LOAD,WIZ_SECURE,get_trust(ch))
    ch.send("Ok.\n")
    return

def do_purge(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        for victim in ch.in_room.people[:]:
            if IS_NPC(victim) and not IS_SET(victim.act,ACT_NOPURGE) and victim != ch: # safety precaution */ )
                extract_char( victim, True )
        for obj in ch.in_room.contents[:]:
            if not IS_OBJ_STAT(obj,ITEM_NOPURGE):
                extract_obj( obj )
        act( "$n purges the room!", ch, None, None, TO_ROOM)
        ch.send("Ok.\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if not IS_NPC(victim):
        if ch == victim:
            ch.send("Ho ho ho.\n")
            return
        if get_trust(ch) <= get_trust(victim):
            ch.send("Maybe that wasn't a good idea...\n")
            victim.send("%s tried to purge you!\n" % ch.name)
            return
        act("$n disintegrates $N.",ch,0,victim,TO_NOTVICT)

        if victim.level > 1:
            save_char_obj( victim )
        d = victim.desc
        extract_char( victim, True )
        if d:
            close_socket( d )
        return
    act( "$n purges $N.", ch, None, victim, TO_NOTVICT )
    extract_char( victim, True )
    return

def do_advance(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1 or not arg2 or not arg2.is_digit():
        ch.send("Syntax: advance <char> <level>.\n")
        return
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("That player is not here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    level = int(arg2)
    if level < 1 or level > MAX_LEVEL:
        ch.send("Level must be 1 to %d.\n" % MAX_LEVEL)
        return
    if level > get_trust( ch ):
        ch.send("Limited to your trust level.\n")
        return
    
     #* Lower level:
     #*   Reset to level 1.
     #*   Then raise again.
     #*   Currently, an imp can lower another imp.
     #*   -- Swiftest
     
    if level <= victim.level:
        ch.send("Lowering a player's level!\n")
        victim.send("**** OOOOHHHHHHHHHH  NNNNOOOO ****\n")
        temp_prac = victim.practice
        victim.level    = 1
        victim.exp      = exp_per_level(victim,victim.pcdata.points)
        victim.max_hit  = 10
        victim.max_mana = 100
        victim.max_move = 100
        victim.practice = 0
        victim.hit      = victim.max_hit
        victim.mana     = victim.max_mana
        victim.move     = victim.max_move
        advance_level( victim, True )
        victim.practice = temp_prac
    else:
        ch.send("Raising a player's level!\n")
        victim.send("**** OOOOHHHHHHHHHH  YYYYEEEESSS ****\n")
    for iLevel in range(victim.level, level):
        victim.level += 1
        advance_level( victim,True)
    victim.send("You are now level %d.\n" % victim.level)
    victim.exp   = exp_per_level(victim,victim.pcdata.points) * max( 1, victim.level )
    victim.trust = 0
    save_char_obj(victim)
    return

def do_trust(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1 or not arg2 or not arg2.is_digit():
        ch.send("Syntax: trust <char> <level>.\n")
        return
    
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("That player is not here.\n")
        return
    level = int(arg2)
    if level < 0 or level > MAX_LEVEL:
        ch.send("Level must be 0 (reset) or 1 to %d.\n" % MAX_LEVEL)
        return
    if level > get_trust( ch ):
        ch.send("Limited to your trust.\n")
        return
    victim.trust = level
    return

def do_restore(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg or arg == "room":
        # cure room */
        for vch in ch.in_room.people:
            affect_strip(vch,"plague")
            affect_strip(vch,"poison")
            affect_strip(vch,"blindness")
            affect_strip(vch,"sleep")
            affect_strip(vch,"curse")
            
            vch.hit  = vch.max_hit
            vch.mana = vch.max_mana
            vch.move = vch.max_move
            update_pos( vch)
            act("$n has restored you.",ch,None,vch,TO_VICT)
        wiznet("$N restored room %d." % ch.in_room.vnum,ch,None,WIZ_RESTORE,WIZ_SECURE,get_trust(ch))
        ch.send("Room restored.\n")
        return
    if get_trust(ch) >= MAX_LEVEL - 1 and arg == "all":
        # cure all */
        for d in descriptor_list:
            victim = d.character
            if victim == None or IS_NPC(victim):
                continue
                
            affect_strip(victim,"plague")
            affect_strip(victim,"poison")
            affect_strip(victim,"blindness")
            affect_strip(victim,"sleep")
            affect_strip(victim,"curse")
            
            victim.hit   = victim.max_hit
            victim.mana  = victim.max_mana
            victim.move  = victim.max_move
            update_pos( victim)
            if victim.in_room:
                act("$n has restored you.",ch,None,victim,TO_VICT)
        ch.send("All active players restored.\n")
        return


    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    affect_strip(victim,"plague")
    affect_strip(victim,"poison")
    affect_strip(victim,"blindness")
    affect_strip(victim,"sleep")
    affect_strip(victim,"curse")
    victim.hit  = victim.max_hit
    victim.mana = victim.max_mana
    victim.move = victim.max_move
    update_pos( victim )
    act( "$n has restored you.", ch, None, victim, TO_VICT )
    buf = "$N restored %s", (victim.short_descr if IS_NPC(victim) else victim.name)
    wiznet(buf,ch,None,WIZ_RESTORE,WIZ_SECURE,get_trust(ch))
    ch.send("Ok.\n")
    return
  
def do_freeze(self, argument):
    ch=self
    argument, arg = read_word( argument)

    if not arg:
        ch.send("Freeze whom?\n")
        return

    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
        ch.send("You failed.\n")
        return

    if IS_SET(victim.act, PLR_FREEZE):
        REMOVE_BIT(victim.act, PLR_FREEZE)
        victim.send("You can play again.\n")
        ch.send("FREEZE removed.\n")
        wiznet("$N thaws %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.act, PLR_FREEZE)
        victim.send("You can't do ANYthing!\n")
        ch.send("FREEZE set.\n")
        wiznet("$N puts %s in the deep freeze." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)

    save_char_obj( victim )
    return

def do_log(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Log whom?\n")
        return
    if arg == "all" :
        if fLogAll:
            fLogAll = False
            ch.send("Log ALL off.\n")
        else:
            fLogAll = True
            ch.send("Log ALL on.\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    
    # * No level check, gods can log anyone.
    if IS_SET(victim.act, PLR_LOG):
        REMOVE_BIT(victim.act, PLR_LOG)
        ch.send("LOG removed.\n")
    else:
        SET_BIT(victim.act, PLR_LOG)
        ch.send("LOG set.\n")
    return
def do_noemote(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Noemote whom?\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
        ch.send("You failed.\n")
        return
    if IS_SET(victim.comm, COMM_NOEMOTE):
        REMOVE_BIT(victim.comm, COMM_NOEMOTE)
        victim.send("You can emote again.\n")
        ch.send("NOEMOTE removed.\n")
        wiznet("$N restores emotes to %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOEMOTE)
        victim.send("You can't emote!\n")
        ch.send("NOEMOTE set.\n")
        wiznet("$N revokes %s's emotes." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return

def do_noshout(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Noshout whom?\n")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
          ch.send("You failed.\n")
          return
    if IS_SET(victim.comm, COMM_NOSHOUT):
        REMOVE_BIT(victim.comm, COMM_NOSHOUT)
        victim.send("You can shout again.\n")
        ch.send("NOSHOUT removed.\n")
        wiznet("$N restores shouts to %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOSHOUT)
        victim.send("You can't shout!\n")
        ch.send("NOSHOUT set.\n")
        wiznet("$N revokes %s's shouts." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return
def do_notell(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Notell whom?")
        return
    victim = get_char_world(ch, arg )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if get_trust( victim ) >= get_trust( ch ):
        ch.send("You failed.\n")
        return
    if IS_SET(victim.comm, COMM_NOTELL):
        REMOVE_BIT(victim.comm, COMM_NOTELL)
        victim.send("You can tell again.\n")
        ch.send("NOTELL removed.\n")
        wiznet("$N restores tells to %s." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    else:
        SET_BIT(victim.comm, COMM_NOTELL)
        victim.send("You can't tell!\n")
        ch.send("NOTELL set.\n")
        wiznet("$N revokes %s's tells." % victim.name,ch,None,WIZ_PENALTIES,WIZ_SECURE,0)
    return

def do_peace(self, argument):
    ch=self
    for rch in ch.in_room.people:
        if rch.fighting:
            stop_fighting( rch, True )
        if IS_NPC(rch) and IS_SET(rch.act,ACT_AGGRESSIVE):
            REMOVE_BIT(rch.act,ACT_AGGRESSIVE)
    ch.send("Ok.\n")
    return

def do_wizlock(self, argument):
    ch=self
    global WIZLOCK

    if not WIZLOCK:
        wiznet("$N has wizlocked the game.",ch,None,0,0,0)
        ch.send("Game wizlocked.\n")
        WIZLOCK = True
    else:
        wiznet("$N removes wizlock.",ch,None,0,0,0)
        ch.send("Game un-wizlocked.\n")
        WIZLOCK = False
    return
# RT anti-newbie code */
def do_newlock(self, argument):
    ch=self
    global NEWLOCK
    if not NEWLOCK:
        wiznet("$N locks out new characters.",ch,None,0,0,0)
        ch.send("New characters have been locked out.\n")
        NEWLOCK = True
    else:
        wiznet("$N allows new characters back in.",ch,None,0,0,0)
        ch.send("Newlock removed.\n")
        NEWLOCK = False 
    return

def do_slookup(self, argument):
    ch=self
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Lookup which skill or spell?\n")
        return
    if arg == "all" :
        for sn, skill in skill_table.items():
            ch.send("Sn: %15s  Slot: %3d  Skill/spell: '%s'\n", sn, skill.slot, skill.name )
    else:
        skill = prefix_lookup(skill_table, arg)
        if not skill:
            ch.send("No such skill or spell.\n")
            return
  
        ch.send("Sn: %15s  Slot: %3d  Skill/spell: '%s'\n", skill.name, skill.slot, skill.name )

# RT set replaces sset, mset, oset, and rset */
def do_set(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Syntax:\n")
        ch.send("  set mob   <name> <field> <value>\n")
        ch.send("  set obj   <name> <field> <value>\n")
        ch.send("  set room  <room> <field> <value>\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        return
    if "character".startswith(arg) or "mobile".startswith(arg):
        ch.do_mset(argument)
        return
    if "spell".startswith(arg) or "skill".startswith(arg):
        ch.do_sset(argument)
        return
    if "object".startswith(arg):
        ch.do_oset(argument)
        return
    if "room".startswith(arg):
        ch.do_rset(argument)
        return
    # echo syntax */
    ch.do_set("")

def do_sset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    argument, arg3  = read_word(argument)

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        ch.send("  set skill <name> all <value>\n")  
        ch.send("   (use the name of the skill, not the number)\n")
        return
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_NPC(victim):
        ch.send("Not on NPC's.\n")
        return
    fAll = arg2 == "all"
    sn = prefix_lookup(skill_table,arg2)
    if not fAll and not sn:
        ch.send("No such skill or spell.\n")
        return
    sn = sn.name
    # Snarf the value.
    if not arg3.is_digit():
        ch.send("Value must be numeric.\n")
        return
    value = int( arg3 )
    if value < 0 or value > 100:
        ch.send("Value range is 0 to 100.\n")
        return

    if fAll:
        for sn in skill_table.keys():
            victim.pcdata.learned[sn] = value
    else:
        victim.pcdata.learned[sn] = value

def do_mset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set char <name> <field> <value>\n") 
        ch.send("  Field being one of:\n")
        ch.send("    str int wis dex con sex class level\n")
        ch.send("    race group gold silver hp mana move prac\n")
        ch.send("    align train thirst hunger drunk full\n")
        return
    victim = get_char_world(ch, arg1 )
    if not victim:
        ch.send("They aren't here.\n")
        return
    # clear zones for mobs */
    victim.zone = None
    #* Snarf the value (which need not be numeric).
    value = int(arg3) if arg3.is_digit() else -1
    #* Set something.
    if arg2 == "str" :
        if value < 3 or value > get_max_train(victim,STAT_STR):
            ch.send( "Strength range is 3 to %d\n." % get_max_train(victim,STAT_STR))
            return
        victim.perm_stat[STAT_STR] = value
        return
    if arg2 == "int" :
        if value < 3 or value > get_max_train(victim,STAT_INT):
            ch.send("Intelligence range is 3 to %d.\n" % get_max_train(victim,STAT_INT))
            return
        victim.perm_stat[STAT_INT] = value
        return
    if arg2 == "wis" :
        if value < 3 or value > get_max_train(victim,STAT_WIS):
            ch.send("Wisdom range is 3 to %d.\n" % get_max_train(victim,STAT_WIS))
            return
        victim.perm_stat[STAT_WIS] = value
        return
    if arg2 == "dex" :
        if value < 3 or value > get_max_train(victim,STAT_DEX):
            ch.send("Dexterity range is 3 to %d.\n" % get_max_train(victim,STAT_DEX))
            return
        victim.perm_stat[STAT_DEX] = value
        return
    if arg2 == "con" :
        if value < 3 or value > get_max_train(victim,STAT_CON):
            ch.send("Constitution range is 3 to %d.\n" % get_max_train(victim,STAT_CON))
            return
        victim.perm_stat[STAT_CON] = value
        return
    if "sex".startswith(arg2):
        if value < 0 or value > 2:
            ch.send("Sex range is 0 to 2.\n")
            return
        victim.sex = value
        if not IS_NPC(victim):
            victim.pcdata.true_sex = value
        return
    if "class".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Mobiles have no class.\n")
            return
        guild = prefix_lookup(guild_table, arg3)
        if not guild:
            ch.send("Possible classes are: " )
            for guild in guild_table.keys():
                ch.send("%s " % guild )
            ch.send(".\n" )
            return
        victim.guild = guild
        return
    if "level".startswith(arg2):
        if not IS_NPC(victim):
            ch.send("Not on PC's.\n")
            return
        if value < 0 or value > MAX_LEVEL:
            ch.send("Level range is 0 to %d.\n" % MAX_LEVEL)
            return
        victim.level = value
        return
    if "gold".startswith(arg2):
        victim.gold = value
        return
    if "silver".startswith(arg2):
        victim.silver = value
        return
    if "hp".startswith(arg2):
        if value < -10 or value > 30000:
            ch.send("Hp range is -10 to 30,000 hit points.\n")
            return
        victim.max_hit = value
        if not IS_NPC(victim):
            victim.pcdata.perm_hit = value
        return
    if "mana".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Mana range is 0 to 30,000 mana points.\n")
            return
        victim.max_mana = value
        if not IS_NPC(victim):
            victim.pcdata.perm_mana = value
        return
    if "move".startswith(arg2):
        if value < 0 or value > 30000:
            ch.send("Move range is 0 to 30,000 move points.\n")
            return
        victim.max_move = value
        if not IS_NPC(victim):
            victim.pcdata.perm_move = value
        return
    if "practice".startswith(arg2):
        if value < 0 or value > 250:
            ch.send("Practice range is 0 to 250 sessions.\n")
            return
        victim.practice = value
        return
    if "train".startswith(arg2):
        if value < 0 or value > 50:
            ch.send("Training session range is 0 to 50 sessions.\n")
            return
        victim.train = value
        return
    if "align".startswith(arg2):
        if value < -1000 or value > 1000:
            ch.send("Alignment range is -1000 to 1000.\n")
            return
        victim.alignment = value
        return
    if "thirst".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Thirst range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_THIRST] = value
        return
    if "drunk".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Drunk range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_DRUNK] = value
        return
    if "full".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_FULL] = value
        return
    if "hunger".startswith(arg2):
        if IS_NPC(victim):
            ch.send("Not on NPC's.\n")
            return
        if value < -1 or value > 100:
            ch.send("Full range is -1 to 100.\n")
            return
        victim.pcdata.condition[COND_HUNGER] = value
        return
    if "race".startswith(arg2):
        race = prefix_lookup(race_table, arg3)
        if not race:
            ch.send("That is not a valid race.\n")
            return
        if not IS_NPC(victim) and race.name not in pc_race_table:
            ch.send("That is not a valid player race.\n")
            return
        victim.race = race
        return
    if "group".startswith(arg2):
        if not IS_NPC(victim):
            ch.send("Only on NPCs.\n")
            return
        victim.group = value
        return
    #* Generate usage message.
    ch.do_mset("" )

def do_string(self, argument):
    ch=self
    argument, type  = read_word(argument)
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

    if not type or not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  string char <name> <field> <string>\n")
        ch.send("    fields: name short long desc title spec\n")
        ch.send("  string obj  <name> <field> <string>\n")
        ch.send("    fields: name short long extended\n")
        return
    if "mobile".startswith(type) or "character".startswith(type):
        victim = get_char_world(ch, arg1 )
        if not victim:
            ch.send("They aren't here.\n")
            return
        # clear zone for mobs */
        victim.zone = None
        # string something */
        if "name".startswith(arg2):
            if not IS_NPC(victim):
                ch.send("Not on PC's.\n")
                return
            victim.name = arg3
            return
        if "description".startswith(arg2):
            victim.description = arg3
            return
        if "short".startswith(arg2):
            victim.short_descr = arg3
            return
        if "long".startswith(arg2):
            victim.long_descr = arg3 + "\n"
            return
        if "title".startswith(arg2):
            if IS_NPC(victim):
                ch.send("Not on NPC's.\n")
                return
            set_title( victim, arg3 )
            return
        if "spec".startswith(arg2):
            if not IS_NPC(victim):
                ch.send("Not on PC's.\n")
                return
            spec = prefix_lookup(spec_table, arg3)
            if not spec:
                ch.send("No such spec fun.\n")
                return
            victim.spec_fun = spec
            ch.send("spec_fun set.\r\n")
            return
    if "object".startswith(type):
        # string an obj */
        obj = get_obj_world( ch, arg1 )
        if not obj:
            ch.send("Nothing like that in heaven or earth.\n")
            return
        if "name".startswith(arg2):
            obj.name = arg3
            return
        if "short".startswith(arg2):
            obj.short_descr = arg3
            return
        if "long".startswith(arg2):
            obj.description = arg3
            return
        if "extended".startswith(arg2) or  "ed".startswith(arg2):
            argument, arg3  = read_word(argument)
            if argument == None:
                ch.send( "Syntax: oset <object> ed <keyword> <string>\n")
                return
            argument += "\n"
            ed = EXTRA_DESCR_DATA()
            ed.keyword = arg3
            ed.description = argument
            obj.extra_descr.append(ed)
            return
    # echo bad use message */
    ch.do_string("")

def do_oset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    arg3 = argument

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set obj <object> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    value0 value1 value2 value3 value4 (v1-v4)\n")
        ch.send("    extra wear level weight cost timer\n")
        return
    obj = get_obj_world(ch, arg1)
    if not obj:
        ch.send("Nothing like that in heaven or earth.\n")
        return
    #
    #* Snarf the value (which need not be numeric).
    value = int( arg3 ) if arg3.is_digit else -1
    if value == -1:
        ch.do_oset("")
    #* Set something.
    if arg2 == "value0" or arg2 == "v0":
        obj.value[0] = min(50,value)
        return
    if arg2 == "value1" or arg2 == "v1":
        obj.value[1] = value
        return
    if arg2 == "value2" or arg2 == "v2":
        obj.value[2] = value
        return
    if arg2 == "value3" or arg2 == "v3" :
        obj.value[3] = value
        return
    if arg2 == "value4" or arg2 == "v4":
        obj.value[4] = value
        return
    if "extra".startswith(arg2):
        obj.extra_flags = value
        return
    if "wear".startswith(arg2):
        obj.wear_flags = value
        return
    if "level".startswith(arg2):
        obj.level = value
        return
    if "weight" .startswith(arg2):
        obj.weight = value
        return
    if "cost" .startswith(arg2):
        obj.cost = value
        return
    if "timer" .startswith(arg2):
        obj.timer = value
        return
     
    #* Generate usage message.
    ch.do_oset("" )
    return

def do_rset(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)
    strcpy( arg3, argument )

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set room <location> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    flags sector\n")
        return
    location = find_location( ch, arg1 )
    if not location:
        ch.send("No such location.\n")
        return
    if not is_room_owner(ch,location) and ch.in_room != location \
    and room_is_private(location) and not IS_TRUSTED(ch,IMPLEMENTOR):
        ch.send("That room is private right now.\n")
        return

    #* Snarf the value.
    if not arg3.is_digit():
        ch.send("Value must be numeric.\n")
        return
    value = int( arg3 )

    #* Set something.
    if "flags".startswith(arg2):
        location.room_flags  = value
        return
    if "sector".startswith(arg2):
        location.sector_type = value
        return
    #  Generate usage message.
    ch.do_rset("")
    return

def do_sockets(self, argument):
    ch=self
    count = 0
    argument, arg = read_word(argument)
    for d in descriptor_list:
        if d.character and can_see( ch, d.character ) \
        and (not arg or arg not in  d.character.name) \
        or (d.original and is_name(arg,d.original.name)):
            count+=1
            ch.send("[%3d %2d] %s@%s\n" % (
                    d.descriptor,
                    d.connected,
                    d.original.name if d.original else d.character.name if d.character else "(none)",
                    d.host ) )
    if count == 0:
        ch.send("No one by that name is connected.\n")
        return
    ch.send("%d user%s\n" % (count, "" if count == 1 else "s" ) )
    return
#
# * Thanks to Grodyn for pointing out bugs in this function.
def do_force(self, argument):
    ch=self
    argument, arg  = read_word(argument)

    if not arg or not argument:
        ch.send("Force whom to do what?\n")
        return
    temp, arg2 = read_word(argument)
    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    buf = "$n forces you to '%s'." % argument
    if arg == "all":
        if get_trust(ch) < MAX_LEVEL - 3:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and get_trust( vch ) < get_trust( ch ):
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    elif arg == "players":
        if get_trust(ch) < MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and get_trust( vch ) < get_trust( ch ) and vch.level < LEVEL_HERO:
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    elif arg == "gods":
        if get_trust(ch) < MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in char_list[:]:
            if not IS_NPC(vch) and get_trust( vch ) < get_trust( ch ) and vch.level >= LEVEL_HERO:
                act( buf, ch, None, vch, TO_VICT )
                interpret( vch, argument )
    else:
        victim = get_char_world(ch, arg )
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not is_room_owner(ch,victim.in_room) and  ch.in_room != victim.in_room \
        and room_is_private(victim.in_room) and not IS_TRUSTED(ch,IMPLEMENTOR):
            ch.send("That character is in a private room.\n")
            return
        if get_trust( victim ) >= get_trust( ch ):
            ch.send("Do it yourself!\n")
            return
        if not IS_NPC(victim) and get_trust(ch) < MAX_LEVEL -3:
            ch.send("Not at your level!\n")
            return
        act( buf, ch, None, victim, TO_VICT )
        interpret( victim, argument )
    ch.send("Ok.\n")
    return


# * New routines by Dionysos.
def do_invis(self, argument):
    ch=self
    # RT code for taking a level argument */
    argument, arg = read_word(argument)

    if not arg: 
    # take the default path */
        if ch.invis_level:
            ch.invis_level = 0
            act( "$n slowly fades into existence.", ch, None, None, TO_ROOM )
            ch.send("You slowly fade back into existence.\n")
        else:
            ch.invis_level = get_trust(ch)
            act( "$n slowly fades into thin air.", ch, None, None, TO_ROOM )
            ch.send("You slowly vanish into thin air.\n")
    else:
    # do the level thing */
          level = int(arg) if arg.is_digit() else -1
          if level < 2 or level > get_trust(ch):
              ch.send("Invis level must be between 2 and your level.\n")
              return
          else:
              ch.reply = None
              ch.invis_level = level
              act( "$n slowly fades into thin air.", ch, None, None, TO_ROOM )
              ch.send("You slowly vanish into thin air.\n")
              return


def do_incognito(self, argument):
    ch=self
    # RT code for taking a level argument */
    argument, arg = read_word(argument)
    if not arg:
    # take the default path */
        if ch.incog_level:
            ch.incog_level = 0
            act( "$n is no longer cloaked.", ch, None, None, TO_ROOM )
            ch.send("You are no longer cloaked.\n")
        else:
            ch.incog_level = get_trust(ch)
            act( "$n cloaks $s presence.", ch, None, None, TO_ROOM )
            ch.send("You cloak your presence.\n")
    else:
    # do the level thing */
          level = int(arg) if arg.is_digit() else -1
          if level < 2 or level > get_trust(ch):
              ch.send("Incog level must be between 2 and your level.\n")
              return
          else:
              ch.reply = None
              ch.incog_level = level
              act( "$n cloaks $s presence.", ch, None, None, TO_ROOM )
              ch.send("You cloak your presence.\n")
    return


def do_holylight(self, argument):
    ch=self
    if IS_NPC(ch):
        return
    if IS_SET(ch.act, PLR_HOLYLIGHT):
        REMOVE_BIT(ch.act, PLR_HOLYLIGHT)
        ch.send("Holy light mode off.\n")
    else:
        SET_BIT(ch.act, PLR_HOLYLIGHT)
        ch.send("Holy light mode on.\n")
    return
# prefix command: it will put the string typed on each line typed */
def do_prefi(self, argument):
    ch=self
    ch.send("You cannot abbreviate the prefix command.\r\n")
    return

def do_prefix(self, argument):
    ch=self
    if not argument:
        if not ch.prefix:
            ch.send("You have no prefix to clear.\r\n")
            return
        ch.send("Prefix removed.\r\n")
        ch.prefix = ""
        return
    if ch.prefix:
        ch.send("Prefix changed to %s.\r\n" % argument)
        ch.prefix = ""
    else:
        ch.send("Prefix set to %s.\r\n" % argument)
    ch.prefix = argument

def do_areas(ch, argument):
    if argument:
        ch.send("No argument is used with this command.\n")
        return
    col = 0
    for iArea in area_list:
        ch.send("%-39s\n" % iArea.credits)
        col += 1
        if col % 2 == 0:
            ch.send("\n")
        
def do_memory(ch, argument):
    pass

def do_dump(ch,argument):
    pass