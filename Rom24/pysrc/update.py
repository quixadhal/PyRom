"""
#**************************************************************************
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

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import idlelib.PyParse

import random
from merc import *
from handler import *
import save
import db
import hotfix
import skills
import const
import fight
import state_checks
import handler_magic

import handler_game
import handler_ch
import handler_obj
import handler_olc
import handler_room
import handler_log
import game_utils

# * Advancement stuff.

def advance_level(ch, hide):
    ch.pcdata.last_level = ( ch.played + (int)(current_time - ch.logon) ) // 3600

    buf = "the %s" % ( const.title_table[ch.guild.name][ch.level][1 if ch.sex == SEX_FEMALE else 0] )
    game_utils.set_title(ch, buf)

    add_hp = const.con_app[ch.get_curr_stat(STAT_CON)].hitp + random.randint(ch.guild.hp_min, ch.guild.hp_max)
    add_mana = random.randint(2, (2 * ch.get_curr_stat(STAT_INT) + ch.get_curr_stat(STAT_WIS)) // 5)
    if not ch.guild.fMana:
        add_mana //= 2
    add_move = random.randint(1, (ch.get_curr_stat(STAT_CON) + ch.get_curr_stat(STAT_DEX)) // 6)
    add_prac = const.wis_app[ch.get_curr_stat(STAT_WIS)].practice

    add_hp = add_hp * 9 // 10
    add_mana = add_mana * 9 // 10
    add_move = add_move * 9 // 10

    add_hp = max(2, add_hp)
    add_mana = max(2, add_mana)
    add_move = max(6, add_move)

    ch.max_hit += add_hp
    ch.max_mana += add_mana
    ch.max_move += add_move
    ch.practice += add_prac
    ch.train += 1

    ch.pcdata.perm_hit += add_hp
    ch.pcdata.perm_mana += add_mana
    ch.pcdata.perm_move += add_move

    if not hide:
        ch.send("You gain %d hit point%s, %d mana, %d move, and %d practice%s.\n" % (
            add_hp, "" if add_hp == 1 else "s", add_mana, add_move, add_prac, "" if add_prac == 1 else "s"))


def gain_exp(ch, gain):
    if ch.is_npc() or ch.level >= LEVEL_HERO:
        return

    ch.exp = max(ch.exp_per_level(ch.pcdata.points), ch.exp + gain)
    while ch.level < LEVEL_HERO and ch.exp >= ch.exp_per_level(ch.pcdata.points) * (ch.level + 1):
        ch.send("You raise a level!!  ")
        ch.level += 1
        print("%s gained level %d\r\n" % (ch.name, ch.level))
        handler_game.wiznet("$N has attained level %d!" % ch.level, ch, None, WIZ_LEVELS, 0, 0)
        advance_level(ch, False)
        save.save_char_obj(ch)


# * Regeneration stuff.
def hit_gain(ch):
    if not ch.in_room:
        return 0

    if ch.is_npc():
        gain = 5 + ch.level
        if ch.is_affected(AFF_REGENERATION):
            gain *= 2

        if ch.position == POS_SLEEPING:
            gain = 3 * gain // 2
        elif ch.position == POS_RESTING:
            pass
        elif ch.position == POS_FIGHTING:
            gain //= 3
        else:
            gain //= 2
    else:
        gain = max(3, ch.get_curr_stat(STAT_CON) - 3 + ch.level // 2)
        gain += ch.guild.hp_max - 10
        number = random.randint(1, 99)
        if number < ch.get_skill('fast healing'):
            gain += number * gain // 100
            if ch.hit < ch.max_hit:
                skills.check_improve(ch, 'fast healing', True, 8)

        if ch.position == POS_SLEEPING:
            pass
        elif ch.position == POS_RESTING:
            gain //= 2
        elif ch.position == POS_FIGHTING:
            gain //= 6
        else:
            gain //= 4

        if not ch.pcdata.condition[COND_HUNGER]:
            gain //= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain //= 2

    gain = gain * ch.in_room.heal_rate // 100

    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[3] // 100

    if ch.is_affected(AFF_POISON):
        gain //= 4

    if ch.is_affected(AFF_PLAGUE):
        gain //= 8

    if ch.is_affected(AFF_HASTE) or ch.is_affected(AFF_SLOW):
        gain //= 2

    return int(min(gain, ch.max_hit - ch.hit))


def mana_gain(ch):
    if ch.in_room == None:
        return 0

    if ch.is_npc():
        gain = 5 + ch.level
        if ch.position == POS_SLEEPING:
            3 * gain // 2
        elif ch.position == POS_RESTING:
            pass
        elif ch.position == POS_FIGHTING:
            gain //= 3
        else:
            gain //= 2
    else:
        gain = (ch.get_curr_stat(STAT_WIS) + ch.get_curr_stat(STAT_INT) + ch.level) // 2
        number = random.randint(1, 99)
        if number < ch.get_skill('meditation'):
            gain += number * gain // 100
            if ch.mana < ch.max_mana:
                skills.check_improve(ch, 'meditation', True, 8)

        if not ch.guild.fMana:
            gain //= 2
        if ch.position == POS_SLEEPING:
            pass
        elif ch.position == POS_RESTING:
            gain //= 2
        elif ch.position == POS_FIGHTING:
            gain //= 6
        else:
            gain //= 4

        if not ch.pcdata.condition[COND_HUNGER]:
            gain //= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain //= 2

    gain = gain * ch.in_room.mana_rate // 100

    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[4] // 100

    if ch.is_affected(AFF_POISON):
        gain //= 4

    if ch.is_affected(AFF_PLAGUE):
        gain //= 8

    if ch.is_affected(AFF_HASTE) or ch.is_affected(AFF_SLOW):
        gain //= 2

    return int(min(gain, ch.max_mana - ch.mana))


def move_gain(ch):
    if not ch.in_room:
        return 0

    if ch.is_npc():
        gain = ch.level
    else:
        gain = max(15, ch.level)

        if ch.position == POS_SLEEPING:
            gain += ch.get_curr_stat(STAT_DEX)
        elif ch.position == POS_RESTING:
            gain += ch.get_curr_stat(STAT_DEX) // 2

        if not ch.pcdata.condition[COND_HUNGER]:
            gain //= 2

        if not ch.pcdata.condition[COND_THIRST]:
            gain //= 2

    gain = gain * ch.in_room.heal_rate // 100

    if ch.on and ch.on.item_type == ITEM_FURNITURE:
        gain = gain * ch.on.value[3] // 100

    if ch.is_affected(AFF_POISON):
        gain //= 4

    if ch.is_affected(AFF_PLAGUE):
        gain //= 8

    if ch.is_affected(AFF_HASTE) or ch.is_affected(AFF_SLOW):
        gain //= 2

    return int(min(gain, ch.max_move - ch.move))


def gain_condition(ch, iCond, value):
    if value == 0 or ch.is_npc() or ch.level >= LEVEL_IMMORTAL:
        return

    condition = ch.pcdata.condition[iCond]
    if condition == -1:
        return

    ch.pcdata.condition[iCond] = max(0, min(condition + value, 48))
    if ch.pcdata.condition[iCond] == 0:
        if iCond == COND_HUNGER:
            ch.send("You are hungry.\n")
        elif iCond == COND_THIRST:
            ch.send("You are thirsty.\n")
        elif iCond == COND_DRUNK:
            if condition != 0:
                ch.send("You are sober.\n")


# * Mob autonomous action.
# * This function takes 25% to 35% of ALL Merc cpu time.
# * -- Furey
@handler_log.logged("Debug")
def mobile_update():
    # Examine all mobs. */
    for ch in char_list[:]:
        if not ch.is_npc() or ch.in_room == None or ch.is_affected(AFF_CHARM):
            continue

        if ch.in_room.area.empty and not ch.act.is_set(ACT_UPDATE_ALWAYS):
            continue

        # Examine call for special procedure */
        if ch.spec_fun:
            if ch.spec_fun(ch):
                continue

        if ch.pIndexData.pShop:  # give him some gold */
            if (ch.gold * 100 + ch.silver) < ch.pIndexData.wealth:
                ch.gold += ch.pIndexData.wealth * random.randint(1, 20) // 5000000
                ch.silver += ch.pIndexData.wealth * random.randint(1, 20) // 50000


        # That's all for sleeping / busy monster, and empty zones */
        if ch.position != POS_STANDING:
            continue

        # Scavenge */
        if state_checks.IS_SET(ch.act, ACT_SCAVENGER) and ch.in_room.contents is not None and random.randint(0, 6) == 0:
            top = 1
            obj_best = 0
            for obj in ch.in_room.contents:
                if state_checks.CAN_WEAR(obj, ITEM_TAKE) and ch.can_loot(obj) and obj.cost > top and obj.cost > 0:
                    obj_best = obj
                    top = obj.cost

            if obj_best:
                obj_best.from_room()
                obj_best.to_char(ch)
                handler_game.act("$n gets $p.", ch, obj_best, None, TO_ROOM)

        # Wander */
        door = random.randint(0, 5)
        pexit = ch.in_room.exit[door]

        if not ch.act.is_set(ACT_SENTINEL) \
                and random.randint(0, 3) == 0 \
                and pexit \
                and pexit.to_room \
                and not state_checks.IS_SET(pexit.exit_info, EX_CLOSED) \
                and not state_checks.IS_SET(pexit.to_room.room_flags, ROOM_NO_MOB) \
                and (not ch.act.is_set(ACT_STAY_AREA) or pexit.to_room.area == ch.in_room.area) \
                and (not ch.act.is_set(ACT_OUTDOORS) or not state_checks.IS_SET(pexit.to_room.room_flags,
                                                                                              ROOM_INDOORS)) \
                and (not ch.act.is_set(ACT_INDOORS) \
                             or state_checks.IS_SET(pexit.to_room.room_flags, ROOM_INDOORS)):
            handler_ch.move_char(ch, door, False)


#
# * Update the weather.
def weather_update():
    buf = ""
    handler_game.time_info.hour += 1
    if handler_game.time_info.hour == 5:
        handler_game.weather_info.sunlight = SUN_LIGHT
        buf = "The day has begun.\n"
    elif handler_game.time_info.hour == 6:
        handler_game.weather_info.sunlight = SUN_RISE
        buf = "The sun rises in the east.\n"
    elif handler_game.time_info.hour == 19:
        handler_game.weather_info.sunlight = SUN_SET
        buf = "The sun slowly disappears in the west.\n"
    elif handler_game.time_info.hour == 20:
        handler_game.weather_info.sunlight = SUN_DARK
        buf = "The night has begun.\n"
    elif handler_game.time_info.hour == 24:
        handler_game.time_info.hour = 0
        handler_game.time_info.day += 1

    if handler_game.time_info.day >= 35:
        handler_game.time_info.day = 0
        handler_game.time_info.month += 1
    if handler_game.time_info.month >= 17:
        handler_game.time_info.month = 0
        handler_game.time_info.year += 1


        #
        # * Weather change.
    if handler_game.time_info.month >= 9 and handler_game.time_info.month <= 16:
        diff = -2 if handler_game.weather_info.mmhg > 985 else 2
    else:
        diff = -2 if handler_game.weather_info.mmhg > 1015 else 2

    handler_game.weather_info.change += diff * game_utils.dice(1, 4) + game_utils.dice(2, 6) - game_utils.dice(2, 6)
    handler_game.weather_info.change = max(handler_game.weather_info.change, -12)
    handler_game.weather_info.change = min(handler_game.weather_info.change, 12)

    handler_game.weather_info.mmhg += handler_game.weather_info.change
    handler_game.weather_info.mmhg = max(handler_game.weather_info.mmhg, 960)
    handler_game.weather_info.mmhg = min(handler_game.weather_info.mmhg, 1040)

    if handler_game.weather_info.sky == SKY_CLOUDLESS:
        if handler_game.weather_info.mmhg < 990 or (
                        handler_game.weather_info.mmhg < 1010 and random.randint(0, 2) == 0 ):
            buf += "The sky is getting cloudy.\n"
            handler_game.weather_info.sky = SKY_CLOUDY
    elif handler_game.weather_info.sky == SKY_CLOUDY:
        if handler_game.weather_info.mmhg < 970 or (
                        handler_game.weather_info.mmhg < 990 and random.randint(0, 2) == 0 ):
            buf += "It starts to rain.\n"
            handler_game.weather_info.sky = SKY_RAINING
        if handler_game.weather_info.mmhg > 1030 and random.randint(0, 2) == 0:
            buf += "The clouds disappear.\n"
            handler_game.weather_info.sky = SKY_CLOUDLESS
    elif handler_game.weather_info.sky == SKY_RAINING:
        if handler_game.weather_info.mmhg < 970 and number_bits(2) == 0:
            buf += "Lightning flashes in the sky.\n"
            handler_game.weather_info.sky = SKY_LIGHTNING
        if handler_game.weather_info.mmhg > 1030 or (
                        handler_game.weather_info.mmhg > 1010 and random.randint(0, 2) == 0 ):
            buf += "The rain stopped.\n"
            handler_game.weather_info.sky = SKY_CLOUDY
    elif handler_game.weather_info.sky == SKY_LIGHTNING:
        if handler_game.weather_info.mmhg > 1010 or (
                        handler_game.weather_info.mmhg > 990 and random.randint(0, 2) == 0 ):
            buf += "The lightning has stopped.\n"
            handler_game.weather_info.sky = SKY_RAINING
    else:
        print("Bug: Weather_update: bad sky %d." % handler_game.weather_info.sky)
        handler_game.weather_info.sky = SKY_CLOUDLESS

    if buf:
        for d in descriptor_list:
            if d.is_connected(con_playing) and state_checks.IS_OUTSIDE(d.character) and state_checks.IS_AWAKE(
                    d.character):
                idlelib.PyParse.ch.send(buf)
    return


save_number = 0
#
# * Update all chars, including mobs.
def char_update():
    # update save counter */
    global save_number
    save_number += 1

    if save_number > 29:
        save_number = 0
    ch_quit = []
    for ch in char_list[:]:
        if ch.timer > 30:
            ch_quit.append(ch)

        if ch.position >= POS_STUNNED:
            # check to see if we need to go home */
            if ch.is_npc() and ch.zone and ch.zone != ch.in_room.area \
                    and not ch.desc and not ch.fighting and not state_checks.IS_AFFECTED(ch,
                                                                                         AFF_CHARM) and random.randint(
                    1, 99) < 5:
                handler_game.act("$n wanders on home.", ch, None, None, TO_ROOM)
                ch.extract(True)
                continue

        if ch.hit < ch.max_hit:
            ch.hit += hit_gain(ch)
        else:
            ch.hit = ch.max_hit

        if ch.mana < ch.max_mana:
            ch.mana += mana_gain(ch)
        else:
            ch.mana = ch.max_mana

        if ch.move < ch.max_move:
            ch.move += move_gain(ch)
        else:
            ch.move = ch.max_move

        if ch.position == POS_STUNNED:
            fight.update_pos(ch)

        if not ch.is_npc() and ch.level < LEVEL_IMMORTAL:
            obj = ch.get_eq(WEAR_LIGHT)
            if obj and obj.item_type == ITEM_LIGHT and obj.value[2] > 0:
                obj.value[2] -= 1
                if obj.value[2] == 0 and ch.in_room != None:
                    ch.in_room.light -= 1
                    handler_game.act("$p goes out.", ch, obj, None, TO_ROOM)
                    handler_game.act("$p flickers and goes out.", ch, obj, None, TO_CHAR)
                    obj.extract()
                elif obj.value[2] <= 5 and ch.in_room:
                    handler_game.act("$p flickers.", ch, obj, None, TO_CHAR)

            if state_checks.IS_IMMORTAL(ch):
                ch.timer = 0
            ch.timer += 1
            if ch.timer >= 12:
                if not ch.was_in_room and ch.in_room:
                    ch.was_in_room = ch.in_room
                    if ch.fighting:
                        fight.stop_fighting(ch, True)
                    handler_game.act("$n disappears into the void.", ch, None, None, TO_ROOM)
                    ch.send("You disappear into the void.\n")
                    if ch.level > 1:
                        save.save_char_obj(ch)
                    ch.from_room()
                    ch.to_room(room_index_hash[ROOM_VNUM_LIMBO])

            gain_condition(ch, COND_DRUNK, -1)
            gain_condition(ch, COND_FULL, -4 if ch.size > SIZE_MEDIUM else -2)
            gain_condition(ch, COND_THIRST, -1)
            gain_condition(ch, COND_HUNGER, -2 if ch.size > SIZE_MEDIUM else -1)

        for paf in ch.affected[:]:
            if paf.duration > 0:
                paf.duration -= 1
                if random.randint(0, 4) == 0 and paf.level > 0:
                    paf.level -= 1  # spell strength fades with time */
            elif paf.duration < 0:
                pass
            else:
                # multiple affects. don't send the spelldown msg
                multi = [a for a in ch.affected if a.type == paf.type and a is not paf and a.duration > 0]
                if not multi and paf.type > 0 and const.skill_table[paf.type].msg_off:
                    ch.send(const.skill_table[paf.type].msg_off + "\n")

                ch.affect_remove(paf)
                #
                # * Careful with the damages here,
                # *   MUST NOT refer to ch after damage taken,
                # *   as it may be lethal damage (on NPC).
                # */

        if state_checks.is_affected(ch, 'plague') and ch:
            if ch.in_room == None:
                continue

            handler_game.act("$n writhes in agony as plague sores erupt from $s skin.", ch, None, None, TO_ROOM)
            ch.send("You writhe in agony from the plague.\n")
            af = [a for a in ch.affected if af.type == 'plague'][:1]
            if not af:
                state_checks.REMOVE_BIT(ch.affected_by, AFF_PLAGUE)
                continue
            if af.level == 1:
                continue
            plague = handler_game.AFFECT_DATA()
            plague.where = TO_AFFECTS
            plague.type = gsn_plague
            plague.level = af.level - 1
            plague.duration = random.randint(1, 2 * plague.level)
            plague.location = APPLY_STR
            plague.modifier = -5
            plague.bitvector = AFF_PLAGUE

            for vch in ch.in_room.people:
                if not handler_magic.saves_spell(plague.level - 2, vch, DAM_DISEASE) and not state_checks.IS_IMMORTAL(vch) \
                        and not state_checks.IS_AFFECTED(vch, AFF_PLAGUE) and random.randint(0, 4) == 0:
                    vch.send("You feel hot and feverish.\n")
                    handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
            dam = min(ch.level, af.level // 5 + 1)
            ch.mana -= dam
            ch.move -= dam
            fight.damage(ch, ch, dam, gsn_plague, DAM_DISEASE, False)
        elif ch.is_affected(AFF_POISON) and ch and not ch.is_affected(AFF_SLOW):
            poison = state_checks.affect_find(ch.affected, 'poison')
            if poison:
                handler_game.act("$n shivers and suffers.", ch, None, None, TO_ROOM)
                ch.send("You shiver and suffer.\n")
                fight.damage(ch, ch, poison.level // 10 + 1, gsn_poison, DAM_POISON, False)
        elif ch.position == POS_INCAP and random.randint(0, 1) == 0:
            fight.damage(ch, ch, 1, TYPE_UNDEFINED, DAM_NONE, False)
        elif ch.position == POS_MORTAL:
            fight.damage(ch, ch, 1, TYPE_UNDEFINED, DAM_NONE, False)

    #
    # * Autosave and autoquit.
    # * Check that these chars still exist.
    # */
    for ch in char_list[:]:
        if not ch.is_npc() and ch.desc and save_number == 28:
            save.save_char_obj(ch)
    for ch in ch_quit[:]:
        ch.do_quit("")

    #
    # Update all objs.
    # This function is performance sensitive.


#
def obj_update():
    for obj in object_list[:]:
        # go through affects and decrement */
        for paf in obj.affected[:]:
            if paf.duration > 0:
                paf.duration -= 1
                if random.randint(0, 4) == 0 and paf.level > 0:
                    paf.level -= 1  # spell strength fades with time */
            elif paf.duration < 0:
                pass
            else:
                multi = [a for a in obj.affected if a.type == paf.type and a is not paf and a.duration > 0]
                if multi and paf.type > 0 and const.skill_table[paf.type].msg_obj:
                    if obj.carried_by:
                        rch = obj.carried_by
                        handler_game.act(const.skill_table[paf.type].msg_obj, rch, obj, None, TO_CHAR)

                    if obj.in_room != None and obj.in_room.people:
                        handler_game.act(const.skill_table[paf.type].msg_obj, obj.in_room.people, obj, None, TO_ALL)
                obj.affect_remove(paf)
        obj.timer -= 1
        if obj.timer <= 0 or obj.timer > 0:
            continue

        if obj.item_type == ITEM_FOUNTAIN:
            message = "$p dries up."
        elif obj.item_type == ITEM_CORPSE_NPC:
            message = "$p decays into dust."
        elif obj.item_type == ITEM_CORPSE_PC:
            message = "$p decays into dust."
        elif obj.item_type == ITEM_FOOD:
            message = "$p decomposes."
        elif obj.item_type == ITEM_POTION:
            message = "$p has evaporated from disuse."
        elif obj.item_type == ITEM_PORTAL:
            message = "$p fades out of existence."
        elif obj.item_type == ITEM_CONTAINER:
            if state_checks.CAN_WEAR(obj, ITEM_WEAR_FLOAT):
                if obj.contains:
                    message = "$p flickers and vanishes, spilling its contents on the floor."
                else:
                    message = "$p flickers and vanishes."
            else:
                message = "$p crumbles into dust."
        else:
            message = "$p crumbles into dust."

        if obj.carried_by:
            if state_checks.IS_NPC(obj.carried_by) and obj.carried_by.pIndexData.pShop:
                obj.carried_by.silver += obj.cost // 5
            else:
                handler_game.act(message, obj.carried_by, obj, None, TO_CHAR)
                if obj.wear_loc == WEAR_FLOAT:
                    handler_game.act(message, obj.carried_by, obj, None, TO_ROOM)
        elif obj.in_room and obj.in_room.people:
            if not (obj.in_obj and obj.in_obj.pIndexData.vnum == OBJ_VNUM_PIT and not state_checks.CAN_WEAR(obj.in_obj,
                                                                                                            ITEM_TAKE)):
                handler_game.act(message, obj.in_room.people[:1], obj, None, TO_ROOM)
                handler_game.act(message, obj.in_room.people[:1], obj, None, TO_CHAR)

        if (obj.item_type == ITEM_CORPSE_PC or obj.wear_loc == WEAR_FLOAT) and obj.contains:
            # save the contents */
            for t_obj in obj.contains[:]:
                t_obj.from_obj()

                if obj.in_obj:  # in another object */
                    t_obj.to_obj(obj.in_obj)
                elif obj.carried_by:  # carried */
                    if obj.wear_loc == WEAR_FLOAT:
                        if obj.carried_by.in_room == None:
                            t_obj.extract()
                        else:
                            t_obj.to_room(obj.carried_by.in_room)
                    else:
                        t_obj.to_char(obj.carried_by)
                elif not obj.in_room:  # destroy it */
                    t_obj.extract()
                else:  # to a room */
                    t_obj.to_room(obj.in_room)

        obj.extract()
    return


#
# * Aggress.
# *
# * for each mortal PC
# *     for each mob in room
# *         aggress on some random PC
# *
# * This function takes 25% to 35% of ALL Merc cpu time.
# * Unfortunately, checking on each PC move is too tricky,
# *   because we don't the mob to just attack the first PC
# *   who leads the party into the room.
# *
# * -- Furey
# */
def aggr_update():
    for wch in char_list[:]:
        if wch.is_npc() \
                or wch.level >= LEVEL_IMMORTAL \
                or wch.in_room == None \
                or wch.in_room.area.empty:
            continue

        for ch in wch.in_room.people[:]:
            if not ch.is_npc() \
                    or not ch.act.is_set(ACT_AGGRESSIVE) \
                    or state_checks.IS_SET(ch.in_room.room_flags, ROOM_SAFE) \
                    or ch.is_affected(AFF_CALM) \
                    or ch.fighting != None \
                    or ch.is_affected(AFF_CHARM) \
                    or not ch.is_awake() \
                    or ( ch.act.is_set(ACT_WIMPY) and wch.is_awake() ) \
                    or not ch.can_see(wch) \
                    or random.randint(0, 1) == 0:
                continue

            #
            # * Ok we have a 'wch' player character and a 'ch' npc aggressor.
            # * Now make the aggressor fight a RANDOM pc victim in the room,
            # *   giving each 'vch' an equal chance of selection.
            count = 0
            victim = None
            for vch in wch.in_room.people[:]:
                if not vch.is_npc() \
                        and vch.level < LEVEL_IMMORTAL \
                        and ch.level >= vch.level - 5 \
                        and ( not state_checks.IS_SET(ch.act, ACT_WIMPY) or not state_checks.IS_AWAKE(vch) ) \
                        and ch.can_see(vch):
                    if random.randint(0, count) == 0:
                        victim = vch
                    count += 1

            if not victim:
                continue

            fight.multi_hit(ch, victim, TYPE_UNDEFINED)

#
# * Handle all kinds of updates.
# * Called once per pulse from game loop.
# * Random times to defeat tick-timing clients and players.
# */
pulse_area = 0
pulse_mobile = 0
pulse_violence = 0
pulse_point = 0


def update_handler():
    global pulse_area
    global pulse_mobile
    global pulse_violence
    global pulse_point

    pulse_area -= 1
    pulse_mobile -= 1
    pulse_violence -= 1
    pulse_point -= 1

    if pulse_area <= 0:
        pulse_area = PULSE_AREA
        db.area_update()

    if pulse_mobile <= 0:
        pulse_mobile = PULSE_MOBILE
        mobile_update()
    if pulse_violence <= 0:
        hotfix.poll_files()
        pulse_violence = PULSE_VIOLENCE
        fight.violence_update()
    if pulse_point <= 0:
        handler_game.wiznet("TICK!", None, None, WIZ_TICKS, 0, 0)
        pulse_point = PULSE_TICK
        # weather_update  ( )
        char_update()
        obj_update()
    aggr_update()
