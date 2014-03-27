"""
/***************************************************************************
 *  Original Diku Mud copyright=C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright=C) 1992, 1993 by Michael          *
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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor=rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor=gtaylor@hypercube.org)			               *
*	    Brian Moore=zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""

import time

#Global MAXes       
MAX_TRADE=5
MAX_GUILDROOMS=2
MAX_STATS=5
MAX_SKILL=150
MAX_GROUP=30


#Global Classes
class CHAR_DATA:
    master = None
    leader = None
    fighting = None
    reply = None
    pet = None
    memory = None
    spec_fun = None
    pIndexData = None
    desc = None
    affected = None
    pnote = None
    carrying = []
    on = None
    in_room = None
    was_in_room = None
    zone = None
    pcdata = None
    gen_data = None
    valid = False
    name = ""
    id = 0
    version = 5
    short_descr = ""
    long_descr = ""
    description = ""
    prompt = "<%%hhp %%mm %%vmv>"
    prefix = ""
    group = 0
    clan = 0
    sex=0
    guild=0
    race=0
    level=0
    trust=0
    played=0
    lines=20
    logon=0
    timer=0
    wait=0
    daze=0
    hit=20
    max_hit=20
    mana=100
    max_mana=100
    move=100
    max_move=100
    gold=0
    silver=0
    exp=0
    act=0
    comm=0
    wiznet=0
    imm_flags=0
    res_flags=0
    vuln_flags=0
    invis_level=0
    incog_level=0
    affected_by=0
    position=0
    practice=0
    train=0
    carry_weight=0
    carry_number=0
    saving_throw=0
    alignment=0
    hitroll=0
    damroll=0
    armor=[100, 100, 100, 100];
    wimpy=0
    # stats */
    perm_stat=[13 for x in range(MAX_STATS)]
    mod_stat=[0 for x in range(MAX_STATS)]
    # parts stuff */
    form=0
    parts=0
    size=0
    material=""
    # mobile stuff */
    off_flags=0
    damage=[0,0,0]
    dam_type=17
    start_pos=0
    default_pos=0
    def __repr__(self):
        return self.name
    def __init__(self):
        from const import race_table
        self.race = race_table['human']
        self.act=PLR_NOSUMMON
        self.comm=COMM_COMBINE | COMM_PROMPT

class PC_DATA:
    buffer=None
    valid=False
    pwd=""
    bamfin=""
    bamfout=""
    title=""
    last_note=0;
    last_idea=0
    last_penalty=0
    last_news=0
    last_changes=0
    perm_hit=0
    perm_mana=0
    perm_move=0
    true_sex=0
    last_level=0
    condition=[48,48,48,0]
    learned =[0 for x in range(MAX_SKILL)]
    group_known=[False for x in range(MAX_GROUP)]
    points=0
    confirm_delete=False
    alias={}

class AREA_DATA:
    reset_list = []
    file_name = ""
    name = ""
    credits = ""
    age = 0
    nplayer = 0
    low_range = 0
    high_range = 0
    min_vnum = 0
    max_vnum = 0
    empty = True

    def __repr__(self):
        return "<%s(%s): %d-%d>" % ( self.name, self.file_name, self.min_vnum, self.max_vnum )

class HELP_DATA:
    level = 0
    keyword = ""
    text = ""

    def __repr__(self):
        return "<%s:%d>" % ( self.keyword, self.level)

class MOB_INDEX_DATA:
    spec_fun = None
    pShop = None
    vnum = 0
    group = 0
    new_format = True
    count = 0
    killed = 0
    player_name = ""
    short_descr = ""
    long_descr = ""
    description = ""
    act = 0
    affected_by = 0
    alignment = 0
    level = 0
    hitroll = 0
    hit = [0, 0, 0]
    mana = [0, 0, 0]
    damage = [0, 0, 0]
    ac = [0, 0, 0, 0]
    dam_type = 0
    off_flags = 0
    imm_flags = 0
    res_flags = 0
    vuln_flags = 0
    start_pos = 0
    default_pos = 0
    sex = 0
    race = 0
    wealth = 0
    form = 0
    parts = 0
    size = 0
    material = ""
    def __repr__(self):
        return "<MobIndex: %s:%s>" % ( self.short_descr, self.vnum )

class OBJ_INDEX_DATA:
    extra_descr = None
    affected = None
    new_format = True
    name = ""
    short_descr = ""
    description = ""
    vnum = 0
    reset_num = 0
    material = ""
    item_type = 0
    extra_flags = 0
    wear_flags = 0
    level = 0
    condition = 0
    count = 0
    weight = 0
    cost = 0
    value = [0, 0, 0, 0, 0]
    def __repr__(self):
        return "<ObjIndex: %s:%d>" % (self.short_descr, self.vnum)    

class ROOM_INDEX_DATA:
    people = []
    contents = []
    extra_descr = []
    area = None
    exit = [None, None, None, None, None, None]
    old_exit = [None, None, None, None, None, None]
    name = ""
    description = ""
    owner = ""
    vnum = 0
    room_flags = 0
    light = 0
    sector_type = 0
    heal_rate = 0
    mana_rate = 0
    clan = 0
    def __repr__(self):
        return "<RoomIndex: %d" % (self.vnum)

class EXTRA_DESCR_DATA:
    keyword = ""# Keyword in look/examine
    description = ""

class EXIT_DATA:
    to_room=None
    exit_info=0
    key=0
    keyword=""
    description=""

class RESET_DATA:
    command = ""
    arg1=0
    arg2=0
    arg3=0
    arg4=0

class SHOP_DATA:
    keeper = 0
    buy_type = {}
    profit_buy = 0
    profit_sell = 0
    open_hour = 0
    close_hour = 0

class SOCIAL_DATA:
    name = ""
    char_no_arg = ""
    others_no_arg = ""
    char_found = ""
    others_found = ""
    vict_found = ""
    char_not_found = ""
    char_auto = ""
    others_auto = ""


#Global Lists
descriptor_list = []
mob_index_hash = {}
obj_index_hash = {}
room_index_hash = {}
area_list = []
help_list = []
greeting_list = []
reset_list = []
shop_list = []
social_list = []


#Global Constants
#Stats
STAT_STR=0
STAT_INT=1
STAT_WIS=2
STAT_DEX=3
STAT_CON=4


#Item types
ITEM_LIGHT=1
ITEM_SCROLL=2
ITEM_WAND=3
ITEM_STAFF=4
ITEM_WEAPON=5
ITEM_TREASURE=8
ITEM_ARMOR=9
ITEM_POTION=10
ITEM_CLOTHING=11
ITEM_FURNITURE=12
ITEM_TRASH=13
ITEM_CONTAINER=15
ITEM_DRINK_CON=17
ITEM_KEY=18
ITEM_FOOD=19
ITEM_MONEY=20
ITEM_BOAT=22
ITEM_CORPSE_NPC=23
ITEM_CORPSE_PC=24
ITEM_FOUNTAIN=25
ITEM_PILL=26
ITEM_PROTECT=27
ITEM_MAP=28
ITEM_PORTAL=29
ITEM_WARP_STONE=30
ITEM_ROOM_KEY=31
ITEM_GEM=32
ITEM_JEWELRY=33
ITEM_JUKEBOX=34


#Sexes
SEX_NEUTRAL=0
SEX_MALE=1
SEX_FEMALE=2

#Sizes
SIZE_TINY=0
SIZE_SMALL=1
SIZE_MEDIUM=2
SIZE_LARGE=3
SIZE_HUGE=4
SIZE_GIANT=5


#  Target types.
 
TAR_IGNORE=0
TAR_CHAR_OFFENSIVE=1
TAR_CHAR_DEFENSIVE=2
TAR_CHAR_SELF=3
TAR_OBJ_INV=4
TAR_OBJ_CHAR_DEF=5
TAR_OBJ_CHAR_OFF=6

TARGET_CHAR=0
TARGET_OBJ=1
TARGET_ROOM=2
TARGET_NONE=3

#Positions
POS_DEAD=0
POS_MORTAL=1
POS_INCAP=2
POS_STUNNED=3
POS_SLEEPING=4
POS_RESTING=5
POS_SITTING=6
POS_FIGHTING=7
POS_STANDING=8

# TO types for act.

TO_ROOM=0
TO_NOTVICT=1
TO_VICT=2
TO_CHAR=3
TO_ALL=4

DAM_NONE=0
DAM_BASH=1
DAM_PIERCE=2
DAM_SLASH=3
DAM_FIRE=4
DAM_COLD=5
DAM_LIGHTNIN=6
DAM_ACID=7
DAM_POISON=8
DAM_NEGATIVE=9
DAM_HOLY=10
DAM_ENERGY=11
DAM_MENTAL=12
DAM_DISEASE=13
DAM_DROWNING=14
DAM_LIGHT=15
DAM_OTHER=16
DAM_HARM=17
DAM_CHARM=18
DAM_SOUND=19



def IS_SET(flag, bit):
    return flag & bit
def SET_BIT(var, bit):
    return var | bit
def REMOVE_BIT(var, bit):
    return var & ~(bit)

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
W = 1 << 25
Z = 1 << 26
aa = 1 << 27
bb = 1 << 28
cc = 1 << 29
dd = 1 << 30
ee = 1 << 31
ff = 1 << 32
gg = 1 << 33
hh = 1 << 34
ii = 1 << 35
jj = 1 << 36
kk = 1 << 37
ll = 1 << 38
mm = 1 << 39
nn = 1 << 40
oo = 1 << 41
pp = 1 << 42
qq = 1 << 43
rr = 1 << 44
ss = 1 << 45
tt = 1 << 46
uu = 1 << 47
vv = 1 << 48
ww = 1 << 49
xx = 1 << 50
yy = 1 << 51
zz = 1 << 52



#  ACT bits for mobs.
#  Used in #MOBILES.

ACT_IS_NPC=A  # Auto set for mobs    */
ACT_SENTINEL=B #  Stays in one room    */
ACT_SCAVENGER=C  # Picks up objects */
ACT_AGGRESSIVE=F   # Attacks PC's     */
ACT_STAY_AREA=G    # Won't leave area */
ACT_WIMPY=H
ACT_PET=I     # Auto set for pets    */
ACT_TRAIN=J     # Can train PC's   */
ACT_PRACTICE=K     # Can practice PC's    */
ACT_UNDEAD=O 
ACT_CLERIC=Q
ACT_MAGE=R
ACT_THIEF=S
ACT_WARRIOR=T
ACT_NOALIGN=U
ACT_NOPURGE=V
ACT_OUTDOORS=W
ACT_INDOORS=Y
ACT_IS_HEALER=aa
ACT_GAIN=bb
ACT_UPDATE_ALWAYS=cc
ACT_IS_CHANGER=dd

OFF_AREA_ATTACK=A
OFF_BACKSTAB=B
OFF_BASH=C
OFF_BERSERK=D
OFF_DISARM=E
OFF_DODGE=F
OFF_FADE=G
OFF_FAST=H
OFF_KICK=I
OFF_KICK_DIRT=J
OFF_PARRY=K
OFF_RESCUE=L
OFF_TAIL=M
OFF_TRIP=N
OFF_CRUSH=O
ASSIST_ALL=P
ASSIST_ALIGN=Q
ASSIST_RACE=R
ASSIST_PLAYERS=S
ASSIST_GUARD=T
ASSIST_VNUM=U

IMM_SUMMON=A
IMM_CHARM=B
IMM_MAGIC=C
IMM_WEAPON=D
IMM_BASH=E
IMM_PIERCE=F
IMM_SLASH=G
IMM_FIRE=H
IMM_COLD=I
IMM_LIGHTNING=J
IMM_ACID=K
IMM_POISON=L
IMM_NEGATIVE=M
IMM_HOLY=N
IMM_ENERGY=O
IMM_MENTAL=P
IMM_DISEASE=Q
IMM_DROWNING=R
IMM_LIGHT=S
IMM_SOUND=T
IMM_WOOD=X
IMM_SILVER=Y
IMM_IRON=Z
 
# RES bits for mobs */
RES_SUMMON=A
RES_CHARM=B
RES_MAGIC=C
RES_WEAPON=D
RES_BASH=E
RES_PIERCE=F
RES_SLASH=G
RES_FIRE=H
RES_COLD=I
RES_LIGHTNING=J
RES_ACID=K
RES_POISON=L
RES_NEGATIVE=M
RES_HOLY=N
RES_ENERGY=O
RES_MENTAL=P
RES_DISEASE=Q
RES_DROWNING=R
RES_LIGHT=S
RES_SOUND=T
RES_WOOD=X
RES_SILVER=Y
RES_IRON=Z
 
# VULN bits for mobs */
VULN_SUMMON=A
VULN_CHARM=B
VULN_MAGIC=C
VULN_WEAPON=D
VULN_BASH=E
VULN_PIERCE=F
VULN_SLASH=G
VULN_FIRE=H
VULN_COLD=I
VULN_LIGHTNING=J
VULN_ACID=K
VULN_POISON=L
VULN_NEGATIVE=M
VULN_HOLY=N
VULN_ENERGY=O
VULN_MENTAL=P
VULN_DISEASE=Q
VULN_DROWNING=R
VULN_LIGHT=S
VULN_SOUND=T
VULN_WOOD=X
VULN_SILVER=Y
VULN_IRON=Z
 
# body form */
FORM_EDIBLE=A
FORM_POISON=B
FORM_MAGICAL=C
FORM_INSTANT_DECAY=D
FORM_OTHER=E  # defined by material bit */
 
# actual form */
FORM_ANIMAL=G
FORM_SENTIENT=H
FORM_UNDEAD=I
FORM_CONSTRUCT=J
FORM_MIST=K
FORM_INTANGIBLE=L
 
FORM_BIPED=M
FORM_CENTAUR=N
FORM_INSECT=O
FORM_SPIDER=P
FORM_CRUSTACEAN=Q
FORM_WORM=R
FORM_BLOB=S
 
FORM_MAMMAL=V
FORM_BIRD=W
FORM_REPTILE=X
FORM_SNAKE=Y
FORM_DRAGON=Z
FORM_AMPHIBIAN=aa
FORM_FISH=bb
FORM_COLD_BLOOD=cc    
 
# body parts */
PART_HEAD=A
PART_ARMS=B
PART_LEGS=C
PART_HEART=D
PART_BRAINS=E
PART_GUTS=F
PART_HANDS=G
PART_FEET=H
PART_FINGERS=I
PART_EAR=J
PART_EYE=K
PART_LONG_TONGUE=L
PART_EYESTALKS=M
PART_TENTACLES=N
PART_FINS=O
PART_WINGS=P
PART_TAIL=Q
# for combat */
PART_CLAWS=U
PART_FANGS=V
PART_HORNS=W
PART_SCALES=X
PART_TUSKS=Y


# Bits for 'affected_by'.
# Used in #MOBILES.

AFF_BLIND=A
AFF_INVISIBLE=B
AFF_DETECT_EVIL=C
AFF_DETECT_INVIS=D
AFF_DETECT_MAGIC=E
AFF_DETECT_HIDDEN=F
AFF_DETECT_GOOD=G
AFF_SANCTUARY=H
AFF_FAERIE_FIRE=I
AFF_INFRARED=J
AFF_CURSE=K
AFF_UNUSED_FLAG=L # unused */
AFF_POISON=M
AFF_PROTECT_EVIL=N
AFF_PROTECT_GOOD=O
AFF_SNEAK=P
AFF_HIDE=Q
AFF_SLEEP=R
AFF_CHARM=S
AFF_FLYING=T
AFF_PASS_DOOR=U
AFF_HASTE=V
AFF_CALM=W
AFF_PLAGUE=X
AFF_WEAKEN=Y
AFF_DARK_VISION=Z
AFF_BERSERK=aa
AFF_SWIM=bb
AFF_REGENERATION=cc
AFF_SLOW=dd


# Extra flags.
# Used in #OBJECTS.

ITEM_GLOW=A
ITEM_HUM=B
ITEM_DARK=C
ITEM_LOCK=D
ITEM_EVIL=E
ITEM_INVIS=F
ITEM_MAGIC=G
ITEM_NODROP=H
ITEM_BLESS=I
ITEM_ANTI_GOOD=J
ITEM_ANTI_EVIL=K
ITEM_ANTI_NEUTRAL=L
ITEM_NOREMOVE=M
ITEM_INVENTORY=N
ITEM_NOPURGE=O
ITEM_ROT_DEATH=P
ITEM_VIS_DEATH=Q
ITEM_NONMETAL=S
ITEM_NOLOCATE=T
ITEM_MELT_DROP=U
ITEM_HAD_TIMER=V
ITEM_SELL_EXTRACT=W
ITEM_BURN_PROOF=Y
ITEM_NOUNCURSE=Z



# Wear flags.
# Used in #OBJECTS.

ITEM_TAKE=A
ITEM_WEAR_FINGER=B
ITEM_WEAR_NECK=C
ITEM_WEAR_BODY=D
ITEM_WEAR_HEAD=E
ITEM_WEAR_LEGS=F
ITEM_WEAR_FEET=G
ITEM_WEAR_HANDS=H
ITEM_WEAR_ARMS=I
ITEM_WEAR_SHIELD=J
ITEM_WEAR_ABOUT=K
ITEM_WEAR_WAIST=L
ITEM_WEAR_WRIST=M
ITEM_WIELD=N
ITEM_HOLD=O
ITEM_NO_SAC=P
ITEM_WEAR_FLOAT=Q


# weapon types */
WEAPON_FLAMING=A
WEAPON_FROST=B
WEAPON_VAMPIRIC=C
WEAPON_SHARP=D
WEAPON_VORPAL=E
WEAPON_TWO_HANDS=F
WEAPON_SHOCKING=G
WEAPON_POISON=H

# gate flags */
GATE_NORMAL_EXIT=A
GATE_NOCURSE=B
GATE_GOWITH=C
GATE_BUGGY=D
GATE_RANDOM=E

# furniture flags */
STAND_AT=A
STAND_ON=B
STAND_IN=C
SIT_AT=D
SIT_ON=E
SIT_IN=F
REST_AT=G
REST_ON=H
REST_IN=I
SLEEP_AT=J
SLEEP_ON=K
SLEEP_IN=L
PUT_AT=M
PUT_ON=N
PUT_IN=O
PUT_INSIDE=P


# Room flags.
# Used in #ROOMS.

ROOM_DARK=A
ROOM_NO_MOB=C
ROOM_INDOORS=D

ROOM_PRIVATE=J
ROOM_SAFE=K
ROOM_SOLITARY=L
ROOM_PET_SHOP=M
ROOM_NO_RECALL=N
ROOM_IMP_ONLY=O
ROOM_GODS_ONLY=P
ROOM_HEROES_ONLY=Q
ROOM_NEWBIES_ONLY=R
ROOM_LAW=S
ROOM_NOWHERE=T


# Exit flags.
# Used in #ROOMS.

EX_ISDOOR=A
EX_CLOSED=B
EX_LOCKED=C
EX_PICKPROOF=F
EX_NOPASS=G
EX_EASY=H
EX_HARD=I
EX_INFURIATING=J
EX_NOCLOSE=K
EX_NOLOCK=L


# ACT bits for players.

PLR_IS_NPC=A     # Don't EVER set.  */

# RT auto flags */
PLR_AUTOASSIST=C
PLR_AUTOEXIT=D
PLR_AUTOLOOT=E
PLR_AUTOSAC=F
PLR_AUTOGOLD=G
PLR_AUTOSPLIT=H

# RT personal flags */
PLR_HOLYLIGHT=N
PLR_CANLOOT=P
PLR_NOSUMMON=Q
PLR_NOFOLLOW=R
# 2 bits reserved, S-T */

# penalty flags */
PLR_PERMIT=U
PLR_LOG=W
PLR_DENY=X
PLR_FREEZE=Y
PLR_THIEF=Z
PLR_KILLER=aa


# RT comm flags -- may be used on both mobs and chars */
COMM_QUIET=A
COMM_DEAF=B
COMM_NOWIZ=C
COMM_NOAUCTION=D
COMM_NOGOSSIP=E
COMM_NOQUESTION=F
COMM_NOMUSIC=G
COMM_NOCLAN=H
COMM_NOQUOTE=I
COMM_SHOUTSOFF=J

# display flags */
COMM_COMPACT=L
COMM_BRIEF=M
COMM_PROMPT=N
COMM_COMBINE=O
COMM_TELNET_GA=P
COMM_SHOW_AFFECTS=Q
COMM_NOGRATS=R

# penalties */
COMM_NOEMOTE=T
COMM_NOSHOUT=U
COMM_NOTELL=V
COMM_NOCHANNELS=W 
COMM_SNOOP_PROOF=Y
COMM_AFK=Z

# WIZnet flags */
WIZ_ON=A
WIZ_TICKS=B
WIZ_LOGINS=C
WIZ_SITES=D
WIZ_LINKS=E
WIZ_DEATHS=F
WIZ_RESETS=G
WIZ_MOBDEATHS=H
WIZ_FLAGS=I
WIZ_PENALTIES=J
WIZ_SACCING=K
WIZ_LEVELS=L
WIZ_SECURE=M
WIZ_SWITCHES=N
WIZ_SNOOPS=O
WIZ_RESTORE=P
WIZ_LOAD=Q
WIZ_NEWBIE=R
WIZ_PREFIX=S
WIZ_SPAM=T

# memory settings */
MEM_CUSTOMER=A   
MEM_SELLER=B
MEM_HOSTILE=C
MEM_AFRAID=D


#utility functions

def prefix_lookup(dict, arg):
    return {k:v for k,v in dict.iteritems() if k.startswith(arg) }[0]

def mass_replace(str, dict)
    for k,v in dict.iteritems():
        str.replace(k,v)

def PERS(ch, looker):
    if not can_see(looker, ch):
        return "someone"
    if IS_NPC(ch):
        return ch.short_descr
    else:
        return ch.name

def OPERS(looker, obj):
    if not can_see_obj(looker,obj):
        return "something"
    return obj.short_descr

def IS_NPC(ch):
    return IS_SET(ch.act, ACT_IS_NPC)

def IS_IMMORTAL(ch):
     return get_trust(ch) >= LEVEL_IMMORTAL

def IS_HERO(ch):
     return get_trust(ch) >= LEVEL_HERO

def IS_TRUSTED(ch,level):
    return get_trust(ch) >= level

def IS_AFFECTED(ch, bit):
    return IS_SET(ch.affected_by, bit))

def GET_AGE(ch):
    return int((17 + (ch.played + time.time() - ch.logon)/72000))

def IS_GOOD(ch):
    return ch.alignment >= 350

def IS_EVIL(ch):
    return ch.alignment <= -350

def IS_NEUTRAL(ch):
    return not IS_GOOD(ch) and not IS_EVIL(ch)

def IS_AWAKE(ch):
    return ch.position > POS_SLEEPING

def GET_AC(ch,type):
    return (ch.armor[type] + ( dex_app[get_curr_stat(ch,STAT_DEX)].defensive if IS_AWAKE(ch) else 0 ) )

def GET_HITROLL(ch):
    return ((ch.hitroll+str_app[get_curr_stat(ch,STAT_STR)].tohit)

def GET_DAMROLL(ch):
    return ((ch.damroll+str_app[get_curr_stat(ch,STAT_STR)].todam)

def IS_OUTSIDE(ch):
    return not IS_SET( ch.in_room.room_flags, ROOM_INDOORS )

def WAIT_STATE(ch, npulse):
    ch.wait = max(ch.wait, npulse)

def DAZE_STATE(ch, npulse):
    ch.daze = max(ch.daze, npulse)

def get_carry_weight(ch):
    return ch.carry_weight + (ch.silver/10 + (ch.gold * 2 / 5) )


 # Object macros.

def CAN_WEAR(obj, part):
    return IS_SET((obj.wear_flags,  (part))

def IS_OBJ_STAT(obj, stat):
    return IS_SET((obj.extra_flags, (stat))
def IS_WEAPON_STAT(obj,stat):
    return IS_SET((obj.value[4],(stat))
def WEIGHT_MULT(obj):
    return obj.value[4] if obj.item_type is ITEM_CONTAINER else 100

def dice(number, size):
    return sum( [ random.randint(1, size ) for x in range(number) ])

def number_fuzzy(number):
    return random.randint(number-1, number+1)