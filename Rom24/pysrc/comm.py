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
from collections import OrderedDict
from types import MethodType
from merc import descriptor_list, greeting_list, POS_RESTING
from db import boot_db
from nanny import *
from alias import *

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
    d.snoop_by = None
    d.close = d.deactivate
    descriptor_list.append(d)

def close_socket(d):
    descriptor_list.remove(d)
    d.active = False

 #* Bust a prompt (player settable prompt)
 #* coded by Morgenes for Aldara Mud
def bust_a_prompt( ch ):
    dir_name = ["N","E","S","W","U","D"]
    str = ch.prompt
    if not str:
        ch.send("<%dhp %dm %dmv> %s" % (ch.hit,ch.mana,ch.move,ch.prefix))
        return
    if IS_SET(ch.comm,COMM_AFK):
        ch.send("<AFK> ")
        return
    replace = OrderedDict()
    found = False
    for pexit in ch.in_room.exit:
        if pexit \
        and pexit.to_room \
        and (can_see_room(ch,pexit.to_room) or (IS_AFFECTED(ch,AFF_INFRARED) \
        and not IS_AFFECTED(ch,AFF_BLIND))) \
        and not IS_SET(pexit.exit_info,EX_CLOSED):
            found = True
            doors += dir_name[door]
        if not found:
            replace['%e'] = "none"
        else:
            replace['%e'] = doors
    replace['%c'] = '\n\r'
    replace['%h'] = '%s' % ch.hit
    replace['%H'] = "%s" % ch.max_hit
    replace['%m'] = "%d" % ch.mana
    replace['%M'] = "%d" % ch.max_mana
    replace['%v'] = "%d" % ch.move
    replace['%V'] = "%d" % ch.max_move
    replace['%x'] = "%d" % ch.exp
    replace['%X'] = "%d" % (0 if IS_NPC(ch) else (ch.level + 1) * exp_per_level(ch,ch.pcdata.points) - ch.exp)
    replace['%g'] = "%ld" % ch.gold
    replace['%s'] = "%ld" % ch.silver
    if ch.level > 9:
        replace['%a'] = "%d" % ch.alignment
    else:
        replace['%a'] = "%s" % "good" if IS_GOOD(ch) else "evil" if IS_EVIL(ch) else "neutral"
    
    if ch.in_room:
        if ( not IS_NPC(ch) and IS_SET(ch.act,PLR_HOLYLIGHT)) or \
        (not IS_AFFECTED(ch,AFF_BLIND) and not room_is_dark( ch.in_room )):
            replace['%r'] = ch.in_room.name 
        else: 
            replace['%r'] = "darkness"
    else:
        replace['%r'] = " "
     
    if IS_IMMORTAL( ch ) and ch.in_room:
        replace['%R'] = "%d" % ch.in_room.vnum 
    else:
        replace['%R'] = " "
    
    if IS_IMMORTAL( ch ) and ch.in_room:
        replace['%z'] = "%s" % ch.in_room.area.name
    else:
        replace['%z'] = " "
        
    #replace['%%'] = '%'
    prompt = ch.prompt
    prompt = mass_replace(prompt, replace)
    ch.send(prompt)
    if ch.prefix:
        ch.send(ch.prefix)
    return


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
        
        act_trans = []
        if arg1:
            act_trans['$t'] = str(arg1)
        if arg2:
            act_trans['$T'] = str(arg2)
        if ch:
            act_trans['$n'] = PERS(ch, to)
            act_trans['$e'] = he_she[ch.sex]
            act_trans['$m'] = him_her[ch.sex]
            act_trans['$s'] = his_her[ch.sex]
        if vch:
            act_trans['$N'] = PERS(vch, to)
            act_trans['$E'] = he_she[vch.sex]
            act_trans['$M'] = him_her[vch.sex]
            act_trans['$S'] = his_her[vch.sex]
        if obj1:
            act_trans['$p'] = OPERS(to, obj1)
        if obj2:
            act_trans['$P'] = OPERS(to, obj2)
        act_trans['$d'] = arg2 if not arg2 else "door"
        format = mass_replace(format, act_trans)
        to.send(format+"\r\n")
    return

def game_loop(server):
    from update import update_handler
    boot_db()

    print "\nPyom is ready to rock on port %d\n" % server.port

    while True: 
        server.poll()
        process_input()
        update_handler()
