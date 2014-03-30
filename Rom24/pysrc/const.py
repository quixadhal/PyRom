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
 ************/
"""
from merc import *
from magic import *
class race_type:
    def __init__(self, name, pc_race, act, aff, off, imm, res, vuln, form, parts):
        self.name = name
        self.pc_race = pc_race
        self.act=act
        self.aff=aff
        self.off=off
        self.imm=imm
        self.res=res
        self.vuln=vuln
        self.form=form
        self.parts=parts

race_table = {}
race_table["unique"] = race_type("unique", False, 0, 0, 0, 0, 0, 0, 0, 0)
race_table["human"] = race_type("human", True, 0, 0, 0, 0, 0, 0, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K)
race_table["elf"] = race_type("elf", True, 0, AFF_INFRARED, 0, 0, RES_CHARM, VULN_IRON, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K)
race_table["dwarf"] = race_type("dwarf", True, 0, AFF_INFRARED, 0, 0, RES_POISON|RES_DISEASE, VULN_DROWNING, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K)
race_table["giant"] = race_type("giant", True, 0, 0, 0, 0, RES_FIRE|RES_COLD, VULN_MENTAL|VULN_LIGHTNING, A|H|M|V,  A|B|C|D|E|F|G|H|I|J|K)
race_table["bat"] = race_type("bat", False, 0, AFF_FLYING|AFF_DARK_VISION, OFF_DODGE|OFF_FAST, 0, 0, VULN_LIGHT, A|G|V, A|C|D|E|F|H|J|K|P)
race_table["bear"] = race_type("bear", False, 0, 0, OFF_CRUSH|OFF_DISARM|OFF_BERSERK, 0, RES_BASH|RES_COLD, 0, A|G|V, A|B|C|D|E|F|H|J|K|U|V)
race_table["cat"] = race_type("cat", False, 0, AFF_DARK_VISION, OFF_FAST|OFF_DODGE, 0, 0, 0, A|G|V, A|C|D|E|F|H|J|K|Q|U|V) 
race_table["centipede"] = race_type("centipede", False, 0, AFF_DARK_VISION, 0, 0, RES_PIERCE|RES_COLD, VULN_BASH, A|B|G|O, A|C|K) 
race_table["dog"] = race_type("dog", False, 0, 0, OFF_FAST, 0, 0, 0, A|G|V, A|C|D|E|F|H|J|K|U|V) 
race_table["doll"] = race_type("doll", False, 0, 0, 0, IMM_COLD|IMM_POISON|IMM_HOLY|IMM_NEGATIVE|IMM_MENTAL|IMM_DISEASE |IMM_DROWNING, RES_BASH|RES_LIGHT, VULN_SLASH|VULN_FIRE|VULN_ACID|VULN_LIGHTNING|VULN_ENERGY, E|J|M|cc, A|B|C|G|H|K) 
race_table["dragon"] = race_type("dragon", False, 0, AFF_INFRARED|AFF_FLYING, 0, 0, RES_FIRE|RES_BASH|RES_CHARM, VULN_PIERCE|VULN_COLD, A|H|Z, A|C|D|E|F|G|H|I|J|K|P|Q|U|V|X) 
race_table["fido"] = race_type("fido", False, 0, 0, OFF_DODGE|ASSIST_RACE, 0, 0, VULN_MAGIC, A|B|G|V, A|C|D|E|F|H|J|K|Q|V) 
race_table["fox"] = race_type("fox", False, 0, AFF_DARK_VISION, OFF_FAST|OFF_DODGE, 0, 0, 0, A|G|V, A|C|D|E|F|H|J|K|Q|V) 
race_table["goblin"] = race_type("goblin", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE, VULN_MAGIC, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K) 
race_table["hobgoblin"] = race_type("hobgoblin", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE|RES_POISON, 0, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K|Y) 
race_table["kobold"] = race_type("kobold", False, 0, AFF_INFRARED, 0, 0, RES_POISON, VULN_MAGIC, A|B|H|M|V, A|B|C|D|E|F|G|H|I|J|K|Q) 
race_table["lizard"] = race_type("lizard", False, 0, 0, 0, 0, RES_POISON, VULN_COLD, A|G|X|cc, A|C|D|E|F|H|K|Q|V) 
race_table["modron"] = race_type("modron", False, 0, AFF_INFRARED, ASSIST_RACE|ASSIST_ALIGN, IMM_CHARM|IMM_DISEASE|IMM_MENTAL|IMM_HOLY|IMM_NEGATIVE, RES_FIRE|RES_COLD|RES_ACID, 0, H, A|B|C|G|H|J|K) 
race_table["orc"] = race_type("orc", False, 0, AFF_INFRARED, 0, 0, RES_DISEASE, VULN_LIGHT, A|H|M|V, A|B|C|D|E|F|G|H|I|J|K) 
race_table["pig"] = race_type("pig", False, 0, 0, 0, 0, 0, 0, A|G|V, A|C|D|E|F|H|J|K) 
race_table["rabbit"] = race_type("rabbit", False, 0, 0, OFF_DODGE|OFF_FAST, 0, 0, 0, A|G|V, A|C|D|E|F|H|J|K)
race_table["school monster"] = race_type("school monster", False, ACT_NOALIGN, 0, 0, IMM_CHARM|IMM_SUMMON, 0, VULN_MAGIC, A|M|V, A|B|C|D|E|F|H|J|K|Q|U) 
race_table["snake"] = race_type("snake", False, 0, 0, 0, 0, RES_POISON, VULN_COLD, A|G|X|Y|cc, A|D|E|F|K|L|Q|V|X)
race_table["song bird"] = race_type("song bird", False, 0, AFF_FLYING, OFF_FAST|OFF_DODGE, 0, 0, 0, A|G|W, A|C|D|E|F|H|K|P) 
race_table["troll"] = race_type("troll", False, 0, AFF_REGENERATION|AFF_INFRARED|AFF_DETECT_HIDDEN, OFF_BERSERK, 0, RES_CHARM|RES_BASH, VULN_FIRE|VULN_ACID, A|B|H|M|V, A|B|C|D|E|F|G|H|I|J|K|U|V) 
race_table["water fowl"] = race_type("water fowl", False, 0, AFF_SWIM|AFF_FLYING, 0, 0, RES_DROWNING, 0, A|G|W, A|C|D|E|F|H|K|P) 
race_table["wolf"] = race_type("wolf", False, 0, AFF_DARK_VISION, OFF_FAST|OFF_DODGE, 0, 0, 0, A|G|V, A|C|D|E|F|J|K|Q|V) 
race_table["wyvern"] = race_type("wyvern", False, 0, AFF_FLYING|AFF_DETECT_INVIS|AFF_DETECT_HIDDEN, OFF_BASH|OFF_FAST|OFF_DODGE, IMM_POISON, 0, VULN_LIGHT, A|B|G|Z, A|C|D|E|F|H|J|K|Q|V|X) 

class pc_race_type:
    def __init__(self, name, who_name, points, class_mult, skills, stats, max_stats, size):
        self.name = name
        self.who_name = who_name
        self.points = points
        self.class_mult = class_mult
        self.skills = skills
        self.stats = stats
        self.max_stats = max_stats
        self.size = size

pc_race_table={}
pc_race_table['human'] = pc_race_type("human", "Human", 0, [ 100, 100, 100, 100 ], [ "" ], [13, 13, 13, 13, 13], [18, 18, 18, 18, 18 ], SIZE_MEDIUM)
pc_race_table['elf'] = pc_race_type("elf", " Elf ", 5, { 'mage':100, 'cleric':125, 'thief':100, 'warrior':120 }, ["sneak", "hide"], [12, 14, 13, 15, 11], [16, 20, 18, 21, 15], SIZE_SMALL)
pc_race_table['dwarf'] = pc_race_type("dwarf", "Dwarf", 8, { 'mage':150, 'cleric':100, 'thief':125, 'warrior':100 }, ["berserk"], [14, 12, 14, 10, 15], [20, 16, 19, 14, 21], SIZE_MEDIUM)
pc_race_table['giant'] = pc_race_type("giant", "Giant", 6, { 'mage':200, 'cleric':150, 'thief':150, 'warrior':105 }, ["bash", "fast healing"], [16, 11, 13, 11, 14], [22, 15, 18, 15, 20], SIZE_LARGE)

def SLOT(i):
    return i

class skill_type:
    def __init__(self, name, skill_level, rating, spell_fun, target, minimum_position, pgsn, slot, min_mana, beats, noun_damage, msg_off, msg_obj ):
        self.name = name
        self.skill_level = skill_level
        self.rating = rating
        self.spell_fun = spell_fun
        self.target = target
        self.minimum_position = minimum_position
        self.pgsn = pgsn
        self.slot = slot
        self.min_mana = min_mana
        self.beats = beats
        self.noun_damage = noun_damage
        self.msg_off = msg_off
        self.msg_obj = msg_obj

skill_table = {}
skill_table["reserved"] = skill_type("reserved", { 'mage':99, 'cleric':99, 'thief':99, 'warrior':99 }, { 'mage':99, 'cleric':99, 'thief':99, 'warrior':99 }, 0, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 0, "", "", "")
skill_table["acid blast"] = skill_type("acid blast", { 'mage':28, 'cleric':53, 'thief':35, 'warrior':32 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_acid_blast, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(70), 20, 12, "acid blast", "!Acid Blast!", "")
skill_table["armor"] = skill_type("armor", { 'mage':7, 'cleric':2, 'thief':10, 'warrior':5 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_armor, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT( 1), 5, 12, "", "You feel less armored.", "")
skill_table["bless"] = skill_type("bless", { 'mage':53, 'cleric':7, 'thief':53, 'warrior':8 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_bless, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT( 3), 5, 12, "", "You feel less righteous.", "$p's holy aura fades.")
skill_table["blindness"] = skill_type("blindness", { 'mage':12, 'cleric':8, 'thief':17, 'warrior':15 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_blindness, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 4), 5, 12, "", "You can see again.", "")
skill_table["burning hands"] = skill_type("burning hands", { 'mage':7, 'cleric':53, 'thief':10, 'warrior':9 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_burning_hands, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 5), 15, 12, "burning hands", "!Burning Hands!", "")
skill_table["call lightning"] = skill_type("call lightning", { 'mage':26, 'cleric':18, 'thief':31, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_call_lightning, TAR_IGNORE, POS_FIGHTING, None, SLOT( 6), 15, 12, "lightning bolt", "!Call Lightning!", "")
skill_table["calm"] = skill_type("calm", { 'mage':48, 'cleric':16, 'thief':50, 'warrior':20 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_calm, TAR_IGNORE, POS_FIGHTING, None, SLOT(509), 30, 12, "", "You have lost your peace of mind.", "")
skill_table["cancellation"] = skill_type("cancellation", { 'mage':18, 'cleric':26, 'thief':34, 'warrior':34 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cancellation, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(507), 20, 12, "", "!cancellation!", "")
skill_table["cause critical"] = skill_type("cause critical", { 'mage':53, 'cleric':13, 'thief':53, 'warrior':19 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cause_critical, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(63), 20, 12, "spell", "!Cause Critical!", "")
skill_table["cause light"] = skill_type("cause light", { 'mage':53, 'cleric':1, 'thief':53, 'warrior':3 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cause_light, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(62), 15, 12, "spell", "!Cause Light!", "")
skill_table["cause serious"] = skill_type("cause serious", { 'mage':53, 'cleric':7, 'thief':53, 'warrior':10 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cause_serious, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(64), 17, 12, "spell", "!Cause Serious!", "")
skill_table["chain lightning"] = skill_type("chain lightning", { 'mage':33, 'cleric':53, 'thief':39, 'warrior':36 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_chain_lightning, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(500), 25, 12, "lightning", "!Chain Lightning!", "")
skill_table["change sex"] = skill_type("change sex", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_change_sex, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(82), 15, 12, "", "Your body feels familiar again.", "")
skill_table["charm person"] = skill_type("charm person", { 'mage':20, 'cleric':53, 'thief':25, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_charm_person, TAR_CHAR_OFFENSIVE, POS_STANDING, None, SLOT( 7), 5, 12, "", "You feel more self-confident.", "")
skill_table["chill touch"] = skill_type("chill touch", { 'mage':4, 'cleric':53, 'thief':6, 'warrior':6 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_chill_touch, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 8), 15, 12, "chilling touch", "You feel less cold.", "")
skill_table["colour spray"] = skill_type("colour spray", { 'mage':16, 'cleric':53, 'thief':22, 'warrior':20 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_colour_spray, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(10), 15, 12, "colour spray", "!Colour Spray!", "")
skill_table["continual light"] = skill_type("continual light", { 'mage':6, 'cleric':4, 'thief':6, 'warrior':9 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_continual_light, TAR_IGNORE, POS_STANDING, None, SLOT(57), 7, 12, "", "!Continual Light!", "")
skill_table["control weather"] = skill_type("control weather", { 'mage':15, 'cleric':19, 'thief':28, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_control_weather, TAR_IGNORE, POS_STANDING, None, SLOT(11), 25, 12, "", "!Control Weather!", "")
skill_table["create food"] = skill_type("create food", { 'mage':10, 'cleric':5, 'thief':11, 'warrior':12 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_create_food, TAR_IGNORE, POS_STANDING, None, SLOT(12), 5, 12, "", "!Create Food!", "")
skill_table["create rose"] = skill_type("create rose", { 'mage':16, 'cleric':11, 'thief':10, 'warrior':24 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_create_rose, TAR_IGNORE, POS_STANDING, None, SLOT(511), 30, 12, "", "!Create Rose!", "")
skill_table["create spring"] = skill_type("create spring", { 'mage':14, 'cleric':17, 'thief':23, 'warrior':20 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_create_spring, TAR_IGNORE, POS_STANDING, None, SLOT(80), 20, 12, "", "!Create Spring!", "")
skill_table["create water"] = skill_type("create water", { 'mage':8, 'cleric':3, 'thief':12, 'warrior':11 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_create_water, TAR_OBJ_INV, POS_STANDING, None, SLOT(13), 5, 12, "", "!Create Water!", "")
skill_table["cure blindness"] = skill_type("cure blindness", { 'mage':53, 'cleric':6, 'thief':53, 'warrior':8 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_blindness, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(14), 5, 12, "", "!Cure Blindness!", "")
skill_table["cure critical"] = skill_type("cure critical", { 'mage':53, 'cleric':13, 'thief':53, 'warrior':19 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_critical, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(15), 20, 12, "", "!Cure Critical!", "")
skill_table["cure disease"] = skill_type("cure disease", { 'mage':53, 'cleric':13, 'thief':53, 'warrior':14 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_disease, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(501), 20, 12, "", "!Cure Disease!", "")
skill_table["cure light"] = skill_type("cure light", { 'mage':53, 'cleric':1, 'thief':53, 'warrior':3 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_light, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(16), 10, 12, "", "!Cure Light!", "")
skill_table["cure poison"] = skill_type("cure poison", { 'mage':53, 'cleric':14, 'thief':53, 'warrior':16 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_poison, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(43), 5, 12, "", "!Cure Poison!", "")
skill_table["cure serious"] = skill_type("cure serious", { 'mage':53, 'cleric':7, 'thief':53, 'warrior':10 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_cure_serious, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(61), 15, 12, "", "!Cure Serious!", "")
skill_table["curse"] = skill_type("curse", { 'mage':18, 'cleric':18, 'thief':26, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_curse, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None, SLOT(17), 20, 12, "curse", "The curse wears off.", "$p is no longer impure.")
skill_table["demonfire"] = skill_type("demonfire", { 'mage':53, 'cleric':34, 'thief':53, 'warrior':45 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_demonfire, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(505), 20, 12, "torments", "!Demonfire!", "")
skill_table["detect evil"] = skill_type("detect evil", { 'mage':11, 'cleric':4, 'thief':12, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_evil, TAR_CHAR_SELF, POS_STANDING, None, SLOT(18), 5, 12, "", "The red in your vision disappears.", "")
skill_table["detect good"] = skill_type("detect good", { 'mage':11, 'cleric':4, 'thief':12, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_good, TAR_CHAR_SELF, POS_STANDING, None, SLOT(513), 5, 12, "", "The gold in your vision disappears.", "")
skill_table["detect hidden"] = skill_type("detect hidden", { 'mage':15, 'cleric':11, 'thief':12, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_hidden, TAR_CHAR_SELF, POS_STANDING, None, SLOT(44), 5, 12, "", "You feel less aware of your surroundings.", "")
skill_table["detect invis"] = skill_type("detect invis", { 'mage':3, 'cleric':8, 'thief':6, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_invis, TAR_CHAR_SELF, POS_STANDING, None, SLOT(19), 5, 12, "", "You no longer see invisible objects.", "")
skill_table["detect magic"] = skill_type("detect magic", { 'mage':2, 'cleric':6, 'thief':5, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_magic, TAR_CHAR_SELF, POS_STANDING, None, SLOT(20), 5, 12, "", "The detect magic wears off.", "")
skill_table["detect poison"] = skill_type("detect poison", { 'mage':15, 'cleric':7, 'thief':9, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_detect_poison, TAR_OBJ_INV, POS_STANDING, None, SLOT(21), 5, 12, "", "!Detect Poison!", "")
skill_table["dispel evil"] = skill_type("dispel evil", { 'mage':53, 'cleric':15, 'thief':53, 'warrior':21 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_dispel_evil, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(22), 15, 12, "dispel evil", "!Dispel Evil!", "")
skill_table["dispel good"] = skill_type("dispel good", { 'mage':53, 'cleric':15, 'thief':53, 'warrior':21 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_dispel_good, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(512), 15, 12, "dispel good", "!Dispel Good!", "")
skill_table["dispel magic"] = skill_type("dispel magic", { 'mage':16, 'cleric':24, 'thief':30, 'warrior':30 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_dispel_magic, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(59), 15, 12, "", "!Dispel Magic!", "")
skill_table["earthquake"] = skill_type("earthquake", { 'mage':53, 'cleric':10, 'thief':53, 'warrior':14 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_earthquake, TAR_IGNORE, POS_FIGHTING, None, SLOT(23), 15, 12, "earthquake", "!Earthquake!", "")
skill_table["enchant armor"] = skill_type("enchant armor", { 'mage':16, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_enchant_armor, TAR_OBJ_INV, POS_STANDING, None, SLOT(510), 100, 24, "", "!Enchant Armor!", "")
skill_table["enchant weapon"] = skill_type("enchant weapon", { 'mage':17, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_enchant_weapon, TAR_OBJ_INV, POS_STANDING, None, SLOT(24), 100, 24, "", "!Enchant Weapon!", "")
skill_table["energy drain"] = skill_type("energy drain", { 'mage':19, 'cleric':22, 'thief':26, 'warrior':23 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_energy_drain, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(25), 35, 12, "energy drain", "!Energy Drain!", "")
skill_table["faerie fire"] = skill_type("faerie fire", { 'mage':6, 'cleric':3, 'thief':5, 'warrior':8 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_faerie_fire, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(72), 5, 12, "faerie fire", "The pink aura around you fades away.", "")
skill_table["faerie fog"] = skill_type("faerie fog", { 'mage':14, 'cleric':21, 'thief':16, 'warrior':24 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_faerie_fog, TAR_IGNORE, POS_STANDING, None, SLOT(73), 12, 12, "faerie fog", "!Faerie Fog!", "")
skill_table["farsight"] = skill_type("farsight", { 'mage':14, 'cleric':16, 'thief':16, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_farsight, TAR_IGNORE, POS_STANDING, None, SLOT(521), 36, 20, "farsight", "!Farsight!", "")
skill_table["fireball"] = skill_type("fireball", { 'mage':22, 'cleric':53, 'thief':30, 'warrior':26 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_fireball, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(26), 15, 12, "fireball", "!Fireball!", "")
skill_table["fireproof"] = skill_type("fireproof", { 'mage':13, 'cleric':12, 'thief':19, 'warrior':18 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_fireproof, TAR_OBJ_INV, POS_STANDING, None, SLOT(523), 10, 12, "", "", "$p's protective aura fades.")
skill_table["flamestrike"] = skill_type("flamestrike", { 'mage':53, 'cleric':20, 'thief':53, 'warrior':27 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_flamestrike, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(65), 20, 12, "flamestrike", "!Flamestrike!", "")
skill_table["fly"] = skill_type("fly", { 'mage':10, 'cleric':18, 'thief':20, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_fly, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(56), 10, 18, "", "You slowly float to the ground.", "")
skill_table["floating disc"] = skill_type("floating disc", { 'mage':4, 'cleric':10, 'thief':7, 'warrior':16 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_floating_disc, TAR_IGNORE, POS_STANDING, None, SLOT(522), 40, 24, "", "!Floating disc!", "")
skill_table["frenzy"] = skill_type("frenzy", { 'mage':53, 'cleric':24, 'thief':53, 'warrior':26 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_frenzy, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(504), 30, 24, "", "Your rage ebbs.", "")
skill_table["gate"] = skill_type("gate", { 'mage':27, 'cleric':17, 'thief':32, 'warrior':28 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_gate, TAR_IGNORE, POS_FIGHTING, None, SLOT(83), 80, 12, "", "!Gate!", "")
skill_table["giant strength"] = skill_type("giant strength", { 'mage':11, 'cleric':53, 'thief':22, 'warrior':20 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_giant_strength, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(39), 20, 12, "", "You feel weaker.", "")
skill_table["harm"] = skill_type("harm", { 'mage':53, 'cleric':23, 'thief':53, 'warrior':28 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_harm, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(27), 35, 12, "harm spell", "!Harm!", "")
skill_table["haste"] = skill_type("haste", { 'mage':21, 'cleric':53, 'thief':26, 'warrior':29 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_haste, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(502), 30, 12, "", "You feel yourself slow down.", "")
skill_table["heal"] = skill_type("heal", { 'mage':53, 'cleric':21, 'thief':33, 'warrior':30 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_heal, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(28), 50, 12, "", "!Heal!", "")
skill_table["heat metal"] = skill_type("heat metal", { 'mage':53, 'cleric':16, 'thief':53, 'warrior':23 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_heat_metal, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(516), 25, 18, "spell", "!Heat Metal!", "")
skill_table["holy word"] = skill_type("holy word", { 'mage':53, 'cleric':36, 'thief':53, 'warrior':42 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_holy_word, TAR_IGNORE, POS_FIGHTING, None, SLOT(506), 200, 24, "divine wrath", "!Holy Word!", "")
skill_table["identify"] = skill_type("identify", { 'mage':15, 'cleric':16, 'thief':18, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_identify, TAR_OBJ_INV, POS_STANDING, None, SLOT(53), 12, 24, "", "!Identify!", "")
skill_table["infravision"] = skill_type("infravision", { 'mage':9, 'cleric':13, 'thief':10, 'warrior':16 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_infravision, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(77), 5, 18, "", "You no longer see in the dark.", "")
skill_table["invisibility"] = skill_type("invisibility", { 'mage':5, 'cleric':53, 'thief':9, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_invis, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT(29), 5, 12, "", "You are no longer invisible.", "$p fades into view.")
skill_table["know alignment"] = skill_type("know alignment", { 'mage':12, 'cleric':9, 'thief':20, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_know_alignment, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(58), 9, 12, "", "!Know Alignment!", "")
skill_table["lightning bolt"] = skill_type("lightning bolt", { 'mage':13, 'cleric':23, 'thief':18, 'warrior':16 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_lightning_bolt, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(30), 15, 12, "lightning bolt", "!Lightning Bolt!", "")
skill_table["locate object"] = skill_type("locate object", { 'mage':9, 'cleric':15, 'thief':11, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_locate_object, TAR_IGNORE, POS_STANDING, None, SLOT(31), 20, 18, "", "!Locate Object!", "")
skill_table["magic missile"] = skill_type("magic missile", { 'mage':1, 'cleric':53, 'thief':2, 'warrior':2 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_magic_missile, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(32), 15, 12, "magic missile", "!Magic Missile!", "")
skill_table["mass healing"] = skill_type("mass healing", { 'mage':53, 'cleric':38, 'thief':53, 'warrior':46 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_mass_healing, TAR_IGNORE, POS_STANDING, None, SLOT(508), 100, 36, "", "!Mass Healing!", "")
skill_table["mass invis"] = skill_type("mass invis", { 'mage':22, 'cleric':25, 'thief':31, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_mass_invis, TAR_IGNORE, POS_STANDING, None, SLOT(69), 20, 24, "", "You are no longer invisible.", "")
skill_table["nexus"] = skill_type("nexus", { 'mage':40, 'cleric':35, 'thief':50, 'warrior':45 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_nexus, TAR_IGNORE, POS_STANDING, None, SLOT(520), 150, 36, "", "!Nexus!", "")
skill_table["pass door"] = skill_type("pass door", { 'mage':24, 'cleric':32, 'thief':25, 'warrior':37 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_pass_door, TAR_CHAR_SELF, POS_STANDING, None, SLOT(74), 20, 12, "", "You feel solid again.", "")
skill_table["plague"] = skill_type("plague", { 'mage':23, 'cleric':17, 'thief':36, 'warrior':26 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_plague, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(503), 20, 12, "sickness", "Your sores vanish.", "")
skill_table["poison"] = skill_type("poison", { 'mage':17, 'cleric':12, 'thief':15, 'warrior':21 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_poison, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None, SLOT(33), 10, 12, "poison", "You feel less sick.", "The poison on $p dries up.")
skill_table["portal"] = skill_type("portal", { 'mage':35, 'cleric':30, 'thief':45, 'warrior':40 }, { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 }, spell_portal, TAR_IGNORE, POS_STANDING, None, SLOT(519), 100, 24, "", "!Portal!", "")
skill_table["protection evil"] = skill_type("protection evil", { 'mage':12, 'cleric':9, 'thief':17, 'warrior':11 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_protection_evil, TAR_CHAR_SELF, POS_STANDING, None, SLOT(34), 5, 12, "", "You feel less protected.", "")
skill_table["protection good"] = skill_type("protection good", { 'mage':12, 'cleric':9, 'thief':17, 'warrior':11 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_protection_good, TAR_CHAR_SELF, POS_STANDING, None, SLOT(514), 5, 12, "", "You feel less protected.", "")
skill_table["ray of truth"] = skill_type("ray of truth", { 'mage':53, 'cleric':35, 'thief':53, 'warrior':47 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_ray_of_truth, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(518), 20, 12, "ray of truth", "!Ray of Truth!", "")
skill_table["recharge"] = skill_type("recharge", { 'mage':9, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_recharge, TAR_OBJ_INV, POS_STANDING, None, SLOT(517), 60, 24, "", "!Recharge!", "")
skill_table["refresh"] = skill_type("refresh", { 'mage':8, 'cleric':5, 'thief':12, 'warrior':9 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_refresh, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(81), 12, 18, "refresh", "!Refresh!", "")
skill_table["remove curse"] = skill_type("remove curse", { 'mage':53, 'cleric':18, 'thief':53, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_remove_curse, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT(35), 5, 12, "", "!Remove Curse!", "")
skill_table["sanctuary"] = skill_type("sanctuary", { 'mage':36, 'cleric':20, 'thief':42, 'warrior':30 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_sanctuary, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(36), 75, 12, "", "The white aura around your body fades.", "")
skill_table["shield"] = skill_type("shield", { 'mage':20, 'cleric':35, 'thief':35, 'warrior':40 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_shield, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(67), 12, 18, "", "Your force shield shimmers then fades away.", "")
skill_table["shocking grasp"] = skill_type("shocking grasp", { 'mage':10, 'cleric':53, 'thief':14, 'warrior':13 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_shocking_grasp, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(53), 15, 12, "shocking grasp", "!Shocking Grasp!", "")
skill_table["sleep"] = skill_type("sleep", { 'mage':10, 'cleric':53, 'thief':11, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_sleep, TAR_CHAR_OFFENSIVE, POS_STANDING, None, SLOT(38), 15, 12, "", "You feel less tired.", "")
skill_table["slow"] = skill_type("slow", { 'mage':23, 'cleric':30, 'thief':29, 'warrior':32 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_slow, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(515), 30, 12, "", "You feel yourself speed up.", "")
skill_table["stone skin"] = skill_type("stone skin", { 'mage':25, 'cleric':40, 'thief':40, 'warrior':45 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_stone_skin, TAR_CHAR_SELF, POS_STANDING, None, SLOT(66), 12, 18, "", "Your skin feels soft again.", "")
skill_table["summon"] = skill_type("summon", { 'mage':24, 'cleric':12, 'thief':29, 'warrior':22 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_summon, TAR_IGNORE, POS_STANDING, None, SLOT(40), 50, 12, "", "!Summon!", "")
skill_table["teleport"] = skill_type("teleport", { 'mage':13, 'cleric':22, 'thief':25, 'warrior':36 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_teleport, TAR_CHAR_SELF, POS_FIGHTING, None, SLOT( 2), 35, 12, "", "!Teleport!", "")
skill_table["ventriloquate"] = skill_type("ventriloquate", { 'mage':1, 'cleric':53, 'thief':2, 'warrior':53 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_ventriloquate, TAR_IGNORE, POS_STANDING, None, SLOT(41), 5, 12, "", "!Ventriloquate!", "")
skill_table["weaken"] = skill_type("weaken", { 'mage':11, 'cleric':14, 'thief':16, 'warrior':17 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_weaken, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(68), 20, 12, "spell", "You feel stronger.", "")
skill_table["word of recall"] = skill_type("word of recall", { 'mage':32, 'cleric':28, 'thief':40, 'warrior':30 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_word_of_recall, TAR_CHAR_SELF, POS_RESTING, None, SLOT(42), 5, 12, "", "!Word of Recall!", "") # * Dragon breath */
skill_table["acid breath"] = skill_type("acid breath", { 'mage':31, 'cleric':32, 'thief':33, 'warrior':34 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_acid_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(200), 100, 24, "blast of acid", "!Acid Breath!", "")
skill_table["fire breath"] = skill_type("fire breath", { 'mage':40, 'cleric':45, 'thief':50, 'warrior':51 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_fire_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(201), 200, 24, "blast of flame", "The smoke leaves your eyes.", "")
skill_table["frost breath"] = skill_type("frost breath", { 'mage':34, 'cleric':36, 'thief':38, 'warrior':40 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_frost_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(202), 125, 24, "blast of frost", "!Frost Breath!", "")
skill_table["gas breath"] = skill_type("gas breath", { 'mage':39, 'cleric':43, 'thief':47, 'warrior':50 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_gas_breath, TAR_IGNORE, POS_FIGHTING, None, SLOT(203), 175, 24, "blast of gas", "!Gas Breath!", "")
skill_table["lightning breath"] = skill_type("lightning breath", { 'mage':37, 'cleric':40, 'thief':43, 'warrior':46 }, { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 }, spell_lightning_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(204), 150, 24, "blast of lightning", "!Lightning Breath!", "") # * Spells for mega1.are from Glop/Erkenbrand. */
skill_table["general purpose"] = skill_type("general purpose", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':0, 'cleric':0, 'thief':0, 'warrior':0 }, spell_general_purpose, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(401), 0, 12, "general purpose ammo", "!General Purpose Ammo!", "")
skill_table["high explosive"] = skill_type("high explosive", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':53 }, { 'mage':0, 'cleric':0, 'thief':0, 'warrior':0 }, spell_high_explosive, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(402), 0, 12, "high explosive ammo", "!High Explosive Ammo!", "") # combat and weapons skills */
skill_table["axe"] = skill_type("axe", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':6, 'cleric':6, 'thief':5, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Axe!", "")
skill_table["dagger"] = skill_type("dagger", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':2, 'cleric':3, 'thief':2, 'warrior':2 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Dagger!", "")
skill_table["flail"] = skill_type("flail", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':6, 'cleric':3, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Flail!", "")
skill_table["mace"] = skill_type("mace", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':5, 'cleric':2, 'thief':3, 'warrior':3 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Mace!", "")
skill_table["polearm"] = skill_type("polearm", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':6, 'cleric':6, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Polearm!", "")
skill_table["shield block"] = skill_type("shield block", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':6, 'cleric':4, 'thief':6, 'warrior':2 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Shield!", "")
skill_table["spear"] = skill_type("spear", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':4, 'cleric':4, 'thief':4, 'warrior':3 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Spear!", "")
skill_table["sword"] = skill_type("sword", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':5, 'cleric':6, 'thief':3, 'warrior':2 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!sword!", "")
skill_table["whip"] = skill_type("whip", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':6, 'cleric':5, 'thief':5, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Whip!", "")
skill_table["backstab"] = skill_type("backstab", { 'mage':53, 'cleric':53, 'thief':1, 'warrior':53 }, { 'mage':0, 'cleric':0, 'thief':5, 'warrior':0 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "backstab", "!Backstab!", "")
skill_table["bash"] = skill_type("bash", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':1 }, { 'mage':0, 'cleric':0, 'thief':0, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "bash", "!Bash!", "")
skill_table["berserk"] = skill_type("berserk", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':18 }, { 'mage':0, 'cleric':0, 'thief':0, 'warrior':5 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "", "You feel your pulse slow down.", "")
skill_table["dirt kicking"] = skill_type("dirt kicking", { 'mage':53, 'cleric':53, 'thief':3, 'warrior':3 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "kicked dirt", "You rub the dirt out of your eyes.", "")
skill_table["disarm"] = skill_type("disarm", { 'mage':53, 'cleric':53, 'thief':12, 'warrior':11 }, { 'mage':0, 'cleric':0, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "", "!Disarm!", "")
skill_table["dodge"] = skill_type("dodge", { 'mage':20, 'cleric':22, 'thief':1, 'warrior':13 }, { 'mage':8, 'cleric':8, 'thief':4, 'warrior':6 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Dodge!", "")
skill_table["enhanced damage"] = skill_type("enhanced damage", { 'mage':45, 'cleric':30, 'thief':25, 'warrior':1 }, { 'mage':10, 'cleric':9, 'thief':5, 'warrior':3 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Enhanced Damage!", "")
skill_table["envenom"] = skill_type("envenom", { 'mage':53, 'cleric':53, 'thief':10, 'warrior':53 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':0 }, spell_null, TAR_IGNORE, POS_RESTING, None, SLOT(0), 0, 36, "", "!Envenom!", "")
skill_table["hand to hand"] = skill_type("hand to hand", { 'mage':25, 'cleric':10, 'thief':15, 'warrior':6 }, { 'mage':8, 'cleric':5, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Hand to Hand!", "")
skill_table["kick"] = skill_type("kick", { 'mage':53, 'cleric':12, 'thief':14, 'warrior':8 }, { 'mage':0, 'cleric':4, 'thief':6, 'warrior':3 }, spell_null, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 0), 0, 12, "kick", "!Kick!", "")
skill_table["parry"] = skill_type("parry", { 'mage':22, 'cleric':20, 'thief':13, 'warrior':1 }, { 'mage':8, 'cleric':8, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Parry!", "")
skill_table["rescue"] = skill_type("rescue", { 'mage':53, 'cleric':53, 'thief':53, 'warrior':1 }, { 'mage':0, 'cleric':0, 'thief':0, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 12, "", "!Rescue!", "")
skill_table["trip"] = skill_type("trip", { 'mage':53, 'cleric':53, 'thief':1, 'warrior':15 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':8 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "trip", "!Trip!", "")
skill_table["second attack"] = skill_type("second attack", { 'mage':30, 'cleric':24, 'thief':12, 'warrior':5 }, { 'mage':10, 'cleric':8, 'thief':5, 'warrior':3 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Second Attack!", "")
skill_table["third attack"] = skill_type("third attack", { 'mage':53, 'cleric':53, 'thief':24, 'warrior':12 }, { 'mage':0, 'cleric':0, 'thief':10, 'warrior':4 }, spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Third Attack!", "") # non-combat skills */
skill_table["fast healing"] = skill_type("fast healing", { 'mage':15, 'cleric':9, 'thief':16, 'warrior':6 }, { 'mage':8, 'cleric':5, 'thief':6, 'warrior':4 }, spell_null, TAR_IGNORE, POS_SLEEPING, None, SLOT( 0), 0, 0, "", "!Fast Healing!", "")
skill_table["haggle"] = skill_type("haggle", { 'mage':7, 'cleric':18, 'thief':1, 'warrior':14 }, { 'mage':5, 'cleric':8, 'thief':3, 'warrior':6 }, spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 0, "", "!Haggle!", "")
skill_table["hide"] = skill_type("hide", { 'mage':53, 'cleric':53, 'thief':1, 'warrior':12 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':6 }, spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 12, "", "!Hide!", "")
skill_table["lore"] = skill_type("lore", { 'mage':10, 'cleric':10, 'thief':6, 'warrior':20 }, { 'mage':6, 'cleric':6, 'thief':4, 'warrior':8 }, spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 36, "", "!Lore!", "")
skill_table["meditation"] = skill_type("meditation", { 'mage':6, 'cleric':6, 'thief':15, 'warrior':15 }, { 'mage':5, 'cleric':5, 'thief':8, 'warrior':8 }, spell_null, TAR_IGNORE, POS_SLEEPING, None, SLOT( 0), 0, 0, "", "Meditation", "")
skill_table["peek"] = skill_type("peek", { 'mage':8, 'cleric':21, 'thief':1, 'warrior':14 }, { 'mage':5, 'cleric':7, 'thief':3, 'warrior':6 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 0, "", "!Peek!", "")
skill_table["pick lock"] = skill_type("pick lock", { 'mage':25, 'cleric':25, 'thief':7, 'warrior':25 }, { 'mage':8, 'cleric':8, 'thief':4, 'warrior':8 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Pick!", "")
skill_table["sneak"] = skill_type("sneak", { 'mage':53, 'cleric':53, 'thief':4, 'warrior':10 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':6 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "You no longer feel stealthy.", "")
skill_table["steal"] = skill_type("steal", { 'mage':53, 'cleric':53, 'thief':5, 'warrior':53 }, { 'mage':0, 'cleric':0, 'thief':4, 'warrior':0 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "", "!Steal!", "")
skill_table["scrolls"] = skill_type("scrolls", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':2, 'cleric':3, 'thief':5, 'warrior':8 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "", "!Scrolls!", "")
skill_table["staves"] = skill_type("staves", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':2, 'cleric':3, 'thief':5, 'warrior':8 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Staves!", "")
skill_table["wands"] = skill_type("wands", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':2, 'cleric':3, 'thief':5, 'warrior':8 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Wands!", "")
skill_table["recall"] = skill_type("recall", { 'mage':1, 'cleric':1, 'thief':1, 'warrior':1 }, { 'mage':2, 'cleric':2, 'thief':2, 'warrior':2 }, spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Recall!", "")

class group_type:
    def __init__(self, name, rating, spells):
        self.name=name;
        self.rating=rating
        self.spells=spells

group_table = {}
group_table["rom basics"] = group_type("rom basics", { 'mage':0, 'cleric':0, 'thief':0, 'warrior':0 }, ["scrolls", "staves", "wands", "recall"])
group_table["mage basics"] = group_type("mage basics", { 'mage':0, 'cleric':-1, 'thief':-1, 'warrior':-1 }, ["dagger"])
group_table["cleric basics"] = group_type("cleric basics", { 'mage':-1, 'cleric':0, 'thief':-1, 'warrior':-1 }, ["mace"])
group_table["thief basics"] = group_type("thief basics", { 'mage':-1, 'cleric':-1, 'thief':0, 'warrior':-1 }, ["dagger", "steal"])
group_table["warrior basics"] = group_type("warrior basics", { 'mage':-1, 'cleric':-1, 'thief':-1, 'warrior':0 }, ["sword", "second attack"])
group_table["mage default"] = group_type("mage default", { 'mage':40, 'cleric':-1, 'thief':-1, 'warrior':-1 }, ["lore", "beguiling", "combat", "detection", "enhancement", "illusion", "maladictions", "protective", "transportation", "weather"])
group_table["cleric default"] = group_type("cleric default", { 'mage':-1, 'cleric':40, 'thief':-1, 'warrior':-1 }, ["flail", "attack", "creation", "curative", "benedictions", "detection", "healing", "maladictions", "protective", "shield block", "transportation", "weather"])
group_table["thief default"] = group_type("thief default", { 'mage':-1, 'cleric':-1, 'thief':40, 'warrior':-1 }, ["mace", "sword", "backstab", "disarm", "dodge", "second attack", "trip", "hide", "peek", "pick lock", "sneak"])
group_table["warrior default"] = group_type("warrior default", { 'mage':-1, 'cleric':-1, 'thief':-1, 'warrior':40 }, ["weaponsmaster", "shield block", "bash", "disarm", "enhanced damage", "parry", "rescue", "third attack"])
group_table["weaponsmaster"] = group_type("weaponsmaster", { 'mage':40, 'cleric':40, 'thief':40, 'warrior':20 }, ["axe", "dagger", "flail", "mace", "polearm", "spear", "sword","whip"])
group_table["attack"] = group_type("attack", { 'mage':-1, 'cleric':5, 'thief':-1, 'warrior':8 }, ["demonfire", "dispel evil", "dispel good", "earthquake", "flamestrike", "heat metal", "ray of truth"])
group_table["beguiling"] = group_type("beguiling", { 'mage':4, 'cleric':-1, 'thief':6, 'warrior':-1 }, ["calm", "charm person", "sleep"])
group_table["benedictions"] = group_type("benedictions", { 'mage':-1, 'cleric':4, 'thief':-1, 'warrior':8 }, ["bless", "calm", "frenzy", "holy word", "remove curse"])
group_table["combat"] = group_type("combat", { 'mage':6, 'cleric':-1, 'thief':10, 'warrior':9 }, ["acid blast", "burning hands", "chain lightning", "chill touch", "colour spray", "fireball", "lightning bolt", "magic missile", "shocking grasp"])
group_table["creation"] = group_type("creation", { 'mage':4, 'cleric':4, 'thief':8, 'warrior':8 }, ["continual light", "create food", "create spring", "create water", "create rose", "floating disc"])
group_table["curative"] = group_type("curative", { 'mage':-1, 'cleric':4, 'thief':-1, 'warrior':8 }, ["cure blindness", "cure disease", "cure poison"])
group_table["detection"] = group_type("detection", { 'mage':4, 'cleric':3, 'thief':6, 'warrior':-1 }, ["detect evil", "detect good", "detect hidden", "detect invis", "detect magic", "detect poison", "farsight", "identify", "know alignment", "locate object"])
group_table["draconian"] = group_type("draconian", { 'mage':8, 'cleric':-1, 'thief':-1, 'warrior':-1 }, ["acid breath", "fire breath", "frost breath", "gas breath", "lightning breath"])
group_table["enchantment"] = group_type("enchantment", { 'mage':6, 'cleric':-1, 'thief':-1, 'warrior':-1 }, ["enchant armor", "enchant weapon", "fireproof", "recharge"])
group_table["enhancement"] = group_type("enhancement", { 'mage':5, 'cleric':-1, 'thief':9, 'warrior':9 }, ["giant strength", "haste", "infravision", "refresh"])
group_table["harmful"] = group_type("harmful", { 'mage':-1, 'cleric':3, 'thief':-1, 'warrior':6 }, ["cause critical", "cause light", "cause serious", "harm"])
group_table["healing"] = group_type("healing", { 'mage':-1, 'cleric':3, 'thief':-1, 'warrior':6 }, ["cure critical", "cure light", "cure serious", "heal", "mass healing", "refresh"])
group_table["illusion"] = group_type("illusion", { 'mage':4, 'cleric':-1, 'thief':7, 'warrior':-1 }, ["invis", "mass invis", "ventriloquate"])
group_table["maladictions"] = group_type("maladictions", { 'mage':5, 'cleric':5, 'thief':9, 'warrior':9 }, ["blindness", "change sex", "curse", "energy drain", "plague", "poison", "slow", "weaken"])
group_table["protective"] = group_type("protective", { 'mage':4, 'cleric':4, 'thief':7, 'warrior':8 }, ["armor", "cancellation", "dispel magic", "fireproof", "protection evil", "protection good", "sanctuary", "shield", "stone skin"])
group_table["transportation"] = group_type("transportation", { 'mage':4, 'cleric':4, 'thief':8, 'warrior':9 }, ["fly", "gate", "nexus", "pass door", "portal", "summon", "teleport", "word of recall"])
group_table["weather"] = group_type("weather", { 'mage':4, 'cleric':4, 'thief':8, 'warrior':8 }, ["call lightning", "control weather", "faerie fire", "faerie fog", "lightning bolt"])
    
class guild_type:
    def __init__(self, name, who_name, attr_prime, weapon, guild_rooms, skill_adept, thac0_00, thac0_32, hp_min, hp_max, fMana, base_group, default_group):
        self.name=name      # the full name of the class */
        self.who_name=who_name      # Three-letter name for 'who'  */
        self.attr_prime=attr_prime      # Prime attribute      */
        self.weapon=weapon      # First weapon         */
        self.guild_rooms = guild_rooms
        self.skill_adept=skill_adept      # Maximum skill level      */
        self.thac0_00=thac0_00      # Thac0 for level  0       */
        self.thac0_32=thac0_32      # Thac0 for level 32       */
        self.hp_min=hp_min      # Min hp gained on leveling    */
        self.hp_max=hp_max      # Max hp gained on leveling    */
        self.fMana=fMana      # Class gains mana on level    */
        self.base_group=base_group      # base skills gained       */
        self.default_group=default_group      # default skills gained    */

guild_table={}
guild_table["mage"] = guild_type("mage", "Mag", STAT_INT, OBJ_VNUM_SCHOOL_DAGGER, [3018,9618], 75, 20, 6, 6, 8, True, "mage basics", "mage default" )
guild_table["cleric"] = guild_type("cleric", "Cle", STAT_WIS, OBJ_VNUM_SCHOOL_MACE, [3003,9619], 75, 20, 2, 7, 10, True, "cleric basics", "cleric default")
guild_table["thief"] = guild_type("thief", "Thi", STAT_DEX, OBJ_VNUM_SCHOOL_DAGGER, [3028,9639], 75, 20, -4, 8, 13, False, "thief basics", "thief default")
guild_table["warrior"] = guild_type("warrior", "War", STAT_STR, OBJ_VNUM_SCHOOL_SWORD, [3022,9633], 75, 20, -10, 11, 15, False, "warrior basics", "warrior default")

class weapon_type:
    def __init__(self, name, vnum, type, gsn):
        self.name=name
        self.vnum=vnum
        self.type=type
        self.gsn=gsn
weapon_table = {}
weapon_table['sword'] = weapon_type('sword',   OBJ_VNUM_SCHOOL_SWORD,  WEAPON_SWORD, 'sword'  )
weapon_table['mace'] = weapon_type('mace',    OBJ_VNUM_SCHOOL_MACE,   WEAPON_MACE,   'mace'   )
weapon_table['dagger'] = weapon_type('dagger',  OBJ_VNUM_SCHOOL_DAGGER, WEAPON_DAGGER,  'dagger' )
weapon_table['axe'] = weapon_type('axe', OBJ_VNUM_SCHOOL_AXE,    WEAPON_AXE, 'axe'   )
weapon_table['staff'] = weapon_type('staff',   OBJ_VNUM_SCHOOL_STAFF,  WEAPON_SPEAR,   'spear'  )
weapon_table['flail'] = weapon_type('flail',   OBJ_VNUM_SCHOOL_FLAIL,  WEAPON_FLAIL,   'flail'  )
weapon_table['whip'] = weapon_type('whip',    OBJ_VNUM_SCHOOL_WHIP,   WEAPON_WHIP,    'whip'   )
weapon_table['polearm'] = weapon_type('polearm', OBJ_VNUM_SCHOOL_POLEARM,WEAPON_POLEARM, 'polearm'    )
   