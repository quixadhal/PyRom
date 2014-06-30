"""
 #**************************************************************************
 *  Original Diku Mud copyright(C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright(C) 1992, 1993 by Michael           *
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

logger = logging.getLogger()

# * Move a char into a room.
import collections
import random

from merc import *
import const
import magic
import fight
import skills
import state_checks
import game_utils
import handler_game
import handler_obj

depth = 0

class MOB_INDEX_DATA:
    def __init__(self):
        self.spec_fun = None
        self.pShop = None
        self.vnum = 0
        self.group = 0
        self.new_format = True
        self.count = 0
        self.killed = 0
        self.player_name = ""
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.act = 0
        self.affected_by = 0
        self.alignment = 0
        self.level = 0
        self.hitroll = 0
        self.hit = [0, 0, 0]
        self.mana = [0, 0, 0]
        self.damage = [0, 0, 0]
        self.ac = [0, 0, 0, 0]
        self.dam_type = 0
        self.off_flags = 0
        self.imm_flags = 0
        self.res_flags = 0
        self.vuln_flags = 0
        self.start_pos = 0
        self.default_pos = 0
        self.sex = 0
        self.race = 0
        self.wealth = 0
        self.form = 0
        self.parts = 0
        self.size = 0
        self.material = ""

    def __repr__(self):
        return "<MobIndex: %s:%s>" % (self.short_descr, self.vnum)


def CH(d):
    return d.original if d.original else d.character

def move_char(ch, door, follow):
    if door < 0 or door > 5:
        logger.error("BUG: Do_move: bad door %d." % door)
        return
    in_room = ch.in_room
    pexit = in_room.exit[door]
    if not pexit or not pexit.to_room or not ch.can_see_room(pexit.to_room):
        ch.send("Alas, you cannot go that way.\n")
        return
    to_room = pexit.to_room
    if state_checks.IS_SET(pexit.exit_info, EX_CLOSED) \
            and (not ch.is_affected(AFF_PASS_DOOR)
                 or state_checks.IS_SET(pexit.exit_info, EX_NOPASS)) \
            and not state_checks.IS_TRUSTED(ch, L7):
        handler_game.act("The $d is closed.", ch, None, pexit.keyword, TO_CHAR)
        return
    if ch.is_affected(AFF_CHARM) \
            and ch.master and in_room == ch.master.in_room:
        ch.send("What?  And leave your beloved master?\n")
        return
    if not ch.is_room_owner(to_room) and to_room.is_private():
        ch.send("That room is private right now.\n")
        return
    if not ch.is_npc():
        for gn, guild in const.guild_table.items():
            for room in guild.guild_rooms:
                if guild != ch.guild and to_room.vnum == room:
                    ch.send("You aren't allowed in there.\n")
                    return
        if in_room.sector_type == SECT_AIR \
                or to_room.sector_type == SECT_AIR:
            if not ch.is_affected(AFF_FLYING) \
                    and not ch.is_immortal():
                ch.send("You can't fly.\n")
                return
        if (in_room.sector_type == SECT_WATER_NOSWIM
             or to_room.sector_type == SECT_WATER_NOSWIM) \
                and not ch.is_affected(AFF_FLYING):
            # Look for a boat.
            boats = [obj for obj in ch.contents if obj.item_type == ITEM_BOAT]
            if not boats and not ch.is_immortal():
                ch.send("You need a boat to go there.\n")
                return
        move = movement_loss[min(SECT_MAX - 1, in_room.sector_type)] + movement_loss[
            min(SECT_MAX - 1, to_room.sector_type)]
        move /= 2  # i.e. the average */
        # conditional effects */
        if ch.is_affected(AFF_FLYING) or ch.is_affected(AFF_HASTE):
            move //= 2
        if ch.is_affected(AFF_SLOW):
            move *= 2
        if ch.move < move:
            ch.send("You are too exhausted.\n")
            return
        state_checks.WAIT_STATE(ch, 1)
        ch.move -= move
    if not ch.is_affected(AFF_SNEAK) and (not ch.is_npc() and ch.invis_level < LEVEL_HERO):
        handler_game.act("$n leaves $T.", ch, None, dir_name[door], TO_ROOM)
    ch.from_room()
    ch.to_room(to_room)
    if not ch.is_affected(AFF_SNEAK) and (not ch.is_npc() and ch.invis_level < LEVEL_HERO):
        handler_game.act("$n has arrived.", ch, None, None, TO_ROOM)
    ch.do_look("auto")
    if in_room == to_room:  # no circular follows */
        return

    for fch in in_room.people[:]:
        if fch.master == ch and fch.is_affected(AFF_CHARM) and fch.position < POS_STANDING:
            fch.do_stand("")

        if fch.master == ch and fch.position == POS_STANDING and fch.can_see_room(to_room):
            if state_checks.IS_SET(ch.in_room.room_flags, ROOM_LAW) \
                    and (fch.is_npc()
                         and fch.act.is_set(ACT_AGGRESSIVE)):
                handler_game.act("You can't bring $N into the city.", ch, None, fch, TO_CHAR)
                handler_game.act("You aren't allowed in the city.", fch, None, None, TO_CHAR)
                continue
            handler_game.act("You follow $N.", fch, None, ch, TO_CHAR)
            move_char(fch, door, True)


def add_follower(ch, master):
    if ch.master:
        logger.error("BUG: Add_follower: non-null master.")
        return
    ch.master = master
    ch.leader = None
    if master.can_see(ch):
        handler_game.act("$n now follows you.", ch, None, master, TO_VICT)
    handler_game.act("You now follow $N.", ch, None, master, TO_CHAR)
    return


# nukes charmed monsters and pets */
def nuke_pets(ch):
    if ch.pet:
        stop_follower(ch.pet)
        if ch.pet.in_room:
            handler_game.act("$N slowly fades away.", ch, None, ch.pet, TO_NOTVICT)
        ch.pet.extract(True)
    ch.pet = None
    return


def die_follower(ch):
    if ch.master:
        if ch.master.pet == ch:
            ch.master.pet = None
        stop_follower(ch)
    ch.leader = None

    for fch in char_list[:]:
        if fch.master == ch:
            stop_follower(fch)
        if fch.leader == ch:
            fch.leader = fch
    return


def stop_follower(ch):
    if not ch.master:
        logger.error("BUG: Stop_follower: null master.")
        return

    if ch.is_affected(AFF_CHARM):
        ch.affected_by.rem_bit(AFF_CHARM)
        ch.affect_strip('charm person')

    if ch.master.can_see(ch) and ch.in_room:
        handler_game.act("$n stops following you.", ch, None, ch.master, TO_VICT)
        handler_game.act("You stop following $N.", ch, None, ch.master, TO_CHAR)
    if ch.master.pet == ch:
        ch.master.pet = None
    ch.master = None
    ch.leader = None
    return

    # * Show a list to a character.


# * Can coalesce duplicated items.
def show_list_to_char(clist, ch, fShort, fShowNothing):
    if not ch.desc:
        return
    objects = collections.OrderedDict()
    for obj in clist:
        if obj.wear_loc == WEAR_NONE and ch.can_see_obj(obj):
            frmt = handler_obj.format_obj_to_char(obj, ch, fShort)
            if frmt not in objects:
                objects[frmt] = 1
            else:
                objects[frmt] += 1

    if not objects and fShowNothing:
        if ch.is_npc() or ch.comm.is_set(COMM_COMBINE):
            ch.send("     ")
        ch.send("Nothing.\n")

        #* Output the formatted list.
    for desc, count in objects.items():
        if ch.is_npc() or ch.comm.is_set(COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\n" % (count, desc))
        else:
            for i in range(count):
                ch.send("     %s\n" % desc)


def show_char_to_char_0(victim, ch):
    buf = ''
    if victim.comm.is_set(COMM_AFK):
        buf += "[AFK] "
    if victim.is_affected( AFF_INVISIBLE):
        buf += "(Invis) "
    if victim.invis_level >= LEVEL_HERO:
        buf += "(Wizi) "
    if victim.is_affected( AFF_HIDE):
        buf += "(Hide) "
    if victim.is_affected( AFF_CHARM):
        buf += "(Charmed) "
    if victim.is_affected( AFF_PASS_DOOR):
        buf += "(Translucent) "
    if victim.is_affected( AFF_FAERIE_FIRE):
        buf += "(Pink Aura) "
    if victim.is_evil() and ch.is_affected(AFF_DETECT_EVIL):
        buf += "(Red Aura) "
    if victim.is_evil() and ch.is_affected(AFF_DETECT_GOOD):
        buf += "(Golden Aura) "
    if victim.is_affected( AFF_SANCTUARY):
        buf += "(White Aura) "
    if not victim.is_npc() and victim.act.is_set(PLR_KILLER):
        buf += "(KILLER) "
    if not victim.is_npc() and victim.act.is_set(PLR_THIEF):
        buf += "(THIEF) "

    if victim.is_npc() and victim.position == victim.start_pos and victim.long_descr:
        buf += victim.long_descr
        ch.send(buf)
        if ch.act.is_set(PLR_OMNI):
            ch.send("(%d)" % victim.pIndexData.vnum)
        return

    buf += state_checks.PERS(victim, ch)
    if not victim.is_npc() and not ch.comm.is_set(COMM_BRIEF) \
            and victim.position == POS_STANDING and not ch.on:
        buf += victim.pcdata.title

    if victim.position == POS_DEAD:
        buf += " is DEAD!!"
    elif victim.position == POS_MORTAL:
        buf += " is mortally wounded."
    elif victim.position == POS_INCAP:
        buf += " is incapacitated."
    elif victim.position == POS_STUNNED:
        buf += " is lying here stunned."
    elif victim.position == POS_SLEEPING:
        if victim.on:
            if state_checks.IS_SET(victim.on.value[2], SLEEP_AT):
                buf += " is sleeping at %s." % victim.on.short_descr
            elif state_checks.IS_SET(victim.on.value[2], SLEEP_ON):
                buf += " is sleeping on %s." % victim.on.short_descr
            else:
                buf += " is sleeping in %s." % victim.on.short_descr
        else:
            buf += " is sleeping here."
    elif victim.position == POS_RESTING:
        if victim.on:
            if state_checks.IS_SET(victim.on.value[2], REST_AT):
                buf += " is resting at %s." % victim.on.short_descr
            elif state_checks.IS_SET(victim.on.value[2], REST_ON):
                buf += " is resting on %s." % victim.on.short_descr
            else:
                buf += " is resting in %s." % victim.on.short_descr
        else:
            buf += " is resting here."
    elif victim.position == POS_SITTING:
        if victim.on:
            if state_checks.IS_SET(victim.on.value[2], SIT_AT):
                buf += " is sitting at %s." % victim.on.short_descr
            elif state_checks.IS_SET(victim.on.value[2], SIT_ON):
                buf += " is sitting on %s." % victim.on.short_descr
            else:
                buf += " is sitting in %s." % victim.on.short_descr
        else:
            buf += " is sitting here."
    elif victim.position == POS_STANDING:
        if victim.on:
            if state_checks.IS_SET(victim.on.value[2], STAND_AT):
                buf += " is standing at %s." % victim.on.short_descr
            elif state_checks.IS_SET(victim.on.value[2], STAND_ON):
                buf += " is standing on %s." % victim.on.short_descr
            else:
                buf += " is standing in %s." % victim.on.short_descr
        else:
            buf += " is here."
    elif victim.position == POS_FIGHTING:
        buf += " is here, fighting "
        if not victim.fighting:
            buf += "thin air??"
        elif victim.fighting == ch:
            buf += "YOU!"
        elif victim.in_room == victim.fighting.in_room:
            buf += "%s." % state_checks.PERS(victim.fighting, ch)
        else:
            buf += "someone who left??"
    buf = buf.capitalize()
    if victim.is_npc() and ch.act.is_set(PLR_OMNI):
        buf += "(%s)" % victim.pIndexData.vnum
    ch.send(buf)
    return


def show_char_to_char_1(victim, ch):
    if victim.can_see(ch):
        if ch == victim:
            handler_game.act("$n looks at $mself.", ch, None, None, TO_ROOM)
        else:
            handler_game.act("$n looks at you.", ch, None, victim, TO_VICT)
            handler_game.act("$n looks at $N.", ch, None, victim, TO_NOTVICT)
    if victim.description:
        ch.send(victim.description + "\n")
    else:
        handler_game.act("You see nothing special about $M.", ch, None, victim, TO_CHAR)
    if victim.max_hit > 0:
        percent = (100 * victim.hit) // victim.max_hit
    else:
        percent = -1
    buf = state_checks.PERS(victim, ch)
    if percent >= 100:
        buf += " is in excellent condition.\n"
    elif percent >= 90:
        buf += " has a few scratches.\n"
    elif percent >= 75:
        buf += " has some small wounds and bruises.\n"
    elif percent >= 50:
        buf += " has quite a few wounds.\n"
    elif percent >= 30:
        buf += " has some big nasty wounds and scratches.\n"
    elif percent >= 15:
        buf += " looks pretty hurt.\n"
    elif percent >= 0:
        buf += " is in awful condition.\n"
    else:
        buf += " is bleeding to death.\n"
    buf = buf.capitalize()
    ch.send(buf)
    found = False
    for iWear in range(MAX_WEAR):
        obj = victim.get_eq(iWear)
        if obj and ch.can_see_obj(obj):
            if not found:
                handler_game.act("$N is using:", ch, None, victim, TO_CHAR)
                found = True
            ch.send(where_name[iWear])
            ch.send(handler_obj.format_obj_to_char(obj, ch, True) + "\n")
    if victim != ch and not ch.is_npc() \
            and random.randint(1, 99) < ch.get_skill("peek"):
        ch.send("\nYou peek at the inventory:\n")
        ch.check_improve( 'peek', True, 4)
        show_list_to_char(victim.contents, ch, True, True)
    return


def show_char_to_char(plist, ch):
    for rch in plist:
        if rch == ch:
            continue
        if ch.trust < rch.invis_level:
            continue
        if ch.can_see(rch):
            show_char_to_char_0(rch, ch)
            ch.send("\n")
        elif ch.in_room.is_dark() and rch.is_affected(AFF_INFRARED):
            ch.send("You see glowing red eyes watching YOU!\n")

