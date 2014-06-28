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
# * Move a char into a room.
import collections
import random
from handler_obj import format_obj_to_char
from merc import *
import const
import magic
import fight
from skills import check_improve
import state_checks
import game_utils
import handler_game

depth = 0

#Global Classes
class CHAR_DATA(object):
    def __init__(self):
        from const import race_table
        from tables import clan_table
        self.master = None
        self.leader = None
        self.fighting = None
        self.reply = None
        self.pet = None
        self.memory = None
        self.spec_fun = None
        self.pIndexData = None
        self.desc = None
        self.affected = []
        self.pnote = None
        self.carrying = []
        self.on = None
        self.in_room = None
        self.was_in_room = None
        self.zone = None
        self.pcdata = None
        self.gen_data = None
        self.valid = False
        self.name = ""
        self.id = 0
        self.version = 5
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.prompt = "<%hhp %mm %vmv>"
        self.prefix = ""
        self.group = 0
        self.clan = clan_table[""]
        self.sex = 0
        self.guild = 0
        self.race = 0
        self.level = 0
        self.trust = 0
        self.played = 0
        self.lines = 22
        self.logon = 0
        self.timer = 0
        self.wait = 0
        self.daze = 0
        self.hit = 20
        self.max_hit = 20
        self.mana = 100
        self.max_mana = 100
        self.move = 100
        self.max_move = 100
        self.gold = 0
        self.silver =0
        self.exp = 0
        self.act = 0
        self.comm = 0
        self.wiznet = 0
        self.imm_flags = 0
        self.res_flags = 0
        self.vuln_flags = 0
        self.invis_level = 0
        self.incog_level = 0
        self.affected_by = 0
        self.position = 0
        self.practice = 0
        self.train = 0
        self.carry_weight = 0
        self.carry_number = 0
        self.saving_throw = 0
        self.alignment = 0
        self.hitroll = 0
        self.damroll = 0
        self.armor = [100, 100, 100, 100]
        self.wimpy = 0
    # stats */
        self.perm_stat = [13 for x in range(MAX_STATS)]
        self.mod_stat = [0 for x in range(MAX_STATS)]
    # parts stuff */
        self.form = 0
        self.parts = 0
        self.size = 0
        self.material = ""
    # mobile stuff */
        self.off_flags = 0
        self.damage = [0, 0, 0]
        self.dam_type = 17
        self.start_pos = 0
        self.default_pos = 0
        self.race = race_table['human']
        self.act = PLR_NOSUMMON
        self.comm = COMM_COMBINE | COMM_PROMPT

    def __repr__(self):
        return self.name

    def send(self, cstr):
        pass


class PC_DATA:
    def __init__(self):
        self.buffer = None
        self.valid = False
        self.pwd = ""
        self.bamfin = ""
        self.bamfout = ""
        self.title = ""
        self.last_note = 0
        self.last_idea = 0
        self.last_penalty = 0
        self.last_news = 0
        self.last_changes = 0
        self.perm_hit = 0
        self.perm_mana = 0
        self.perm_move = 0
        self.true_sex = 0
        self.last_level = 0
        self.condition = [48, 48, 48, 0]
        self.learned = {}
        self.group_known = {}
        self.points = 0
        self.confirm_delete = False
        self.alias = {}


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
        return "<MobIndex: %s:%s>" % ( self.short_descr, self.vnum )

def CH(d):
    return d.original if d.original else d.character


class handler_ch:
    def to_room(ch, pRoomIndex):
        if not pRoomIndex:
            print("Char_to_room: None.")
            room = room_index_hash[ROOM_VNUM_TEMPLE]
            ch.to_room(room)
            return

        ch.in_room = pRoomIndex
        pRoomIndex.people.append(ch)

        if not state_checks.IS_NPC(ch):
            if ch.in_room.area.empty:
                ch.in_room.area.empty = False
                ch.in_room.area.age = 0

            ch.in_room.area.nplayer += 1

        obj = ch.get_eq(WEAR_LIGHT)

        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            ch.in_room.light += 1

        if state_checks.IS_AFFECTED(ch, AFF_PLAGUE):
            af = [af for af in ch.affected if af.type == 'plague']
            if not af:
                state_checks.REMOVE_BIT(ch.affected_by, AFF_PLAGUE)
                return
            af = af[0]

            if af.level == 1:
                return
            plague = handler_game.AFFECT_DATA()
            plague.where = TO_AFFECTS
            plague.type = "plague"
            plague.level = af.level - 1
            plague.duration = random.randint(1, 2 * plague.level)
            plague.location = APPLY_STR
            plague.modifier = -5
            plague.bitvector = AFF_PLAGUE

            for vch in ch.in_room.people[:]:
                if not magic.saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not state_checks.IS_IMMORTAL(vch) and not state_checks.IS_AFFECTED(vch, AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return

    #
    # * Give an affect to a char.
    def affect_add(ch, paf):
        paf_new = handler_game.AFFECT_DATA()
        paf_new.__dict__ = paf.__dict__.copy()
        ch.affected.append(paf_new)
        ch.affect_modify(paf_new, True)
        return

    #
    # * Apply or remove an affect to a character.
    def affect_modify(ch, paf, fAdd):
        mod = paf.modifier
        if fAdd:
            if paf.where == TO_AFFECTS:
                state_checks.SET_BIT(ch.affected_by, paf.bitvector)
            elif paf.where == TO_IMMUNE:
                state_checks.SET_BIT(ch.imm_flags, paf.bitvector)
            elif paf.where == TO_RESIST:
                state_checks.SET_BIT(ch.res_flags, paf.bitvector)
            elif paf.where == TO_VULN:
                state_checks.SET_BIT(ch.vuln_flags, paf.bitvector)
        else:
            if paf.where == TO_AFFECTS:
                state_checks.REMOVE_BIT(ch.affected_by, paf.bitvector)
            elif paf.where == TO_IMMUNE:
                state_checks.REMOVE_BIT(ch.imm_flags, paf.bitvector)
            elif paf.where == TO_RESIST:
                state_checks.REMOVE_BIT(ch.res_flags, paf.bitvector)
            elif paf.where == TO_VULN:
                state_checks.REMOVE_BIT(ch.vuln_flags, paf.bitvector)
            mod = 0 - mod

        if paf.location == APPLY_NONE:
            pass
        elif paf.location == APPLY_STR:
            ch.mod_stat[STAT_STR] += mod
        elif paf.location == APPLY_DEX:
            ch.mod_stat[STAT_DEX] += mod
        elif paf.location == APPLY_INT:
            ch.mod_stat[STAT_INT] += mod
        elif paf.location == APPLY_WIS:
            ch.mod_stat[STAT_WIS] += mod
        elif paf.location == APPLY_CON:
            ch.mod_stat[STAT_CON] += mod
        elif paf.location == APPLY_SEX:
            ch.sex += mod
        elif paf.location == APPLY_CLASS:
            pass
        elif paf.location == APPLY_LEVEL:
            pass
        elif paf.location == APPLY_AGE:
            pass
        elif paf.location == APPLY_HEIGHT:
            pass
        elif paf.location == APPLY_WEIGHT:
            pass
        elif paf.location == APPLY_MANA:
            ch.max_mana += mod
        elif paf.location == APPLY_HIT:
            ch.max_hit += mod
        elif paf.location == APPLY_MOVE:
            ch.max_move += mod
        elif paf.location == APPLY_GOLD:
            pass
        elif paf.location == APPLY_EXP:
            pass
        elif paf.location == APPLY_AC:
            for i in range(4):
                ch.armor[i] += mod
        elif paf.location == APPLY_HITROLL:
            ch.hitroll += mod
        elif paf.location == APPLY_DAMROLL:
            ch.damroll += mod
        elif paf.location == APPLY_SAVES:
            ch.saving_throw += mod
        elif paf.location == APPLY_SAVING_ROD:
            ch.saving_throw += mod
        elif paf.location == APPLY_SAVING_PETRI:
            ch.saving_throw += mod
        elif paf.location == APPLY_SAVING_BREATH:
            ch.saving_throw += mod
        elif paf.location == APPLY_SAVING_SPELL:
            ch.saving_throw += mod
        elif paf.location == APPLY_SPELL_AFFECT:
            pass
        else:
            print("Affect_modify: unknown location %d." % paf.location)
            return
        #
        # * Check for weapon wielding.
        # * Guard against recursion (for weapons with affects).
        wield = ch.get_eq(WEAR_WIELD)
        if not state_checks.IS_NPC(ch) and wield and wield.get_weight() > (const.str_app[ch.get_curr_stat(STAT_STR)].wield * 10):
            global depth

            if depth == 0:
                depth += 1
                handler_game.act("You drop $p.", ch, wield, None, TO_CHAR)
                handler_game.act("$n drops $p.", ch, wield, None, TO_ROOM)
                wield.from_char()
                wield.to_room(ch.in_room)
                depth -= 1
        return

    def check_immune(ch, dam_type):
        immune = -1
        defence = IS_NORMAL

        if dam_type is DAM_NONE:
            return immune

        if dam_type <= 3:
            if state_checks.IS_SET(ch.imm_flags, IMM_WEAPON):
                defence = IS_IMMUNE
            elif state_checks.IS_SET(ch.res_flags, RES_WEAPON):
                defence = IS_RESISTANT
            elif state_checks.IS_SET(ch.vuln_flags, VULN_WEAPON):
                defence = IS_VULNERABLE
        else:  # magical attack */
            if state_checks.IS_SET(ch.imm_flags, IMM_MAGIC):
                defence = IS_IMMUNE
            elif state_checks.IS_SET(ch.res_flags, RES_MAGIC):
                defence = IS_RESISTANT
            elif state_checks.IS_SET(ch.vuln_flags, VULN_MAGIC):
                defence = IS_VULNERABLE

        bit = {DAM_BASH: IMM_BASH,
               DAM_PIERCE: IMM_PIERCE,
               DAM_SLASH: IMM_SLASH,
               DAM_FIRE: IMM_FIRE,
               DAM_COLD: IMM_COLD,
               DAM_LIGHTNING: IMM_LIGHTNING,
               DAM_ACID: IMM_ACID,
               DAM_POISON: IMM_POISON,
               DAM_NEGATIVE: IMM_NEGATIVE,
               DAM_HOLY: IMM_HOLY,
               DAM_ENERGY: IMM_ENERGY,
               DAM_MENTAL: IMM_MENTAL,
               DAM_DISEASE: IMM_DISEASE,
               DAM_DROWNING: IMM_DROWNING,
               DAM_LIGHT: IMM_LIGHT,
               DAM_CHARM: IMM_CHARM,
               DAM_SOUND: IMM_SOUND}
        if dam_type not in bit:
            return defence
        bit = bit[dam_type]

        if state_checks.IS_SET(ch.imm_flags, bit):
            immune = IS_IMMUNE
        elif state_checks.IS_SET(ch.res_flags, bit) and immune is not IS_IMMUNE:
            immune = IS_RESISTANT
        elif state_checks.IS_SET(ch.vuln_flags, bit):
            if immune == IS_IMMUNE:
                immune = IS_RESISTANT
            elif immune == IS_RESISTANT:
                immune = IS_NORMAL
        else:
            immune = IS_VULNERABLE

        if immune == -1:
            return defence
        else:
            return immune

            # * Retrieve a character's trusted level for permission checking.

    def get_trust(ch):
        if ch.desc and ch.desc.original:
            ch = ch.desc.original

        if ch.trust:
            return ch.trust

        if state_checks.IS_NPC(ch) and ch.level >= LEVEL_HERO:
            return LEVEL_HERO - 1
        else:
            return ch.level

    # used to de-screw characters */
    def reset(ch):
        if state_checks.IS_NPC(ch):
            return

        if ch.pcdata.perm_hit == 0 \
                or ch.pcdata.perm_mana == 0 \
                or ch.pcdata.perm_move == 0 \
                or ch.pcdata.last_level == 0:
            # do a FULL reset */
            for loc in range(MAX_WEAR):
                obj = ch.get_eq(loc)
                if not obj:
                    continue
                affected = obj.affected
                if not obj.enchanted:
                    affected.extend(obj.pIndexData.affected)
                for af in affected:
                    mod = af.modifier
                    if af.location == APPLY_SEX:
                        ch.sex -= mod
                        if ch.sex < 0 or ch.sex > 2:
                            ch.sex = 0 if state_checks.IS_NPC(ch) else ch.pcdata.true_sex
                    elif af.location == APPLY_MANA:
                        ch.max_mana -= mod
                    elif af.location == APPLY_HIT:
                        ch.max_hit -= mod
                    elif af.location == APPLY_MOVE:
                        ch.max_move -= mod
            # now reset the permanent stats */
            ch.pcdata.perm_hit = ch.max_hit
            ch.pcdata.perm_mana = ch.max_mana
            ch.pcdata.perm_move = ch.max_move
            ch.pcdata.last_level = ch.played / 3600
            if ch.pcdata.true_sex < 0 or ch.pcdata.true_sex > 2:
                if 0 < ch.sex < 3:
                    ch.pcdata.true_sex = ch.sex
                else:
                    ch.pcdata.true_sex = 0

        # now restore the character to his/her true condition */
        for stat in range(MAX_STATS):
            ch.mod_stat[stat] = 0

        if ch.pcdata.true_sex < 0 or ch.pcdata.true_sex > 2:
            ch.pcdata.true_sex = 0
        ch.sex = ch.pcdata.true_sex
        ch.max_hit = ch.pcdata.perm_hit
        ch.max_mana = ch.pcdata.perm_mana
        ch.max_move = ch.pcdata.perm_move

        for i in range(4):
            ch.armor[i] = 100

        ch.hitroll = 0
        ch.damroll = 0
        ch.saving_throw = 0

        # now start adding back the effects */
        for loc in range(MAX_WEAR):
            obj = ch.get_eq(loc)
            if not obj:
                continue
            for i in range(4):
                ch.armor[i] -= obj.apply_ac(loc, i)
            affected = obj.affected
            if not obj.enchanted:
                affected.extend(obj.pIndexData.affected)

            for af in affected:
                mod = af.modifier
                if af.location == APPLY_STR:
                    ch.mod_stat[STAT_STR] += mod
                elif af.location == APPLY_DEX:
                    ch.mod_stat[STAT_DEX] += mod
                elif af.location == APPLY_INT:
                    ch.mod_stat[STAT_INT] += mod
                elif af.location == APPLY_WIS:
                    ch.mod_stat[STAT_WIS] += mod
                elif af.location == APPLY_CON:
                    ch.mod_stat[STAT_CON] += mod
                elif af.location == APPLY_SEX:
                    ch.sex += mod
                elif af.location == APPLY_MANA:
                    ch.max_mana += mod
                elif af.location == APPLY_HIT:
                    ch.max_hit += mod
                elif af.location == APPLY_MOVE:
                    ch.max_move += mod
                elif af.location == APPLY_AC:
                    ch.armor = [i + mod for i in ch.armor]
                elif af.location == APPLY_HITROLL:
                    ch.hitroll += mod
                elif af.location == APPLY_DAMROLL:
                    ch.damroll += mod
                elif af.location == APPLY_SAVES:
                    ch.saving_throw += mod
                elif af.location == APPLY_SAVING_ROD:
                    ch.saving_throw += mod
                elif af.location == APPLY_SAVING_PETRI:
                    ch.saving_throw += mod
                elif af.location == APPLY_SAVING_BREATH:
                    ch.saving_throw += mod
                elif af.location == APPLY_SAVING_SPELL:
                    ch.saving_throw += mod

        # now add back spell effects */
        for af in ch.affected:
            mod = af.modifier
            if af.location == APPLY_STR:
                ch.mod_stat[STAT_STR] += mod
            elif af.location == APPLY_DEX:
                ch.mod_stat[STAT_DEX] += mod
            elif af.location == APPLY_INT:
                ch.mod_stat[STAT_INT] += mod
            elif af.location == APPLY_WIS:
                ch.mod_stat[STAT_WIS] += mod
            elif af.location == APPLY_CON:
                ch.mod_stat[STAT_CON] += mod
            elif af.location == APPLY_SEX:
                ch.sex += mod
            elif af.location == APPLY_MANA:
                ch.max_mana += mod
            elif af.location == APPLY_HIT:
                ch.max_hit += mod
            elif af.location == APPLY_MOVE:
                ch.max_move += mod
            elif af.location == APPLY_AC:
                ch.armor = [i + mod for i in ch.armor]
            elif af.location == APPLY_HITROLL:
                ch.hitroll += mod
            elif af.location == APPLY_DAMROLL:
                ch.damroll += mod
            elif af.location == APPLY_SAVES:
                ch.saving_throw += mod
            elif af.location == APPLY_SAVING_ROD:
                ch.saving_throw += mod
            elif af.location == APPLY_SAVING_PETRI:
                ch.saving_throw += mod
            elif af.location == APPLY_SAVING_BREATH:
                ch.saving_throw += mod
            elif af.location == APPLY_SAVING_SPELL:
                ch.saving_throw += mod
        # make sure sex is RIGHT!!!! */
        if ch.sex < 0 or ch.sex > 2:
            ch.sex = ch.pcdata.true_sex

    # Find a piece of eq on a character.
    def get_eq(ch, iWear):
        if not ch:
            return None
        objs = [obj for obj in ch.carrying if obj.wear_loc == iWear]
        if not objs:
            return None
        return objs[0]

    # * Equip a char with an obj.
    def equip(ch, obj, iWear):
        if ch.get_eq(iWear):
            print("Equip_char: already equipped (%d)." % iWear)
            return

        if (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_EVIL) and state_checks.IS_EVIL(ch)) \
                or (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_GOOD) and state_checks.IS_GOOD(ch)) \
                or (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) and state_checks.IS_NEUTRAL(ch)):
            # Thanks to Morgenes for the bug fix here!
            handler_game.act("You are zapped by $p and drop it.", ch, obj, None, TO_CHAR)
            handler_game.act("$n is zapped by $p and drops it.", ch, obj, None, TO_ROOM)
            obj.from_char()
            obj.to_room(ch.in_room)
            return

        for i in range(4):
            ch.armor[i] -= obj.apply_ac(iWear, i)
        obj.wear_loc = iWear

        if not obj.enchanted:
            for paf in obj.pIndexData.affected:
                if paf.location != APPLY_SPELL_AFFECT:
                    ch.affect_modify(paf, True)

        for paf in obj.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                ch.affect_add(ch, paf)
            else:
                ch.affect_modify(paf, True)

        if obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and ch.in_room is not None:
            ch.in_room.light += 1
        return


    #
    # * Unequip a char with an obj.
    def unequip(ch, obj):
        if obj.wear_loc == WEAR_NONE:
            print("Unequip_char: already unequipped.")
            return

        for i in range(4):
            ch.armor[i] += obj.apply_ac(obj.wear_loc, i)
        obj.wear_loc = -1

        if not obj.enchanted:
            for paf in obj.pIndexData.affected:
                if paf.location == APPLY_SPELL_AFFECT:
                    for lpaf in ch.affected[:]:
                        if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                            ch.affect_remove(lpaf)
                            break
                else:
                    ch.affect_modify(paf, False)
                    ch.affect_check(paf.where, paf.bitvector)

        for paf in obj.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                print("Bug: Norm-Apply")
                for lpaf in ch.affected:
                    if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                        print("bug: location = %d" % lpaf.location)
                        print("bug: type = %d" % lpaf.type)
                        ch.affect_remove(lpaf)
                        break
            else:
                ch.affect_modify(paf, False)
                ch.affect_check(paf.where, paf.bitvector)

        if obj.item_type == ITEM_LIGHT \
                and obj.value[2] != 0 \
                and ch.in_room \
                and ch.in_room.light > 0:
            ch.in_room.light -= 1
        return

    # fix object affects when removing one */
    def affect_check(ch, where, vector):
        if where == TO_OBJECT or where == TO_WEAPON or vector == 0:
            return

        for paf in ch.affected:
            if paf.where == where and paf.bitvector == vector:
                if where == TO_AFFECTS:
                    state_checks.SET_BIT(ch.affected_by, vector)
                elif where == TO_IMMUNE:
                    state_checks.SET_BIT(ch.imm_flags, vector)
                elif where == TO_RESIST:
                    state_checks.SET_BIT(ch.res_flags, vector)
                elif where == TO_VULN:
                    state_checks.SET_BIT(ch.vuln_flags, vector)
                return

        for obj in ch.carrying:
            if obj.wear_loc == -1:
                continue
            for paf in obj.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        state_checks.SET_BIT(ch.affected_by, vector)
                    elif where == TO_IMMUNE:
                        state_checks.SET_BIT(ch.imm_flags, vector)
                    elif where == TO_RESIST:
                        state_checks.SET_BIT(ch.res_flags, vector)
                    elif where == TO_VULN:
                        state_checks.SET_BIT(ch.vuln_flags, vector)
                    return
            if obj.enchanted:
                continue
            for paf in obj.pIndexData.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        state_checks.SET_BIT(ch.affected_by, vector)
                    elif where == TO_IMMUNE:
                        state_checks.SET_BIT(ch.imm_flags, vector)
                    elif where == TO_RESIST:
                        state_checks.SET_BIT(ch.res_flags, vector)
                    elif where == TO_VULN:
                        state_checks.SET_BIT(ch.vuln_flags, vector)
                    return

    # * Remove an affect from a char.
    def affect_remove(ch, paf):
        if not ch.affected:
            print("BUG: Affect_remove: no affect.")
            return

        ch.affect_modify(paf, False)
        where = paf.where
        vector = paf.bitvector

        if paf not in ch.affected:
            print("Affect_remove: cannot find paf.")
            return
        ch.affected.remove(paf)
        del paf
        ch.affect_check(where, vector)
        return

    # * Strip all affects of a given sn.
    def affect_strip(ch, sn):
        [ch.affect_remove(paf) for paf in ch.affected[:] if paf.type == sn]
        return

    #
    # * Add or enhance an affect.
    def affect_join(ch, paf):
        for paf_old in ch.affected:
            if paf_old.type == paf.type:
                paf.level = (paf.level + paf_old.level) / 2
                paf.duration += paf_old.duration
                paf.modifier += paf_old.modifier
                ch.affect_remove(paf_old)
                break

        ch.affect_add(paf)
        return

    # * Move a char out of a room.
    def from_room(ch):
        if not ch.in_room:
            print("BUG: Char_from_room: None.")
            return

        if not state_checks.IS_NPC(ch):
            ch.in_room.area.nplayer -= 1
        obj = ch.get_eq(WEAR_LIGHT)
        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and ch.in_room.light > 0:
            ch.in_room.light -= 1

        if ch not in ch.in_room.people:
            print("BUG: Char_from_room: ch not found.")
            return
        ch.in_room.people.remove(ch)
        ch.in_room = None
        ch.on = None  # sanity check! */
        return

    # * Move a char into a room.
    def to_room(ch, pRoomIndex):
        if not pRoomIndex:
            print("Char_to_room: None.")
            room = room_index_hash[ROOM_VNUM_TEMPLE]
            ch.to_room(room)
            return

        ch.in_room = pRoomIndex
        pRoomIndex.people.append(ch)

        if not state_checks.IS_NPC(ch):
            if ch.in_room.area.empty:
                ch.in_room.area.empty = False
                ch.in_room.area.age = 0

            ch.in_room.area.nplayer += 1

        obj = ch.get_eq(WEAR_LIGHT)

        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            ch.in_room.light += 1

        if state_checks.IS_AFFECTED(ch, AFF_PLAGUE):
            af = [af for af in ch.affected if af.type == 'plague']
            if not af:
                state_checks.REMOVE_BIT(ch.affected_by, AFF_PLAGUE)
                return
            af = af[0]

            if af.level == 1:
                return
            plague = handler_game.AFFECT_DATA()
            plague.where = TO_AFFECTS
            plague.type = "plague"
            plague.level = af.level - 1
            plague.duration = random.randint(1, 2 * plague.level)
            plague.location = APPLY_STR
            plague.modifier = -5
            plague.bitvector = AFF_PLAGUE

            for vch in ch.in_room.people[:]:
                if not magic.saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not state_checks.IS_IMMORTAL(vch) \
                        and not state_checks.IS_AFFECTED(vch, AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return

    # * Extract a char from the world.
    def extract(ch, fPull):
        # doesn't seem to be necessary
        #if not ch.in_room:
        #    print "Extract_char: None."
        #    return

        #    nuke_pets(ch)
        ch.pet = None  # just in case */

        #if fPull:
        #    die_follower( ch )
        fight.stop_fighting(ch, True)

        for obj in ch.carrying[:]:
            obj.extract()

        if ch.in_room:
            ch.from_room()

        # Death room is set in the clan tabe now */
        if not fPull:
            ch.to_room(room_index_hash[ch.clan.hall])
            return

        if ch.desc and ch.desc.original:
            ch.do_return("")
            ch.desc = None

        for wch in player_list:
            if wch.reply == ch:
                wch.reply = None

        if ch not in char_list:
            print("Extract_char: char not found.")
            return

        char_list.remove(ch)
        if ch in player_list:
            player_list.remove(ch)

        if ch.desc:
            ch.desc.character = None
        return

    # * Find a char in the room.
    def get_char_room(ch, argument):
        number, arg = game_utils.number_argument(argument)
        count = 0
        arg = arg.lower()
        if arg == "self":
            return ch
        for rch in ch.in_room.people:
            if not ch.can_see(rch):
                continue
            if not state_checks.IS_NPC(rch) and not rch.name.lower().startswith(arg):
                continue
            if state_checks.IS_NPC(rch) and not game_utils.is_name(arg, rch.name):
                continue
            count += 1
            if count == number:
                return rch
        return None

    # * Find a char in the world.
    def get_char_world(ch, argument):
        wch = ch.get_char_room(argument)
        if wch:
            return wch

        number, arg = game_utils.number_argument(argument)
        count = 0
        for wch in char_list:
            if wch.in_room is None or not ch.can_see(wch):
                continue
            if not state_checks.IS_NPC(wch) and not game_utils.is_name(arg, wch.name.lower()):
                continue
            if state_checks.IS_NPC(wch) and arg not in wch.name:
                continue
            count += 1
            if count == number:
                return wch
        return None

    # * Find an obj in a list.
    def get_obj_list(ch, argument, contents):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for obj in contents:
            if ch.can_see_obj(obj) and game_utils.is_name(arg, obj.name.lower()):
                count += 1
                if count == number:
                    return obj
        return None

    # * Find an obj in player's inventory.
    def get_obj_carry(ch, argument, viewer):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for obj in ch.carrying:
            if obj.wear_loc == WEAR_NONE and viewer.can_see_obj(obj) and game_utils.is_name(arg, obj.name.lower()):
                count += 1
                if count == number:
                    return obj
        return None

    # * Find an obj in player's equipment.
    def get_obj_wear(ch, argument):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for obj in ch.carrying:
            if obj.wear_loc != WEAR_NONE and ch.can_see_obj(obj) and game_utils.is_name(arg, obj.name.lower()):
                count += 1
                if count == number:
                    return obj
        return None

    # * Find an obj in the room or in inventory.
    def get_obj_here(ch, argument):
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if obj:
            return obj
        obj = ch.get_obj_carry(argument, ch)
        if obj:
            return obj
        obj = ch.get_obj_wear(argument)
        if obj:
            return obj
        return None

    # * Find an obj in the world.
    def get_obj_world(ch, argument):
        obj = ch.get_obj_here(argument)
        if obj:
            return obj

        number, arg = game_utils.number_argument(argument)
        count = 0
        arg = arg.lower()
        for obj in object_list:
            if ch.can_see_obj(obj) and game_utils.is_name(arg, obj.name.lower()):
                count += 1
            if count == number:
                return obj
        return None

    # deduct cost from a character */
    def deduct_cost(ch, cost):
        silver = min(ch.silver, cost)
        gold = 0
        if silver < cost:
            gold = ((cost - silver + 99) / 100)
            silver = cost - 100 * gold
        ch.gold -= gold
        ch.silver -= silver

        if ch.gold < 0:
            print("Bug: deduct costs: gold %d < 0" % ch.gold)
            ch.gold = 0
        if ch.silver < 0:
            print("BUG: deduct costs: silver %d < 0" % ch.silver)
            ch.silver = 0

    def is_room_owner(ch, room):
        if not room.owner:
            return False
        return True if ch.name in room.owner else False

    # visibility on a room -- for entering and exits */
    def can_see_room(ch, pRoomIndex):
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_IMP_ONLY) and ch.get_trust() < MAX_LEVEL:
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_GODS_ONLY) and not state_checks.IS_IMMORTAL(ch):
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_HEROES_ONLY) and not state_checks.IS_IMMORTAL(ch):
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_NEWBIES_ONLY) and ch.level > 5 and not state_checks.IS_IMMORTAL(ch):
            return False
        if not state_checks.IS_IMMORTAL(ch) and pRoomIndex.clan and ch.clan != pRoomIndex.clan:
            return False
        return True

    # * True if char can see victim.
    def can_see(ch, victim):
        # RT changed so that WIZ_INVIS has levels */
        if ch == victim:
            return True
        if ch.get_trust() < victim.invis_level:
            return False
        if ch.get_trust() < victim.incog_level and ch.in_room != victim.in_room:
            return False
        if (not state_checks.IS_NPC(ch) and state_checks.IS_SET(ch.act, PLR_HOLYLIGHT)) or (state_checks.IS_NPC(ch) and state_checks.IS_IMMORTAL(ch)):
            return True
        if state_checks.IS_AFFECTED(ch, AFF_BLIND):
            return False
        if ch.in_room.is_dark() and not state_checks.IS_AFFECTED(ch, AFF_INFRARED):
            return False
        if state_checks.IS_AFFECTED(victim, AFF_INVISIBLE) and not state_checks.IS_AFFECTED(ch, AFF_DETECT_INVIS):
            return False
        # sneaking */

        if state_checks.IS_AFFECTED(victim, AFF_SNEAK) and not state_checks.IS_AFFECTED(ch, AFF_DETECT_HIDDEN) and victim.fighting is None:
            chance = victim.get_skill("sneak")
            chance += victim.get_curr_stat(STAT_DEX) * 3 // 2
            chance -= ch.get_curr_stat(STAT_INT) * 2
            chance -= ch.level - victim.level * 3 // 2

            if random.randint(1, 99) < chance:
                return False

        if state_checks.IS_AFFECTED(victim, AFF_HIDE) and not state_checks.IS_AFFECTED(ch, AFF_DETECT_HIDDEN) and victim.fighting is None:
            return False

        return True

    # * True if char can see obj.
    def can_see_obj(ch, obj):
        if not state_checks.IS_NPC(ch) and state_checks.IS_SET(ch.act, PLR_HOLYLIGHT):
            return True
        if state_checks.IS_SET(obj.extra_flags, ITEM_VIS_DEATH):
            return False
        if state_checks.IS_AFFECTED(ch, AFF_BLIND) and obj.item_type != ITEM_POTION:
            return False
        if obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            return True
        if state_checks.IS_SET(obj.extra_flags, ITEM_INVIS) and not state_checks.IS_AFFECTED(ch, AFF_DETECT_INVIS):
            return False
        if state_checks.IS_OBJ_STAT(obj, ITEM_GLOW):
            return True
        if ch.in_room.is_dark() and not state_checks.IS_AFFECTED(ch, AFF_DARK_VISION):
            return False
        return True

    # * True if char can drop obj.
    def can_drop_obj(ch, obj):
        if not state_checks.IS_SET(obj.extra_flags, ITEM_NODROP):
            return True
        if not state_checks.IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
            return True
        return False

    # for returning skill information */
    def get_skill(ch, sn):

        if sn == -1:  # shorthand for level based skills */
            skill = ch.level * 5 / 2
        elif sn not in const.skill_table:
            print("BUG: Bad sn %s in get_skill." % sn)
            skill = 0
        elif not state_checks.IS_NPC(ch):
            if ch.level < const.skill_table[sn].skill_level[ch.guild.name] or sn not in ch.pcdata.learned:
                skill = 0
            else:
                skill = ch.pcdata.learned[sn]
        else:  # mobiles */
            if const.skill_table[sn].spell_fun != None:
                skill = 40 + 2 * ch.level
            elif sn == 'sneak' or sn == 'hide':
                skill = ch.level * 2 + 20
            elif (sn == 'dodge' and state_checks.IS_SET(ch.off_flags, OFF_DODGE)) \
                    or (sn == 'parry' and state_checks.IS_SET(ch.off_flags, OFF_PARRY)):
                skill = ch.level * 2
            elif sn == 'shield block':
                skill = 10 + 2 * ch.level
            elif sn == 'second attack' \
                    and (state_checks.IS_SET(ch.act, ACT_WARRIOR) or state_checks.IS_SET(ch.act, ACT_THIEF)):
                skill = 10 + 3 * ch.level
            elif sn == 'third_attack' and state_checks.IS_SET(ch.act, ACT_WARRIOR):
                skill = 4 * ch.level - 40
            elif sn == 'hand to hand':
                skill = 40 + 2 * ch.level
            elif sn == "trip" and state_checks.IS_SET(ch.off_flags, OFF_TRIP):
                skill = 10 + 3 * ch.level
            elif sn == "bash" and state_checks.IS_SET(ch.off_flags, OFF_BASH):
                skill = 10 + 3 * ch.level
            elif sn == "disarm" and (state_checks.IS_SET(ch.off_flags, OFF_DISARM) \
                                             or state_checks.IS_SET(ch.act, ACT_WARRIOR) or state_checks.IS_SET(ch.act, ACT_THIEF)):
                skill = 20 + 3 * ch.level
            elif sn == "berserk" and state_checks.IS_SET(ch.off_flags, OFF_BERSERK):
                skill = 3 * ch.level
            elif sn == "kick":
                skill = 10 + 3 * ch.level
            elif sn == "backstab" and state_checks.IS_SET(ch.act, ACT_THIEF):
                skill = 20 + 2 * ch.level
            elif sn == "rescue":
                skill = 40 + ch.level
            elif sn == "recall":
                skill = 40 + ch.level
            elif sn in ["sword", "dagger", "spear", "mace", "axe", "flail", "whip", "polearm"]:
                skill = 40 + 5 * ch.level / 2
            else:
                skill = 0
        if ch.daze > 0:
            if const.skill_table[sn].spell_fun != None:
                skill /= 2
            else:
                skill = 2 * skill / 3
        if not state_checks.IS_NPC(ch) and ch.pcdata.condition[COND_DRUNK] > 10:
            skill = 9 * skill / 10

        return max(0, min(skill, 100))

    # for returning weapon information */
    def get_weapon_sn(ch):
        wield = ch.get_eq(WEAR_WIELD)
        if not wield or wield.item_type != ITEM_WEAPON:
            sn = "hand to hand"
            return sn
        else:
            return wield.value[0]

    def get_weapon_skill(ch, sn):
        # -1 is exotic */
        skill = 0
        if state_checks.IS_NPC(ch):
            if sn == -1:
                skill = 3 * ch.level
            elif sn == "hand to hand":
                skill = 40 + 2 * ch.level
            else:
                skill = 40 + 5 * ch.level / 2
        elif sn in ch.pcdata.learned:
            if sn == -1:
                skill = 3 * ch.level
            else:
                skill = ch.pcdata.learned[sn]
        return max(0, min(skill, 100))

    # * Retrieve a character's age.
    def get_age(ch):
        return 17 + (ch.played + (int)(time.time() - ch.logon)) / 72000

    # * Retrieve a character's carry capacity.
    def can_carry_n(ch):
        if not state_checks.IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
            return 1000
        if state_checks.IS_NPC(ch) and state_checks.IS_SET(ch.act, ACT_PET):
            return 0
        return MAX_WEAR + 2 * ch.get_curr_stat(STAT_DEX) + ch.level

    # * Retrieve a character's carry capacity.
    def can_carry_w(ch):
        if not state_checks.IS_NPC(ch) and ch.level >= LEVEL_IMMORTAL:
            return 10000000
        if state_checks.IS_NPC(ch) and state_checks.IS_SET(ch.act, ACT_PET):
            return 0
        return const.str_app[ch.get_curr_stat(STAT_STR)].carry * 10 + ch.level * 25

    #/* command for retrieving stats */
    def get_curr_stat(ch, stat):
        if state_checks.IS_NPC(ch) or ch.level > LEVEL_IMMORTAL:
            smax = 25
        else:
            smax = const.pc_race_table[ch.race.name].max_stats[stat] + 4

            if ch.guild.attr_prime == stat:
                smax += 2

            if ch.race == const.race_table["human"]:
                smax += 1

            smax = min(smax, 25);
        return max(3, min(ch.perm_stat[stat] + ch.mod_stat[stat], smax))

    # command for returning max training score */
    def get_max_train(ch, stat):
        smax = 0
        if state_checks.IS_NPC(ch) or ch.level > LEVEL_IMMORTAL:
            return 25

        smax = const.pc_race_table[ch.race.name].max_stats[stat]
        if ch.guild.attr_prime == stat:
            if ch.race == const.race_table["human"]:
                smax += 3
            else:
                smax += 2
        return min(smax, 25)

    # * It is very important that this be an equivalence relation:
    # * (1) A ~ A
    # * (2) if A ~ B then B ~ A
    # * (3) if A ~ B  and B ~ C, then A ~ C
    def is_same_group(ch, bch):
        if ch == None or bch == None:
            return False

        if ch.leader is not None:
            ch = ch.leader
        if bch.leader is not None:
            bch = bch.leader
        return ch == bch

    def is_clan(ch):
        return ch.clan.name != ""

    def is_same_clan(ch, victim):
        if ch.clan.independent:
            return False
        else:
            return ch.clan == victim.clan

    def exp_per_level(ch, points):
        if state_checks.IS_NPC(ch):
            return 1000

        expl = 1000
        inc = 500

        if points < 40:
            return 1000 * const.pc_race_table[ch.race.name].class_mult[ch.guild.name] / 100 if \
            const.pc_race_table[ch.race.name].class_mult[ch.guild.name] else 1

        # processing */
        points -= 40

        while points > 9:
            expl += inc
            points -= 10
            if points > 9:
                expl += inc
                inc *= 2
                points -= 10

        expl += points * inc / 10

        return expl * const.pc_race_table[ch.race.name].class_mult[ch.guild.name] / 100

    def can_loot(ch, obj):
        if state_checks.IS_IMMORTAL(ch):
            return True
        if not obj.owner or obj.owner is None:
            return True
        owner = None
        for wch in char_list:
            if wch.name == obj.owner:
                owner = wch
        if owner is None:
            return True
        if ch.name == owner.name:
            return True
        if not state_checks.IS_NPC(owner) and state_checks.IS_SET(owner.act, PLR_CANLOOT):
            return True
        if ch.is_same_group(owner):
            return True
        return False


methods = {d: f for d, f in handler_ch.__dict__.items() if not d.startswith('__')}
for m, f in methods.items():
    setattr(CHAR_DATA, m, f)

def has_key(ch, key):
    for obj in ch.carrying:
        if obj.pIndexData.vnum == key:
            return True
    return False

def move_char(ch, door, follow):
    if door < 0 or door > 5:
        print("BUG: Do_move: bad door %d." % door)
        return
    in_room = ch.in_room
    pexit = in_room.exit[door]
    if not pexit or not pexit.to_room or not ch.can_see_room(pexit.to_room):
        ch.send("Alas, you cannot go that way.\n")
        return
    to_room = pexit.to_room
    if state_checks.IS_SET(pexit.exit_info, EX_CLOSED) \
            and (not state_checks.IS_AFFECTED(ch, AFF_PASS_DOOR) or state_checks.IS_SET(pexit.exit_info, EX_NOPASS)) \
            and not state_checks.IS_TRUSTED(ch, L7):
        handler_game.act("The $d is closed.", ch, None, pexit.keyword, TO_CHAR)
        return
    if state_checks.IS_AFFECTED(ch, AFF_CHARM) and ch.master and in_room == ch.master.in_room:
        ch.send("What?  And leave your beloved master?\n")
        return
    if not ch.is_room_owner(to_room) and to_room.is_private():
        ch.send("That room is private right now.\n")
        return
    if not state_checks.IS_NPC(ch):
        for gn, guild in const.guild_table.items():
            for room in guild.guild_rooms:
                if guild != ch.guild and to_room.vnum == room:
                    ch.send("You aren't allowed in there.\n")
                    return
        if in_room.sector_type == SECT_AIR or to_room.sector_type == SECT_AIR:
            if not state_checks.IS_AFFECTED(ch, AFF_FLYING) and not state_checks.IS_IMMORTAL(ch):
                ch.send("You can't fly.\n")
                return
        if ( in_room.sector_type == SECT_WATER_NOSWIM or to_room.sector_type == SECT_WATER_NOSWIM ) \
                and not state_checks.IS_AFFECTED(ch, AFF_FLYING):
            # Look for a boat.
            boats = [obj for obj in ch.carrying if obj.item_type == ITEM_BOAT]
            if not boats and not state_checks.IS_IMMORTAL(ch):
                ch.send("You need a boat to go there.\n")
                return
        move = movement_loss[min(SECT_MAX - 1, in_room.sector_type)] + movement_loss[
            min(SECT_MAX - 1, to_room.sector_type)]
        move /= 2  # i.e. the average */
        # conditional effects */
        if state_checks.IS_AFFECTED(ch, AFF_FLYING) or state_checks.IS_AFFECTED(ch, AFF_HASTE):
            move /= 2
        if state_checks.IS_AFFECTED(ch, AFF_SLOW):
            move *= 2
        if ch.move < move:
            ch.send("You are too exhausted.\n")
            return
        state_checks.WAIT_STATE(ch, 1)
        ch.move -= move
    if not state_checks.IS_AFFECTED(ch, AFF_SNEAK) and ch.invis_level < LEVEL_HERO:
        handler_game.act("$n leaves $T.", ch, None, dir_name[door], TO_ROOM)
    ch.from_room()
    ch.to_room(to_room)
    if not state_checks.IS_AFFECTED(ch, AFF_SNEAK) and ch.invis_level < LEVEL_HERO:
        handler_game.act("$n has arrived.", ch, None, None, TO_ROOM)
    ch.do_look("auto")
    if in_room == to_room:  # no circular follows */
        return

    for fch in in_room.people[:]:
        if fch.master == ch and state_checks.IS_AFFECTED(fch, AFF_CHARM) and fch.position < POS_STANDING:
            fch.do_stand("")

        if fch.master == ch and fch.position == POS_STANDING and fch.can_see_room(to_room):
            if state_checks.IS_SET(ch.in_room.room_flags, ROOM_LAW) and (state_checks.IS_NPC(fch) and state_checks.IS_SET(fch.act, ACT_AGGRESSIVE)):
                handler_game.act("You can't bring $N into the city.", ch, None, fch, TO_CHAR)
                handler_game.act("You aren't allowed in the city.", fch, None, None, TO_CHAR)
                continue

            handler_game.act("You follow $N.", fch, None, ch, TO_CHAR)
            move_char(fch, door, True)

def add_follower( ch, master ):
    if ch.master:
        print ("BUG: Add_follower: non-null master.")
        return
    ch.master        = master
    ch.leader        = None
    if master.can_see(ch):
        handler_game.act( "$n now follows you.", ch, None, master, TO_VICT )
    handler_game.act( "You now follow $N.",  ch, None, master, TO_CHAR )
    return

# nukes charmed monsters and pets */
def nuke_pets( ch ):
    if ch.pet:
        stop_follower(ch.pet)
        if ch.pet.in_room:
            handler_game.act("$N slowly fades away.",ch,None,ch.pet,TO_NOTVICT)
        ch.pet.extract(True)
    ch.pet = None
    return

def die_follower(ch):
    if ch.master:
        if ch.master.pet == ch:
            ch.master.pet = None
        stop_follower( ch )
    ch.leader = None

    for fch in char_list[:]:
        if fch.master == ch:
            stop_follower( fch )
        if fch.leader == ch:
            fch.leader = fch
    return

def stop_follower( ch ):
    if not ch.master:
        print ("BUG: Stop_follower: null master.")
        return

    if state_checks.IS_AFFECTED(ch, AFF_CHARM):
        state_checks.REMOVE_BIT( ch.affected_by, AFF_CHARM )
        ch.affect_strip('charm person')

    if ch.master.can_see(ch) and ch.in_room:
        handler_game.act( "$n stops following you.", ch, None, ch.master, TO_VICT)
        handler_game.act( "You stop following $N.", ch, None, ch.master, TO_CHAR)
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
            frmt = format_obj_to_char(obj, ch, fShort)
            if frmt not in objects:
                objects[frmt] = 1
            else:
                objects[frmt] += 1


    if not objects and fShowNothing:
        if state_checks.IS_NPC(ch) or state_checks.IS_SET(ch.comm, COMM_COMBINE):
            ch.send("     ")
        ch.send("Nothing.\n")

     #* Output the formatted list.
    for desc, count in objects.items():
        if state_checks.IS_NPC(ch) or state_checks.IS_SET(ch.comm, COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\n" % (count, desc))
        else:
            for i in range(count):
                ch.send("     %s\n" % desc)

def show_char_to_char_0(victim, ch):
    buf = ''
    if state_checks.IS_SET(victim.comm, COMM_AFK):
        buf += "[AFK] "
    if state_checks.IS_AFFECTED(victim, AFF_INVISIBLE):
        buf += "(Invis) "
    if victim.invis_level >= LEVEL_HERO:
        buf += "(Wizi) "
    if state_checks.IS_AFFECTED(victim, AFF_HIDE):
        buf += "(Hide) "
    if state_checks.IS_AFFECTED(victim, AFF_CHARM):
        buf += "(Charmed) "
    if state_checks.IS_AFFECTED(victim, AFF_PASS_DOOR):
        buf += "(Translucent) "
    if state_checks.IS_AFFECTED(victim, AFF_FAERIE_FIRE):
        buf += "(Pink Aura) "
    if state_checks.IS_EVIL(victim) and state_checks.IS_AFFECTED(ch, AFF_DETECT_EVIL):
        buf += "(Red Aura) "
    if state_checks.IS_GOOD(victim) and state_checks.IS_AFFECTED(ch, AFF_DETECT_GOOD):
        buf += "(Golden Aura) "
    if state_checks.IS_AFFECTED(victim, AFF_SANCTUARY):
        buf += "(White Aura) "
    if not state_checks.IS_NPC(victim) and state_checks.IS_SET(victim.act, PLR_KILLER):
        buf += "(KILLER) "
    if not state_checks.IS_NPC(victim) and state_checks.IS_SET(victim.act, PLR_THIEF):
        buf += "(THIEF) "

    if state_checks.IS_NPC(victim) and victim.position == victim.start_pos and victim.long_descr:
        buf += victim.long_descr
        ch.send(buf)
        if state_checks.IS_SET(ch.act, PLR_OMNI):
            ch.send("(%d)" % victim.pIndexData.vnum)
        return

    buf += state_checks.PERS(victim, ch)
    if not state_checks.IS_NPC(victim) and not state_checks.IS_SET(ch.comm, COMM_BRIEF) \
            and victim.position == POS_STANDING and not ch.on:
        buf += victim.pcdata.title

    if victim.position == POS_DEAD: buf += " is DEAD!!"
    elif victim.position == POS_MORTAL: buf += " is mortally wounded."
    elif victim.position == POS_INCAP: buf += " is incapacitated."
    elif victim.position == POS_STUNNED: buf += " is lying here stunned."
    elif victim.position == POS_SLEEPING:
        if victim.on:
            if state_checks.IS_SET(victim.on.value[2], SLEEP_AT):
                buf += " is sleeping at %s." % (victim.on.short_descr)
            elif state_checks.IS_SET(victim.on.value[2], SLEEP_ON):
                buf += " is sleeping on %s." % (victim.on.short_descr)
            else:
                buf += " is sleeping in %s." % (victim.on.short_descr)
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
    if state_checks.IS_NPC(victim) and state_checks.IS_SET(ch.act, PLR_OMNI):
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
            ch.send(format_obj_to_char(obj, ch, True) + "\n")

    if victim != ch and not state_checks.IS_NPC(ch) \
    and random.randint(1, 99) < ch.get_skill("peek"):
        ch.send("\nYou peek at the inventory:\n")
        check_improve(ch, 'peek', True, 4)
        show_list_to_char(victim.carrying, ch, True, True)
    return

def show_char_to_char(list, ch):
    for rch in list:
        if rch == ch:
            continue

        if ch.get_trust() < rch.invis_level:
            continue

        if ch.can_see(rch):
            show_char_to_char_0(rch, ch)
            ch.send("\n")
        elif ch.in_room.is_dark() and state_checks.IS_AFFECTED(rch, AFF_INFRARED):
            ch.send("You see glowing red eyes watching YOU!\n")

