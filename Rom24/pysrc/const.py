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
pc_race_table['elf'] = pc_race_type("elf", " Elf ", 5, [100, 125, 100, 120], ["sneak", "hide"], [12, 14, 13, 15, 11], [16, 20, 18, 21, 15], SIZE_SMALL)
pc_race_table['dwarf'] = pc_race_type("dwarf", "Dwarf", 8, [150, 100, 125, 100], ["berserk"], [14, 12, 14, 10, 15], [20, 16, 19, 14, 21], SIZE_MEDIUM)
pc_race_table['giant'] = pc_race_type("giant", "Giant", 6, [200, 150, 150, 105], ["bash", "fast healing"], [16, 11, 13, 11, 14], [22, 15, 18, 15, 20], SIZE_LARGE)

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
skill_table["reserved"] = skill_type("reserved", [99, 99, 99, 99], [99, 99, 99, 99], 0, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 0, "", "", "")
skill_table["acid blast"] = skill_type("acid blast", [28, 53, 35, 32], [1, 1, 2, 2], spell_acid_blast, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(70), 20, 12, "acid blast", "!Acid Blast!", "")
skill_table["armor"] = skill_type("armor", [7, 2, 10, 5], [1, 1, 2, 2], spell_armor, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT( 1), 5, 12, "", "You feel less armored.", "")
skill_table["bless"] = skill_type("bless", [53, 7, 53, 8], [1, 1, 2, 2], spell_bless, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT( 3), 5, 12, "", "You feel less righteous.", "$p's holy aura fades.")
skill_table["blindness"] = skill_type("blindness", [12, 8, 17, 15], [1, 1, 2, 2], spell_blindness, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 4), 5, 12, "", "You can see again.", "")
skill_table["burning hands"] = skill_type("burning hands", [7, 53, 10, 9], [1, 1, 2, 2], spell_burning_hands, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 5), 15, 12, "burning hands", "!Burning Hands!", "")
skill_table["call lightning"] = skill_type("call lightning", [26, 18, 31, 22], [1, 1, 2, 2], spell_call_lightning, TAR_IGNORE, POS_FIGHTING, None, SLOT( 6), 15, 12, "lightning bolt", "!Call Lightning!", "")
skill_table["calm"] = skill_type("calm", [48, 16, 50, 20], [1, 1, 2, 2], spell_calm, TAR_IGNORE, POS_FIGHTING, None, SLOT(509), 30, 12, "", "You have lost your peace of mind.", "")
skill_table["cancellation"] = skill_type("cancellation", [18, 26, 34, 34], [1, 1, 2, 2], spell_cancellation, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(507), 20, 12, "", "!cancellation!", "")
skill_table["cause critical"] = skill_type("cause critical", [53, 13, 53, 19], [1, 1, 2, 2], spell_cause_critical, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(63), 20, 12, "spell", "!Cause Critical!", "")
skill_table["cause light"] = skill_type("cause light", [53, 1, 53, 3], [1, 1, 2, 2], spell_cause_light, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(62), 15, 12, "spell", "!Cause Light!", "")
skill_table["cause serious"] = skill_type("cause serious", [53, 7, 53, 10], [1, 1, 2, 2], spell_cause_serious, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(64), 17, 12, "spell", "!Cause Serious!", "")
skill_table["chain lightning"] = skill_type("chain lightning", [33, 53, 39, 36], [1, 1, 2, 2], spell_chain_lightning, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(500), 25, 12, "lightning", "!Chain Lightning!", "")
skill_table["change sex"] = skill_type("change sex", [53, 53, 53, 53], [1, 1, 2, 2], spell_change_sex, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(82), 15, 12, "", "Your body feels familiar again.", "")
skill_table["charm person"] = skill_type("charm person", [20, 53, 25, 53], [1, 1, 2, 2], spell_charm_person, TAR_CHAR_OFFENSIVE, POS_STANDING, None, SLOT( 7), 5, 12, "", "You feel more self-confident.", "")
skill_table["chill touch"] = skill_type("chill touch", [4, 53, 6, 6], [1, 1, 2, 2], spell_chill_touch, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 8), 15, 12, "chilling touch", "You feel less cold.", "")
skill_table["colour spray"] = skill_type("colour spray", [16, 53, 22, 20], [1, 1, 2, 2], spell_colour_spray, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(10), 15, 12, "colour spray", "!Colour Spray!", "")
skill_table["continual light"] = skill_type("continual light", [6, 4, 6, 9], [1, 1, 2, 2], spell_continual_light, TAR_IGNORE, POS_STANDING, None, SLOT(57), 7, 12, "", "!Continual Light!", "")
skill_table["control weather"] = skill_type("control weather", [15, 19, 28, 22], [1, 1, 2, 2], spell_control_weather, TAR_IGNORE, POS_STANDING, None, SLOT(11), 25, 12, "", "!Control Weather!", "")
skill_table["create food"] = skill_type("create food", [10, 5, 11, 12], [1, 1, 2, 2], spell_create_food, TAR_IGNORE, POS_STANDING, None, SLOT(12), 5, 12, "", "!Create Food!", "")
skill_table["create rose"] = skill_type("create rose", [16, 11, 10, 24], [1, 1, 2, 2], spell_create_rose, TAR_IGNORE, POS_STANDING, None, SLOT(511), 30, 12, "", "!Create Rose!", "")
skill_table["create spring"] = skill_type("create spring", [14, 17, 23, 20], [1, 1, 2, 2], spell_create_spring, TAR_IGNORE, POS_STANDING, None, SLOT(80), 20, 12, "", "!Create Spring!", "")
skill_table["create water"] = skill_type("create water", [8, 3, 12, 11], [1, 1, 2, 2], spell_create_water, TAR_OBJ_INV, POS_STANDING, None, SLOT(13), 5, 12, "", "!Create Water!", "")
skill_table["cure blindness"] = skill_type("cure blindness", [53, 6, 53, 8], [1, 1, 2, 2], spell_cure_blindness, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(14), 5, 12, "", "!Cure Blindness!", "")
skill_table["cure critical"] = skill_type("cure critical", [53, 13, 53, 19], [1, 1, 2, 2], spell_cure_critical, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(15), 20, 12, "", "!Cure Critical!", "")
skill_table["cure disease"] = skill_type("cure disease", [53, 13, 53, 14], [1, 1, 2, 2], spell_cure_disease, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(501), 20, 12, "", "!Cure Disease!", "")
skill_table["cure light"] = skill_type("cure light", [53, 1, 53, 3], [1, 1, 2, 2], spell_cure_light, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(16), 10, 12, "", "!Cure Light!", "")
skill_table["cure poison"] = skill_type("cure poison", [53, 14, 53, 16], [1, 1, 2, 2], spell_cure_poison, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(43), 5, 12, "", "!Cure Poison!", "")
skill_table["cure serious"] = skill_type("cure serious", [53, 7, 53, 10], [1, 1, 2, 2], spell_cure_serious, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(61), 15, 12, "", "!Cure Serious!", "")
skill_table["curse"] = skill_type("curse", [18, 18, 26, 22], [1, 1, 2, 2], spell_curse, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None, SLOT(17), 20, 12, "curse", "The curse wears off.", "$p is no longer impure.")
skill_table["demonfire"] = skill_type("demonfire", [53, 34, 53, 45], [1, 1, 2, 2], spell_demonfire, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(505), 20, 12, "torments", "!Demonfire!", "")
skill_table["detect evil"] = skill_type("detect evil", [11, 4, 12, 53], [1, 1, 2, 2], spell_detect_evil, TAR_CHAR_SELF, POS_STANDING, None, SLOT(18), 5, 12, "", "The red in your vision disappears.", "")
skill_table["detect good"] = skill_type("detect good", [11, 4, 12, 53], [1, 1, 2, 2], spell_detect_good, TAR_CHAR_SELF, POS_STANDING, None, SLOT(513), 5, 12, "", "The gold in your vision disappears.", "")
skill_table["detect hidden"] = skill_type("detect hidden", [15, 11, 12, 53], [1, 1, 2, 2], spell_detect_hidden, TAR_CHAR_SELF, POS_STANDING, None, SLOT(44), 5, 12, "", "You feel less aware of your surroundings.", "")
skill_table["detect invis"] = skill_type("detect invis", [3, 8, 6, 53], [1, 1, 2, 2], spell_detect_invis, TAR_CHAR_SELF, POS_STANDING, None, SLOT(19), 5, 12, "", "You no longer see invisible objects.", "")
skill_table["detect magic"] = skill_type("detect magic", [2, 6, 5, 53], [1, 1, 2, 2], spell_detect_magic, TAR_CHAR_SELF, POS_STANDING, None, SLOT(20), 5, 12, "", "The detect magic wears off.", "")
skill_table["detect poison"] = skill_type("detect poison", [15, 7, 9, 53], [1, 1, 2, 2], spell_detect_poison, TAR_OBJ_INV, POS_STANDING, None, SLOT(21), 5, 12, "", "!Detect Poison!", "")
skill_table["dispel evil"] = skill_type("dispel evil", [53, 15, 53, 21], [1, 1, 2, 2], spell_dispel_evil, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(22), 15, 12, "dispel evil", "!Dispel Evil!", "")
skill_table["dispel good"] = skill_type("dispel good", [53, 15, 53, 21], [1, 1, 2, 2], spell_dispel_good, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(512), 15, 12, "dispel good", "!Dispel Good!", "")
skill_table["dispel magic"] = skill_type("dispel magic", [16, 24, 30, 30], [1, 1, 2, 2], spell_dispel_magic, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(59), 15, 12, "", "!Dispel Magic!", "")
skill_table["earthquake"] = skill_type("earthquake", [53, 10, 53, 14], [1, 1, 2, 2], spell_earthquake, TAR_IGNORE, POS_FIGHTING, None, SLOT(23), 15, 12, "earthquake", "!Earthquake!", "")
skill_table["enchant armor"] = skill_type("enchant armor", [16, 53, 53, 53], [2, 2, 4, 4], spell_enchant_armor, TAR_OBJ_INV, POS_STANDING, None, SLOT(510), 100, 24, "", "!Enchant Armor!", "")
skill_table["enchant weapon"] = skill_type("enchant weapon", [17, 53, 53, 53], [2, 2, 4, 4], spell_enchant_weapon, TAR_OBJ_INV, POS_STANDING, None, SLOT(24), 100, 24, "", "!Enchant Weapon!", "")
skill_table["energy drain"] = skill_type("energy drain", [19, 22, 26, 23], [1, 1, 2, 2], spell_energy_drain, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(25), 35, 12, "energy drain", "!Energy Drain!", "")
skill_table["faerie fire"] = skill_type("faerie fire", [6, 3, 5, 8], [1, 1, 2, 2], spell_faerie_fire, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(72), 5, 12, "faerie fire", "The pink aura around you fades away.", "")
skill_table["faerie fog"] = skill_type("faerie fog", [14, 21, 16, 24], [1, 1, 2, 2], spell_faerie_fog, TAR_IGNORE, POS_STANDING, None, SLOT(73), 12, 12, "faerie fog", "!Faerie Fog!", "")
skill_table["farsight"] = skill_type("farsight", [14, 16, 16, 53], [1, 1, 2, 2], spell_farsight, TAR_IGNORE, POS_STANDING, None, SLOT(521), 36, 20, "farsight", "!Farsight!", "")
skill_table["fireball"] = skill_type("fireball", [22, 53, 30, 26], [1, 1, 2, 2], spell_fireball, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(26), 15, 12, "fireball", "!Fireball!", "")
skill_table["fireproof"] = skill_type("fireproof", [13, 12, 19, 18], [1, 1, 2, 2], spell_fireproof, TAR_OBJ_INV, POS_STANDING, None, SLOT(523), 10, 12, "", "", "$p's protective aura fades.")
skill_table["flamestrike"] = skill_type("flamestrike", [53, 20, 53, 27], [1, 1, 2, 2], spell_flamestrike, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(65), 20, 12, "flamestrike", "!Flamestrike!", "")
skill_table["fly"] = skill_type("fly", [10, 18, 20, 22], [1, 1, 2, 2], spell_fly, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(56), 10, 18, "", "You slowly float to the ground.", "")
skill_table["floating disc"] = skill_type("floating disc", [4, 10, 7, 16], [1, 1, 2, 2], spell_floating_disc, TAR_IGNORE, POS_STANDING, None, SLOT(522), 40, 24, "", "!Floating disc!", "")
skill_table["frenzy"] = skill_type("frenzy", [53, 24, 53, 26], [1, 1, 2, 2], spell_frenzy, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(504), 30, 24, "", "Your rage ebbs.", "")
skill_table["gate"] = skill_type("gate", [27, 17, 32, 28], [1, 1, 2, 2], spell_gate, TAR_IGNORE, POS_FIGHTING, None, SLOT(83), 80, 12, "", "!Gate!", "")
skill_table["giant strength"] = skill_type("giant strength", [11, 53, 22, 20], [1, 1, 2, 2], spell_giant_strength, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(39), 20, 12, "", "You feel weaker.", "")
skill_table["harm"] = skill_type("harm", [53, 23, 53, 28], [1, 1, 2, 2], spell_harm, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(27), 35, 12, "harm spell", "!Harm!", "")
skill_table["haste"] = skill_type("haste", [21, 53, 26, 29], [1, 1, 2, 2], spell_haste, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(502), 30, 12, "", "You feel yourself slow down.", "")
skill_table["heal"] = skill_type("heal", [53, 21, 33, 30], [1, 1, 2, 2], spell_heal, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(28), 50, 12, "", "!Heal!", "")
skill_table["heat metal"] = skill_type("heat metal", [53, 16, 53, 23], [1, 1, 2, 2], spell_heat_metal, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(516), 25, 18, "spell", "!Heat Metal!", "")
skill_table["holy word"] = skill_type("holy word", [53, 36, 53, 42], [2, 2, 4, 4], spell_holy_word, TAR_IGNORE, POS_FIGHTING, None, SLOT(506), 200, 24, "divine wrath", "!Holy Word!", "")
skill_table["identify"] = skill_type("identify", [15, 16, 18, 53], [1, 1, 2, 2], spell_identify, TAR_OBJ_INV, POS_STANDING, None, SLOT(53), 12, 24, "", "!Identify!", "")
skill_table["infravision"] = skill_type("infravision", [9, 13, 10, 16], [1, 1, 2, 2], spell_infravision, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(77), 5, 18, "", "You no longer see in the dark.", "")
skill_table["invisibility"] = skill_type("invisibility", [5, 53, 9, 53], [1, 1, 2, 2], spell_invis, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT(29), 5, 12, "", "You are no longer invisible.", "$p fades into view.")
skill_table["know alignment"] = skill_type("know alignment", [12, 9, 20, 53], [1, 1, 2, 2], spell_know_alignment, TAR_CHAR_DEFENSIVE, POS_FIGHTING, None, SLOT(58), 9, 12, "", "!Know Alignment!", "")
skill_table["lightning bolt"] = skill_type("lightning bolt", [13, 23, 18, 16], [1, 1, 2, 2], spell_lightning_bolt, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(30), 15, 12, "lightning bolt", "!Lightning Bolt!", "")
skill_table["locate object"] = skill_type("locate object", [9, 15, 11, 53], [1, 1, 2, 2], spell_locate_object, TAR_IGNORE, POS_STANDING, None, SLOT(31), 20, 18, "", "!Locate Object!", "")
skill_table["magic missile"] = skill_type("magic missile", [1, 53, 2, 2], [1, 1, 2, 2], spell_magic_missile, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(32), 15, 12, "magic missile", "!Magic Missile!", "")
skill_table["mass healing"] = skill_type("mass healing", [53, 38, 53, 46], [2, 2, 4, 4], spell_mass_healing, TAR_IGNORE, POS_STANDING, None, SLOT(508), 100, 36, "", "!Mass Healing!", "")
skill_table["mass invis"] = skill_type("mass invis", [22, 25, 31, 53], [1, 1, 2, 2], spell_mass_invis, TAR_IGNORE, POS_STANDING, None, SLOT(69), 20, 24, "", "You are no longer invisible.", "")
skill_table["nexus"] = skill_type("nexus", [40, 35, 50, 45], [2, 2, 4, 4], spell_nexus, TAR_IGNORE, POS_STANDING, None, SLOT(520), 150, 36, "", "!Nexus!", "")
skill_table["pass door"] = skill_type("pass door", [24, 32, 25, 37], [1, 1, 2, 2], spell_pass_door, TAR_CHAR_SELF, POS_STANDING, None, SLOT(74), 20, 12, "", "You feel solid again.", "")
skill_table["plague"] = skill_type("plague", [23, 17, 36, 26], [1, 1, 2, 2], spell_plague, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(503), 20, 12, "sickness", "Your sores vanish.", "")
skill_table["poison"] = skill_type("poison", [17, 12, 15, 21], [1, 1, 2, 2], spell_poison, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None, SLOT(33), 10, 12, "poison", "You feel less sick.", "The poison on $p dries up.")
skill_table["portal"] = skill_type("portal", [35, 30, 45, 40], [2, 2, 4, 4], spell_portal, TAR_IGNORE, POS_STANDING, None, SLOT(519), 100, 24, "", "!Portal!", "")
skill_table["protection evil"] = skill_type("protection evil", [12, 9, 17, 11], [1, 1, 2, 2], spell_protection_evil, TAR_CHAR_SELF, POS_STANDING, None, SLOT(34), 5, 12, "", "You feel less protected.", "")
skill_table["protection good"] = skill_type("protection good", [12, 9, 17, 11], [1, 1, 2, 2], spell_protection_good, TAR_CHAR_SELF, POS_STANDING, None, SLOT(514), 5, 12, "", "You feel less protected.", "")
skill_table["ray of truth"] = skill_type("ray of truth", [53, 35, 53, 47], [1, 1, 2, 2], spell_ray_of_truth, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(518), 20, 12, "ray of truth", "!Ray of Truth!", "")
skill_table["recharge"] = skill_type("recharge", [9, 53, 53, 53], [1, 1, 2, 2], spell_recharge, TAR_OBJ_INV, POS_STANDING, None, SLOT(517), 60, 24, "", "!Recharge!", "")
skill_table["refresh"] = skill_type("refresh", [8, 5, 12, 9], [1, 1, 2, 2], spell_refresh, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(81), 12, 18, "refresh", "!Refresh!", "")
skill_table["remove curse"] = skill_type("remove curse", [53, 18, 53, 22], [1, 1, 2, 2], spell_remove_curse, TAR_OBJ_CHAR_DEF, POS_STANDING, None, SLOT(35), 5, 12, "", "!Remove Curse!", "")
skill_table["sanctuary"] = skill_type("sanctuary", [36, 20, 42, 30], [1, 1, 2, 2], spell_sanctuary, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(36), 75, 12, "", "The white aura around your body fades.", "")
skill_table["shield"] = skill_type("shield", [20, 35, 35, 40], [1, 1, 2, 2], spell_shield, TAR_CHAR_DEFENSIVE, POS_STANDING, None, SLOT(67), 12, 18, "", "Your force shield shimmers then fades away.", "")
skill_table["shocking grasp"] = skill_type("shocking grasp", [10, 53, 14, 13], [1, 1, 2, 2], spell_shocking_grasp, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(53), 15, 12, "shocking grasp", "!Shocking Grasp!", "")
skill_table["sleep"] = skill_type("sleep", [10, 53, 11, 53], [1, 1, 2, 2], spell_sleep, TAR_CHAR_OFFENSIVE, POS_STANDING, None, SLOT(38), 15, 12, "", "You feel less tired.", "")
skill_table["slow"] = skill_type("slow", [23, 30, 29, 32], [1, 1, 2, 2], spell_slow, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(515), 30, 12, "", "You feel yourself speed up.", "")
skill_table["stone skin"] = skill_type("stone skin", [25, 40, 40, 45], [1, 1, 2, 2], spell_stone_skin, TAR_CHAR_SELF, POS_STANDING, None, SLOT(66), 12, 18, "", "Your skin feels soft again.", "")
skill_table["summon"] = skill_type("summon", [24, 12, 29, 22], [1, 1, 2, 2], spell_summon, TAR_IGNORE, POS_STANDING, None, SLOT(40), 50, 12, "", "!Summon!", "")
skill_table["teleport"] = skill_type("teleport", [13, 22, 25, 36], [1, 1, 2, 2], spell_teleport, TAR_CHAR_SELF, POS_FIGHTING, None, SLOT( 2), 35, 12, "", "!Teleport!", "")
skill_table["ventriloquate"] = skill_type("ventriloquate", [1, 53, 2, 53], [1, 1, 2, 2], spell_ventriloquate, TAR_IGNORE, POS_STANDING, None, SLOT(41), 5, 12, "", "!Ventriloquate!", "")
skill_table["weaken"] = skill_type("weaken", [11, 14, 16, 17], [1, 1, 2, 2], spell_weaken, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(68), 20, 12, "spell", "You feel stronger.", "")
skill_table["word of recall"] = skill_type("word of recall", [32, 28, 40, 30], [1, 1, 2, 2], spell_word_of_recall, TAR_CHAR_SELF, POS_RESTING, None, SLOT(42), 5, 12, "", "!Word of Recall!", "") # * Dragon breath */
skill_table["acid breath"] = skill_type("acid breath", [31, 32, 33, 34], [1, 1, 2, 2], spell_acid_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(200), 100, 24, "blast of acid", "!Acid Breath!", "")
skill_table["fire breath"] = skill_type("fire breath", [40, 45, 50, 51], [1, 1, 2, 2], spell_fire_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(201), 200, 24, "blast of flame", "The smoke leaves your eyes.", "")
skill_table["frost breath"] = skill_type("frost breath", [34, 36, 38, 40], [1, 1, 2, 2], spell_frost_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(202), 125, 24, "blast of frost", "!Frost Breath!", "")
skill_table["gas breath"] = skill_type("gas breath", [39, 43, 47, 50], [1, 1, 2, 2], spell_gas_breath, TAR_IGNORE, POS_FIGHTING, None, SLOT(203), 175, 24, "blast of gas", "!Gas Breath!", "")
skill_table["lightning breath"] = skill_type("lightning breath", [37, 40, 43, 46], [1, 1, 2, 2], spell_lightning_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(204), 150, 24, "blast of lightning", "!Lightning Breath!", "") # * Spells for mega1.are from Glop/Erkenbrand. */
skill_table["general purpose"] = skill_type("general purpose", [53, 53, 53, 53], [0, 0, 0, 0], spell_general_purpose, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(401), 0, 12, "general purpose ammo", "!General Purpose Ammo!", "")
skill_table["high explosive"] = skill_type("high explosive", [53, 53, 53, 53], [0, 0, 0, 0], spell_high_explosive, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT(402), 0, 12, "high explosive ammo", "!High Explosive Ammo!", "") # combat and weapons skills */
skill_table["axe"] = skill_type("axe", [1, 1, 1, 1], [6, 6, 5, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Axe!", "")
skill_table["dagger"] = skill_type("dagger", [1, 1, 1, 1], [2, 3, 2, 2], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Dagger!", "")
skill_table["flail"] = skill_type("flail", [1, 1, 1, 1], [6, 3, 6, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Flail!", "")
skill_table["mace"] = skill_type("mace", [1, 1, 1, 1], [5, 2, 3, 3], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Mace!", "")
skill_table["polearm"] = skill_type("polearm", [1, 1, 1, 1], [6, 6, 6, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Polearm!", "")
skill_table["shield block"] = skill_type("shield block", [1, 1, 1, 1], [6, 4, 6, 2], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT(0), 0, 0, "", "!Shield!", "")
skill_table["spear"] = skill_type("spear", [1, 1, 1, 1], [4, 4, 4, 3], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Spear!", "")
skill_table["sword"] = skill_type("sword", [1, 1, 1, 1], [5, 6, 3, 2], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!sword!", "")
skill_table["whip"] = skill_type("whip", [1, 1, 1, 1], [6, 5, 5, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Whip!", "")
skill_table["backstab"] = skill_type("backstab", [53, 53, 1, 53], [0, 0, 5, 0], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "backstab", "!Backstab!", "")
skill_table["bash"] = skill_type("bash", [53, 53, 53, 1], [0, 0, 0, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "bash", "!Bash!", "")
skill_table["berserk"] = skill_type("berserk", [53, 53, 53, 18], [0, 0, 0, 5], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "", "You feel your pulse slow down.", "")
skill_table["dirt kicking"] = skill_type("dirt kicking", [53, 53, 3, 3], [0, 0, 4, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "kicked dirt", "You rub the dirt out of your eyes.", "")
skill_table["disarm"] = skill_type("disarm", [53, 53, 12, 11], [0, 0, 6, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "", "!Disarm!", "")
skill_table["dodge"] = skill_type("dodge", [20, 22, 1, 13], [8, 8, 4, 6], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Dodge!", "")
skill_table["enhanced damage"] = skill_type("enhanced damage", [45, 30, 25, 1], [10, 9, 5, 3], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Enhanced Damage!", "")
skill_table["envenom"] = skill_type("envenom", [53, 53, 10, 53], [0, 0, 4, 0], spell_null, TAR_IGNORE, POS_RESTING, None, SLOT(0), 0, 36, "", "!Envenom!", "")
skill_table["hand to hand"] = skill_type("hand to hand", [25, 10, 15, 6], [8, 5, 6, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Hand to Hand!", "")
skill_table["kick"] = skill_type("kick", [53, 12, 14, 8], [0, 4, 6, 3], spell_null, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None, SLOT( 0), 0, 12, "kick", "!Kick!", "")
skill_table["parry"] = skill_type("parry", [22, 20, 13, 1], [8, 8, 6, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Parry!", "")
skill_table["rescue"] = skill_type("rescue", [53, 53, 53, 1], [0, 0, 0, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 12, "", "!Rescue!", "")
skill_table["trip"] = skill_type("trip", [53, 53, 1, 15], [0, 0, 4, 8], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 24, "trip", "!Trip!", "")
skill_table["second attack"] = skill_type("second attack", [30, 24, 12, 5], [10, 8, 5, 3], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Second Attack!", "")
skill_table["third attack"] = skill_type("third attack", [53, 53, 24, 12], [0, 0, 10, 4], spell_null, TAR_IGNORE, POS_FIGHTING, None, SLOT( 0), 0, 0, "", "!Third Attack!", "") # non-combat skills */
skill_table["fast healing"] = skill_type("fast healing", [15, 9, 16, 6], [8, 5, 6, 4], spell_null, TAR_IGNORE, POS_SLEEPING, None, SLOT( 0), 0, 0, "", "!Fast Healing!", "")
skill_table["haggle"] = skill_type("haggle", [7, 18, 1, 14], [5, 8, 3, 6], spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 0, "", "!Haggle!", "")
skill_table["hide"] = skill_type("hide", [53, 53, 1, 12], [0, 0, 4, 6], spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 12, "", "!Hide!", "")
skill_table["lore"] = skill_type("lore", [10, 10, 6, 20], [6, 6, 4, 8], spell_null, TAR_IGNORE, POS_RESTING, None, SLOT( 0), 0, 36, "", "!Lore!", "")
skill_table["meditation"] = skill_type("meditation", [6, 6, 15, 15], [5, 5, 8, 8], spell_null, TAR_IGNORE, POS_SLEEPING, None, SLOT( 0), 0, 0, "", "Meditation", "")
skill_table["peek"] = skill_type("peek", [8, 21, 1, 14], [5, 7, 3, 6], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 0, "", "!Peek!", "")
skill_table["pick lock"] = skill_type("pick lock", [25, 25, 7, 25], [8, 8, 4, 8], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Pick!", "")
skill_table["sneak"] = skill_type("sneak", [53, 53, 4, 10], [0, 0, 4, 6], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "You no longer feel stealthy.", "")
skill_table["steal"] = skill_type("steal", [53, 53, 5, 53], [0, 0, 4, 0], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "", "!Steal!", "")
skill_table["scrolls"] = skill_type("scrolls", [1, 1, 1, 1], [2, 3, 5, 8], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 24, "", "!Scrolls!", "")
skill_table["staves"] = skill_type("staves", [1, 1, 1, 1], [2, 3, 5, 8], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Staves!", "")
skill_table["wands"] = skill_type("wands", [1, 1, 1, 1], [2, 3, 5, 8], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Wands!", "")
skill_table["recall"] = skill_type("recall", [1, 1, 1, 1], [2, 2, 2, 2], spell_null, TAR_IGNORE, POS_STANDING, None, SLOT( 0), 0, 12, "", "!Recall!", "")

class group_type:
    def __init__(self, name, rating, spells):
        self.name=name;
        self.rating=rating
        self.spells=spells

group_table = {}
group_table["rom basics"] = group_type("rom basics", [0, 0, 0, 0], ["scrolls", "staves", "wands", "recall"])
group_table["mage basics"] = group_type("mage basics", [0, -1, -1, -1], ["dagger"])
group_table["cleric basics"] = group_type("cleric basics", [-1, 0, -1, -1], ["mace"])
group_table["thief basics"] = group_type("thief basics", [-1, -1, 0, -1], ["dagger", "steal"])
group_table["warrior basics"] = group_type("warrior basics", [-1, -1, -1, 0], ["sword", "second attack"])
group_table["mage default"] = group_type("mage default", [40, -1, -1, -1], ["lore", "beguiling", "combat", "detection", "enhancement", "illusion", "maladictions", "protective", "transportation", "weather"])
group_table["cleric default"] = group_type("cleric default", [-1, 40, -1, -1], ["flail", "attack", "creation", "curative", "benedictions", "detection", "healing", "maladictions", "protective", "shield block", "transportation", "weather"])
group_table["thief default"] = group_type("thief default", [-1, -1, 40, -1], ["mace", "sword", "backstab", "disarm", "dodge", "second attack", "trip", "hide", "peek", "pick lock", "sneak"])
group_table["warrior default"] = group_type("warrior default", [-1, -1, -1, 40], ["weaponsmaster", "shield block", "bash", "disarm", "enhanced damage", "parry", "rescue", "third attack"])
group_table["weaponsmaster"] = group_type("weaponsmaster", [40, 40, 40, 20], ["axe", "dagger", "flail", "mace", "polearm", "spear", "sword","whip"])
group_table["attack"] = group_type("attack", [-1, 5, -1, 8], ["demonfire", "dispel evil", "dispel good", "earthquake", "flamestrike", "heat metal", "ray of truth"])
group_table["beguiling"] = group_type("beguiling", [4, -1, 6, -1], ["calm", "charm person", "sleep"])
group_table["benedictions"] = group_type("benedictions", [-1, 4, -1, 8], ["bless", "calm", "frenzy", "holy word", "remove curse"])
group_table["combat"] = group_type("combat", [6, -1, 10, 9], ["acid blast", "burning hands", "chain lightning", "chill touch", "colour spray", "fireball", "lightning bolt", "magic missile", "shocking grasp"])
group_table["creation"] = group_type("creation", [4, 4, 8, 8], ["continual light", "create food", "create spring", "create water", "create rose", "floating disc"])
group_table["curative"] = group_type("curative", [-1, 4, -1, 8], ["cure blindness", "cure disease", "cure poison"])
group_table["detection"] = group_type("detection", [4, 3, 6, -1], ["detect evil", "detect good", "detect hidden", "detect invis", "detect magic", "detect poison", "farsight", "identify", "know alignment", "locate object"])
group_table["draconian"] = group_type("draconian", [8, -1, -1, -1], ["acid breath", "fire breath", "frost breath", "gas breath", "lightning breath"])
group_table["enchantment"] = group_type("enchantment", [6, -1, -1, -1], ["enchant armor", "enchant weapon", "fireproof", "recharge"])
group_table["enhancement"] = group_type("enhancement", [5, -1, 9, 9], ["giant strength", "haste", "infravision", "refresh"])
group_table["harmful"] = group_type("harmful", [-1, 3, -1, 6], ["cause critical", "cause light", "cause serious", "harm"])
group_table["healing"] = group_type("healing", [-1, 3, -1, 6], ["cure critical", "cure light", "cure serious", "heal", "mass healing", "refresh"])
group_table["illusion"] = group_type("illusion", [4, -1, 7, -1], ["invis", "mass invis", "ventriloquate"])
group_table["maladictions"] = group_type("maladictions", [5, 5, 9, 9], ["blindness", "change sex", "curse", "energy drain", "plague", "poison", "slow", "weaken"])
group_table["protective"] = group_type("protective", [4, 4, 7, 8], ["armor", "cancellation", "dispel magic", "fireproof", "protection evil", "protection good", "sanctuary", "shield", "stone skin"])
group_table["transportation"] = group_type("transportation", [4, 4, 8, 9], ["fly", "gate", "nexus", "pass door", "portal", "summon", "teleport", "word of recall"])
group_table["weather"] = group_type("weather", [4, 4, 8, 8], ["call lightning", "control weather", "faerie fire", "faerie fog", "lightning bolt"])
    
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
