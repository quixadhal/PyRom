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

import time

MAX_TRADE = 5
MAX_GUILDROOMS = 2
MAX_STATS = 5
MAX_SKILL = 150
MAX_GROUP = 30
MAX_LEVEL = 60
MAX_ALIAS = 10
LEVEL_HERO = (MAX_LEVEL - 9)
LEVEL_IMMORTAL = (MAX_LEVEL - 8)

ML = MAX_LEVEL   # implementor */
L1 = MAX_LEVEL - 1   # creator */
L2 = MAX_LEVEL - 2   # supreme being */
L3 = MAX_LEVEL - 3   # deity */
L4 = MAX_LEVEL - 4   # god */
L5 = MAX_LEVEL - 5   # immortal */
L6 = MAX_LEVEL - 6   # demigod */
L7 = MAX_LEVEL - 7   # angel */
L8 = MAX_LEVEL - 8   # avatar */
IM = LEVEL_IMMORTAL  # avatar */
HE = LEVEL_HERO  # hero */


#Global Lists
descriptor_list = []
player_list = []
char_list = []
mob_index_hash = {}
obj_index_hash = {}
object_list = []
room_index_hash = {}
area_list = []
help_list = []
greeting_list = []
reset_list = []
shop_list = []
social_list = []

GDCF = False
GDF = False

#Global Constants
PULSE_PER_SECOND = 12
PULSE_VIOLENCE = (1 * PULSE_PER_SECOND)
PULSE_MOBILE = (4 * PULSE_PER_SECOND)
PULSE_MUSIC = (6 * PULSE_PER_SECOND)
PULSE_TICK = (60 * PULSE_PER_SECOND)
PULSE_AREA = (120 * PULSE_PER_SECOND)


# * Time and weather stuff.
SUN_DARK = 0
SUN_RISE = 1
SUN_LIGHT = 2
SUN_SET = 3

SKY_CLOUDLESS = 0
SKY_CLOUDY = 1
SKY_RAINING = 2
SKY_LIGHTNING = 3

#Stats
STAT_STR = 0
STAT_INT = 1
STAT_WIS = 2
STAT_DEX = 3
STAT_CON = 4

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_UP = 4
DIR_DOWN = 5


#Item types
ITEM_LIGHT = 'light'
ITEM_SCROLL = 'scroll'
ITEM_WAND = 'wand'
ITEM_STAFF = 'staff'
ITEM_WEAPON = 'weapon'
ITEM_TREASURE = 'treasure'
ITEM_ARMOR = 'armor'
ITEM_POTION = 'potion'
ITEM_CLOTHING = 'clothing'
ITEM_FURNITURE = 'furniture'
ITEM_TRASH = 'trash'
ITEM_CONTAINER = 'container'
ITEM_DRINK_CON = 'drink'
ITEM_KEY = 'key'
ITEM_FOOD = 'food'
ITEM_MONEY = 'money'
ITEM_BOAT = 'boat'
ITEM_CORPSE_NPC = 'npc_corpse'
ITEM_CORPSE_PC = 'pc_corpse'
ITEM_FOUNTAIN = 'fountain'
ITEM_PILL = 'pill'
ITEM_PROTECT = 'protect'
ITEM_MAP = 'map'
ITEM_PORTAL = 'portal'
ITEM_WARP_STONE = 'warp_stone'
ITEM_ROOM_KEY = 'room_key'
ITEM_GEM = 'gem'
ITEM_JEWELRY = 'jewelry'
ITEM_JUKEBOX = 'jukebox'


#Sexes
SEX_NEUTRAL = 0
SEX_MALE = 1
SEX_FEMALE = 2

#Sizes
SIZE_TINY = 0
SIZE_SMALL = 1
SIZE_MEDIUM = 2
SIZE_LARGE = 3
SIZE_HUGE = 4
SIZE_GIANT = 5

# AC types */
AC_PIERCE = 0
AC_BASH = 1
AC_SLASH = 2
AC_EXOTIC = 3

DICE_NUMBER = 0
DICE_TYPE = 1
DICE_BONUS = 2

#  Target types.
 
TAR_IGNORE = 0
TAR_CHAR_OFFENSIVE = 1
TAR_CHAR_DEFENSIVE = 2
TAR_CHAR_SELF = 3
TAR_OBJ_INV = 4
TAR_OBJ_CHAR_DEF = 5
TAR_OBJ_CHAR_OFF = 6

TARGET_CHAR = 0
TARGET_OBJ = 1
TARGET_ROOM = 2
TARGET_NONE = 3

#Positions
POS_DEAD = 0
POS_MORTAL = 1
POS_INCAP = 2
POS_STUNNED = 3
POS_SLEEPING = 4
POS_RESTING = 5
POS_SITTING = 6
POS_FIGHTING = 7
POS_STANDING = 8


# * Sector types.
# * Used in #ROOMS.

SECT_INSIDE = 0
SECT_CITY = 1
SECT_FIELD = 2
SECT_FOREST = 3
SECT_HILLS = 4
SECT_MOUNTAIN = 5
SECT_WATER_SWIM = 6
SECT_WATER_NOSWIM = 7
SECT_UNUSED = 8
SECT_AIR = 9
SECT_DESERT = 10
SECT_MAX = 11

# TO types for act.

TO_ROOM = 0
TO_NOTVICT = 1
TO_VICT = 2
TO_CHAR = 3
TO_ALL = 4

# damage classes
DAM_NONE = 0
DAM_BASH = 1
DAM_PIERCE = 2
DAM_SLASH = 3
DAM_FIRE = 4
DAM_COLD = 5
DAM_LIGHTNING = 6
DAM_ACID = 7
DAM_POISON = 8
DAM_NEGATIVE = 9
DAM_HOLY = 10
DAM_ENERGY = 11
DAM_MENTAL = 12
DAM_DISEASE = 13
DAM_DROWNING = 14
DAM_LIGHT = 15
DAM_OTHER = 16
DAM_HARM = 17
DAM_CHARM = 18
DAM_SOUND = 19

LOG_NORMAL = 0
LOG_ALWAYS = 1
LOG_NEVER = 2

WEAPON_EXOTIC = 0
WEAPON_SWORD = 1
WEAPON_DAGGER = 2
WEAPON_SPEAR = 3
WEAPON_MACE = 4
WEAPON_AXE = 5
WEAPON_FLAIL = 6
WEAPON_WHIP = 7
WEAPON_POLEARM = 8


# * Equpiment wear locations.
# * Used in #RESETS.

WEAR_NONE = -1
WEAR_LIGHT = 0
WEAR_FINGER_L = 1
WEAR_FINGER_R = 2
WEAR_NECK_1 = 3
WEAR_NECK_2 = 4
WEAR_BODY = 5
WEAR_HEAD = 6
WEAR_LEGS = 7
WEAR_FEET = 8
WEAR_HANDS = 9
WEAR_ARMS = 10
WEAR_SHIELD = 11
WEAR_ABOUT = 12
WEAR_WAIST = 13
WEAR_WRIST_L = 14
WEAR_WRIST_R = 15
WEAR_WIELD = 16
WEAR_HOLD = 17
WEAR_FLOAT = 18
MAX_WEAR = 19


# * Conditions.

COND_DRUNK = 0
COND_FULL = 1
COND_THIRST = 2
COND_HUNGER = 3

#/* where definitions */
TO_AFFECTS = 0
TO_OBJECT = 1
TO_IMMUNE = 2
TO_RESIST = 3
TO_VULN = 4
TO_WEAPON = 5

# return values for check_imm */
IS_NORMAL = 0
IS_IMMUNE = 1
IS_RESISTANT = 2
IS_VULNERABLE = 3

#Item constants

OBJ_VNUM_SILVER_ONE = 1
OBJ_VNUM_GOLD_ONE = 2
OBJ_VNUM_GOLD_SOME = 3
OBJ_VNUM_SILVER_SOME = 4
OBJ_VNUM_COINS = 5
OBJ_VNUM_CORPSE_NPC = 10
OBJ_VNUM_CORPSE_PC = 11
OBJ_VNUM_SEVERED_HEAD = 12
OBJ_VNUM_TORN_HEART = 13
OBJ_VNUM_SLICED_ARM = 14
OBJ_VNUM_SLICED_LEG = 15
OBJ_VNUM_GUTS = 16
OBJ_VNUM_BRAINS = 17
OBJ_VNUM_MUSHROOM = 20
OBJ_VNUM_LIGHT_BALL = 21
OBJ_VNUM_SPRING = 22
OBJ_VNUM_DISC = 23
OBJ_VNUM_PORTAL = 25
OBJ_VNUM_ROSE = 1001
OBJ_VNUM_PIT = 3010
OBJ_VNUM_SCHOOL_MACE = 3700
OBJ_VNUM_SCHOOL_DAGGER = 3701
OBJ_VNUM_SCHOOL_SWORD = 3702
OBJ_VNUM_SCHOOL_SPEAR = 3717
OBJ_VNUM_SCHOOL_STAFF = 3718
OBJ_VNUM_SCHOOL_AXE = 3719
OBJ_VNUM_SCHOOL_FLAIL = 3720
OBJ_VNUM_SCHOOL_WHIP = 3721
OBJ_VNUM_SCHOOL_POLEARM = 3722
OBJ_VNUM_SCHOOL_VEST = 3703
OBJ_VNUM_SCHOOL_SHIELD = 3704
OBJ_VNUM_SCHOOL_BANNER = 3716
OBJ_VNUM_MAP = 3162
OBJ_VNUM_WHISTLE = 2116

# * Well known room virtual numbers.
# * Defined in #ROOMS.
ROOM_VNUM_LIMBO = 2
ROOM_VNUM_CHAT = 1200
ROOM_VNUM_TEMPLE = 3001
ROOM_VNUM_ALTAR = 3054
ROOM_VNUM_SCHOOL = 3700
ROOM_VNUM_BALANCE = 4500
ROOM_VNUM_CIRCLE = 4400
ROOM_VNUM_DEMISE = 4201
ROOM_VNUM_HONOR = 4300

#* but may be arbitrary beyond that.
TYPE_UNDEFINED = -1
TYPE_HIT = 1000


A = 1
B = 1 << 1
C = 1 << 2
D = 1 << 3
E = 1 << 4
F = 1 << 5
G = 1 << 6
H = 1 << 7
I = 1 << 8
J = 1 << 9
K = 1 << 10
L = 1 << 11
M = 1 << 12
N = 1 << 13
O = 1 << 14
P = 1 << 15
Q = 1 << 16
R = 1 << 17
S = 1 << 18
T = 1 << 19
U = 1 << 20
V = 1 << 21
W = 1 << 22
X = 1 << 23
Y = 1 << 24
Z = 1 << 25
aa = 1 << 26
bb = 1 << 27
cc = 1 << 28
dd = 1 << 29
ee = 1 << 30
ff = 1 << 31
gg = 1 << 32
hh = 1 << 33
ii = 1 << 34
jj = 1 << 35
kk = 1 << 36
ll = 1 << 37
mm = 1 << 38
nn = 1 << 39
oo = 1 << 40
pp = 1 << 41
qq = 1 << 42
rr = 1 << 43
ss = 1 << 44
tt = 1 << 45
uu = 1 << 46
vv = 1 << 47
ww = 1 << 48
xx = 1 << 49
yy = 1 << 50
zz = 1 << 51


#  ACT bits for mobs.
#  Used in #MOBILES.

ACT_IS_NPC = A  # Auto set for mobs    */
ACT_SENTINEL = B #  Stays in one room    */
ACT_SCAVENGER = C  # Picks up objects */
ACT_AGGRESSIVE = F   # Attacks PC's     */
ACT_STAY_AREA = G    # Won't leave area */
ACT_WIMPY = H
ACT_PET = I     # Auto set for pets    */
ACT_TRAIN = J     # Can train PC's   */
ACT_PRACTICE = K     # Can practice PC's    */
ACT_UNDEAD = O 
ACT_CLERIC = Q
ACT_MAGE = R
ACT_THIEF = S
ACT_WARRIOR = T
ACT_NOALIGN = U
ACT_NOPURGE = V
ACT_OUTDOORS = W
ACT_INDOORS = Y
ACT_IS_HEALER = aa
ACT_GAIN = bb
ACT_UPDATE_ALWAYS = cc
ACT_IS_CHANGER = dd

OFF_AREA_ATTACK = A
OFF_BACKSTAB = B
OFF_BASH = C
OFF_BERSERK = D
OFF_DISARM = E
OFF_DODGE = F
OFF_FADE = G
OFF_FAST = H
OFF_KICK = I
OFF_KICK_DIRT = J
OFF_PARRY = K
OFF_RESCUE = L
OFF_TAIL = M
OFF_TRIP = N
OFF_CRUSH = O
ASSIST_ALL = P
ASSIST_ALIGN = Q
ASSIST_RACE = R
ASSIST_PLAYERS = S
ASSIST_GUARD = T
ASSIST_VNUM = U

IMM_SUMMON = A
IMM_CHARM = B
IMM_MAGIC = C
IMM_WEAPON = D
IMM_BASH = E
IMM_PIERCE = F
IMM_SLASH = G
IMM_FIRE = H
IMM_COLD = I
IMM_LIGHTNING = J
IMM_ACID = K
IMM_POISON = L
IMM_NEGATIVE = M
IMM_HOLY = N
IMM_ENERGY = O
IMM_MENTAL = P
IMM_DISEASE = Q
IMM_DROWNING = R
IMM_LIGHT = S
IMM_SOUND = T
IMM_WOOD = X
IMM_SILVER = Y
IMM_IRON = Z
 
# RES bits for mobs */
RES_SUMMON = A
RES_CHARM = B
RES_MAGIC = C
RES_WEAPON = D
RES_BASH = E
RES_PIERCE = F
RES_SLASH = G
RES_FIRE = H
RES_COLD = I
RES_LIGHTNING = J
RES_ACID = K
RES_POISON = L
RES_NEGATIVE = M
RES_HOLY = N
RES_ENERGY = O
RES_MENTAL = P
RES_DISEASE = Q
RES_DROWNING = R
RES_LIGHT = S
RES_SOUND = T
RES_WOOD = X
RES_SILVER = Y
RES_IRON = Z
 
# VULN bits for mobs */
VULN_SUMMON = A
VULN_CHARM = B
VULN_MAGIC = C
VULN_WEAPON = D
VULN_BASH = E
VULN_PIERCE = F
VULN_SLASH = G
VULN_FIRE = H
VULN_COLD = I
VULN_LIGHTNING = J
VULN_ACID = K
VULN_POISON = L
VULN_NEGATIVE = M
VULN_HOLY = N
VULN_ENERGY = O
VULN_MENTAL = P
VULN_DISEASE = Q
VULN_DROWNING = R
VULN_LIGHT = S
VULN_SOUND = T
VULN_WOOD = X
VULN_SILVER = Y
VULN_IRON = Z
 
# body form */
FORM_EDIBLE = A
FORM_POISON = B
FORM_MAGICAL = C
FORM_INSTANT_DECAY = D
FORM_OTHER = E  # defined by material bit */
 
# actual form */
FORM_ANIMAL = G
FORM_SENTIENT = H
FORM_UNDEAD = I
FORM_CONSTRUCT = J
FORM_MIST = K
FORM_INTANGIBLE = L
 
FORM_BIPED = M
FORM_CENTAUR = N
FORM_INSECT = O
FORM_SPIDER = P
FORM_CRUSTACEAN = Q
FORM_WORM = R
FORM_BLOB = S
 
FORM_MAMMAL = V
FORM_BIRD = W
FORM_REPTILE = X
FORM_SNAKE = Y
FORM_DRAGON = Z
FORM_AMPHIBIAN = aa
FORM_FISH = bb
FORM_COLD_BLOOD = cc    
 
# body parts */
PART_HEAD = A
PART_ARMS = B
PART_LEGS = C
PART_HEART = D
PART_BRAINS = E
PART_GUTS = F
PART_HANDS = G
PART_FEET = H
PART_FINGERS = I
PART_EAR = J
PART_EYE = K
PART_LONG_TONGUE = L
PART_EYESTALKS = M
PART_TENTACLES = N
PART_FINS = O
PART_WINGS = P
PART_TAIL = Q
# for combat */
PART_CLAWS = U
PART_FANGS = V
PART_HORNS = W
PART_SCALES = X
PART_TUSKS = Y


# Bits for 'affected_by'.
# Used in #MOBILES.

AFF_BLIND = A
AFF_INVISIBLE = B
AFF_DETECT_EVIL = C
AFF_DETECT_INVIS = D
AFF_DETECT_MAGIC = E
AFF_DETECT_HIDDEN = F
AFF_DETECT_GOOD = G
AFF_SANCTUARY = H
AFF_FAERIE_FIRE = I
AFF_INFRARED = J
AFF_CURSE = K
AFF_UNUSED_FLAG = L  # unused
AFF_POISON = M
AFF_PROTECT_EVIL = N
AFF_PROTECT_GOOD = O
AFF_SNEAK = P
AFF_HIDE = Q
AFF_SLEEP = R
AFF_CHARM = S
AFF_FLYING = T
AFF_PASS_DOOR = U
AFF_HASTE = V
AFF_CALM = W
AFF_PLAGUE = X
AFF_WEAKEN = Y
AFF_DARK_VISION = Z
AFF_BERSERK = aa
AFF_SWIM = bb
AFF_REGENERATION = cc
AFF_SLOW = dd


# Extra flags.
# Used in #OBJECTS.

ITEM_GLOW = A
ITEM_HUM = B
ITEM_DARK = C
ITEM_LOCK = D
ITEM_EVIL = E
ITEM_INVIS = F
ITEM_MAGIC = G
ITEM_NODROP = H
ITEM_BLESS = I
ITEM_ANTI_GOOD = J
ITEM_ANTI_EVIL = K
ITEM_ANTI_NEUTRAL = L
ITEM_NOREMOVE = M
ITEM_INVENTORY = N
ITEM_NOPURGE = O
ITEM_ROT_DEATH = P
ITEM_VIS_DEATH = Q
ITEM_NONMETAL = S
ITEM_NOLOCATE = T
ITEM_MELT_DROP = U
ITEM_HAD_TIMER = V
ITEM_SELL_EXTRACT = W
ITEM_BURN_PROOF = Y
ITEM_NOUNCURSE = Z


# Wear flags.
# Used in #OBJECTS.
ITEM_TAKE = A
ITEM_WEAR_FINGER = B
ITEM_WEAR_NECK = C
ITEM_WEAR_BODY = D
ITEM_WEAR_HEAD = E
ITEM_WEAR_LEGS = F
ITEM_WEAR_FEET = G
ITEM_WEAR_HANDS = H
ITEM_WEAR_ARMS = I
ITEM_WEAR_SHIELD = J
ITEM_WEAR_ABOUT = K
ITEM_WEAR_WAIST = L
ITEM_WEAR_WRIST = M
ITEM_WIELD = N
ITEM_HOLD = O
ITEM_NO_SAC = P
ITEM_WEAR_FLOAT = Q


# weapon types */
WEAPON_FLAMING = A
WEAPON_FROST = B
WEAPON_VAMPIRIC = C
WEAPON_SHARP = D
WEAPON_VORPAL = E
WEAPON_TWO_HANDS = F
WEAPON_SHOCKING = G
WEAPON_POISON = H

# gate flags */
GATE_NORMAL_EXIT = A
GATE_NOCURSE = B
GATE_GOWITH = C
GATE_BUGGY = D
GATE_RANDOM = E

# furniture flags */
STAND_AT = A
STAND_ON = B
STAND_IN = C
SIT_AT = D
SIT_ON = E
SIT_IN = F
REST_AT = G
REST_ON = H
REST_IN = I
SLEEP_AT = J
SLEEP_ON = K
SLEEP_IN = L
PUT_AT = M
PUT_ON = N
PUT_IN = O
PUT_INSIDE = P


# * Apply types (for affects).
# * Used in #OBJECTS.
APPLY_NONE = 0
APPLY_STR = 1
APPLY_DEX = 2
APPLY_INT = 3
APPLY_WIS = 4
APPLY_CON = 5
APPLY_SEX = 6
APPLY_CLASS = 7
APPLY_LEVEL = 8
APPLY_AGE = 9
APPLY_HEIGHT = 10
APPLY_WEIGHT = 11
APPLY_MANA = 12
APPLY_HIT = 13
APPLY_MOVE = 14
APPLY_GOLD = 15
APPLY_EXP = 16
APPLY_AC = 17
APPLY_HITROLL = 18
APPLY_DAMROLL = 19
APPLY_SAVES = 20
APPLY_SAVING_PARA = 20
APPLY_SAVING_ROD = 21
APPLY_SAVING_PETRI = 22
APPLY_SAVING_BREATH = 23
APPLY_SAVING_SPELL = 24
APPLY_SPELL_AFFECT = 25


# * Values for containers (value[1]).
# * Used in #OBJECTS.
CONT_CLOSEABLE = 1
CONT_PICKPROOF = 2
CONT_CLOSED = 4
CONT_LOCKED = 8
CONT_PUT_ON = 16

# Room flags.
# Used in #ROOMS.
ROOM_DARK = A
ROOM_NO_MOB = C
ROOM_INDOORS = D

ROOM_PRIVATE = J
ROOM_SAFE = K
ROOM_SOLITARY = L
ROOM_PET_SHOP = M
ROOM_NO_RECALL = N
ROOM_IMP_ONLY = O
ROOM_GODS_ONLY = P
ROOM_HEROES_ONLY = Q
ROOM_NEWBIES_ONLY = R
ROOM_LAW = S
ROOM_NOWHERE = T


# Exit flags.
# Used in #ROOMS.

EX_ISDOOR = A
EX_CLOSED = B
EX_LOCKED = C
EX_PICKPROOF = F
EX_NOPASS = G
EX_EASY = H
EX_HARD = I
EX_INFURIATING = J
EX_NOCLOSE = K
EX_NOLOCK = L


# ACT bits for players.

PLR_IS_NPC = A     # Don't EVER set.  */

# RT auto flags */
PLR_AUTOASSIST = C
PLR_AUTOEXIT = D
PLR_AUTOLOOT = E
PLR_AUTOSAC = F
PLR_AUTOGOLD = G
PLR_AUTOSPLIT = H

# RT personal flags */
PLR_HOLYLIGHT = N
PLR_CANLOOT = P
PLR_NOSUMMON = Q
PLR_NOFOLLOW = R
# 2 bits reserved, S-T */

# penalty flags */
PLR_PERMIT = U
PLR_LOG = W
PLR_DENY = X
PLR_FREEZE = Y
PLR_THIEF = Z
PLR_KILLER = aa
PLR_OMNI = bb

# RT comm flags -- may be used on both mobs and chars */
COMM_QUIET = A
COMM_DEAF = B
COMM_NOWIZ = C
COMM_NOAUCTION = D
COMM_NOGOSSIP = E
COMM_NOQUESTION = F
COMM_NOMUSIC = G
COMM_NOCLAN = H
COMM_NOQUOTE = I
COMM_SHOUTSOFF = J

# display flags */
COMM_COMPACT = L
COMM_BRIEF = M
COMM_PROMPT = N
COMM_COMBINE = O
COMM_TELNET_GA = P
COMM_SHOW_AFFECTS = Q
COMM_NOGRATS = R

# penalties */
COMM_NOEMOTE = T
COMM_NOSHOUT = U
COMM_NOTELL = V
COMM_NOCHANNELS = W 
COMM_SNOOP_PROOF = Y
COMM_AFK = Z

# WIZnet flags */
WIZ_ON = A
WIZ_TICKS = B
WIZ_LOGINS = C
WIZ_SITES = D
WIZ_LINKS = E
WIZ_DEATHS = F
WIZ_RESETS = G
WIZ_MOBDEATHS = H
WIZ_FLAGS = I
WIZ_PENALTIES = J
WIZ_SACCING = K
WIZ_LEVELS = L
WIZ_SECURE = M
WIZ_SWITCHES = N
WIZ_SNOOPS = O
WIZ_RESTORE = P
WIZ_LOAD = Q
WIZ_NEWBIE = R
WIZ_PREFIX = S
WIZ_SPAM = T

# memory settings */
MEM_CUSTOMER = A   
MEM_SELLER = B
MEM_HOSTILE = C
MEM_AFRAID = D

PAGELEN = 22

boot_time = time.time()
current_time = 0

#movement
dir_name = ["north", "east", "south", "west", "up", "down"]
rev_dir = [2, 3, 0, 1, 5, 4]
movement_loss = [1, 2, 2, 3, 4, 6, 4, 1, 6, 10, 6]

#Character Tracking
max_on = 0

where_name = ["<used as light>     ",
              "<worn on finger>    ",
              "<worn on finger>    ",
              "<worn around neck>  ",
              "<worn around neck>  ",
              "<worn on torso>     ",
              "<worn on head>      ",
              "<worn on legs>      ",
              "<worn on feet>      ",
              "<worn on hands>     ",
              "<worn on arms>      ",
              "<worn as shield>    ",
              "<worn about body>   ",
              "<worn about waist>  ",
              "<worn around wrist> ",
              "<worn around wrist> ",
              "<wielded>           ",
              "<held>              ",
              "<floating nearby>   "]
