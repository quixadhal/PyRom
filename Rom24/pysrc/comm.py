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
import logging

logger = logging.getLogger()

from collections import OrderedDict
import random
from types import MethodType

import db
import game_utils
import handler_game
import merc
import nanny
import handler_ch
import state_checks


def process_input():
    for d in merc.descriptor_list:
        if d.active and d.cmd_ready and d.connected:
            d.connected()
            if d.is_connected(nanny.con_playing):
                ch = handler_ch.CH(d)
                if ch:
                    ch.timer = 0


def set_connected(self, state):
    self.connected = MethodType(state, self)


def is_connected(self, state):
    return self.connected == MethodType(state, self)


def process_output(self):
    ch = handler_ch.CH(self)
    if ch and self.is_connected(nanny.con_playing) and self.send_buffer:
        #/* battle prompt */
        if ch.fighting:
            victim = merc.characters[ch.fighting]
            if victim and ch.can_see(victim):
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
                wound = "%s %s \n" % (state_checks.PERS(victim, ch), wound)
                wound = wound.capitalize()
                ch.send(wound)
        self.send("\n")
        bust_a_prompt(ch)
    self.miniboa_send()


def init_descriptor(d):
    d.set_connected = MethodType(set_connected, d)
    d.is_connected = MethodType(is_connected, d)
    d.set_connected(nanny.con_get_name)
    greeting = random.choice(merc.greeting_list)
    d.send(greeting.text)
    d.active = True
    d.character = None
    d.original = None
    d.snoop_by = None
    d.close = d.deactivate
    #Gain control over process output without messing with miniboa.
    d.miniboa_send = d.socket_send
    d.socket_send = MethodType(process_output, d)
    merc.descriptor_list.append(d)


#Check if already playing.
def check_playing(d, name):
    for dold in merc.descriptor_list:
        if dold != d and dold.character \
                and dold.connected != nanny.con_get_name \
                and dold.connected != nanny.con_get_old_password \
                and name == (dold.original.name
                             if dold.original
                             else dold.character.name):
            d.send("That character is already playing.\n")
            d.send("Do you wish to connect anyway (Y/N)?")
            d.set_connected(nanny.con_break_connect)
            return True
    return False


#Look for link-dead player to reconnect.
def check_reconnect(d, name, fConn):
    for ch in merc.player_characters.values():
        if not ch.is_npc() and (not fConn or not ch.desc) \
                and d.character.name == ch.name:
            if not fConn:
                d.character.pwd = ch.pwd
            else:
                d.character.pwd = ""
                del d.character
                d.character = ch
                ch.desc = d
                ch.timer = 0
                ch.send("Reconnecting. Type replay to see missed tells.\n")
                handler_game.act("$n has reconnected.", ch, None, None, merc.TO_ROOM)
                logger.info("%s@%s reconnected.", ch.name, d.host)
                handler_game.wiznet("$N groks the fullness of $S link.", ch, None, merc.WIZ_LINKS, 0, 0)
                d.set_connected(nanny.con_playing)
            return True
    return False


def close_socket(d):
    if d in merc.descriptor_list:
        merc.descriptor_list.remove(d)
    d.active = False


#* Bust a prompt (player settable prompt)
#* coded by Morgenes for Aldara Mud
def bust_a_prompt(ch):
    dir_name = ["N", "E", "S", "W", "U", "D"]
    room = merc.rooms[ch.in_room]
    doors = ""
    pstr = ch.prompt
    if not pstr:
        ch.send("<%dhp %dm %dmv> %s" % (ch.hit, ch.mana, ch.move, ch.prefix))
        return
    if ch.comm.is_set(merc.COMM_AFK):
        ch.send("<AFK> ")
        return
    replace = OrderedDict()
    found = False
    for door, pexit in enumerate(room.exit):
        if pexit and (ch.can_see_room(pexit.to_room)
                      or (ch.is_affected(merc.AFF_INFRARED)
                          and not ch.is_affected(merc.AFF_BLIND))) \
                and not state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED):
            found = True
            doors += dir_name[door]
        if not found:
            replace['%e'] = "none"
        else:
            replace['%e'] = doors
    replace['%c'] = '\n'
    replace['%h'] = '%s' % ch.hit
    replace['%H'] = "%s" % ch.max_hit
    replace['%m'] = "%d" % ch.mana
    replace['%M'] = "%d" % ch.max_mana
    replace['%v'] = "%d" % ch.move
    replace['%V'] = "%d" % ch.max_move
    replace['%x'] = "%d" % ch.exp
    replace['%X'] = "%d" % (0 if ch.is_npc()
                            else (ch.level + 1) * ch.exp_per_level(ch.points) - ch.exp)
    replace['%g'] = "%ld" % ch.gold
    replace['%s'] = "%ld" % ch.silver
    if ch.level > 9:
        replace['%a'] = "%d" % ch.alignment
    else:
        replace['%a'] = "%s" % "good" \
            if ch.is_good() \
            else "evil" \
            if ch.is_evil() \
            else "neutral"
    
    if merc.rooms[ch.in_room]:
        if (not ch.is_npc()
            and ch.act.is_set(merc.PLR_HOLYLIGHT)) \
                or (not ch.is_affected(merc.AFF_BLIND)
                    and not merc.rooms[ch.in_room].is_dark()):
            replace['%r'] = merc.rooms[ch.in_room].name
        else: 
            replace['%r'] = "darkness"
    else:
        replace['%r'] = " "
     
    if ch.is_immortal() and ch.in_room:
        replace['%R'] = "%d" % ch.in_room
    else:
        replace['%R'] = " "
    
    if ch.is_immortal() and ch.in_room:
        replace['%z'] = "%s" % merc.areaTemplate[merc.rooms[ch.in_room].area].name
    else:
        replace['%z'] = " "
        
    #replace['%%'] = '%'
    prompt = ch.prompt
    prompt = game_utils.mass_replace(prompt, replace)
    
    ch.send(prompt)
    if ch.prefix:
        ch.send(ch.prefix)
    return


def is_reconnecting(d, name):
    for ch in merc.player_characters.values():
        if not ch.desc and ch.name == name:
            return True
    return False


def game_loop(server):
    from update import update_handler
    db.boot_db()

    logger.info("Pyom is ready to rock on port %d", server.port)

    while True: 
        server.poll()
        process_input()
        update_handler()
