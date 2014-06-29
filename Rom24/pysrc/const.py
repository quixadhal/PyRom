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
from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger()


race_type = namedtuple('race_type', 'name, pc_race, act, aff, off, imm, res, vuln, form, parts')
race_table = OrderedDict()

pc_race_type = namedtuple('pc_race_type', 'name, who_name, points, class_mult, skills, stats, max_stats, size')
pc_race_table = OrderedDict()


def SLOT(i):
    return i

skill_type = namedtuple('skilltype', 'name, skill_level, rating, spell_fun, '
                                     'target, minimum_position, pgsn, slot, '
                                     'min_mana, beats, noun_damage, msg_off, msg_obj')
skill_table = OrderedDict()


def register_spell(entry: skill_type):
    skill_table[entry.name] = entry
    global spell_lookup_dict = {entry.name: }
    logger.debug('    %s registered in skill table.', entry.name)

group_type = namedtuple('group_type', 'name, rating, spells')
group_table = OrderedDict()

guild_type = namedtuple('guild_type', 'name, who_name, attr_prime, weapon, guild_rooms, '
                                      'skill_adept, thac0_00, thac0_32, hp_min, hp_max, '
                                      'fMana, base_group, default_group')
guild_table = OrderedDict()

weapon_type = namedtuple('weapon_type', 'name, vnum, type, gsn')
weapon_table = OrderedDict()

title_table = {}

# * Attribute bonus structures.
str_app_type = namedtuple('str_app_type', 'tohit, todam, carry, wield')
str_app = OrderedDict()

int_app_type = namedtuple('int_app_type', 'learn')
int_app = OrderedDict()

wis_app_type = namedtuple('wis_app_type', 'practice')
wis_app = OrderedDict()

dex_app_type = namedtuple('dex_app_type', 'defensive')
dex_app = OrderedDict()

con_app_type = namedtuple('con_app_type', 'hitp, shock')
con_app = OrderedDict()


#/* attack table  -- not very organized :( */
attack_type = namedtuple('attack_type', 'name, noun, damage')
attack_table = OrderedDict()


wiznet_type = namedtuple('wiznet_type', 'name flag level')
wiznet_table = OrderedDict()

liq_type = namedtuple('liq_type', 'name color proof full thirst food ssize')
liq_table = OrderedDict()
