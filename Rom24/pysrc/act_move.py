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
