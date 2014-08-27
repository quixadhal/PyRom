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
__author__ = 'syn'

import copy
import json
import logging

logger = logging.getLogger()

import handler_ch
import handler_item
import living
import game_utils
import merc
import state_checks
import instance


class SOCIAL_DATA:
    def __init__(self):
        self.name = ""
        self.char_no_arg = ""
        self.others_no_arg = ""
        self.char_found = ""
        self.others_found = ""
        self.vict_found = ""
        self.char_not_found = ""
        self.char_auto = ""
        self.others_auto = ""


# An affect.
class AFFECT_DATA:
    load_count = 0

    def __init__(self, **kwargs):
        AFFECT_DATA.load_count += 1
        self.valid = True
        self.where = 0
        self.type = 0
        self.level = 0
        self.duration = 0
        self.location = 0
        self.modifier = 0
        self.bitvector = 0
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data


class HELP_DATA:
    def __init__(self):
        self.level = 0
        self.keyword = ""
        self.text = ""

    def __repr__(self):
        return "<%s:%d>" % (self.keyword, self.level)


class time_info_data:
    def __init__(self):
        self.hour = 0
        self.day = 0
        self.month = 0
        self.year = 0


class weather_data:
    def __init__(self):
        self.mmhg = 0
        self.change = 0
        self.sky = 0
        self.sunlight = 0

time_info = time_info_data()
weather_info = weather_data()

def act(format, ch, arg1=None, arg2=None, send_to=merc.TO_ROOM, min_pos=merc.POS_RESTING):
    if not format:
        return
    if not ch or not ch.in_room:
        return

    vch = arg2
    obj1 = arg1
    obj2 = arg2

    he_she = ["it",  "he",  "she"]
    him_her = ["it",  "him", "her"]
    his_her = ["its", "his", "her"]

    to_players = [instance.characters[instance_id] for instance_id in ch.in_room.people[:]]

    if send_to is merc.TO_VICT:
        if not vch:
            print("Act: null vict with TO_VICT: " + format)
            return
        if not vch.in_room:
            return
        to_players = [instance.characters[instance_id] for instance_id in ch.in_room.people[:]]

    for to in to_players:
        if not to.desc or to.position < min_pos:
            continue
        if send_to is merc.TO_CHAR and to is not ch:
            continue
        if send_to is merc.TO_VICT and (to is not vch or to is ch):
            continue
        if send_to is merc.TO_ROOM and to is ch:
            continue
        if send_to is merc.TO_NOTVICT and (to is ch or to is vch):
            continue

        act_trans = {}
        if arg1:
            act_trans['$t'] = str(arg1)
        if arg2 and type(arg2) == str:
            act_trans['$T'] = str(arg2)
        if ch:
            act_trans['$n'] = state_checks.PERS(ch, to)
            act_trans['$e'] = he_she[ch.sex]
            act_trans['$m'] = him_her[ch.sex]
            act_trans['$s'] = his_her[ch.sex]
        if vch and isinstance(vch, living.Living):
            act_trans['$N'] = state_checks.PERS(vch, to)
            act_trans['$E'] = he_she[vch.sex]
            act_trans['$M'] = him_her[vch.sex]
            act_trans['$S'] = his_her[vch.sex]
        if obj1 and obj1.__class__ == handler_item.Items:
            act_trans['$p'] = state_checks.OPERS(to, obj1)
        if obj2 and obj2.__class__ == handler_item.Items:
            act_trans['$P'] = state_checks.OPERS(to, obj2)
        act_trans['$d'] = arg2 if not arg2 else "door"

        format = game_utils.mass_replace(format, act_trans)
        to.send(format+"\n")
    return

def wiznet( string, ch, obj, flag, flag_skip, min_level):
    from nanny import con_playing
    for d in merc.descriptor_list:
        if   d.is_connected(con_playing) \
        and d.character.is_immortal() \
        and  d.character.wiznet.is_set(merc.WIZ_ON) \
        and  (not flag or d.character.wiznet.is_set(flag)) \
        and  (not flag_skip or not d.character.wiznet.set(flag_skip)) \
        and  d.character.trust >= min_level \
        and  d.character != ch:
            if d.character.wiznet.set_bit(merc.WIZ_PREFIX):
                d.send("-. ",d.character)
            act(string,d.character,obj,ch, merc.TO_CHAR, merc.POS_DEAD)

# does aliasing and other fun stuff */
def substitute_alias(d, argument):
    ch = handler_ch.CH(d)
    MAX_INPUT_LENGTH = 500
    # check for prefix */
    if ch.prefix and not "prefix".startswith(argument):
        if len(ch.prefix) + len(argument) > MAX_INPUT_LENGTH:
            ch.send("Line to long, prefix not processed.\r\n")
        else:
            prefix = "%s %s" % (ch.prefix,argument)

    if ch.is_npc() or not ch.alias \
    or "alias".startswith(argument) or "unalias".startswith(argument)  \
    or "prefix".startswith(argument):
        ch.interpret(argument)
        return
    remains, sub = game_utils.read_word(argument)
    if sub not in ch.alias:
        ch.interpret(argument)
        return
    buf = "%s %s" % (ch.alias[sub], remains)
    ch.interpret(buf)

