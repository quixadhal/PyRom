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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor (rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor (gtaylor@hypercube.org)			               *
*	    Brian Moore (zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
import random
from types import MethodType
from merc import descriptor_list, greeting_list, POS_RESTING
from db import boot_db
from nanny import *


def game_loop(server):
    boot_db()
    print "\nPyom is ready to rock on port %d\n" % server.port

    while True: 
        server.poll()
        process_input()
        #update_handler()

def process_input():
    for d in descriptor_list:
        if d.active and d.cmd_ready and d.connected:
            d.connected()

def set_connected(self, state):
    self.connected = MethodType(state,self)

def init_descriptor(d):
    d.set_connected = MethodType(set_connected,d)
    d.set_connected(con_get_name)
    greeting = random.choice(greeting_list)
    d.send(greeting.text)
    d.active = True
    d.character = None
    d.original = None
    d.close = d.deactivate
    descriptor_list.append(d)

def close_socket(d):
    descriptor_list.remove(d)
    d.active = False

def is_reconnecting(d, name):
    for ch in player_list:
        if not ch.desc and ch.name == name:
            return True
    return False

def act(format, ch, arg1, arg2, type, min_pos=POS_RESTING):
    if not format:
        return
    if not ch or not ch.in_room:
        return

    vch = arg2
    obj1 = arg1
    obj2 = arg2

    he_she=["it",  "he",  "she"]
    him_her=["it",  "him", "her"]
    his_her=["its", "his", "her"]

    to_players = ch.in_room.people

    if type is TO_VICT:
        if not vch:
            print "Act: null vict with TO_VICT: " + format
            return
        if not vch.in_room:
            return
        to_players = vch.in_room.people

    for to in to_players:
        if not to.desc or to.position < min_pos:
            continue
        if type is TO_CHAR and to is not ch:
            continue
        if type is TO_VICT and ( to is not vch or to is ch ):
            continue
        if type is TO_ROOM and to is ch:
            continue
        if type is TO_NOTVICT and (to is ch or to is vch):
            continue
        
        act_trans = { '$t': str(arg1), 
                      '$T': str(arg2), 
                      '$n': PERS(ch, to),  
                      '$N': PERS(vch, to), 
                      '$e': he_she[ch.sex], 
                      '$E': he_she[vch.sex], 
                      '$m': him_her[ch.sex], 
                      '$M': him_her[vch.sex], 
                      '$s': his_her[ch.sex], 
                      '$S': his_her[vch.sex], 
                      '$p': OPERS(to, obj1), 
                      '$P': OPERS(to, obj2), 
                      '$d': arg2 if not arg2 else "door"
                    }
        format = mass_replace(format, act_trans)
        to.send(format+"\r\n")
    return
