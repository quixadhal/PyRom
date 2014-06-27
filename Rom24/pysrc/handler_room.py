"""
 #**************************************************************************
 *  Original Diku Mud copyright(C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright(C) 1992, 1993 by Michael           *
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
*       Gabrielle Taylor=gtaylor@hypercube.org)                            *
*       Brian Moore=zump@rom.org)                                          *
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

import const
import handler_game
from merc import *
import state_checks


class ROOM_INDEX_DATA:
    def __init__(self):
        self.people = []
        self.contents = []
        self.extra_descr = []
        self.area = None
        self.exit = [None, None, None, None, None, None]
        self.old_exit = [None, None, None, None, None, None]
        self.name = ""
        self.description = ""
        self.owner = ""
        self.vnum = 0
        self.room_flags = 0
        self.light = 0
        self.sector_type = 0
        self.heal_rate = 0
        self.mana_rate = 0
        self.clan = 0

    def __repr__(self):
        return "<RoomIndex: %d" % self.vnum


def random_room(ch):
    room = None
    while True:
        room = random.choice(room_index_hash)
        if ch.can_see_room(room) and not room.is_private() \
            and not state_checks.IS_SET(room.room_flags, ROOM_PRIVATE) \
            and not state_checks.IS_SET(room.room_flags, ROOM_SOLITARY) \
            and not state_checks.IS_SET(room.room_flags, ROOM_SAFE) \
            and (state_checks.IS_NPC(ch) or state_checks.IS_SET(ch.act, ACT_AGGRESSIVE)
                 or not state_checks.IS_SET(room.room_flags, ROOM_LAW)):
            break
    return room

def random_door(self=None):
    return random.randint(0, 5)

def find_door(ch, arg):
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
            if pexit and state_checks.IS_SET(pexit.exit_info, EX_ISDOOR) and pexit.keyword and arg in pexit.keyword:
                return door
        handler_game.act("I see no $T here.", ch, None, arg, TO_CHAR)
        return -1
    pexit = ch.in_room.exit[door]
    if not pexit:
        handler_game.act("I see no door $T here.", ch, None, arg, TO_CHAR)
        return -1
    if not state_checks.IS_SET(pexit.exit_info, EX_ISDOOR):
        ch.send("You can't do that.\n")
        return -1
    return door

class handler_room:
    def is_dark(pRoomIndex):
        if pRoomIndex.light > 0:
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_DARK):
            return True
        if pRoomIndex.sector_type == SECT_INSIDE or pRoomIndex.sector_type == SECT_CITY:
            return False
        if handler_game.weather_info.sunlight == SUN_SET or handler_game.weather_info.sunlight == SUN_DARK:
            return True
        return False
    
    # * True if room is private.
    def is_private(pRoomIndex):
        if pRoomIndex.owner:
            return True
        count = len(pRoomIndex.people)
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_PRIVATE) and count >= 2:
            return True
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_SOLITARY) and count >= 1:
            return True
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_IMP_ONLY):
            return True
        return False

methods = {d:f for d,f in handler_room.__dict__.items() if not d.startswith('__')}
for m,f in methods.items():
    setattr(ROOM_INDEX_DATA, m, f)
