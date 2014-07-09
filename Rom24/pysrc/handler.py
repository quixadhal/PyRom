"""
 #**************************************************************************
 *  Original Diku Mud copyright=C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright=C) 1992, 1993 by Michael           *
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

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                            *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/ 
 ************/
"""
import logging
import os
import settings

logger = logging.getLogger()

import merc
import state_checks

def global_instance_generator():
    merc.instance_number += 1
    instance_num_file = os.path.join(settings.AREA_DIR, "instance_tracker.txt")
    fp = open(instance_num_file, 'w')
    fp.write(str(merc.instance_number))
    fp.close()
    return merc.instance_number

# * Return ascii name of an affect location.
def affect_loc_name(location):
    if location == merc.APPLY_NONE:
        return "none"
    if location == merc.APPLY_STR:
        return "strength"
    if location == merc.APPLY_DEX:
        return "dexterity"
    if location == merc.APPLY_INT:
        return "intelligence"
    if location == merc.APPLY_WIS:
        return "wisdom"
    if location == merc.APPLY_CON:
        return "constitution"
    if location == merc.APPLY_SEX:
        return "sex"
    if location == merc.APPLY_CLASS:
        return "class"
    if location == merc.APPLY_LEVEL:
        return "level"
    if location == merc.APPLY_AGE:
        return "age"
    if location == merc.APPLY_MANA:
        return "mana"
    if location == merc.APPLY_HIT:
        return "hp"
    if location == merc.APPLY_MOVE:
        return "moves"
    if location == merc.APPLY_GOLD:
        return "gold"
    if location == merc.APPLY_EXP:
        return "experience"
    if location == merc.APPLY_AC:
        return "armor class"
    if location == merc.APPLY_HITROLL:
        return "hit roll"
    if location == merc.APPLY_DAMROLL:
        return "damage roll"
    if location == merc.APPLY_SAVES:
        return "saves"
    if location == merc.APPLY_SAVING_ROD:
        return "save vs rod"
    if location == merc.APPLY_SAVING_PETRI:
        return "save vs petrification"
    if location == merc.APPLY_SAVING_BREATH:
        return "save vs breath"
    if location == merc.APPLY_SAVING_SPELL:
        return "save vs spell"
    if location == merc.APPLY_SPELL_AFFECT:
        return "none"
    logger.error("Affect_location_name: unknown location %d.", location)
    return "(unknown)"


# * Return ascii name of an affect bit vector.
def affect_bit_name(vector):
    buf = ""
    if vector & merc.AFF_BLIND:
        buf += " blind"
    if vector & merc.AFF_INVISIBLE:
        buf += " invisible"
    if vector & merc.AFF_DETECT_EVIL:
        buf += " detect_evil"
    if vector & merc.AFF_DETECT_GOOD:
        buf += " detect_good"
    if vector & merc.AFF_DETECT_INVIS:
        buf += " detect_invis"
    if vector & merc.AFF_DETECT_MAGIC:
        buf += " detect_magic"
    if vector & merc.AFF_DETECT_HIDDEN:
        buf += " detect_hidden"
    if vector & merc.AFF_SANCTUARY:
        buf += " sanctuary"
    if vector & merc.AFF_FAERIE_FIRE:
        buf += " faerie_fire"
    if vector & merc.AFF_INFRARED:
        buf += " infrared"
    if vector & merc.AFF_CURSE:
        buf += " curse"
    if vector & merc.AFF_POISON:
        buf += " poison"
    if vector & merc.AFF_PROTECT_EVIL:
        buf += " prot_evil"
    if vector & merc.AFF_PROTECT_GOOD:
        buf += " prot_good"
    if vector & merc.AFF_SLEEP:
        buf += " sleep"
    if vector & merc.AFF_SNEAK:
        buf += " sneak"
    if vector & merc.AFF_HIDE:
        buf += " hide"
    if vector & merc.AFF_CHARM:
        buf += " charm"
    if vector & merc.AFF_FLYING:
        buf += " flying"
    if vector & merc.AFF_PASS_DOOR:
        buf += " pass_door"
    if vector & merc.AFF_BERSERK:
        buf += " berserk"
    if vector & merc.AFF_CALM:
        buf += " calm"
    if vector & merc.AFF_HASTE:
        buf += " haste"
    if vector & merc.AFF_SLOW:
        buf += " slow"
    if vector & merc.AFF_PLAGUE:
        buf += " plague"
    if vector & merc.AFF_DARK_VISION:
        buf += " dark_vision"
    if not buf:
        return "none"
    return buf


#
# * Return ascii name of extra flags vector.
def extra_bit_name(extra_flags):
    buf = ""
    if extra_flags & merc.ITEM_GLOW:
        buf += " glow"
    if extra_flags & merc.ITEM_HUM:
        buf += " hum"
    if extra_flags & merc.ITEM_DARK:
        buf += " dark"
    if extra_flags & merc.ITEM_LOCK:
        buf += " lock"
    if extra_flags & merc.ITEM_EVIL:
        buf += " evil"
    if extra_flags & merc.ITEM_INVIS:
        buf += " invis"
    if extra_flags & merc.ITEM_MAGIC:
        buf += " magic"
    if extra_flags & merc.ITEM_NODROP:
        buf += " nodrop"
    if extra_flags & merc.ITEM_BLESS:
        buf += " bless"
    if extra_flags & merc.ITEM_ANTI_GOOD:
        buf += " anti-good"
    if extra_flags & merc.ITEM_ANTI_EVIL:
        buf += " anti-evil"
    if extra_flags & merc.ITEM_ANTI_NEUTRAL:
        buf += " anti-neutral"
    if extra_flags & merc.ITEM_NOREMOVE:
        buf += " noremove"
    if extra_flags & merc.ITEM_INVENTORY:
        buf += " inventory"
    if extra_flags & merc.ITEM_NOPURGE:
        buf += " nopurge"
    if extra_flags & merc.ITEM_VIS_DEATH:
        buf += " vis_death"
    if extra_flags & merc.ITEM_ROT_DEATH:
        buf += " rot_death"
    if extra_flags & merc.ITEM_NOLOCATE:
        buf += " no_locate"
    if extra_flags & merc.ITEM_SELL_EXTRACT:
        buf += " sell_extract"
    if extra_flags & merc.ITEM_BURN_PROOF:
        buf += " burn_proof"
    if extra_flags & merc.ITEM_NOUNCURSE:
        buf += " no_uncurse"
    return "none" if not buf else buf


# return ascii name of an act vector */
def act_bit_name(act_flags):
    buf = ""

    if state_checks.IS_SET(act_flags, merc.ACT_IS_NPC):
        buf += " npc"
        if act_flags & merc.ACT_SENTINEL:
            buf += " sentinel"
        if act_flags & merc.ACT_SCAVENGER:
            buf += " scavenger"
        if act_flags & merc.ACT_AGGRESSIVE:
            buf += " aggressive"
        if act_flags & merc.ACT_STAY_AREA:
            buf += " stay_area"
        if act_flags & merc.ACT_WIMPY:
            buf += " wimpy"
        if act_flags & merc.ACT_PET:
            buf += " pet"
        if act_flags & merc.ACT_TRAIN:
            buf += " train"
        if act_flags & merc.ACT_PRACTICE:
            buf += " practice"
        if act_flags & merc.ACT_UNDEAD:
            buf += " undead"
        if act_flags & merc.ACT_CLERIC:
            buf += " cleric"
        if act_flags & merc.ACT_MAGE:
            buf += " mage"
        if act_flags & merc.ACT_THIEF:
            buf += " thief"
        if act_flags & merc.ACT_WARRIOR:
            buf += " warrior"
        if act_flags & merc.ACT_NOALIGN:
            buf += " no_align"
        if act_flags & merc.ACT_NOPURGE:
            buf += " no_purge"
        if act_flags & merc.ACT_IS_HEALER:
            buf += " healer"
        if act_flags & merc.ACT_IS_CHANGER:
            buf += " changer"
        if act_flags & merc.ACT_GAIN:
            buf += " skill_train"
        if act_flags & merc.ACT_UPDATE_ALWAYS:
            buf += " update_always"
    else:
        buf += " player"
        if act_flags & merc.PLR_AUTOASSIST:
            buf += " autoassist"
        if act_flags & merc.PLR_AUTOEXIT:
            buf += " autoexit"
        if act_flags & merc.PLR_AUTOLOOT:
            buf += " autoloot"
        if act_flags & merc.PLR_AUTOSAC:
            buf += " autosac"
        if act_flags & merc.PLR_AUTOGOLD:
            buf += " autogold"
        if act_flags & merc.PLR_AUTOSPLIT:
            buf += " autosplit"
        if act_flags & merc.PLR_HOLYLIGHT:
            buf += " holy_light"
        if act_flags & merc.PLR_CANLOOT:
            buf += " loot_corpse"
        if act_flags & merc.PLR_NOSUMMON:
            buf += " no_summon"
        if act_flags & merc.PLR_NOFOLLOW:
            buf += " no_follow"
        if act_flags & merc.PLR_FREEZE:
            buf += " frozen"
        if act_flags & merc.PLR_THIEF:
            buf += " thief"
        if act_flags & merc.PLR_KILLER:
            buf += " killer"
        if act_flags & merc.PLR_OMNI:
            buf += " omni"
    return "none" if not buf else buf


def comm_bit_name(comm_flags):
    buf = ""
    if comm_flags & merc.COMM_QUIET:
        buf += " quiet"
    if comm_flags & merc.COMM_DEAF:
        buf += " deaf"
    if comm_flags & merc.COMM_NOWIZ:
        buf += " no_wiz"
    if comm_flags & merc.COMM_NOAUCTION:
        buf += " no_auction"
    if comm_flags & merc.COMM_NOGOSSIP:
        buf += " no_gossip"
    if comm_flags & merc.COMM_NOQUESTION:
        buf += " no_question"
    if comm_flags & merc.COMM_NOMUSIC:
        buf += " no_music"
    if comm_flags & merc.COMM_NOQUOTE:
        buf += " no_quote"
    if comm_flags & merc.COMM_COMPACT:
        buf += " compact"
    if comm_flags & merc.COMM_BRIEF:
        buf += " brief"
    if comm_flags & merc.COMM_PROMPT:
        buf += " prompt"
    if comm_flags & merc.COMM_COMBINE:
        buf += " combine"
    if comm_flags & merc.COMM_NOEMOTE:
        buf += " no_emote"
    if comm_flags & merc.COMM_NOSHOUT:
        buf += " no_shout"
    if comm_flags & merc.COMM_NOTELL:
        buf += " no_tell"
    if comm_flags & merc.COMM_NOCHANNELS:
        buf += " no_channels"
    return "none" if not buf else buf


def imm_bit_name(imm_flags):
    buf = ""
    if imm_flags & merc.IMM_SUMMON:
        buf += " summon"
    if imm_flags & merc.IMM_CHARM:
        buf += " charm"
    if imm_flags & merc.IMM_MAGIC:
        buf += " magic"
    if imm_flags & merc.IMM_WEAPON:
        buf += " weapon"
    if imm_flags & merc.IMM_BASH:
        buf += " blunt"
    if imm_flags & merc.IMM_PIERCE:
        buf += " piercing"
    if imm_flags & merc.IMM_SLASH:
        buf += " slashing"
    if imm_flags & merc.IMM_FIRE:
        buf += " fire"
    if imm_flags & merc.IMM_COLD:
        buf += " cold"
    if imm_flags & merc.IMM_LIGHTNING:
        buf += " lightning"
    if imm_flags & merc.IMM_ACID:
        buf += " acid"
    if imm_flags & merc.IMM_POISON:
        buf += " poison"
    if imm_flags & merc.IMM_NEGATIVE:
        buf += " negative"
    if imm_flags & merc.IMM_HOLY:
        buf += " holy"
    if imm_flags & merc.IMM_ENERGY:
        buf += " energy"
    if imm_flags & merc.IMM_MENTAL:
        buf += " mental"
    if imm_flags & merc.IMM_DISEASE:
        buf += " disease"
    if imm_flags & merc.IMM_DROWNING:
        buf += " drowning"
    if imm_flags & merc.IMM_LIGHT:
        buf += " light"
    if imm_flags & merc.VULN_IRON:
        buf += " iron"
    if imm_flags & merc.VULN_WOOD:
        buf += " wood"
    if imm_flags & merc.VULN_SILVER:
        buf += " silver"
    return "none" if not buf else buf


def wear_bit_name(wear_flags):
    buf = ""
    if wear_flags & merc.ITEM_TAKE:
        buf += " take"
    if wear_flags & merc.ITEM_WEAR_FINGER:
        buf += " finger"
    if wear_flags & merc.ITEM_WEAR_NECK:
        buf += " neck"
    if wear_flags & merc.ITEM_WEAR_BODY:
        buf += " torso"
    if wear_flags & merc.ITEM_WEAR_HEAD:
        buf += " head"
    if wear_flags & merc.ITEM_WEAR_LEGS:
        buf += " legs"
    if wear_flags & merc.ITEM_WEAR_FEET:
        buf += " feet"
    if wear_flags & merc.ITEM_WEAR_HANDS:
        buf += " hands"
    if wear_flags & merc.ITEM_WEAR_ARMS:
        buf += " arms"
    if wear_flags & merc.ITEM_WEAR_SHIELD:
        buf += " shield"
    if wear_flags & merc.ITEM_WEAR_ABOUT:
        buf += " body"
    if wear_flags & merc.ITEM_WEAR_WAIST:
        buf += " waist"
    if wear_flags & merc.ITEM_WEAR_WRIST:
        buf += " wrist"
    if wear_flags & merc.ITEM_WIELD:
        buf += " wield"
    if wear_flags & merc.ITEM_HOLD:
        buf += " hold"
    if wear_flags & merc.ITEM_NO_SAC:
        buf += " nosac"
    if wear_flags & merc.ITEM_WEAR_FLOAT:
        buf += " float"
    return "none" if not buf else buf


def form_bit_name(form_flags):
    buf = ""
    if form_flags & merc.FORM_POISON:
        buf += " poison"
    elif form_flags & merc.FORM_EDIBLE:
        buf += " edible"
    if form_flags & merc.FORM_MAGICAL:
        buf += " magical"
    if form_flags & merc.FORM_INSTANT_DECAY:
        buf += " instant_rot"
    if form_flags & merc.FORM_OTHER:
        buf += " other"
    if form_flags & merc.FORM_ANIMAL:
        buf += " animal"
    if form_flags & merc.FORM_SENTIENT:
        buf += " sentient"
    if form_flags & merc.FORM_UNDEAD:
        buf += " undead"
    if form_flags & merc.FORM_CONSTRUCT:
        buf += " construct"
    if form_flags & merc.FORM_MIST:
        buf += " mist"
    if form_flags & merc.FORM_INTANGIBLE:
        buf += " intangible"
    if form_flags & merc.FORM_BIPED:
        buf += " biped"
    if form_flags & merc.FORM_CENTAUR:
        buf += " centaur"
    if form_flags & merc.FORM_INSECT:
        buf += " insect"
    if form_flags & merc.FORM_SPIDER:
        buf += " spider"
    if form_flags & merc.FORM_CRUSTACEAN:
        buf += " crustacean"
    if form_flags & merc.FORM_WORM:
        buf += " worm"
    if form_flags & merc.FORM_BLOB:
        buf += " blob"
    if form_flags & merc.FORM_MAMMAL:
        buf += " mammal"
    if form_flags & merc.FORM_BIRD:
        buf += " bird"
    if form_flags & merc.FORM_REPTILE:
        buf += " reptile"
    if form_flags & merc.FORM_SNAKE:
        buf += " snake"
    if form_flags & merc.FORM_DRAGON:
        buf += " dragon"
    if form_flags & merc.FORM_AMPHIBIAN:
        buf += " amphibian"
    if form_flags & merc.FORM_FISH:
        buf += " fish"
    if form_flags & merc.FORM_COLD_BLOOD:
        buf += " cold_blooded"
    return "none" if not buf else buf


def part_bit_name(part_flags):
    buf = ''
    if part_flags & merc.PART_HEAD:
        buf += " head"
    if part_flags & merc.PART_ARMS:
        buf += " arms"
    if part_flags & merc.PART_LEGS:
        buf += " legs"
    if part_flags & merc.PART_HEART:
        buf += " heart"
    if part_flags & merc.PART_BRAINS:
        buf += " brains"
    if part_flags & merc.PART_GUTS:
        buf += " guts"
    if part_flags & merc.PART_HANDS:
        buf += " hands"
    if part_flags & merc.PART_FEET:
        buf += " feet"
    if part_flags & merc.PART_FINGERS:
        buf += " fingers"
    if part_flags & merc.PART_EAR:
        buf += " ears"
    if part_flags & merc.PART_EYE:
        buf += " eyes"
    if part_flags & merc.PART_LONG_TONGUE:
        buf += " long_tongue"
    if part_flags & merc.PART_EYESTALKS:
        buf += " eyestalks"
    if part_flags & merc.PART_TENTACLES:
        buf += " tentacles"
    if part_flags & merc.PART_FINS:
        buf += " fins"
    if part_flags & merc.PART_WINGS:
        buf += " wings"
    if part_flags & merc.PART_TAIL:
        buf += " tail"
    if part_flags & merc.PART_CLAWS:
        buf += " claws"
    if part_flags & merc.PART_FANGS:
        buf += " fangs"
    if part_flags & merc.PART_HORNS:
        buf += " horns"
    if part_flags & merc.PART_SCALES:
        buf += " scales"
    return "none" if not buf else buf


def weapon_bit_name(weapon_flags):
    buf = ''
    if weapon_flags & merc.WEAPON_FLAMING:
        buf += " flaming"
    if weapon_flags & merc.WEAPON_FROST:
        buf += " frost"
    if weapon_flags & merc.WEAPON_VAMPIRIC:
        buf += " vampiric"
    if weapon_flags & merc.WEAPON_SHARP:
        buf += " sharp"
    if weapon_flags & merc.WEAPON_VORPAL:
        buf += " vorpal"
    if weapon_flags & merc.WEAPON_TWO_HANDS:
        buf += " two-handed"
    if weapon_flags & merc.WEAPON_SHOCKING:
        buf += " shocking"
    if weapon_flags & merc.WEAPON_POISON:
        buf += " poison"
    return "none" if not buf else buf


def cont_bit_name(cont_flags):
    buf = ''
    if cont_flags & merc.CONT_CLOSEABLE:
        buf += " closable"
    if cont_flags & merc.CONT_PICKPROOF:
        buf += " pickproof"
    if cont_flags & merc.CONT_CLOSED:
        buf += " closed"
    if cont_flags & merc.CONT_LOCKED:
        buf += " locked"
    return "none" if not buf else buf


def off_bit_name(off_flags):
    buf = ''
    if off_flags & merc.OFF_AREA_ATTACK:
        buf += " area attack"
    if off_flags & merc.OFF_BACKSTAB:
        buf += " backstab"
    if off_flags & merc.OFF_BASH:
        buf += " bash"
    if off_flags & merc.OFF_BERSERK:
        buf += " berserk"
    if off_flags & merc.OFF_DISARM:
        buf += " disarm"
    if off_flags & merc.OFF_DODGE:
        buf += " dodge"
    if off_flags & merc.OFF_FADE:
        buf += " fade"
    if off_flags & merc.OFF_FAST:
        buf += " fast"
    if off_flags & merc.OFF_KICK:
        buf += " kick"
    if off_flags & merc.OFF_KICK_DIRT:
        buf += " kick_dirt"
    if off_flags & merc.OFF_PARRY:
        buf += " parry"
    if off_flags & merc.OFF_RESCUE:
        buf += " rescue"
    if off_flags & merc.OFF_TAIL:
        buf += " tail"
    if off_flags & merc.OFF_TRIP:
        buf += " trip"
    if off_flags & merc.OFF_CRUSH:
        buf += " crush"
    if off_flags & merc.ASSIST_ALL:
        buf += " assist_all"
    if off_flags & merc.ASSIST_ALIGN:
        buf += " assist_align"
    if off_flags & merc.ASSIST_RACE:
        buf += " assist_race"
    if off_flags & merc.ASSIST_PLAYERS:
        buf += " assist_players"
    if off_flags & merc.ASSIST_GUARD:
        buf += " assist_guard"
    if off_flags & merc.ASSIST_VNUM:
        buf += " assist_vnum"
    return "none" if not buf else buf
