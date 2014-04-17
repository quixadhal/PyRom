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
import random
from merc import *

def get_random_room(ch):
    room = None
    while True:
        room = random.choice(room_index_hash)
        if can_see_room(ch,room) and not room_is_private(room) \
        and not IS_SET(room.room_flags, ROOM_PRIVATE) \
        and not IS_SET(room.room_flags, ROOM_SOLITARY) \
        and not IS_SET(room.room_flags, ROOM_SAFE) \
        and (IS_NPC(ch) or IS_SET(ch.act,ACT_AGGRESSIVE) \
        or not IS_SET(room.room_flags,ROOM_LAW)):
            break
    return room

# RT Enter portals */
def do_enter(self, argument):
    ch=self
    ROOM_INDEX_DATA *location 

    if ch.fighting:
        return
    # nifty portal stuff */
    if argument:
        old_room = ch.in_room
        portal = get_obj_list( ch, argument,  ch.in_room.contents )
        if not portal:
            ch.send("You don't see that here.\n\r")
            return
        if portal.item_type != ITEM_PORTAL \
        or  (IS_SET(portal.value[1],EX_CLOSED) and not IS_TRUSTED(ch,ANGEL)):
            ch.send("You can't seem to find a way in.\n\r")
            return
        if not IS_TRUSTED(ch,ANGEL) and not IS_SET(portal.value[2],GATE_NOCURSE) \
        and  (IS_AFFECTED(ch,AFF_CURSE) or IS_SET(old_room.room_flags,ROOM_NO_RECALL)):
            ch.send("Something prevents you from leaving...\n\r")
            return
        location = None
        if IS_SET(portal.value[2],GATE_RANDOM) or portal.value[3] == -1:
            location = get_random_room(ch)
            portal.value[3] = location.vnum # for record keeping :) */
        elif IS_SET(portal.value[2], GATE_BUGGY) and (number_percent() < 5):
            location = get_random_room(ch)
        else:
            location = get_room_index(portal.value[3])
        if not location or location == old_room \
        or  not can_see_room(ch,location) \
        or (room_is_private(location) and not IS_TRUSTED(ch,IMPLEMENTOR)):
            act("$p doesn't seem to go anywhere.",ch,portal,None,TO_CHAR)
            return
        if IS_NPC(ch) and IS_SET(ch.act,ACT_AGGRESSIVE) \
        and  IS_SET(location.room_flags,ROOM_LAW):
            ch.send("Something prevents you from leaving...\n\r")
            return
        act("$n steps into $p.",ch,portal,None,TO_ROOM)
  
        if IS_SET(portal.value[2], GATE_NORMAL_EXIT):
            act("You enter $p.",ch,portal,None,TO_CHAR)
        else:
            act("You walk through $p and find yourself somewhere else:...",ch,portal,None,TO_CHAR) 
        char_from_room(ch)
        char_to_room(ch, location)
        if IS_SET(portal.value[2], GATE_GOWITH): # take the gate along */
            obj_from_room(portal)
            obj_to_room(portal,location)
        if IS_SET(portal.value[2], GATE_NORMAL_EXIT):
            act("$n has arrived.",ch,portal,None,TO_ROOM)
        else:
            act("$n has arrived through $p.",ch,portal,None,TO_ROOM)

        ch.do_look("auto")
        # charges */
        if portal.value[0] > 0:
            portal.value[0] -= 1
            if portal.value[0] == 0:
                portal.value[0] = -1
        # protect against circular follows */
        if old_room == location:
            return
        for fch in old_room.people[:]:
            if not portal or portal.value[0] == -1:
                # no following through dead portals */
                continue
            if fch.master == ch and IS_AFFECTED(fch,AFF_CHARM) and fch.position < POS_STANDING:
                fch.do_stand("")
            if fch.master == ch and fch.position == POS_STANDING:
                if IS_SET(ch.in_room.room_flags,ROOM_LAW) and  (IS_NPC(fch) and IS_SET(fch.act,ACT_AGGRESSIVE)):
                    act("You can't bring $N into the city.", ch,None,fch,TO_CHAR)
                    act("You aren't allowed in the city.", fch,None,None,TO_CHAR)
                    continue
                act( "You follow $N.", fch, None, ch, TO_CHAR )
                fch.do_enter(argument)
        if portal and portal.value[0] == -1:
            act("$p fades out of existence.",ch,portal,None,TO_CHAR)
            if ch.in_room == old_room:
                act("$p fades out of existence.",ch,portal,None,TO_ROOM)
            elif old_room.people:
                act("$p fades out of existence.", old_room.people,portal,None,TO_CHAR)
                act("$p fades out of existence.", old_room.people,portal,None,TO_ROOM)
            extract_obj(portal)
        return
    ch.send("Nope, can't do it.\n\r")
    return