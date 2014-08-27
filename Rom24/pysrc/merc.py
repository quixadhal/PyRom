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
import collections
import logging

logger = logging.getLogger()

import state_checks

#Merc Setup
#Letter->Bit conversion
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

#Boot Time, Current Time
boot_time = time.time()
current_time = 0

#Old Style Lists
descriptor_list = []
shop_list = []
help_list = []
greeting_list = []
social_list = []

'''
Game Defines
'''

#Wiznet Flags
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

#TODO: RemoveDebug - switch to false
GDCF = True
GDF = True

#Global Constants
PULSE_PER_SECOND = 4
MILLISECONDS_PER_PULSE = float(1000.0 / PULSE_PER_SECOND)
PULSE_VIOLENCE = (3 * PULSE_PER_SECOND)
PULSE_MOBILE = (4 * PULSE_PER_SECOND)
PULSE_MUSIC = (6 * PULSE_PER_SECOND)
PULSE_TICK = (60 * PULSE_PER_SECOND)
PULSE_AREA = (120 * PULSE_PER_SECOND)

#Time - Quarter of Day
SUN_DARK = 0
SUN_RISE = 1
SUN_LIGHT = 2
SUN_SET = 3

#Weather Defines
SKY_CLOUDLESS = 0
SKY_CLOUDY = 1
SKY_RAINING = 2
SKY_LIGHTNING = 3

#Dice Numbers
DICE_NUMBER = 0
DICE_TYPE = 1
DICE_BONUS = 2

#Target types
TAR_IGNORE = 0
TAR_CHAR_OFFENSIVE = 1
TAR_CHAR_DEFENSIVE = 2
TAR_CHAR_SELF = 3
TAR_OBJ_INV = 4
TAR_OBJ_CHAR_DEF = 5
TAR_OBJ_CHAR_OFF = 6

TARGET_CHAR = 0
TARGET_ITEM = 1
TARGET_ROOM = 2
TARGET_NONE = 3

#To types for act function
TO_ROOM = 0
TO_NOTVICT = 1
TO_VICT = 2
TO_CHAR = 3
TO_ALL = 4

#Log types
LOG_NORMAL = 0
LOG_ALWAYS = 1
LOG_NEVER = 2

#Damage classes
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

PAGELEN = 22

#Pc Tracking
max_on = 0

#Where definitions
TO_AFFECTS = 0
TO_OBJECT = 1
TO_IMMUNE = 2
TO_RESIST = 3
TO_VULN = 4
TO_WEAPON = 5

#Vulnerability States
IS_NORMAL = 0
IS_IMMUNE = 1
IS_RESISTANT = 2
IS_VULNERABLE = 3

#Hit or Undefined
TYPE_UNDEFINED = -1
TYPE_HIT = 1000

#Affected by Bits
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


'''
Character Defines
'''


''' Equipment Slot Strings - for use with displaying EQ to characters '''

eq_slot_strings = collections.OrderedDict([('light', '<used as light>     '),
                                           ('left_finger', '<worn on finger>    '),
                                           ('right_finger', '<worn on finger>    '),
                                           ('neck', '<worn around neck>  '),
                                           ('collar', '<worn around neck>  '),
                                           ('body', '<worn on torso>     '),
                                           ('head', '<worn on head>      '),
                                           ('legs', '<worn on legs>      '),
                                           ('feet', '<worn on feet>      '),
                                           ('hands', '<worn on hands>     '),
                                           ('arms', '<worn on arms>      '),
                                           ('off_hand', '<worn as shield>    '),
                                           ('about_body', '<worn about body>   '),
                                           ('waist', '<worn about waist>  '),
                                           ('left_wrist', '<worn around wrist> '),
                                           ('right_wrist', '<worn around wrist> '),
                                           ('main_hand', '<wielded>           '),
                                           ('held', '<held>              '),
                                           ('float', '<floating nearby>   ')])

#Immunity Bits
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

#Resist Bits
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

#Vulnerable Bits
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

#Sexes
SEX_NEUTRAL = 0
SEX_MALE = 1
SEX_FEMALE = 2

#Stats
STAT_STR = 0
STAT_INT = 1
STAT_WIS = 2
STAT_DEX = 3
STAT_CON = 4

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

# penalty flags */
PLR_PERMIT = U
PLR_LOG = W
PLR_DENY = X
PLR_FREEZE = Y
PLR_THIEF = Z
PLR_KILLER = aa
PLR_OMNI = bb

#Player Conditions
COND_DRUNK = 0
COND_FULL = 1
COND_THIRST = 2
COND_HUNGER = 3

#RT Comm Flags
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

#Display Flags
COMM_COMPACT = L
COMM_BRIEF = M
COMM_PROMPT = N
COMM_COMBINE = O
COMM_TELNET_GA = P
COMM_SHOW_AFFECTS = Q
COMM_NOGRATS = R

#Comm Penalties
COMM_NOEMOTE = T
COMM_NOSHOUT = U
COMM_NOTELL = V
COMM_NOCHANNELS = W
COMM_SNOOP_PROOF = Y
COMM_AFK = Z

#Assist Bits
ASSIST_ALL = P
ASSIST_ALIGN = Q
ASSIST_RACE = R
ASSIST_PLAYERS = S
ASSIST_GUARD = T
ASSIST_VNUM = U

#ACT Bits for NPCs
ACT_IS_NPC = A  # Auto set for mobs    */
ACT_SENTINEL = B  # Stays in one room    */
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

#Offensive Bits
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

#Body Form Bits, descriptive
FORM_EDIBLE = A
FORM_POISON = B
FORM_MAGICAL = C
FORM_INSTANT_DECAY = D
FORM_OTHER = E  # defined by material bit */

#Character Form Bits
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

#Body Parts Bits
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

#Parts Combat Bits
PART_CLAWS = U
PART_FANGS = V
PART_HORNS = W
PART_SCALES = X
PART_TUSKS = Y

#NPC Memory Flags
MEM_CUSTOMER = A
MEM_SELLER = B
MEM_HOSTILE = C
MEM_AFRAID = D


'''
Room Defines
'''


#Room Sector Types
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

#Directions
DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_UP = 4
DIR_DOWN = 5

#Movement
dir_name = ["north", "east", "south", "west", "up", "down"]
rev_dir = [2, 3, 0, 1, 5, 4]
movement_loss = [1, 2, 2, 3, 4, 6, 4, 1, 6, 10, 6]

#Static Room VNUMs
ROOM_VNUM_LIMBO = 2
ROOM_VNUM_CHAT = 1200
ROOM_VNUM_TEMPLE = 3001
ROOM_VNUM_ALTAR = 3054
ROOM_VNUM_SCHOOL = 3700
ROOM_VNUM_BALANCE = 4500
ROOM_VNUM_CIRCLE = 4400
ROOM_VNUM_DEMISE = 4201
ROOM_VNUM_HONOR = 4300

#Room Flags
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

#Exit Flags
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


'''
Item Defines
'''


#Apply Types
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

#Weapon Types
WEAPON_EXOTIC = 0
WEAPON_SWORD = 1
WEAPON_DAGGER = 2
WEAPON_SPEAR = 3
WEAPON_MACE = 4
WEAPON_AXE = 5
WEAPON_FLAIL = 6
WEAPON_WHIP = 7
WEAPON_POLEARM = 8

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

#Gate Flags
GATE_NORMAL_EXIT = A
GATE_NOCURSE = B
GATE_GOWITH = C
GATE_BUGGY = D
GATE_RANDOM = E

#Furniture Flags
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

#Container Values (EG, Bags, etc)
CONT_CLOSEABLE = 1
CONT_PICKPROOF = 2
CONT_CLOSED = 4
CONT_LOCKED = 8
CONT_PUT_ON = 16


'''
Conversion Maps
'''


#Item Bits
rom_wear_flag_map = {'A': 'Take',
                     'B': 'Finger',
                     'C': 'Neck',
                     'D': 'Body',
                     'E': 'Head',
                     'F': 'Legs',
                     'G': 'Feet',
                     'H': 'Hands',
                     'I': 'Arms',
                     'J': 'Shield',
                     'K': 'About',
                     'L': 'Waist',
                     'M': 'Wrist',
                     'N': 'Main Hand',
                     'O': 'Off Hand',
                     'P': 'No Sac',
                     'Q': 'Float'}

rom_wear_loc_map = {-1: None,
                    0: 'Light',
                    1: 'Left Finger',
                    2: 'Right Finger',
                    3: 'Neck',
                    4: 'Collar',
                    5: 'Body',
                    6: 'Head',
                    7: 'Legs',
                    8: 'Feet',
                    9: 'Hands',
                    10: 'Arms',
                    11: 'Off Hand',
                    12: 'About',
                    13: 'Waist',
                    14: 'Left Wrist',
                    15: 'Right Wrist',
                    16: 'Main Hand',
                    17: 'Held',
                    18: 'Float'}

# * Equpiment wear locations.
# * Used in #RESETS.

wear_num_to_str = collections.OrderedDict([(-1, 'none'),
                                           (0, 'light'),
                                           (1, 'left_finger'),
                                           (2, 'right_finger'),
                                           (3, 'neck'),
                                           (4, 'collar'),
                                           (5, 'body'),
                                           (6, 'head'),
                                           (7, 'legs'),
                                           (8, 'feet'),
                                           (9, 'hands'),
                                           (10, 'arms'),
                                           (11, 'unused'),
                                           (12, 'about'),
                                           (13, 'waist'),
                                           (14, 'left_wrist'),
                                           (15, 'right_wrist'),
                                           (16, 'main_hand'),
                                           (17, 'off_hand'),
                                           (18, 'float')])


'''
Legacy Bits n Bobs
'''


#legacy WEAR locations
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

# Extra flags - Legacy
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

# Wear flags - Legacy
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

#Weapon Types - Legacy
WEAPON_FLAMING = A
WEAPON_FROST = B
WEAPON_VAMPIRIC = C
WEAPON_SHARP = D
WEAPON_VORPAL = E
WEAPON_TWO_HANDS = F
WEAPON_SHOCKING = G
WEAPON_POISON = H

# Return ascii name of an affect location.
def affect_loc_name(location):
    affect_loc = {APPLY_NONE: "none",
                  APPLY_STR: "strength",
                  APPLY_DEX: "dexterity",
                  APPLY_INT: "intelligence",
                  APPLY_WIS: "wisdom",
                  APPLY_CON: "constitution",
                  APPLY_SEX: "sex",
                  APPLY_CLASS: "class",
                  APPLY_LEVEL: "level",
                  APPLY_AGE: "age",
                  APPLY_MANA: "mana",
                  APPLY_HIT: "hp",
                  APPLY_MOVE: "moves",
                  APPLY_GOLD: "gold",
                  APPLY_EXP: "experience",
                  APPLY_AC: "armor class",
                  APPLY_HITROLL: "hit roll",
                  APPLY_DAMROLL: "damage roll",
                  APPLY_SAVES: "saves",
                  APPLY_SAVING_ROD: "save vs rod",
                  APPLY_SAVING_PETRI: "save vs petrification",
                  APPLY_SAVING_BREATH: "save vs breath",
                  APPLY_SAVING_SPELL: "save vs spell",
                  APPLY_SPELL_AFFECT: "none"}
    location = affect_loc.get(location, None)
    if not location:
        logger.error("Affect_location_name: unknown location %d.", location)
        return "(unknown)"
    return location


# Return ascii name of an affect bit vector.
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


# Return ascii name of extra flags vector.
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


# return ascii name of an act vector
def act_bit_name(act_flags):
    buf = ""

    if state_checks.IS_SET(act_flags, ACT_IS_NPC):
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
