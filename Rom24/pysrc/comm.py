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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
from collections import OrderedDict
from types import MethodType
import logging
logger = logging.getLogger()

from merc import descriptor_list, greeting_list, POS_RESTING
from db import boot_db
from nanny import *
from alias import *

def process_input():
    for d in descriptor_list:
        if d.active and d.cmd_ready and d.connected:
            d.connected()
            if d.is_connected(con_playing):
                ch = CH(d)
                if ch:
                    ch.timer = 0

def set_connected(self, state):
    self.connected = MethodType(state,self)

def is_connected(self, state):
    return self.connected == MethodType(state,self)

def process_output(self):
    ch = CH(self)
    if ch and self.is_connected(con_playing) and self.send_buffer:
        #/* battle prompt */
        victim = ch.fighting
        if victim and ch.can_see(victim):
            percent = 0
            wound = ""
            if victim.max_hit > 0:
                percent = victim.hit * 100 / victim.max_hit
            else:
                percent = -1
 
            if percent >= 100:
                wound = "is in excellent condition."
            elif percent >= 90:
                wound = "has a few scratches."
            elif percent >= 75:
                wound = "has some small wounds and bruises."
            elif percent >= 50:
                wound = "has quite a few wounds."
            elif percent >= 30:
                wound = "has some big nasty wounds and scratches."
            elif percent >= 15:
                wound = "looks pretty hurt."
            elif percent >= 0:
                wound = "is in awful condition."
            else:
                wound = "is bleeding to death."
            wound = "%s %s \n" % (PERS(victim, ch), wound)
            wound = wound.capitalize()
            ch.send(wound)

        self.send("\n")
        bust_a_prompt(ch)

    self.miniboa_send()        

def init_descriptor(d):
    d.set_connected = MethodType(set_connected,d)
    d.is_connected = MethodType(is_connected,d)
    d.set_connected(con_get_name)
    greeting = random.choice(greeting_list)
    d.send(greeting.text)
    d.active = True
    d.character = None
    d.original = None
    d.snoop_by = None
    d.close = d.deactivate
    #Gain control over process output without messing with miniboa.
    d.miniboa_send = d.socket_send
    d.socket_send = MethodType(process_output,d)
    descriptor_list.append(d)

#Check if already playing.
def check_playing( d, name ):
    for dold in descriptor_list:
        if dold != d and dold.character \
        and dold.connected != con_get_name \
        and dold.connected != con_get_old_password \
        and name == (dold.original.name if dold.original else dold.character.name):
            d.send("That character is already playing.\n")
            d.send("Do you wish to connect anyway (Y/N)?")
            d.set_connected(con_break_connect)
            return True
    return False

#Look for link-dead player to reconnect.
def check_reconnect( d, name, fConn ):
    for ch in char_list:
        if not IS_NPC(ch) and ( not fConn or not ch.desc) \
        and d.character.name == ch.name:
            if fConn == False:
                d.character.pcdata.pwd = ch.pcdata.pwd
            else:
                d.character.pcdata.pwd = ""
                del d.character
                d.character = ch
                ch.desc = d
                ch.timer = 0
                ch.send("Reconnecting. Type replay to see missed tells.\n")
                act( "$n has reconnected.", ch, NULL, NULL, TO_ROOM )
                logger.info ("%s@%s reconnected.", ch.name, d.host)
                wiznet("$N groks the fullness of $S link.",ch,None,WIZ_LINKS,0,0)
                d.set_connected(con_playing)
            return True
    return False

def close_socket(d):
    if d in descriptor_list:
        descriptor_list.remove(d)
    d.active = False

#* Bust a prompt (player settable prompt)
#* coded by Morgenes for Aldara Mud
def bust_a_prompt( ch ):
    dir_name = ["N","E","S","W","U","D"]
    doors = ""
    str = ch.prompt
    if not str:
        ch.send("<%dhp %dm %dmv> %s" % (ch.hit,ch.mana,ch.move,ch.prefix))
        return
    if IS_SET(ch.comm,COMM_AFK):
        ch.send("<AFK> ")
        return
    replace = OrderedDict()
    found = False
    for door, pexit in enumerate(ch.in_room.exit):
        if pexit \
        and pexit.to_room \
        and (ch.can_see_room(pexit.to_room) or (IS_AFFECTED(ch,AFF_INFRARED) \
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
    replace['%X'] = "%d" % (0 if IS_NPC(ch) else (ch.level + 1) * ch.exp_per_level(ch.pcdata.points) - ch.exp)
    replace['%g'] = "%ld" % ch.gold
    replace['%s'] = "%ld" % ch.silver
    if ch.level > 9:
        replace['%a'] = "%d" % ch.alignment
    else:
        replace['%a'] = "%s" % "good" if IS_GOOD(ch) else "evil" if IS_EVIL(ch) else "neutral"
    
    if ch.in_room:
        if ( not IS_NPC(ch) and IS_SET(ch.act,PLR_HOLYLIGHT)) or \
        (not IS_AFFECTED(ch,AFF_BLIND) and not ch.in_room.is_dark()):
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

def game_loop(server):
    from update import update_handler
    boot_db()

    logger.info ("Pyom is ready to rock on port %d", server.port)

    while True: 
        server.poll()
        process_input()
        update_handler()
