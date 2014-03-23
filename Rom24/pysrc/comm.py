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
from merc import descriptor_list, greeting_list
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

def init_descriptor(d):
    d.connected = MethodType(con_get_name, d)
    greeting = random.choice(greeting_list)
    d.send(greeting.text)
    d.active = True
    descriptor_list.append(d)

def close_socket(d):
	descriptor_list.remove(d)
