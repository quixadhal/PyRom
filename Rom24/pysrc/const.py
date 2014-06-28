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
import os
from collections import OrderedDict, namedtuple
import logging

logger = logging.getLogger()

from merc import *


race_type = namedtuple('race_type', 'name, pc_race, act, aff, off, imm, res, vuln, form, parts')
race_table = OrderedDict()
race_table["unique"] = race_type("unique", False, 0, 0, 0, 0, 0, 0, 0, 0)
race_table["human"] = race_type("human", True, 0, 0, 0, 0, 0, 0, A | H | M | V,
                                A | B | C | D | E | F | G | H | I | J | K)
race_table["elf"] = race_type("elf", True, 0, AFF_INFRARED, 0, 0, RES_CHARM, VULN_IRON, A | H | M | V,
                              A | B | C | D | E | F | G | H | I | J | K)
race_table["dwarf"] = race_type("dwarf", True, 0, AFF_INFRARED, 0, 0, RES_POISON | RES_DISEASE, VULN_DROWNING,
                                A | H | M | V, A | B | C | D | E | F | G | H | I | J | K)
race_table["giant"] = race_type("giant", True, 0, 0, 0, 0, RES_FIRE | RES_COLD, VULN_MENTAL | VULN_LIGHTNING,
                                A | H | M | V, A | B | C | D | E | F | G | H | I | J | K)
race_table["bat"] = race_type("bat", False, 0, AFF_FLYING | AFF_DARK_VISION, OFF_DODGE | OFF_FAST, 0, 0, VULN_LIGHT,
                              A | G | V, A | C | D | E | F | H | J | K | P)
race_table["bear"] = race_type("bear", False, 0, 0, OFF_CRUSH | OFF_DISARM | OFF_BERSERK, 0, RES_BASH | RES_COLD, 0,
                               A | G | V, A | B | C | D | E | F | H | J | K | U | V)
race_table["cat"] = race_type("cat", False, 0, AFF_DARK_VISION, OFF_FAST | OFF_DODGE, 0, 0, 0, A | G | V,
                              A | C | D | E | F | H | J | K | Q | U | V)
race_table["centipede"] = race_type("centipede", False, 0, AFF_DARK_VISION, 0, 0, RES_PIERCE | RES_COLD, VULN_BASH,
                                    A | B | G | O, A | C | K)
race_table["dog"] = race_type("dog", False, 0, 0, OFF_FAST, 0, 0, 0, A | G | V, A | C | D | E | F | H | J | K | U | V)
race_table["doll"] = race_type("doll", False, 0, 0, 0,
                               IMM_COLD | IMM_POISON | IMM_HOLY | IMM_NEGATIVE | IMM_MENTAL | IMM_DISEASE |
                               IMM_DROWNING, RES_BASH | RES_LIGHT, VULN_SLASH | VULN_FIRE | VULN_ACID | VULN_LIGHTNING |
                               VULN_ENERGY, E | J | M | cc, A | B | C | G | H | K)
race_table["dragon"] = race_type("dragon", False, 0, AFF_INFRARED | AFF_FLYING, 0, 0, RES_FIRE | RES_BASH | RES_CHARM,
                                 VULN_PIERCE | VULN_COLD, A | H | Z,
                                 A | C | D | E | F | G | H | I | J | K | P | Q | U | V | X)
race_table["fido"] = race_type("fido", False, 0, 0, OFF_DODGE | ASSIST_RACE, 0, 0, VULN_MAGIC, A | B | G | V,
                               A | C | D | E | F | H | J | K | Q | V)
race_table["fox"] = race_type("fox", False, 0, AFF_DARK_VISION, OFF_FAST | OFF_DODGE, 0, 0, 0, A | G | V,
                              A | C | D | E | F | H | J | K | Q | V)
race_table["goblin"] = race_type("goblin", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE, VULN_MAGIC, A | H | M | V,
                                 A | B | C | D | E | F | G | H | I | J | K)
race_table["hobgoblin"] = race_type("hobgoblin", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE | RES_POISON, 0,
                                    A | H | M | V, A | B | C | D | E | F | G | H | I | J | K | Y)
race_table["kobold"] = race_type("kobold", False, 0, AFF_INFRARED, 0, 0, RES_POISON, VULN_MAGIC, A | B | H | M | V,
                                 A | B | C | D | E | F | G | H | I | J | K | Q)
race_table["lizard"] = race_type("lizard", False, 0, 0, 0, 0, RES_POISON, VULN_COLD, A | G | X | cc,
                                 A | C | D | E | F | H | K | Q | V)
race_table["modron"] = race_type("modron", False, 0, AFF_INFRARED, ASSIST_RACE | ASSIST_ALIGN,
                                 IMM_CHARM | IMM_DISEASE | IMM_MENTAL | IMM_HOLY | IMM_NEGATIVE,
                                 RES_FIRE | RES_COLD | RES_ACID, 0, H, A | B | C | G | H | J | K)
race_table["orc"] = race_type("orc", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE, VULN_LIGHT, A | H | M | V,
                              A | B | C | D | E | F | G | H | I | J | K)
race_table["pig"] = race_type("pig", False, 0, 0, 0, 0, 0, 0, A | G | V, A | C | D | E | F | H | J | K)
race_table["rabbit"] = race_type("rabbit", False, 0, 0, OFF_DODGE | OFF_FAST, 0, 0, 0, A | G | V,
                                 A | C | D | E | F | H | J | K)
race_table["school monster"] = race_type("school monster", False, ACT_NOALIGN, 0, 0, IMM_CHARM | IMM_SUMMON, 0,
                                         VULN_MAGIC, A | M | V, A | B | C | D | E | F | H | J | K | Q | U)
race_table["snake"] = race_type("snake", False, 0, 0, 0, 0, RES_POISON, VULN_COLD, A | G | X | Y | cc,
                                A | D | E | F | K | L | Q | V | X)
race_table["song bird"] = race_type("song bird", False, 0, AFF_FLYING, OFF_FAST | OFF_DODGE, 0, 0, 0, A | G | W,
                                    A | C | D | E | F | H | K | P)
race_table["troll"] = race_type("troll", False, 0, AFF_REGENERATION | AFF_INFRARED | AFF_DETECT_HIDDEN, OFF_BERSERK, 0,
                                RES_CHARM | RES_BASH, VULN_FIRE | VULN_ACID, A | B | H | M | V,
                                A | B | C | D | E | F | G | H | I | J | K | U | V)
race_table["water fowl"] = race_type("water fowl", False, 0, AFF_SWIM | AFF_FLYING, 0, 0, RES_DROWNING, 0, A | G | W,
                                     A | C | D | E | F | H | K | P)
race_table["wolf"] = race_type("wolf", False, 0, AFF_DARK_VISION, OFF_FAST | OFF_DODGE, 0, 0, 0, A | G | V,
                               A | C | D | E | F | J | K | Q | V)
race_table["wyvern"] = race_type("wyvern", False, 0, AFF_FLYING | AFF_DETECT_INVIS | AFF_DETECT_HIDDEN,
                                 OFF_BASH | OFF_FAST | OFF_DODGE, IMM_POISON, 0, VULN_LIGHT, A | B | G | Z,
                                 A | C | D | E | F | H | J | K | Q | V | X)

pc_race_type = namedtuple('pc_race_type', 'name, who_name, points, class_mult, skills, stats, max_stats, size')
pc_race_table= OrderedDict()
pc_race_table['human'] = pc_race_type("human", "Human", 0, { 'mage':100, 'cleric':100, 'thief':100, 'warrior':100 }, [ "" ], [13, 13, 13, 13, 13], [18, 18, 18, 18, 18 ], SIZE_MEDIUM)
pc_race_table['elf'] = pc_race_type("elf", " Elf ", 5, { 'mage':100, 'cleric':125, 'thief':100, 'warrior':120 }, ["sneak", "hide"], [12, 14, 13, 15, 11], [16, 20, 18, 21, 15], SIZE_SMALL)
pc_race_table['dwarf'] = pc_race_type("dwarf", "Dwarf", 8, { 'mage':150, 'cleric':100, 'thief':125, 'warrior':100 }, ["berserk"], [14, 12, 14, 10, 15], [20, 16, 19, 14, 21], SIZE_MEDIUM)
pc_race_table['giant'] = pc_race_type("giant", "Giant", 6, { 'mage':200, 'cleric':150, 'thief':150, 'warrior':105 }, ["bash", "fast healing"], [16, 11, 13, 11, 14], [22, 15, 18, 15, 20], SIZE_LARGE)

def SLOT(i):
    return i

skill_type = namedtuple('skilltype', 'name, skill_level, rating, spell_fun, target, minimum_position, pgsn, slot, min_mana, beats, noun_damage, msg_off, msg_obj')
skill_table =  OrderedDict()
spell_null = None
skill_table["reserved"] = skill_type("reserved", {'mage': 99, 'cleric': 99, 'thief': 99, 'warrior': 99},
                                     {'mage': 99, 'cleric': 99, 'thief': 99, 'warrior': 99}, spell_null, TAR_IGNORE,
                                     POS_STANDING, None, SLOT(0), 0, 0, "", "", "")
skill_table["axe"] = skill_type("axe", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                {'mage': 6, 'cleric': 6, 'thief': 5, 'warrior': 4}, spell_null, TAR_IGNORE,
                                POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Axe!", "")
skill_table["dagger"] = skill_type("dagger", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                   {'mage': 2, 'cleric': 3, 'thief': 2, 'warrior': 2}, spell_null, TAR_IGNORE,
                                   POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Dagger!", "")
skill_table["flail"] = skill_type("flail", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                  {'mage': 6, 'cleric': 3, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                  POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Flail!", "")
skill_table["mace"] = skill_type("mace", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                 {'mage': 5, 'cleric': 2, 'thief': 3, 'warrior': 3}, spell_null, TAR_IGNORE,
                                 POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Mace!", "")
skill_table["polearm"] = skill_type("polearm", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                    {'mage': 6, 'cleric': 6, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                    POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Polearm!", "")
skill_table["shield block"] = skill_type("shield block", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                         {'mage': 6, 'cleric': 4, 'thief': 6, 'warrior': 2}, spell_null, TAR_IGNORE,
                                         POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Shield!", "")
skill_table["spear"] = skill_type("spear", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                  {'mage': 4, 'cleric': 4, 'thief': 4, 'warrior': 3}, spell_null, TAR_IGNORE,
                                  POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Spear!", "")
skill_table["sword"] = skill_type("sword", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                  {'mage': 5, 'cleric': 6, 'thief': 3, 'warrior': 2}, spell_null, TAR_IGNORE,
                                  POS_FIGHTING, None, SLOT(0), 0, 0, "", "!sword!", "")
skill_table["whip"] = skill_type("whip", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                 {'mage': 6, 'cleric': 5, 'thief': 5, 'warrior': 4}, spell_null, TAR_IGNORE,
                                 POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Whip!", "")
skill_table["backstab"] = skill_type("backstab", {'mage': 53, 'cleric': 53, 'thief': 1, 'warrior': 53},
                                     {'mage': 0, 'cleric': 0, 'thief': 5, 'warrior': 0}, spell_null, TAR_IGNORE,
                                     POS_STANDING, None, SLOT(0), 0, 24, "backstab", "!Backstab!", "")
skill_table["bash"] = skill_type("bash", {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 1},
                                 {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 4}, spell_null, TAR_IGNORE,
                                 POS_FIGHTING, None, SLOT(0), 0, 24, "bash", "!Bash!", "")
skill_table["berserk"] = skill_type("berserk", {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 18},
                                    {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 5}, spell_null, TAR_IGNORE,
                                    POS_FIGHTING, None, SLOT(0), 0, 24, "", "You feel your pulse slow down.", "")
skill_table["dirt kicking"] = skill_type("dirt kicking", {'mage': 53, 'cleric': 53, 'thief': 3, 'warrior': 3},
                                         {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 4}, spell_null, TAR_IGNORE,
                                         POS_FIGHTING, None, SLOT(0), 0, 24, "kicked dirt",
                                         "You rub the dirt out of your eyes.", "")
skill_table["disarm"] = skill_type("disarm", {'mage': 53, 'cleric': 53, 'thief': 12, 'warrior': 11},
                                   {'mage': 0, 'cleric': 0, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                   POS_FIGHTING, None, SLOT(0), 0, 24, "", "!Disarm!", "")
skill_table["dodge"] = skill_type("dodge", {'mage': 20, 'cleric': 22, 'thief': 1, 'warrior': 13},
                                  {'mage': 8, 'cleric': 8, 'thief': 4, 'warrior': 6}, spell_null, TAR_IGNORE,
                                  POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Dodge!", "")
skill_table["enhanced damage"] = skill_type("enhanced damage", {'mage': 45, 'cleric': 30, 'thief': 25, 'warrior': 1},
                                            {'mage': 10, 'cleric': 9, 'thief': 5, 'warrior': 3}, spell_null, TAR_IGNORE,
                                            POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Enhanced Damage!", "")
skill_table["envenom"] = skill_type("envenom", {'mage': 53, 'cleric': 53, 'thief': 10, 'warrior': 53},
                                    {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 0}, spell_null, TAR_IGNORE,
                                    POS_RESTING, None, SLOT(0), 0, 36, "", "!Envenom!", "")
skill_table["hand to hand"] = skill_type("hand to hand", {'mage': 25, 'cleric': 10, 'thief': 15, 'warrior': 6},
                                         {'mage': 8, 'cleric': 5, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                         POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Hand to Hand!", "")
skill_table["kick"] = skill_type("kick", {'mage': 53, 'cleric': 12, 'thief': 14, 'warrior': 8},
                                 {'mage': 0, 'cleric': 4, 'thief': 6, 'warrior': 3}, spell_null, TAR_CHAR_OFFENSIVE,
                                 POS_FIGHTING, None, SLOT(0), 0, 12, "kick", "!Kick!", "")
skill_table["parry"] = skill_type("parry", {'mage': 22, 'cleric': 20, 'thief': 13, 'warrior': 1},
                                  {'mage': 8, 'cleric': 8, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                  POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Parry!", "")
skill_table["rescue"] = skill_type("rescue", {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 1},
                                   {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 4}, spell_null, TAR_IGNORE,
                                   POS_FIGHTING, None, SLOT(0), 0, 12, "", "!Rescue!", "")
skill_table["trip"] = skill_type("trip", {'mage': 53, 'cleric': 53, 'thief': 1, 'warrior': 15},
                                 {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 8}, spell_null, TAR_IGNORE,
                                 POS_FIGHTING, None, SLOT(0), 0, 24, "trip", "!Trip!", "")
skill_table["second attack"] = skill_type("second attack", {'mage': 30, 'cleric': 24, 'thief': 12, 'warrior': 5},
                                          {'mage': 10, 'cleric': 8, 'thief': 5, 'warrior': 3}, spell_null, TAR_IGNORE,
                                          POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Second Attack!", "")
skill_table["third attack"] = skill_type("third attack", {'mage': 53, 'cleric': 53, 'thief': 24, 'warrior': 12},
                                         {'mage': 0, 'cleric': 0, 'thief': 10, 'warrior': 4}, spell_null, TAR_IGNORE,
                                         POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Third Attack!",
                                         "")  # non-combat skills */
skill_table["fast healing"] = skill_type("fast healing", {'mage': 15, 'cleric': 9, 'thief': 16, 'warrior': 6},
                                         {'mage': 8, 'cleric': 5, 'thief': 6, 'warrior': 4}, spell_null, TAR_IGNORE,
                                         POS_SLEEPING, None, SLOT(0), 0, 0, "", "!Fast Healing!", "")
skill_table["haggle"] = skill_type("haggle", {'mage': 7, 'cleric': 18, 'thief': 1, 'warrior': 14},
                                   {'mage': 5, 'cleric': 8, 'thief': 3, 'warrior': 6}, spell_null, TAR_IGNORE,
                                   POS_RESTING, None, SLOT(0), 0, 0, "", "!Haggle!", "")
skill_table["hide"] = skill_type("hide", {'mage': 53, 'cleric': 53, 'thief': 1, 'warrior': 12},
                                 {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 6}, spell_null, TAR_IGNORE,
                                 POS_RESTING, None, SLOT(0), 0, 12, "", "!Hide!", "")
skill_table["lore"] = skill_type("lore", {'mage': 10, 'cleric': 10, 'thief': 6, 'warrior': 20},
                                 {'mage': 6, 'cleric': 6, 'thief': 4, 'warrior': 8}, spell_null, TAR_IGNORE,
                                 POS_RESTING, None, SLOT(0), 0, 36, "", "!Lore!", "")
skill_table["meditation"] = skill_type("meditation", {'mage': 6, 'cleric': 6, 'thief': 15, 'warrior': 15},
                                       {'mage': 5, 'cleric': 5, 'thief': 8, 'warrior': 8}, spell_null, TAR_IGNORE,
                                       POS_SLEEPING, None, SLOT(0), 0, 0, "", "Meditation", "")
skill_table["peek"] = skill_type("peek", {'mage': 8, 'cleric': 21, 'thief': 1, 'warrior': 14},
                                 {'mage': 5, 'cleric': 7, 'thief': 3, 'warrior': 6}, spell_null, TAR_IGNORE,
                                 POS_STANDING, None, SLOT(0), 0, 0, "", "!Peek!", "")
skill_table["pick lock"] = skill_type("pick lock", {'mage': 25, 'cleric': 25, 'thief': 7, 'warrior': 25},
                                      {'mage': 8, 'cleric': 8, 'thief': 4, 'warrior': 8}, spell_null, TAR_IGNORE,
                                      POS_STANDING, None, SLOT(0), 0, 12, "", "!Pick!", "")
skill_table["sneak"] = skill_type("sneak", {'mage': 53, 'cleric': 53, 'thief': 4, 'warrior': 10},
                                  {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 6}, spell_null, TAR_IGNORE,
                                  POS_STANDING, None, SLOT(0), 0, 12, "", "You no longer feel stealthy.", "")
skill_table["steal"] = skill_type("steal", {'mage': 53, 'cleric': 53, 'thief': 5, 'warrior': 53},
                                  {'mage': 0, 'cleric': 0, 'thief': 4, 'warrior': 0}, spell_null, TAR_IGNORE,
                                  POS_STANDING, None, SLOT(0), 0, 24, "", "!Steal!", "")
skill_table["scrolls"] = skill_type("scrolls", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                    {'mage': 2, 'cleric': 3, 'thief': 5, 'warrior': 8}, spell_null, TAR_IGNORE,
                                    POS_STANDING, None, SLOT(0), 0, 24, "", "!Scrolls!", "")
skill_table["staves"] = skill_type("staves", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                   {'mage': 2, 'cleric': 3, 'thief': 5, 'warrior': 8}, spell_null, TAR_IGNORE,
                                   POS_STANDING, None, SLOT(0), 0, 12, "", "!Staves!", "")
skill_table["wands"] = skill_type("wands", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                  {'mage': 2, 'cleric': 3, 'thief': 5, 'warrior': 8}, spell_null, TAR_IGNORE,
                                  POS_STANDING, None, SLOT(0), 0, 12, "", "!Wands!", "")
skill_table["recall"] = skill_type("recall", {'mage': 1, 'cleric': 1, 'thief': 1, 'warrior': 1},
                                   {'mage': 2, 'cleric': 2, 'thief': 2, 'warrior': 2}, spell_null, TAR_IGNORE,
                                   POS_STANDING, None, SLOT(0), 0, 12, "", "!Recall!", "")


def register_spell(entry: skill_type):
    skill_table[entry.name] = entry
    logger.debug('    %s registered in skill table.', entry.name)

group_type = namedtuple('group_type', 'name, rating, spells')
group_table = OrderedDict()
group_table["rom basics"] = group_type("rom basics", {'mage': 0, 'cleric': 0, 'thief': 0, 'warrior': 0},
                                       ["scrolls", "staves", "wands", "recall"])
group_table["mage basics"] = group_type("mage basics", {'mage': 0, 'cleric': -1, 'thief': -1, 'warrior': -1},
                                        ["dagger"])
group_table["cleric basics"] = group_type("cleric basics", {'mage': -1, 'cleric': 0, 'thief': -1, 'warrior': -1},
                                          ["mace"])
group_table["thief basics"] = group_type("thief basics", {'mage': -1, 'cleric': -1, 'thief': 0, 'warrior': -1},
                                         ["dagger", "steal"])
group_table["warrior basics"] = group_type("warrior basics", {'mage': -1, 'cleric': -1, 'thief': -1, 'warrior': 0},
                                           ["sword", "second attack"])
group_table["mage default"] = group_type("mage default", {'mage': 40, 'cleric': -1, 'thief': -1, 'warrior': -1},
                                         ["lore", "beguiling", "combat", "detection", "enhancement", "illusion",
                                          "maladictions", "protective", "transportation", "weather"])
group_table["cleric default"] = group_type("cleric default", {'mage': -1, 'cleric': 40, 'thief': -1, 'warrior': -1},
                                           ["flail", "attack", "creation", "curative", "benedictions", "detection",
                                            "healing", "maladictions", "protective", "shield block", "transportation",
                                            "weather"])
group_table["thief default"] = group_type("thief default", {'mage': -1, 'cleric': -1, 'thief': 40, 'warrior': -1},
                                          ["mace", "sword", "backstab", "disarm", "dodge", "second attack", "trip",
                                           "hide", "peek", "pick lock", "sneak"])
group_table["warrior default"] = group_type("warrior default", {'mage': -1, 'cleric': -1, 'thief': -1, 'warrior': 40},
                                            ["weaponsmaster", "shield block", "bash", "disarm", "enhanced damage",
                                             "parry", "rescue", "third attack"])
group_table["weaponsmaster"] = group_type("weaponsmaster", {'mage': 40, 'cleric': 40, 'thief': 40, 'warrior': 20},
                                          ["axe", "dagger", "flail", "mace", "polearm", "spear", "sword", "whip"])
group_table["attack"] = group_type("attack", {'mage': -1, 'cleric': 5, 'thief': -1, 'warrior': 8},
                                   ["demonfire", "dispel evil", "dispel good", "earthquake", "flamestrike",
                                    "heat metal", "ray of truth"])
group_table["beguiling"] = group_type("beguiling", {'mage': 4, 'cleric': -1, 'thief': 6, 'warrior': -1},
                                      ["calm", "charm person", "sleep"])
group_table["benedictions"] = group_type("benedictions", {'mage': -1, 'cleric': 4, 'thief': -1, 'warrior': 8},
                                         ["bless", "calm", "frenzy", "holy word", "remove curse"])
group_table["combat"] = group_type("combat", {'mage': 6, 'cleric': -1, 'thief': 10, 'warrior': 9},
                                   ["acid blast", "burning hands", "chain lightning", "chill touch", "colour spray",
                                    "fireball", "lightning bolt", "magic missile", "shocking grasp"])
group_table["creation"] = group_type("creation", {'mage': 4, 'cleric': 4, 'thief': 8, 'warrior': 8},
                                     ["continual light", "create food", "create spring", "create water", "create rose",
                                      "floating disc"])
group_table["curative"] = group_type("curative", {'mage': -1, 'cleric': 4, 'thief': -1, 'warrior': 8},
                                     ["cure blindness", "cure disease", "cure poison"])
group_table["detection"] = group_type("detection", {'mage': 4, 'cleric': 3, 'thief': 6, 'warrior': -1},
                                      ["detect evil", "detect good", "detect hidden", "detect invis", "detect magic",
                                       "detect poison", "farsight", "identify", "know alignment", "locate object"])
group_table["draconian"] = group_type("draconian", {'mage': 8, 'cleric': -1, 'thief': -1, 'warrior': -1},
                                      ["acid breath", "fire breath", "frost breath", "gas breath", "lightning breath"])
group_table["enchantment"] = group_type("enchantment", {'mage': 6, 'cleric': -1, 'thief': -1, 'warrior': -1},
                                        ["enchant armor", "enchant weapon", "fireproof", "recharge"])
group_table["enhancement"] = group_type("enhancement", {'mage': 5, 'cleric': -1, 'thief': 9, 'warrior': 9},
                                        ["giant strength", "haste", "infravision", "refresh"])
group_table["harmful"] = group_type("harmful", {'mage': -1, 'cleric': 3, 'thief': -1, 'warrior': 6},
                                    ["cause critical", "cause light", "cause serious", "harm"])
group_table["healing"] = group_type("healing", {'mage': -1, 'cleric': 3, 'thief': -1, 'warrior': 6},
                                    ["cure critical", "cure light", "cure serious", "heal", "mass healing", "refresh"])
group_table["illusion"] = group_type("illusion", {'mage': 4, 'cleric': -1, 'thief': 7, 'warrior': -1},
                                     ["invis", "mass invis", "ventriloquate"])
group_table["maladictions"] = group_type("maladictions", {'mage': 5, 'cleric': 5, 'thief': 9, 'warrior': 9},
                                         ["blindness", "change sex", "curse", "energy drain", "plague", "poison",
                                          "slow", "weaken"])
group_table["protective"] = group_type("protective", {'mage': 4, 'cleric': 4, 'thief': 7, 'warrior': 8},
                                       ["armor", "cancellation", "dispel magic", "fireproof", "protection evil",
                                        "protection good", "sanctuary", "shield", "stone skin"])
group_table["transportation"] = group_type("transportation", {'mage': 4, 'cleric': 4, 'thief': 8, 'warrior': 9},
                                           ["fly", "gate", "nexus", "pass door", "portal", "summon", "teleport",
                                            "word of recall"])
group_table["weather"] = group_type("weather", {'mage': 4, 'cleric': 4, 'thief': 8, 'warrior': 8},
                                    ["call lightning", "control weather", "faerie fire", "faerie fog",
                                     "lightning bolt"])

guild_type = namedtuple('guild_type', 'name, who_name, attr_prime, weapon, guild_rooms, skill_adept, thac0_00, thac0_32, hp_min, hp_max, fMana, base_group, default_group')
guild_table = OrderedDict()
guild_table["mage"] = guild_type("mage", "Mag", STAT_INT, OBJ_VNUM_SCHOOL_DAGGER, [3018, 9618], 75, 20, 6, 6, 8, True,
                                 "mage basics", "mage default")
guild_table["cleric"] = guild_type("cleric", "Cle", STAT_WIS, OBJ_VNUM_SCHOOL_MACE, [3003, 9619], 75, 20, 2, 7, 10,
                                   True, "cleric basics", "cleric default")
guild_table["thief"] = guild_type("thief", "Thi", STAT_DEX, OBJ_VNUM_SCHOOL_DAGGER, [3028, 9639], 75, 20, -4, 8, 13,
                                  False, "thief basics", "thief default")
guild_table["warrior"] = guild_type("warrior", "War", STAT_STR, OBJ_VNUM_SCHOOL_SWORD, [3022, 9633], 75, 20, -10, 11,
                                    15, False, "warrior basics", "warrior default")


weapon_type = namedtuple('weapon_type', 'name, vnum, type, gsn')
weapon_table =  OrderedDict()
weapon_table['sword'] = weapon_type('sword',   OBJ_VNUM_SCHOOL_SWORD,  WEAPON_SWORD, 'sword'  )
weapon_table['mace'] = weapon_type('mace',    OBJ_VNUM_SCHOOL_MACE,   WEAPON_MACE,   'mace'   )
weapon_table['dagger'] = weapon_type('dagger',  OBJ_VNUM_SCHOOL_DAGGER, WEAPON_DAGGER,  'dagger' )
weapon_table['axe'] = weapon_type('axe', OBJ_VNUM_SCHOOL_AXE,    WEAPON_AXE, 'axe'   )
weapon_table['staff'] = weapon_type('staff',   OBJ_VNUM_SCHOOL_STAFF,  WEAPON_SPEAR,   'spear'  )
weapon_table['flail'] = weapon_type('flail',   OBJ_VNUM_SCHOOL_FLAIL,  WEAPON_FLAIL,   'flail'  )
weapon_table['whip'] = weapon_type('whip',    OBJ_VNUM_SCHOOL_WHIP,   WEAPON_WHIP,    'whip'   )
weapon_table['polearm'] = weapon_type('polearm', OBJ_VNUM_SCHOOL_POLEARM,WEAPON_POLEARM, 'polearm'    )

weapon_table = OrderedDict()
weapon_table['sword'] = weapon_type('sword', OBJ_VNUM_SCHOOL_SWORD, WEAPON_SWORD, 'sword')
weapon_table['mace'] = weapon_type('mace', OBJ_VNUM_SCHOOL_MACE, WEAPON_MACE, 'mace')
weapon_table['dagger'] = weapon_type('dagger', OBJ_VNUM_SCHOOL_DAGGER, WEAPON_DAGGER, 'dagger')
weapon_table['axe'] = weapon_type('axe', OBJ_VNUM_SCHOOL_AXE, WEAPON_AXE, 'axe')
weapon_table['staff'] = weapon_type('staff', OBJ_VNUM_SCHOOL_STAFF, WEAPON_SPEAR, 'spear')
weapon_table['flail'] = weapon_type('flail', OBJ_VNUM_SCHOOL_FLAIL, WEAPON_FLAIL, 'flail')
weapon_table['whip'] = weapon_type('whip', OBJ_VNUM_SCHOOL_WHIP, WEAPON_WHIP, 'whip')
weapon_table['polearm'] = weapon_type('polearm', OBJ_VNUM_SCHOOL_POLEARM, WEAPON_POLEARM, 'polearm')

title_table = {"mage": [["Man", "Woman"],
                        ["Apprentice of Magic", "Apprentice of Magic"],
                        ["Spell Student", "Spell Student"],
                        ["Scholar of Magic", "Scholar of Magic"],
                        ["Delver in Spells", "Delveress in Spells"],
                        ["Medium of Magic", "Medium of Magic"],
                        ["Scribe of Magic", "Scribess of Magic"],
                        ["Seer", "Seeress"],
                        ["Sage", "Sage"],
                        ["Illusionist", "Illusionist"],
                        ["Abjurer", "Abjuress"],
                        ["Invoker", "Invoker"],
                        ["Enchanter", "Enchantress"],
                        ["Conjurer", "Conjuress"],
                        ["Magician", "Witch"],
                        ["Creator", "Creator"],
                        ["Savant", "Savant"],
                        ["Magus", "Craftess"],
                        ["Wizard", "Wizard"],
                        ["Warlock", "War Witch"],
                        ["Sorcerer", "Sorceress"],
                        ["Elder Sorcerer", "Elder Sorceress"],
                        ["Grand Sorcerer", "Grand Sorceress"],
                        ["Great Sorcerer", "Great Sorceress"],
                        ["Golem Maker", "Golem Maker"],
                        ["Greater Golem Maker", "Greater Golem Maker"],
                        ["Maker of Stones", "Maker of Stones"],
                        ["Maker of Potions", "Maker of Potions"],
                        ["Maker of Scrolls", "Maker of Scrolls"],
                        ["Maker of Wands", "Maker of Wands"],
                        ["Maker of Staves", "Maker of Staves"],
                        ["Demon Summoner", "Demon Summoner"],
                        ["Greater Demon Summoner", "Greater Demon Summoner"],
                        ["Dragon Charmer", "Dragon Charmer"],
                        ["Greater Dragon Charmer", "Greater Dragon Charmer"],
                        ["Master of all Magic", "Master of all Magic"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Master Mage", "Master Mage"],
                        ["Mage Hero", "Mage Heroine"],
                        ["Avatar of Magic", "Avatar of Magic"],
                        ["Angel of Magic", "Angel of Magic"],
                        ["Demigod of Magic", "Demigoddess of Magic"],
                        ["Immortal of Magic", "Immortal of Magic"],
                        ["God of Magic", "Goddess of Magic"],
                        ["Deity of Magic", "Deity of Magic"],
                        ["Supremity of Magic", "Supremity of Magic"],
                        ["Creator", "Creator"],
                        ["Implementor", "Implementress"]],

               'cleric': [["Man", "Woman"],
                          ["Believer", "Believer"],
                          ["Attendant", "Attendant"],
                          ["Acolyte", "Acolyte"],
                          ["Novice", "Novice"],
                          ["Missionary", "Missionary"],
                          ["Adept", "Adept"],
                          ["Deacon", "Deaconess"],
                          ["Vicar", "Vicaress"],
                          ["Priest", "Priestess"],
                          ["Minister", "Lady Minister"],
                          ["Canon", "Canon"],
                          ["Levite", "Levitess"],
                          ["Curate", "Curess"],
                          ["Monk", "Nun"],
                          ["Healer", "Healess"],
                          ["Chaplain", "Chaplain"],
                          ["Expositor", "Expositress"],
                          ["Bishop", "Bishop"],
                          ["Arch Bishop", "Arch Lady of the Church"],
                          ["Patriarch", "Matriarch"],
                          ["Elder Patriarch", "Elder Matriarch"],
                          ["Grand Patriarch", "Grand Matriarch"],
                          ["Great Patriarch", "Great Matriarch"],
                          ["Demon Killer", "Demon Killer"],
                          ["Greater Demon Killer", "Greater Demon Killer"],
                          ["Cardinal of the Sea", "Cardinal of the Sea"],
                          ["Cardinal of the Earth", "Cardinal of the Earth"],
                          ["Cardinal of the Air", "Cardinal of the Air"],
                          ["Cardinal of the Ether", "Cardinal of the Ether"],
                          ["Cardinal of the Heavens", "Cardinal of the Heavens"],
                          ["Avatar of an Immortal", "Avatar of an Immortal"],
                          ["Avatar of a Deity", "Avatar of a Deity"],
                          ["Avatar of a Supremity", "Avatar of a Supremity"],
                          ["Avatar of an Implementor", "Avatar of an Implementor"],
                          ["Master of all Divinity", "Mistress of all Divinity"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Master Cleric", "Master Cleric"],
                          ["Holy Hero", "Holy Heroine"],
                          ["Holy Avatar", "Holy Avatar"],
                          ["Angel", "Angel"],
                          ["Demigod", "Demigoddess"],
                          ["Immortal", "Immortal"],
                          ["God", "Goddess"],
                          ["Deity", "Deity"],
                          ["Supreme Master", "Supreme Mistress"],
                          ["Creator", "Creator"],
                          ["Implementor", "Implementress"]],
               'thief': [["Man", "Woman"],

                         ["Pilferer", "Pilferess"],
                         ["Footpad", "Footpad"],
                         ["Filcher", "Filcheress"],
                         ["Pick-Pocket", "Pick-Pocket"],
                         ["Sneak", "Sneak"],

                         ["Pincher", "Pincheress"],
                         ["Cut-Purse", "Cut-Purse"],
                         ["Snatcher", "Snatcheress"],
                         ["Sharper", "Sharpress"],
                         ["Rogue", "Rogue"],

                         ["Robber", "Robber"],
                         ["Magsman", "Magswoman"],
                         ["Highwayman", "Highwaywoman"],
                         ["Burglar", "Burglaress"],
                         ["Thief", "Thief"],

                         ["Knifer", "Knifer"],
                         ["Quick-Blade", "Quick-Blade"],
                         ["Killer", "Murderess"],
                         ["Brigand", "Brigand"],
                         ["Cut-Throat", "Cut-Throat"],

                         ["Spy", "Spy"],
                         ["Grand Spy", "Grand Spy"],
                         ["Master Spy", "Master Spy"],
                         ["Assassin", "Assassin"],
                         ["Greater Assassin", "Greater Assassin"],

                         ["Master of Vision", "Mistress of Vision"],
                         ["Master of Hearing", "Mistress of Hearing"],
                         ["Master of Smell", "Mistress of Smell"],
                         ["Master of Taste", "Mistress of Taste"],
                         ["Master of Touch", "Mistress of Touch"],

                         ["Crime Lord", "Crime Mistress"],
                         ["Infamous Crime Lord", "Infamous Crime Mistress"],
                         ["Greater Crime Lord", "Greater Crime Mistress"],
                         ["Master Crime Lord", "Master Crime Mistress"],
                         ["Godfather", "Godmother"],

                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],

                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],

                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],
                         ["Master Thief", "Master Thief"],

                         ["Assassin Hero", "Assassin Heroine"],
                         ["Avatar of Death", "Avatar of Death"],
                         ["Angel of Death", "Angel of Death"],
                         ["Demigod of Assassins", "Demigoddess of Assassins"],
                         ["Immortal Assasin", "Immortal Assassin"],
                         ["God of Assassins", "God of Assassins"],
                         ["Deity of Assassins", "Deity of Assassins"],
                         ["Supreme Master", "Supreme Mistress"],
                         ["Creator", "Creator"],
                         ["Implementor", "Implementress"]],
               'warrior': [["Man", "Woman"],

                           ["Swordpupil", "Swordpupil"],
                           ["Recruit", "Recruit"],
                           ["Sentry", "Sentress"],
                           ["Fighter", "Fighter"],
                           ["Soldier", "Soldier"],

                           ["Warrior", "Warrior"],
                           ["Veteran", "Veteran"],
                           ["Swordsman", "Swordswoman"],
                           ["Fencer", "Fenceress"],
                           ["Combatant", "Combatess"],

                           ["Hero", "Heroine"],
                           ["Myrmidon", "Myrmidon"],
                           ["Swashbuckler", "Swashbuckleress"],
                           ["Mercenary", "Mercenaress"],
                           ["Swordmaster", "Swordmistress"],

                           ["Lieutenant", "Lieutenant"],
                           ["Champion", "Lady Champion"],
                           ["Dragoon", "Lady Dragoon"],
                           ["Cavalier", "Lady Cavalier"],
                           ["Knight", "Lady Knight"],

                           ["Grand Knight", "Grand Knight"],
                           ["Master Knight", "Master Knight"],
                           ["Paladin", "Paladin"],
                           ["Grand Paladin", "Grand Paladin"],
                           ["Demon Slayer", "Demon Slayer"],

                           ["Greater Demon Slayer", "Greater Demon Slayer"],
                           ["Dragon Slayer", "Dragon Slayer"],
                           ["Greater Dragon Slayer", "Greater Dragon Slayer"],
                           ["Underlord", "Underlord"],
                           ["Overlord", "Overlord"],

                           ["Baron of Thunder", "Baroness of Thunder"],
                           ["Baron of Storms", "Baroness of Storms"],
                           ["Baron of Tornadoes", "Baroness of Tornadoes"],
                           ["Baron of Hurricanes", "Baroness of Hurricanes"],
                           ["Baron of Meteors", "Baroness of Meteors"],

                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],

                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],

                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],
                           ["Master Warrior", "Master Warrior"],

                           ["Knight Hero", "Knight Heroine"],
                           ["Avatar of War", "Avatar of War"],
                           ["Angel of War", "Angel of War"],
                           ["Demigod of War", "Demigoddess of War"],
                           ["Immortal Warlord", "Immortal Warlord"],
                           ["God of War", "God of War"],
                           ["Deity of War", "Deity of War"],
                           ["Supreme Master of War", "Supreme Mistress of War"],
                           ["Creator", "Creator"],
                           ["Implementor", "Implementress"]]}


# * Attribute bonus structures.
str_app_type = namedtuple('str_app_type', 'tohit, todam, carry, wield')
str_app = OrderedDict()
str_app[0] = str_app_type(-5, -4, 0, 0)
str_app[1] = str_app_type(-5, -4, 3, 1)
str_app[2] = str_app_type(-3, -2, 3, 2)
str_app[3] = str_app_type(-3, -1, 10, 3)
str_app[4] = str_app_type(-2, -1, 25, 4)
str_app[5] = str_app_type(-2, -1, 55, 5)
str_app[6] = str_app_type(-1, 0, 80, 6)
str_app[7] = str_app_type(-1, 0, 90, 7)
str_app[8] = str_app_type(0, 0, 100, 8)
str_app[9] = str_app_type(0, 0, 100, 9)
str_app[10] = str_app_type(0, 0, 115, 10)
str_app[11] = str_app_type(0, 0, 115, 11)
str_app[12] = str_app_type(0, 0, 130, 12)
str_app[13] = str_app_type(0, 0, 130, 13)
str_app[14] = str_app_type(0, 1, 140, 14)
str_app[15] = str_app_type(1, 1, 150, 15)
str_app[16] = str_app_type(1, 2, 165, 16)
str_app[17] = str_app_type(2, 3, 180, 22)
str_app[18] = str_app_type(2, 3, 200, 25)
str_app[19] = str_app_type(3, 4, 225, 30)
str_app[20] = str_app_type(3, 5, 250, 35)
str_app[21] = str_app_type(4, 6, 300, 40)
str_app[22] = str_app_type(4, 6, 350, 45)
str_app[23] = str_app_type(5, 7, 400, 50)
str_app[24] = str_app_type(5, 8, 450, 55)
str_app[25] = str_app_type(6, 9, 500, 60)

int_app_type = namedtuple('int_app_type', 'learn')
int_app = OrderedDict()
int_app[0] = int_app_type(3)
int_app[1] = int_app_type(5)
int_app[2] = int_app_type(7)
int_app[3] = int_app_type(8)
int_app[4] = int_app_type(9)
int_app[5] = int_app_type(10)
int_app[6] = int_app_type(11)
int_app[7] = int_app_type(12)
int_app[8] = int_app_type(13)
int_app[9] = int_app_type(15)
int_app[10] = int_app_type(17)
int_app[11] = int_app_type(19)
int_app[12] = int_app_type(22)
int_app[13] = int_app_type(25)
int_app[14] = int_app_type(28)
int_app[15] = int_app_type(31)
int_app[16] = int_app_type(34)
int_app[17] = int_app_type(37)
int_app[18] = int_app_type(40)
int_app[19] = int_app_type(44)
int_app[20] = int_app_type(49)
int_app[21] = int_app_type(55)
int_app[22] = int_app_type(60)
int_app[23] = int_app_type(70)
int_app[24] = int_app_type(80)
int_app[25] = int_app_type(85)

wis_app_type = namedtuple('wis_app_type', 'practice')
wis_app = OrderedDict()
wis_app[0] = wis_app_type(0)  # /*  0 */
wis_app[1] = wis_app_type(0)  # /*  1 */
wis_app[2] = wis_app_type(0)
wis_app[3] = wis_app_type(0)  # /*  3 */
wis_app[4] = wis_app_type(0)
wis_app[5] = wis_app_type(1)  # /*  5 */
wis_app[6] = wis_app_type(1)
wis_app[7] = wis_app_type(1)
wis_app[8] = wis_app_type(1)
wis_app[9] = wis_app_type(1)
wis_app[10] = wis_app_type(1)  # /* 10 */
wis_app[11] = wis_app_type(1)
wis_app[12] = wis_app_type(1)
wis_app[13] = wis_app_type(1)
wis_app[14] = wis_app_type(1)
wis_app[15] = wis_app_type(2)  # /* 15 */
wis_app[16] = wis_app_type(2)
wis_app[17] = wis_app_type(2)
wis_app[18] = wis_app_type(3)  # /* 18 */
wis_app[19] = wis_app_type(3)
wis_app[20] = wis_app_type(3)  # /* 20 */
wis_app[21] = wis_app_type(3)
wis_app[22] = wis_app_type(4)
wis_app[23] = wis_app_type(4)
wis_app[24] = wis_app_type(4)
wis_app[25] = wis_app_type(5)  # /* 25 */

dex_app_type = namedtuple('dex_app_type', 'defensive')
dex_app = OrderedDict()
dex_app[0] = dex_app_type(60)  # /* 0 */
dex_app[1] = dex_app_type(50)  # /* 1 */
dex_app[2] = dex_app_type(50)
dex_app[3] = dex_app_type(40)
dex_app[4] = dex_app_type(30)
dex_app[5] = dex_app_type(20)  # /* 5 */
dex_app[6] = dex_app_type(10)
dex_app[7] = dex_app_type(0)
dex_app[8] = dex_app_type(0)
dex_app[9] = dex_app_type(0)
dex_app[10] = dex_app_type(0)  # /* 10 */
dex_app[11] = dex_app_type(0)
dex_app[12] = dex_app_type(0)
dex_app[13] = dex_app_type(0)
dex_app[14] = dex_app_type(0)
dex_app[15] = dex_app_type(-10)  # /* 15 */
dex_app[16] = dex_app_type(-15)
dex_app[17] = dex_app_type(-20)
dex_app[18] = dex_app_type(-30)
dex_app[19] = dex_app_type(-40)
dex_app[20] = dex_app_type(-50)  # /* 20 */
dex_app[21] = dex_app_type(-60)
dex_app[22] = dex_app_type(-75)
dex_app[23] = dex_app_type(-90)
dex_app[24] = dex_app_type(-105)
dex_app[25] = dex_app_type(-120)  # /* 25 */

con_app_type = namedtuple('con_app_type', 'hitp, shock')
con_app = OrderedDict()
con_app[0] = con_app_type(-4, 20)  # /*  0 */
con_app[1] = con_app_type(-3, 25)  # /*  1 */
con_app[2] = con_app_type(-2, 30)
con_app[3] = con_app_type(-2, 35)  # /*  3 */
con_app[4] = con_app_type(-1, 40)
con_app[5] = con_app_type(-1, 45)  # /*  5 */
con_app[6] = con_app_type(-1, 50)
con_app[7] = con_app_type(0, 55)
con_app[8] = con_app_type(0, 60)
con_app[9] = con_app_type(0, 65)
con_app[10] = con_app_type(0, 70)  # /* 10 */
con_app[11] = con_app_type(0, 75)
con_app[12] = con_app_type(0, 80)
con_app[13] = con_app_type(0, 85)
con_app[14] = con_app_type(0, 88)
con_app[15] = con_app_type(1, 90)  # /* 15 */
con_app[16] = con_app_type(2, 95)
con_app[17] = con_app_type(2, 97)
con_app[18] = con_app_type(3, 99)  # /* 18 */
con_app[19] = con_app_type(3, 99)
con_app[20] = con_app_type(4, 99)  # /* 20 */
con_app[21] = con_app_type(4, 99)
con_app[22] = con_app_type(5, 99)
con_app[23] = con_app_type(6, 99)
con_app[24] = con_app_type(7, 99)
con_app[25] = con_app_type(8, 99)  # /* 25 */


#/* attack table  -- not very organized :( */
attack_type = namedtuple('attack_type', 'name, noun, damage')
attack_table = OrderedDict()
attack_table[0] = attack_type("none", "hit", -1)   # 0
attack_table[1] = attack_type("slice", "slice", DAM_SLASH)
attack_table[2] = attack_type("stab", "stab", DAM_PIERCE)
attack_table[3] = attack_type("slash", "slash", DAM_SLASH)
attack_table[4] = attack_type("whip", "whip", DAM_SLASH)
attack_table[5] = attack_type("claw", "claw", DAM_SLASH)  # 5
attack_table[6] = attack_type("blast", "blast", DAM_BASH)
attack_table[7] = attack_type("pound", "pound", DAM_BASH)
attack_table[8] = attack_type("crush", "crush", DAM_BASH)
attack_table[9] = attack_type("grep", "grep", DAM_SLASH)
attack_table[10] = attack_type("bite", "bite", DAM_PIERCE)  # 10
attack_table[11] = attack_type("pierce", "pierce", DAM_PIERCE)
attack_table[12] = attack_type("suction", "suction", DAM_BASH)
attack_table[13] = attack_type("beating", "beating", DAM_BASH)
attack_table[14] = attack_type("digestion", "digestion", DAM_ACID)
attack_table[15] = attack_type("charge", "charge", DAM_BASH)  # 15
attack_table[16] = attack_type("slap", "slap", DAM_BASH)
attack_table[17] = attack_type("punch", "punch", DAM_BASH)
attack_table[18] = attack_type("wrath", "wrath", DAM_ENERGY)
attack_table[19] = attack_type("magic", "magic", DAM_ENERGY)
attack_table[20] = attack_type("divine", "divine power", DAM_HOLY)  # 20
attack_table[21] = attack_type("cleave", "cleave", DAM_SLASH)
attack_table[22] = attack_type("scratch", "scratch", DAM_PIERCE)
attack_table[23] = attack_type("peck", "peck", DAM_PIERCE)
attack_table[24] = attack_type("peckb", "peck", DAM_BASH)
attack_table[25] = attack_type("chop", "chop", DAM_SLASH)  # 25
attack_table[26] = attack_type("sting", "sting", DAM_PIERCE)
attack_table[27] = attack_type("smash", "smash", DAM_BASH)
attack_table[28] = attack_type("shbite", "shocking bite", DAM_LIGHTNING)
attack_table[29] = attack_type("flbite", "flaming bite", DAM_FIRE)
attack_table[30] = attack_type("frbite", "freezing bite", DAM_COLD)  # 30
attack_table[31] = attack_type("acbite", "acidic bite", DAM_ACID)
attack_table[32] = attack_type("chomp", "chomp", DAM_PIERCE)
attack_table[33] = attack_type("drain", "life drain", DAM_NEGATIVE)
attack_table[34] = attack_type("thrust", "thrust", DAM_PIERCE)
attack_table[35] = attack_type("slime", "slime", DAM_ACID)
attack_table[36] = attack_type("shock", "shock", DAM_LIGHTNING)
attack_table[37] = attack_type("thwack", "thwack", DAM_BASH)
attack_table[38] = attack_type("flame", "flame", DAM_FIRE)
attack_table[39] = attack_type("chill", "chill", DAM_COLD)


wiznet_type = namedtuple('wiznet_type', 'name flag level')
wiznet_table = OrderedDict()
wiznet_table["on"] = wiznet_type("on", WIZ_ON, IM)
wiznet_table["prefix"] = wiznet_type("prefix", WIZ_PREFIX, IM)
wiznet_table["ticks"] = wiznet_type("ticks", WIZ_TICKS, IM)
wiznet_table["logins"] = wiznet_type("logins", WIZ_LOGINS, IM)
wiznet_table["sites"] = wiznet_type("sites", WIZ_SITES, L4)
wiznet_table["links"] = wiznet_type("links", WIZ_LINKS, L7)
wiznet_table["newbies"] = wiznet_type("newbies", WIZ_NEWBIE, IM)
wiznet_table["spam"] = wiznet_type("spam", WIZ_SPAM, L5)
wiznet_table["deaths"] = wiznet_type("deaths", WIZ_DEATHS, IM)
wiznet_table["resets"] = wiznet_type("resets", WIZ_RESETS, L4)
wiznet_table["mobdeaths"] = wiznet_type("mobdeaths", WIZ_MOBDEATHS, L4)
wiznet_table["flags"] = wiznet_type("flags", WIZ_FLAGS, L5)
wiznet_table["penalties"] = wiznet_type("penalties", WIZ_PENALTIES, L5)
wiznet_table["saccing"] = wiznet_type("saccing", WIZ_SACCING, L5)
wiznet_table["levels"] = wiznet_type("levels", WIZ_LEVELS, IM)
wiznet_table["load"] = wiznet_type("load", WIZ_LOAD, L2)
wiznet_table["restore"] = wiznet_type("restore", WIZ_RESTORE, L2)
wiznet_table["snoops"] = wiznet_type("snoops", WIZ_SNOOPS, L2)
wiznet_table["switches"] = wiznet_type("switches", WIZ_SWITCHES, L2)
wiznet_table["secure"] = wiznet_type("secure", WIZ_SECURE, L1)

liq_type = namedtuple('liq_type', 'name color proof full thirst food ssize')
liq_table = OrderedDict()
liq_table["water"] = liq_type("water", "clear", 0, 1, 10, 0, 16)
liq_table["beer"] = liq_type("beer", "amber", 12, 1, 8, 1, 12)
liq_table["red wine"] = liq_type("red wine", "burgundy", 30, 1, 8, 1, 5)
liq_table["ale"] = liq_type("ale", "brown", 15, 1, 8, 1, 12)
liq_table["dark ale"] = liq_type("dark ale", "dark", 16, 1, 8, 1, 12)
liq_table["whisky"] = liq_type("whisky", "golden", 120, 1, 5, 0, 2)
liq_table["lemonade"] = liq_type("lemonade", "pink", 0, 1, 9, 2, 12)
liq_table["firebreather"] = liq_type("firebreather", "boiling", 190, 0, 4, 0, 2)
liq_table["local specialty"] = liq_type("local specialty", "clear", 151, 1, 3, 0, 2)
liq_table["slime mold juice"] = liq_type("slime mold juice", "green", 0, 2, -8, 1, 2)
liq_table["milk"] = liq_type("milk", "white", 0, 2, 9, 3, 12)
liq_table["tea"] = liq_type("tea", "tan", 0, 1, 8, 0, 6)
liq_table["coffee"] = liq_type("coffee", "black", 0, 1, 8, 0, 6)
liq_table["blood"] = liq_type("blood", "red", 0, 2, -1, 2, 6)
liq_table["salt water"] = liq_type("salt water", "clear", 0, 1, -2, 0, 1)
liq_table["coke"] = liq_type("coke", "brown", 0, 2, 9, 2, 12)
liq_table["root beer"] = liq_type("root beer", "brown", 0, 2, 9, 2, 12)
liq_table["elvish wine"] = liq_type("elvish wine", "green", 35, 2, 8, 1, 5)
liq_table["white wine"] = liq_type("white wine", "golden", 28, 1, 8, 1, 5)
liq_table["champagne"] = liq_type("champagne", "golden", 32, 1, 8, 1, 5)
liq_table["mead"] = liq_type("mead", "honey-colored", 34, 2, 8, 2, 12)
liq_table["rose wine"] = liq_type("rose wine", "pink", 26, 1, 8, 1, 5)
liq_table["benedictine wine"] = liq_type("benedictine wine", "burgundy", 40, 1, 8, 1, 5)
liq_table["vodka"] = liq_type("vodka", "clear", 130, 1, 5, 0, 2)
liq_table["cranberry juice"] = liq_type("cranberry juice", "red", 0, 1, 9, 2, 12)
liq_table["orange juice"] = liq_type("orange juice", "orange", 0, 2, 9, 3, 12)
liq_table["absinthe"] = liq_type("absinthe", "green", 200, 1, 4, 0, 2)
liq_table["brandy"] = liq_type("brandy", "golden", 80, 1, 5, 0, 4)
liq_table["aquavit"] = liq_type("aquavit", "clear", 140, 1, 5, 0, 2)
liq_table["schnapps"] = liq_type("schnapps", "clear", 90, 1, 5, 0, 2)
liq_table["icewine"] = liq_type("icewine", "purple", 50, 2, 6, 1, 5)
liq_table["amontillado"] = liq_type("amontillado", "burgundy", 35, 2, 8, 1, 5)
liq_table["sherry"] = liq_type("sherry", "red", 38, 2, 7, 1, 5)
liq_table["framboise"] = liq_type("framboise", "red", 50, 1, 7, 1, 5)
liq_table["rum"] = liq_type("rum", "amber", 151, 1, 4, 0, 2)
liq_table["cordial"] = liq_type("cordial", "clear", 100, 1, 5, 0, 2)
