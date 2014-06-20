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
from merc import *

# True if room is dark.
class handler_room:
    def is_dark(pRoomIndex):
        if pRoomIndex.light > 0:
            return False
        if IS_SET(pRoomIndex.room_flags, ROOM_DARK):
            return True
        if pRoomIndex.sector_type == SECT_INSIDE or pRoomIndex.sector_type == SECT_CITY:
            return False
        if weather_info.sunlight == SUN_SET or weather_info.sunlight == SUN_DARK:
            return True
        return False
    
    # * True if room is private.
    def is_private(pRoomIndex):
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

methods = {d:f for d,f in handler_room.__dict__.items() if not d.startswith('__')}
for m,f in methods.items():
    setattr(ROOM_INDEX_DATA, m, f)