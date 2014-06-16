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
from collections import OrderedDict
from merc import *

class clan_type:
    def __init__(self, name, who_name, hall, independent):
        self.name=name
        self.who_name=who_name
        self.hall=hall #Death Transfer Room
        self.independent=independent # true for loners */

clan_table = OrderedDict()
clan_table[""] = clan_type("", "", ROOM_VNUM_ALTAR, True)
clan_table["loner"] = clan_type("loner", "[ Loner ] ", ROOM_VNUM_ALTAR, True)
clan_table["rom"] = clan_type("rom", "[  ROM  ] ", ROOM_VNUM_ALTAR, False)

class position_type:
    def __init__(self, name, short_name):
        self.name=name
        self.short_name=short_name

position_table = OrderedDict()
position_table[POS_DEAD] = position_type("dead", "dead")
position_table[POS_MORTAL] = position_type("mortally wounded", "mort")
position_table[POS_INCAP] = position_type("incapacitated", "incap")
position_table[POS_STUNNED] = position_type("stunned", "stun")
position_table[POS_SLEEPING] = position_type("sleeping", "sleep")
position_table[POS_RESTING] = position_type("resting", "rest")
position_table[POS_SITTING] = position_type("sitting", "sit")
position_table[POS_FIGHTING] = position_type("fighting", "fight")
position_table[POS_STANDING] = position_type("standing", "stand")

sex_table = OrderedDict()
sex_table[SEX_MALE] = "male"
sex_table[SEX_FEMALE] = "female"
sex_table[SEX_NEUTRAL] = "either"


# for sizes */
size_table = OrderedDict()
size_table[SIZE_TINY] = ("tiny")
size_table[SIZE_SMALL] = ("small")
size_table[SIZE_MEDIUM] = ("medium")
size_table[SIZE_LARGE] = ("large")
size_table[SIZE_HUGE] = ("huge")
size_table[SIZE_GIANT] = ("giant")

class flag_type:
    def __init__(self, name, bit, settable):
        self.name=name
        self.bit=bit
        self.settable=settable

# various flag tables */
act_flags = OrderedDict()
act_flags["npc"] = flag_type("npc", A, False)
act_flags["sentinel"] = flag_type("sentinel", B, True)
act_flags["scavenger"] = flag_type("scavenger", C, True)
act_flags["aggressive"] = flag_type("aggressive", F, True)
act_flags["stay_area"] = flag_type("stay_area", G, True)
act_flags["wimpy"] = flag_type("wimpy", H, True)
act_flags["pet"] = flag_type("pet", I, True)
act_flags["train"] = flag_type("train", J, True)
act_flags["practice"] = flag_type("practice", K, True)
act_flags["undead"] = flag_type("undead", O, True)
act_flags["cleric"] = flag_type("cleric", Q, True)
act_flags["mage"] = flag_type("mage", R, True)
act_flags["thief"] = flag_type("thief", S, True)
act_flags["warrior"] = flag_type("warrior", T, True)
act_flags["noalign"] = flag_type("noalign", U, True)
act_flags["nopurge"] = flag_type("nopurge", V, True)
act_flags["outdoors"] = flag_type("outdoors", W, True)
act_flags["indoors"] = flag_type("indoors", Y, True)
act_flags["healer"] = flag_type("healer", aa, True)
act_flags["gain"] = flag_type("gain", bb, True)
act_flags["update_always"] = flag_type("update_always", cc, True)
act_flags["changer"] = flag_type("changer", dd, True)

plr_flags = OrderedDict()
plr_flags["npc"] = flag_type("npc", A, False)
plr_flags["autoassist"] = flag_type("autoassist", C, False)
plr_flags["autoexit"] = flag_type("autoexit", D, False)
plr_flags["autoloot"] = flag_type("autoloot", E, False)
plr_flags["autosac"] = flag_type("autosac", F, False)
plr_flags["autogold"] = flag_type("autogold", G, False)
plr_flags["autosplit"] = flag_type("autosplit", H, False)
plr_flags["holylight"] = flag_type("holylight", N, False)
plr_flags["can_loot"] = flag_type("can_loot", P, False)
plr_flags["nosummon"] = flag_type("nosummon", Q, False)
plr_flags["nofollow"] = flag_type("nofollow", R, False)
plr_flags["permit"] = flag_type("permit", U, True)
plr_flags["log"] = flag_type("log", W, False)
plr_flags["deny"] = flag_type("deny", X, False)
plr_flags["freeze"] = flag_type("freeze", Y, False)
plr_flags["thief"] = flag_type("thief", Z, False)
plr_flags["killer"] = flag_type("killer", aa, False)

affect_flags = OrderedDict()
affect_flags["blind"] = flag_type("blind", A, True)
affect_flags["invisible"] = flag_type("invisible", B, True)
affect_flags["detect_evil"] = flag_type("detect_evil", C, True)
affect_flags["detect_invis"] = flag_type("detect_invis", D, True)
affect_flags["detect_magic"] = flag_type("detect_magic", E, True)
affect_flags["detect_hidden"] = flag_type("detect_hidden", F, True)
affect_flags["detect_good"] = flag_type("detect_good", G, True)
affect_flags["sanctuary"] = flag_type("sanctuary", H, True)
affect_flags["faerie_fire"] = flag_type("faerie_fire", I, True)
affect_flags["infrared"] = flag_type("infrared", J, True)
affect_flags["curse"] = flag_type("curse", K, True)
affect_flags["poison"] = flag_type("poison", M, True)
affect_flags["protect_evil"] = flag_type("protect_evil", N, True)
affect_flags["protect_good"] = flag_type("protect_good", O, True)
affect_flags["sneak"] = flag_type("sneak", P, True)
affect_flags["hide"] = flag_type("hide", Q, True)
affect_flags["sleep"] = flag_type("sleep", R, True)
affect_flags["charm"] = flag_type("charm", S, True)
affect_flags["flying"] = flag_type("flying", T, True)
affect_flags["pass_door"] = flag_type("pass_door", U, True)
affect_flags["haste"] = flag_type("haste", V, True)
affect_flags["calm"] = flag_type("calm", W, True)
affect_flags["plague"] = flag_type("plague", X, True)
affect_flags["weaken"] = flag_type("weaken", Y, True)
affect_flags["dark_vision"] = flag_type("dark_vision", Z, True)
affect_flags["berserk"] = flag_type("berserk", aa, True)
affect_flags["swim"] = flag_type("swim", bb, True)
affect_flags["regeneration"] = flag_type("regeneration", cc, True)
affect_flags["slow"] = flag_type("slow", dd, True)

off_flags = OrderedDict()
off_flags["area_attack"] = flag_type("area_attack", A, True)
off_flags["backstab"] = flag_type("backstab", B, True)
off_flags["bash"] = flag_type("bash", C, True)
off_flags["berserk"] = flag_type("berserk", D, True)
off_flags["disarm"] = flag_type("disarm", E, True)
off_flags["dodge"] = flag_type("dodge", F, True)
off_flags["fade"] = flag_type("fade", G, True)
off_flags["fast"] = flag_type("fast", H, True)
off_flags["kick"] = flag_type("kick", I, True)
off_flags["dirt_kick"] = flag_type("dirt_kick", J, True)
off_flags["parry"] = flag_type("parry", K, True)
off_flags["rescue"] = flag_type("rescue", L, True)
off_flags["tail"] = flag_type("tail", M, True)
off_flags["trip"] = flag_type("trip", N, True)
off_flags["crush"] = flag_type("crush", O, True)
off_flags["assist_all"] = flag_type("assist_all", P, True)
off_flags["assist_align"] = flag_type("assist_align", Q, True)
off_flags["assist_race"] = flag_type("assist_race", R, True)
off_flags["assist_players"] = flag_type("assist_players", S, True)
off_flags["assist_guard"] = flag_type("assist_guard", T, True)
off_flags["assist_vnum"] = flag_type("assist_vnum", U, True)

imm_flags = OrderedDict()
imm_flags["summon"] = flag_type("summon", A, True)
imm_flags["charm"] = flag_type("charm", B, True)
imm_flags["magic"] = flag_type("magic", C, True)
imm_flags["weapon"] = flag_type("weapon", D, True)
imm_flags["bash"] = flag_type("bash", E, True)
imm_flags["pierce"] = flag_type("pierce", F, True)
imm_flags["slash"] = flag_type("slash", G, True)
imm_flags["fire"] = flag_type("fire", H, True)
imm_flags["cold"] = flag_type("cold", I, True)
imm_flags["lightning"] = flag_type("lightning", J, True)
imm_flags["acid"] = flag_type("acid", K, True)
imm_flags["poison"] = flag_type("poison", L, True)
imm_flags["negative"] = flag_type("negative", M, True)
imm_flags["holy"] = flag_type("holy", N, True)
imm_flags["energy"] = flag_type("energy", O, True)
imm_flags["mental"] = flag_type("mental", P, True)
imm_flags["disease"] = flag_type("disease", Q, True)
imm_flags["drowning"] = flag_type("drowning", R, True)
imm_flags["light"] = flag_type("light", S, True)
imm_flags["sound"] = flag_type("sound", T, True)
imm_flags["wood"] = flag_type("wood", X, True)
imm_flags["silver"] = flag_type("silver", Y, True)
imm_flags["iron"] = flag_type("iron", Z, True)

form_flags = OrderedDict()
form_flags["edible"] = flag_type("edible", FORM_EDIBLE, True)
form_flags["poison"] = flag_type("poison", FORM_POISON, True)
form_flags["magical"] = flag_type("magical", FORM_MAGICAL, True)
form_flags["instant_decay"] = flag_type("instant_decay", FORM_INSTANT_DECAY, True)
form_flags["other"] = flag_type("other", FORM_OTHER, True)
form_flags["animal"] = flag_type("animal", FORM_ANIMAL, True)
form_flags["sentient"] = flag_type("sentient", FORM_SENTIENT, True)
form_flags["undead"] = flag_type("undead", FORM_UNDEAD, True)
form_flags["construct"] = flag_type("construct", FORM_CONSTRUCT, True)
form_flags["mist"] = flag_type("mist", FORM_MIST, True)
form_flags["intangible"] = flag_type("intangible", FORM_INTANGIBLE, True)
form_flags["biped"] = flag_type("biped", FORM_BIPED, True)
form_flags["centaur"] = flag_type("centaur", FORM_CENTAUR, True)
form_flags["insect"] = flag_type("insect", FORM_INSECT, True)
form_flags["spider"] = flag_type("spider", FORM_SPIDER, True)
form_flags["crustacean"] = flag_type("crustacean", FORM_CRUSTACEAN, True)
form_flags["worm"] = flag_type("worm", FORM_WORM, True)
form_flags["blob"] = flag_type("blob", FORM_BLOB, True)
form_flags["mammal"] = flag_type("mammal", FORM_MAMMAL, True)
form_flags["bird"] = flag_type("bird", FORM_BIRD, True)
form_flags["reptile"] = flag_type("reptile", FORM_REPTILE, True)
form_flags["snake"] = flag_type("snake", FORM_SNAKE, True)
form_flags["dragon"] = flag_type("dragon", FORM_DRAGON, True)
form_flags["amphibian"] = flag_type("amphibian", FORM_AMPHIBIAN, True)
form_flags["fish"] = flag_type("fish", FORM_FISH, True)
form_flags["cold_blood"] = flag_type("cold_blood", FORM_COLD_BLOOD, True)

part_flags = OrderedDict()
part_flags["head"] = flag_type("head", PART_HEAD, True)
part_flags["arms"] = flag_type("arms", PART_ARMS, True)
part_flags["legs"] = flag_type("legs", PART_LEGS, True)
part_flags["heart"] = flag_type("heart", PART_HEART, True)
part_flags["brains"] = flag_type("brains", PART_BRAINS, True)
part_flags["guts"] = flag_type("guts", PART_GUTS, True)
part_flags["hands"] = flag_type("hands", PART_HANDS, True)
part_flags["feet"] = flag_type("feet", PART_FEET, True)
part_flags["fingers"] = flag_type("fingers", PART_FINGERS, True)
part_flags["ear"] = flag_type("ear", PART_EAR, True)
part_flags["eye"] = flag_type("eye", PART_EYE, True)
part_flags["long_tongue"] = flag_type("long_tongue", PART_LONG_TONGUE, True)
part_flags["eyestalks"] = flag_type("eyestalks", PART_EYESTALKS, True)
part_flags["tentacles"] = flag_type("tentacles", PART_TENTACLES, True)
part_flags["fins"] = flag_type("fins", PART_FINS, True)
part_flags["wings"] = flag_type("wings", PART_WINGS, True)
part_flags["tail"] = flag_type("tail", PART_TAIL, True)
part_flags["claws"] = flag_type("claws", PART_CLAWS, True)
part_flags["fangs"] = flag_type("fangs", PART_FANGS, True)
part_flags["horns"] = flag_type("horns", PART_HORNS, True)
part_flags["scales"] = flag_type("scales", PART_SCALES, True)
part_flags["tusks"] = flag_type("tusks", PART_TUSKS, True)

comm_flags = OrderedDict()
comm_flags["quiet"] = flag_type("quiet", COMM_QUIET, True)
comm_flags["deaf"] = flag_type("deaf", COMM_DEAF, True)
comm_flags["nowiz"] = flag_type("nowiz", COMM_NOWIZ, True)
comm_flags["noclangossip"] = flag_type("noclangossip", COMM_NOAUCTION, True)
comm_flags["nogossip"] = flag_type("nogossip", COMM_NOGOSSIP, True)
comm_flags["noquestion"] = flag_type("noquestion", COMM_NOQUESTION, True)
comm_flags["nomusic"] = flag_type("nomusic", COMM_NOMUSIC, True)
comm_flags["noclan"] = flag_type("noclan", COMM_NOCLAN, True)
comm_flags["noquote"] = flag_type("noquote", COMM_NOQUOTE, True)
comm_flags["shoutsoff"] = flag_type("shoutsoff", COMM_SHOUTSOFF, True)
comm_flags["compact"] = flag_type("compact", COMM_COMPACT, True)
comm_flags["brief"] = flag_type("brief", COMM_BRIEF, True)
comm_flags["prompt"] = flag_type("prompt", COMM_PROMPT, True)
comm_flags["combine"] = flag_type("combine", COMM_COMBINE, True)
comm_flags["telnet_ga"] = flag_type("telnet_ga", COMM_TELNET_GA, True)
comm_flags["show_affects"] = flag_type("show_affects", COMM_SHOW_AFFECTS, True)
comm_flags["nograts"] = flag_type("nograts", COMM_NOGRATS, True)
comm_flags["noemote"] = flag_type("noemote", COMM_NOEMOTE, False)
comm_flags["noshout"] = flag_type("noshout", COMM_NOSHOUT, False)
comm_flags["notell"] = flag_type("notell", COMM_NOTELL, False)
comm_flags["nochannels"] = flag_type("nochannels", COMM_NOCHANNELS, False)
comm_flags["snoop_proof"] = flag_type("snoop_proof", COMM_SNOOP_PROOF, False)
comm_flags["afk"] = flag_type("afk", COMM_AFK, True)
