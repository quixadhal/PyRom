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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor (rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor (gtaylor@hypercube.org)			               *
*	    Brian Moore (zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
#Global Classes

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
        return "<%s:%d>" % (self.keyword, self.level)

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
    dam_typ = 0
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

#Global MAXes
MAX_TRADE=5

#Global Constants
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