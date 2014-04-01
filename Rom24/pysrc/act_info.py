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
from collections import OrderedDict
from merc import *
from nanny import con_playing, con_gen_groups
from handler import get_trust, room_is_dark

# * Show a list to a character.
# * Can coalesce duplicated items.

def show_list_to_char( list, ch, fShort, fShowNothing ):
    if not ch.desc:
        return
    objects = OrderedDict()
    for obj in list:
        if obj.wear_loc == WEAR_NONE and can_see_obj( ch, obj ):
            frmt = format_obj_to_char( obj, ch, fShort )
            if frmt not in objects:
                objects[frmt] = 1
            else:
                objects[frmt] += 1


    if not objects and fShowNothing:
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE):
            ch.send( "     " )
        ch.send( "Nothing.\r\n" )

     #* Output the formatted list.
    for desc,count in objects:
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\r\n" % (count,desc) )
        else:
            for i in range(count):
                ch.send("     %s\r\n")

def show_char_to_char( list, ch ):
    for rch in list:
        if rch == ch:
                continue

        if get_trust(ch) < rch.invis_level:
            continue

        if can_see( ch, rch ):
            show_char_to_char_0( rch, ch );
        elif room_is_dark( ch.in_room ) and IS_AFFECTED(rch, AFF_INFRARED ):
            ch.send( "You see glowing red eyes watching YOU!\r\n")

def do_help( self, argument ):
    ch = self
    if not argument:
        argument = "summary"

    found = [h for h in help_list if h.level <= get_trust(self) and argument.lower() in h.keyword.lower()]

    for pHelp in found:
        if ch.desc.connected == con_playing:
            self.send("\n\r============================================================\n\r")
            ch.send(pHelp.keyword)
            ch.send("\r\n")
        text = pHelp.text
        if pHelp.text[0] == '.':
            text = pHelp.text[1:]
        ch.send(text + "\r\n")
        # small hack :) */
        if ch.desc and ch.desc.connected != con_playing and ch.desc.connected != con_gen_groups:
            break

    if not found:
        self.send( "No help on that word.\n\r")


def do_look( self, argument ):
    ch = self
    if not ch.desc:
        return

    if ch.position < POS_SLEEPING:
        ch.send( "You can't see anything but stars!\r\n")
        return

    if ch.position == POS_SLEEPING:
        ch.send( "You can't see anything, you're sleeping!\n\r")
        return

    if not check_blind( ch ):
        return

    if not IS_NPC(ch) and not IS_SET(ch.act, PLR_HOLYLIGHT) and room_is_dark( ch.in_room ):
        ch.send( "It is pitch black ... \n\r")
        show_char_to_char( ch.in_room.people, ch )
        return

    argument, arg1 = read_word( argument )
    argument, arg2 = read_word( argument )
    
    number, arg3 = number_argument(arg1)
    count = 0

    if not arg1 or arg1 == "auto":
        # 'look' or 'look auto' */
        ch.send( ch.in_room.name )

        if IS_IMMORTAL(ch) and (IS_NPC(ch) or IS_SET(ch.act,PLR_HOLYLIGHT)):
            ch.send(" [Room %d]" % ch.in_room.vnum)

        ch.send("\r\n")

        if not arg1[0] or ( not IS_NPC(ch) and not IS_SET(ch.comm, COMM_BRIEF) ):
            ch.send( "  %s" % ch.in_room.description )
    

        if not IS_NPC(ch) and IS_SET(ch.act, PLR_AUTOEXIT):
            ch.send("\r\n")
            ch.do_exits("auto")


        show_list_to_char( ch.in_room.contents, ch, False, False )
        show_char_to_char( ch.in_room.people,   ch )
        return

    if arg1 == "i" or arg1 == "in" or arg1 == "on":
        # 'look in' */
        if not arg2:
            ch.send( "Look in what?\n\r")
            return
    
        obj = get_obj_here(ch, arg2)
        if not obj:
            ch.send( "You do not see that here.\n\r" )
            return
        
        if item_type == ITEM_DRINK_CON:
            if obj.value[1] <= 0:
                ch.send("It is empty.\r\n")
                return
            if obj.value[1] < obj.value[0] / 4:
                amnt = "less than half-"
            elif obj.value[1] < 3 * obj.value[0] / 4:
                amnt = "abount half-"
            else:
                amnt = "more than half-"
            ch.send("It's %sfilled with a %s liquid.\n\r" % ( amnt, liq_table[obj.value[2]].liq_color ) )
        elif item_type == ITEM_CONTAINER or item_type == ITEM_CORPSE_NPC or item_type == ITEM_CORPSE_PC:
            if IS_SET(obj.value[1], CONT_CLOSED):
                ch.send( "It is closed.\n\r" )
                return
            act( "$p holds:", ch, obj, None, TO_CHAR )
            show_list_to_char( obj.contains, ch, True, True )
            return
        else:
            ch.send("That is not a container.\r\n")
            return
    victim = get_char_room(ch, arg1)
    if victim:
        show_char_to_char_1( victim, ch )
        return
    obj_list = ch.carrying
    obj_list.extend(ch.in_room.contents)
    for obj in obj_list:
        if can_see_obj( ch, obj ):
            #player can see object */
            pdesc = get_extra_descr( arg3, obj.extra_descr )

            if pdesc:
                count += 1
                if count == number:
                    ch.send( pdesc )
                    return
            else: continue
        
            pdesc = get_extra_descr( arg3, obj.pIndexData.extra_descr )
            if pdesc:
                count += 1
                if count == number:
                    ch.send( pdesc )
                    return
            else: continue
        
            if arg3.lower() in obj.name.lower:
                count += 1
                if count == number:
                    ch.send( "%s\r\n" % obj.description )
                    return
 

    pdesc = get_extra_descr(arg3,ch.in_room.extra_descr)
    if pdesc:
        count += 1
        if count == number:
            ch.send(pdesc)
            return
    
    if count > 0 and count != number:
        if count == 1:
            ch.send("You only see one %s here.\n\r" % arg3)
        else:
            ch.send("You only see %d of those here.\n\r" % count)
        return

    if "north".startswith(arg1): door = 0
    elif "east".startswith(arg1): door = 1
    elif "south".startswith(arg1): door = 2
    elif "west".startswith(arg1): door = 3
    elif "up".startswith(arg1): door = 4
    elif "down".startswith(arg1): door = 5
    else:
        ch.send( "You do not see that here.\n\r" )
        return
    

    # 'look direction' */
    if door not in ch.in_room.exit or not ch.in_room.exit[door]:
        ch.send( "Nothing special there.\n\r")
        return
    pexit = ch.in_room.exit[door]

    if pexit.description:
        ch.send( pexit.description )
    else:
        ch.send( "Nothing special there.\n\r" )

    if pexit.keyword and pexit.keyword.strip():
        if IS_SET(pexit.exit_info, EX_CLOSED):
            act( "The $d is closed.", ch, None, pexit.keyword, TO_CHAR )
        elif IS_SET(pexit.exit_info, EX_ISDOOR):
            act( "The $d is open.",   ch, None, pexit.keyword, TO_CHAR )
    return