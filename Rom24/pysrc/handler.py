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
from merc import *


# * Return ascii name of an affect location.
def affect_loc_name(location):
    if location == APPLY_NONE:
        return "none"
    if location == APPLY_STR:
        return "strength"
    if location == APPLY_DEX:
        return "dexterity"
    if location == APPLY_INT:
        return "intelligence"
    if location == APPLY_WIS:
        return "wisdom"
    if location == APPLY_CON:
        return "constitution"
    if location == APPLY_SEX:
        return "sex"
    if location == APPLY_CLASS:
        return "class"
    if location == APPLY_LEVEL:
        return "level"
    if location == APPLY_AGE:
        return "age"
    if location == APPLY_MANA:
        return "mana"
    if location == APPLY_HIT:
        return "hp"
    if location == APPLY_MOVE:
        return "moves"
    if location == APPLY_GOLD:
        return "gold"
    if location == APPLY_EXP:
        return "experience"
    if location == APPLY_AC:
        return "armor class"
    if location == APPLY_HITROLL:
        return "hit roll"
    if location == APPLY_DAMROLL:
        return "damage roll"
    if location == APPLY_SAVES:
        return "saves"
    if location == APPLY_SAVING_ROD:
        return "save vs rod"
    if location == APPLY_SAVING_PETRI:
        return "save vs petrification"
    if location == APPLY_SAVING_BREATH:
        return "save vs breath"
    if location == APPLY_SAVING_SPELL:
        return "save vs spell"
    if location == APPLY_SPELL_AFFECT:
        return "none"
    print("Affect_location_name: unknown location %d." % location)
    return "(unknown)"


# * Return ascii name of an affect bit vector.
def affect_bit_name(vector):
    buf = ""
    if vector & AFF_BLIND:
        buf += " blind"
    if vector & AFF_INVISIBLE:
        buf += " invisible"
    if vector & AFF_DETECT_EVIL:
        buf += " detect_evil"
    if vector & AFF_DETECT_GOOD:
        buf += " detect_good"
    if vector & AFF_DETECT_INVIS:
        buf += " detect_invis"
    if vector & AFF_DETECT_MAGIC:
        buf += " detect_magic"
    if vector & AFF_DETECT_HIDDEN:
        buf += " detect_hidden"
    if vector & AFF_SANCTUARY:
        buf += " sanctuary"
    if vector & AFF_FAERIE_FIRE:
        buf += " faerie_fire"
    if vector & AFF_INFRARED:
        buf += " infrared"
    if vector & AFF_CURSE:
        buf += " curse"
    if vector & AFF_POISON:
        buf += " poison"
    if vector & AFF_PROTECT_EVIL:
        buf += " prot_evil"
    if vector & AFF_PROTECT_GOOD:
        buf += " prot_good"
    if vector & AFF_SLEEP:
        buf += " sleep"
    if vector & AFF_SNEAK:
        buf += " sneak"
    if vector & AFF_HIDE:
        buf += " hide"
    if vector & AFF_CHARM:
        buf += " charm"
    if vector & AFF_FLYING:
        buf += " flying"
    if vector & AFF_PASS_DOOR:
        buf += " pass_door"
    if vector & AFF_BERSERK:
        buf += " berserk"
    if vector & AFF_CALM:
        buf += " calm"
    if vector & AFF_HASTE:
        buf += " haste"
    if vector & AFF_SLOW:
        buf += " slow"
    if vector & AFF_PLAGUE:
        buf += " plague"
    if vector & AFF_DARK_VISION:
        buf += " dark_vision"
    if not buf:
        return "none"
    return buf


#
# * Return ascii name of extra flags vector.
def extra_bit_name(extra_flags):
    buf = ""
    if extra_flags & ITEM_GLOW:
        buf += " glow"
    if extra_flags & ITEM_HUM:
        buf += " hum"
    if extra_flags & ITEM_DARK:
        buf += " dark"
    if extra_flags & ITEM_LOCK:
        buf += " lock"
    if extra_flags & ITEM_EVIL:
        buf += " evil"
    if extra_flags & ITEM_INVIS:
        buf += " invis"
    if extra_flags & ITEM_MAGIC:
        buf += " magic"
    if extra_flags & ITEM_NODROP:
        buf += " nodrop"
    if extra_flags & ITEM_BLESS:
        buf += " bless"
    if extra_flags & ITEM_ANTI_GOOD:
        buf += " anti-good"
    if extra_flags & ITEM_ANTI_EVIL:
        buf += " anti-evil"
    if extra_flags & ITEM_ANTI_NEUTRAL:
        buf += " anti-neutral"
    if extra_flags & ITEM_NOREMOVE:
        buf += " noremove"
    if extra_flags & ITEM_INVENTORY:
        buf += " inventory"
    if extra_flags & ITEM_NOPURGE:
        buf += " nopurge"
    if extra_flags & ITEM_VIS_DEATH:
        buf += " vis_death"
    if extra_flags & ITEM_ROT_DEATH:
        buf += " rot_death"
    if extra_flags & ITEM_NOLOCATE:
        buf += " no_locate"
    if extra_flags & ITEM_SELL_EXTRACT:
        buf += " sell_extract"
    if extra_flags & ITEM_BURN_PROOF:
        buf += " burn_proof"
    if extra_flags & ITEM_NOUNCURSE:
        buf += " no_uncurse"
    return "none" if not buf else buf


# return ascii name of an act vector */
def act_bit_name(act_flags):
    buf = ""

    if IS_SET(act_flags, ACT_IS_NPC):
        buf += " npc"
        if act_flags & ACT_SENTINEL:
            buf += " sentinel"
        if act_flags & ACT_SCAVENGER:
            buf += " scavenger"
        if act_flags & ACT_AGGRESSIVE:
            buf += " aggressive"
        if act_flags & ACT_STAY_AREA:
            buf += " stay_area"
        if act_flags & ACT_WIMPY:
            buf += " wimpy"
        if act_flags & ACT_PET:
            buf += " pet"
        if act_flags & ACT_TRAIN:
            buf += " train"
        if act_flags & ACT_PRACTICE:
            buf += " practice"
        if act_flags & ACT_UNDEAD:
            buf += " undead"
        if act_flags & ACT_CLERIC:
            buf += " cleric"
        if act_flags & ACT_MAGE:
            buf += " mage"
        if act_flags & ACT_THIEF:
            buf += " thief"
        if act_flags & ACT_WARRIOR:
            buf += " warrior"
        if act_flags & ACT_NOALIGN:
            buf += " no_align"
        if act_flags & ACT_NOPURGE:
            buf += " no_purge"
        if act_flags & ACT_IS_HEALER:
            buf += " healer"
        if act_flags & ACT_IS_CHANGER:
            buf += " changer"
        if act_flags & ACT_GAIN:
            buf += " skill_train"
        if act_flags & ACT_UPDATE_ALWAYS:
            buf += " update_always"
    else:
        buf += " player"
        if act_flags & PLR_AUTOASSIST:
            buf += " autoassist"
        if act_flags & PLR_AUTOEXIT:
            buf += " autoexit"
        if act_flags & PLR_AUTOLOOT:
            buf += " autoloot"
        if act_flags & PLR_AUTOSAC:
            buf += " autosac"
        if act_flags & PLR_AUTOGOLD:
            buf += " autogold"
        if act_flags & PLR_AUTOSPLIT:
            buf += " autosplit"
        if act_flags & PLR_HOLYLIGHT:
            buf += " holy_light"
        if act_flags & PLR_CANLOOT:
            buf += " loot_corpse"
        if act_flags & PLR_NOSUMMON:
            buf += " no_summon"
        if act_flags & PLR_NOFOLLOW:
            buf += " no_follow"
        if act_flags & PLR_FREEZE:
            buf += " frozen"
        if act_flags & PLR_THIEF:
            buf += " thief"
        if act_flags & PLR_KILLER:
            buf += " killer"
        if act_flags & PLR_OMNI:
            buf += " omni"
    return "none" if not buf else buf


def comm_bit_name(comm_flags):
    buf = ""
    if comm_flags & COMM_QUIET:
        buf += " quiet"
    if comm_flags & COMM_DEAF:
        buf += " deaf"
    if comm_flags & COMM_NOWIZ:
        buf += " no_wiz"
    if comm_flags & COMM_NOAUCTION:
        buf += " no_auction"
    if comm_flags & COMM_NOGOSSIP:
        buf += " no_gossip"
    if comm_flags & COMM_NOQUESTION:
        buf += " no_question"
    if comm_flags & COMM_NOMUSIC:
        buf += " no_music"
    if comm_flags & COMM_NOQUOTE:
        buf += " no_quote"
    if comm_flags & COMM_COMPACT:
        buf += " compact"
    if comm_flags & COMM_BRIEF:
        buf += " brief"
    if comm_flags & COMM_PROMPT:
        buf += " prompt"
    if comm_flags & COMM_COMBINE:
        buf += " combine"
    if comm_flags & COMM_NOEMOTE:
        buf += " no_emote"
    if comm_flags & COMM_NOSHOUT:
        buf += " no_shout"
    if comm_flags & COMM_NOTELL:
        buf += " no_tell"
    if comm_flags & COMM_NOCHANNELS:
        buf += " no_channels"
    return "none" if not buf else buf


def imm_bit_name(imm_flags):
    buf = ""
    if imm_flags & IMM_SUMMON:
        buf += " summon"
    if imm_flags & IMM_CHARM:
        buf += " charm"
    if imm_flags & IMM_MAGIC:
        buf += " magic"
    if imm_flags & IMM_WEAPON:
        buf += " weapon"
    if imm_flags & IMM_BASH:
        buf += " blunt"
    if imm_flags & IMM_PIERCE:
        buf += " piercing"
    if imm_flags & IMM_SLASH:
        buf += " slashing"
    if imm_flags & IMM_FIRE:
        buf += " fire"
    if imm_flags & IMM_COLD:
        buf += " cold"
    if imm_flags & IMM_LIGHTNING:
        buf += " lightning"
    if imm_flags & IMM_ACID:
        buf += " acid"
    if imm_flags & IMM_POISON:
        buf += " poison"
    if imm_flags & IMM_NEGATIVE:
        buf += " negative"
    if imm_flags & IMM_HOLY:
        buf += " holy"
    if imm_flags & IMM_ENERGY:
        buf += " energy"
    if imm_flags & IMM_MENTAL:
        buf += " mental"
    if imm_flags & IMM_DISEASE:
        buf += " disease"
    if imm_flags & IMM_DROWNING:
        buf += " drowning"
    if imm_flags & IMM_LIGHT:
        buf += " light"
    if imm_flags & VULN_IRON:
        buf += " iron"
    if imm_flags & VULN_WOOD:
        buf += " wood"
    if imm_flags & VULN_SILVER:
        buf += " silver"
    return "none" if not buf else buf


def wear_bit_name(wear_flags):
    buf = ""
    if wear_flags & ITEM_TAKE:
        buf += " take"
    if wear_flags & ITEM_WEAR_FINGER:
        buf += " finger"
    if wear_flags & ITEM_WEAR_NECK:
        buf += " neck"
    if wear_flags & ITEM_WEAR_BODY:
        buf += " torso"
    if wear_flags & ITEM_WEAR_HEAD:
        buf += " head"
    if wear_flags & ITEM_WEAR_LEGS:
        buf += " legs"
    if wear_flags & ITEM_WEAR_FEET:
        buf += " feet"
    if wear_flags & ITEM_WEAR_HANDS:
        buf += " hands"
    if wear_flags & ITEM_WEAR_ARMS:
        buf += " arms"
    if wear_flags & ITEM_WEAR_SHIELD:
        buf += " shield"
    if wear_flags & ITEM_WEAR_ABOUT:
        buf += " body"
    if wear_flags & ITEM_WEAR_WAIST:
        buf += " waist"
    if wear_flags & ITEM_WEAR_WRIST:
        buf += " wrist"
    if wear_flags & ITEM_WIELD:
        buf += " wield"
    if wear_flags & ITEM_HOLD:
        buf += " hold"
    if wear_flags & ITEM_NO_SAC:
        buf += " nosac"
    if wear_flags & ITEM_WEAR_FLOAT:
        buf += " float"
    return "none" if not buf else buf


def form_bit_name(form_flags):
    buf = ""
    if form_flags & FORM_POISON:
        buf += " poison"
    elif form_flags & FORM_EDIBLE:
        buf += " edible"
    if form_flags & FORM_MAGICAL:
        buf += " magical"
    if form_flags & FORM_INSTANT_DECAY:
        buf += " instant_rot"
    if form_flags & FORM_OTHER:
        buf += " other"
    if form_flags & FORM_ANIMAL:
        buf += " animal"
    if form_flags & FORM_SENTIENT:
        buf += " sentient"
    if form_flags & FORM_UNDEAD:
        buf += " undead"
    if form_flags & FORM_CONSTRUCT:
        buf += " construct"
    if form_flags & FORM_MIST:
        buf += " mist"
    if form_flags & FORM_INTANGIBLE:
        buf += " intangible"
    if form_flags & FORM_BIPED:
        buf += " biped"
    if form_flags & FORM_CENTAUR:
        buf += " centaur"
    if form_flags & FORM_INSECT:
        buf += " insect"
    if form_flags & FORM_SPIDER:
        buf += " spider"
    if form_flags & FORM_CRUSTACEAN:
        buf += " crustacean"
    if form_flags & FORM_WORM:
        buf += " worm"
    if form_flags & FORM_BLOB:
        buf += " blob"
    if form_flags & FORM_MAMMAL:
        buf += " mammal"
    if form_flags & FORM_BIRD:
        buf += " bird"
    if form_flags & FORM_REPTILE:
        buf += " reptile"
    if form_flags & FORM_SNAKE:
        buf += " snake"
    if form_flags & FORM_DRAGON:
        buf += " dragon"
    if form_flags & FORM_AMPHIBIAN:
        buf += " amphibian"
    if form_flags & FORM_FISH:
        buf += " fish"
    if form_flags & FORM_COLD_BLOOD:
        buf += " cold_blooded"
    return "none" if not buf else buf


def part_bit_name(part_flags):
    buf = ''
    if part_flags & PART_HEAD:
        buf += " head"
    if part_flags & PART_ARMS:
        buf += " arms"
    if part_flags & PART_LEGS:
        buf += " legs"
    if part_flags & PART_HEART:
        buf += " heart"
    if part_flags & PART_BRAINS:
        buf += " brains"
    if part_flags & PART_GUTS:
        buf += " guts"
    if part_flags & PART_HANDS:
        buf += " hands"
    if part_flags & PART_FEET:
        buf += " feet"
    if part_flags & PART_FINGERS:
        buf += " fingers"
    if part_flags & PART_EAR:
        buf += " ears"
    if part_flags & PART_EYE:
        buf += " eyes"
    if part_flags & PART_LONG_TONGUE:
        buf += " long_tongue"
    if part_flags & PART_EYESTALKS:
        buf += " eyestalks"
    if part_flags & PART_TENTACLES:
        buf += " tentacles"
    if part_flags & PART_FINS:
        buf += " fins"
    if part_flags & PART_WINGS:
        buf += " wings"
    if part_flags & PART_TAIL:
        buf += " tail"
    if part_flags & PART_CLAWS:
        buf += " claws"
    if part_flags & PART_FANGS:
        buf += " fangs"
    if part_flags & PART_HORNS:
        buf += " horns"
    if part_flags & PART_SCALES:
        buf += " scales"
    return "none" if not buf else buf


def weapon_bit_name(weapon_flags):
    buf = ''
    if weapon_flags & WEAPON_FLAMING:
        buf += " flaming"
    if weapon_flags & WEAPON_FROST:
        buf += " frost"
    if weapon_flags & WEAPON_VAMPIRIC:
        buf += " vampiric"
    if weapon_flags & WEAPON_SHARP:
        buf += " sharp"
    if weapon_flags & WEAPON_VORPAL:
        buf += " vorpal"
    if weapon_flags & WEAPON_TWO_HANDS:
        buf += " two-handed"
    if weapon_flags & WEAPON_SHOCKING:
        buf += " shocking"
    if weapon_flags & WEAPON_POISON:
        buf += " poison"
    return "none" if not buf else buf


def cont_bit_name(cont_flags):
    buf = ''
    if cont_flags & CONT_CLOSEABLE:
        buf += " closable"
    if cont_flags & CONT_PICKPROOF:
        buf += " pickproof"
    if cont_flags & CONT_CLOSED:
        buf += " closed"
    if cont_flags & CONT_LOCKED:
        buf += " locked"
    return "none" if not buf else buf


def off_bit_name(off_flags):
    buf = ''
    if off_flags & OFF_AREA_ATTACK:
        buf += " area attack"
    if off_flags & OFF_BACKSTAB:
        buf += " backstab"
    if off_flags & OFF_BASH:
        buf += " bash"
    if off_flags & OFF_BERSERK:
        buf += " berserk"
    if off_flags & OFF_DISARM:
        buf += " disarm"
    if off_flags & OFF_DODGE:
        buf += " dodge"
    if off_flags & OFF_FADE:
        buf += " fade"
    if off_flags & OFF_FAST:
        buf += " fast"
    if off_flags & OFF_KICK:
        buf += " kick"
    if off_flags & OFF_KICK_DIRT:
        buf += " kick_dirt"
    if off_flags & OFF_PARRY:
        buf += " parry"
    if off_flags & OFF_RESCUE:
        buf += " rescue"
    if off_flags & OFF_TAIL:
        buf += " tail"
    if off_flags & OFF_TRIP:
        buf += " trip"
    if off_flags & OFF_CRUSH:
        buf += " crush"
    if off_flags & ASSIST_ALL:
        buf += " assist_all"
    if off_flags & ASSIST_ALIGN:
        buf += " assist_align"
    if off_flags & ASSIST_RACE:
        buf += " assist_race"
    if off_flags & ASSIST_PLAYERS:
        buf += " assist_players"
    if off_flags & ASSIST_GUARD:
        buf += " assist_guard"
    if off_flags & ASSIST_VNUM:
        buf += " assist_vnum"
    return "none" if not buf else buf
