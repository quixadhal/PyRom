import random
import logging

import game_utils
from handler_magic import saves_spell


logger = logging.getLogger()

from const import race_table, wiznet_table, skill_type, guild_table, pc_race_table, str_app, group_table, skill_table, \
    int_app, guild_type
import handler_game
from merc import MAX_STATS, PLR_NOSUMMON, COMM_PROMPT, COMM_COMBINE, ACT_IS_NPC, TO_ROOM, AFF_PLAGUE, DAM_DISEASE, \
    APPLY_STR, TO_AFFECTS, ITEM_LIGHT, WEAR_LIGHT, ROOM_VNUM_TEMPLE, room_index_hash, LEVEL_HERO, STAT_CON, APPLY_SEX, \
    TO_CHAR, STAT_STR, WEAR_WIELD, APPLY_SPELL_AFFECT, APPLY_SAVING_SPELL, APPLY_SAVING_BREATH, APPLY_SAVING_PETRI, \
    APPLY_SAVING_ROD, APPLY_SAVES, APPLY_DAMROLL, APPLY_HITROLL, APPLY_AC, APPLY_EXP, APPLY_GOLD, APPLY_MOVE, APPLY_HIT, \
    APPLY_MANA, APPLY_WEIGHT, APPLY_HEIGHT, APPLY_AGE, APPLY_LEVEL, APPLY_CLASS, APPLY_CON, STAT_WIS, APPLY_WIS, \
    STAT_INT, APPLY_INT, STAT_DEX, APPLY_DEX, APPLY_NONE, TO_VULN, TO_RESIST, TO_IMMUNE, TO_WEAPON, TO_OBJECT, \
    LEVEL_IMMORTAL, MAX_WEAR, ITEM_ANTI_EVIL, ITEM_ANTI_GOOD, WEAR_NONE, ITEM_ANTI_NEUTRAL, PLR_HOLYLIGHT, \
    AFF_DARK_VISION, ITEM_GLOW, AFF_DETECT_INVIS, ITEM_INVIS, ITEM_POTION, AFF_BLIND, ITEM_VIS_DEATH, AFF_DETECT_HIDDEN, \
    AFF_HIDE, AFF_SNEAK, AFF_INVISIBLE, AFF_INFRARED, ROOM_NEWBIES_ONLY, ROOM_HEROES_ONLY, ROOM_GODS_ONLY, MAX_LEVEL, \
    ROOM_IMP_ONLY, POS_SLEEPING
import state_checks
from tables import off_flags, form_flags, act_flags, comm_flags, part_flags, affect_flags, imm_flags
from update import gain_exp

class Bit:
    def __init__(self, default=0,  flags=None):
        self.bits = default
        self.flags = flags

    def set_bit(self, bit):
        bit = self.from_name(bit)
        if bit:
            self.bits = self.bits | bit

    def rem_bit(self, bit):
        bit = self.from_name(bit)
        if bit:
            self.bits = self.bits & ~bit

    def is_set(self, bit):
        bit = self.from_name(bit)
        return self.bits & bit

    def from_name(self, name):
        if type(name) == int:
            return name
        for tok in self.flags.values():
            if tok.name == name:
                return tok.bit
        return None


class Immortal:
    def __init__(self):
        super().__init__()
        #Immortal
        self._trust = 0
        self.invis_level = 0
        self.incog_level = 0
        self.wiznet = Bit(flags=wiznet_table)

    def is_immortal(self):
        return self.trust >= LEVEL_IMMORTAL

    @property
    def trust(self):
        if self.is_npc():
            if self.level >= LEVEL_HERO:
                return LEVEL_HERO - 1
            else:
                return self.level
        trust = self._trust
        level = self.level
        if self.desc and self.desc.original:
            trust = self.desc.original._trust
            level = self.desc.original.level
        if trust:
            return trust
        return level

    @trust.setter
    def trust(self, value):
        self._trust = int(value)

class CharInteract:
    def __init__(self):
        super().__init__()
        self.master = None
        self.leader = None
        self.pet = None
        self.group = 0
        self.clan = None
    # * It is very important that this be an equivalence relation:
    # * (1) A ~ A
    # * (2) if A ~ B then B ~ A
    # * (3) if A ~ B  and B ~ C, then A ~ C
    def is_same_group(self, bch):
        if self is None or bch is None:
            return False

        if self.leader is not None:
            self = self.leader
        if bch.leader is not None:
            bch = bch.leader
        return self == bch

class Physical:
    def __init__(self):
        super().__init__()
        self.name = ""
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.form = Bit(flags=form_flags)
        self.parts = Bit(flags=part_flags)
        self.size = 0
        self.material = ""


class Fight:
    def __init__(self):
        super().__init__()
        self.fighting = None
        self.hitroll = 0
        self.damroll = 0
        self.armor = [100, 100, 100, 100]
        self.wimpy = 0
        self.saving_throw = 0
        self.timer = 0
        self.wait = 0
        self.daze = 0
        self.hit = 20
        self.max_hit = 20
        self.imm_flags = Bit(flags=imm_flags)
        self.res_flags = Bit(flags=imm_flags)
        self.vuln_flags = Bit(flags=imm_flags)

class Location:
    def __init__(self):
        #Location
        super().__init__()
        self.in_room = None
        self.was_in_room = None
        self.on = None
        self.zone = None

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False

    def to_room(self, pRoomIndex):
        if not pRoomIndex:
            logger.error("Char_to_room: None. %s", self.name)
            self.to_room(room_index_hash[ROOM_VNUM_TEMPLE])
            return

        self.in_room = pRoomIndex
        pRoomIndex.people.append(self)

        if not self.is_npc():
            if self.in_room.area.empty:
                self.in_room.area.empty = False
                self.in_room.area.age = 0

            self.in_room.area.nplayer += 1

        obj = self.get_eq(WEAR_LIGHT)

        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            self.in_room.light += 1

        if self.is_affected(AFF_PLAGUE):
            af = [af for af in self.affected if af.type == 'plague']
            if not af:
                self.affected_by.rem_bit(AFF_PLAGUE)
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

            for vch in self.in_room.people[:]:
                if not saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not vch.is_immortal() and not vch.is_affected(AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return
    # * Move a char out of a room.
    def from_room(self):
        if not self.in_room:
            logger.error("BUG: Char_from_room: None.")
            return

        if not self.is_npc():
            self.in_room.area.nplayer -= 1
        obj = self.get_eq(WEAR_LIGHT)
        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and self.in_room.light > 0:
            self.in_room.light -= 1

        if self not in self.in_room.people:
            logger.error("BUG: Char_from_room: ch not found.")
            return
        self.in_room.people.remove(self)
        self.in_room = None
        self.on = None  # sanity check! */
        return


class Effects:
    def __init__(self):
        super().__init__()
        self.affected = []
        self.affected_by = Bit(flags=affect_flags)

    def is_affected(self, aff):
        if isinstance(aff, skill_type):
            aff = aff.name
        if type(aff) == str:
            return True if [paf for paf in self.affected if paf.type == aff][:1] else False
        return self.affected_by.is_set(aff)

    def affect_add(self, paf):
        paf_new = handler_game.AFFECT_DATA()
        paf_new.__dict__ = paf.__dict__.copy()
        self.affected.append(paf_new)
        self.affect_modify(paf_new, True)
        return


    # * Add or enhance an affect.
    def affect_join(self, paf):
        for paf_old in self.affected:
            if paf_old.type == paf.type:
                paf.level = (paf.level + paf_old.level) / 2
                paf.duration += paf_old.duration
                paf.modifier += paf_old.modifier
                self.affect_remove(paf_old)
                break

        self.affect_add(paf)
        return
    # * Remove an affect from a char.
    def affect_remove(self, paf):
        if not self.affected:
            logger.error("BUG: Affect_remove: no affect.")
            return

        self.affect_modify(paf, False)
        where = paf.where
        vector = paf.bitvector

        if paf not in self.affected:
            logger.error("Affect_remove: cannot find paf.")
            return
        self.affected.remove(paf)
        del paf
        self.affect_check(where, vector)
        return

    def affect_check(self, where, vector):
        if where in [TO_OBJECT, TO_WEAPON] or not vector:
            return

        for paf in self.affected:
            if paf.where == where and paf.bitvector == vector:
                if where == TO_AFFECTS:
                    self.affected_by.set_bit(vector)
                elif where == TO_IMMUNE:
                    self.imm_flags.set_bit(vector)
                elif where == TO_RESIST:
                    self.res_flags.set_bit(vector)
                elif where == TO_VULN:
                    self.vuln_flags.set_bit(vector)
                return

        for obj in self.contents:
            if obj.wear_loc == -1:
                continue
            for paf in obj.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        self.affected_by.set_bit(vector)
                    elif where == TO_IMMUNE:
                        self.imm_flags.set_bit(vector)
                    elif where == TO_RESIST:
                        self.res_flags.set_bit(vector)
                    elif where == TO_VULN:
                        self.vuln_flags.set_bit(vector)
                    return
            if obj.enchanted:
                continue
            for paf in obj.pIndexData.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        self.affected_by.set_bit(vector)
                    elif where == TO_IMMUNE:
                        self.imm_flags.set_bit(vector)
                    elif where == TO_RESIST:
                        self.res_flags.set_bit(vector)
                    elif where == TO_VULN:
                        self.vuln_flags.set_bit(vector)
                    return

    # * Apply or remove an affect to a character.
    def affect_modify(self, paf, fAdd):
        mod = paf.modifier
        if fAdd:
            if paf.where == TO_AFFECTS:
                self.affected_by.set_bit(paf.bitvector)
            elif paf.where == TO_IMMUNE:
                self.imm_flags.set_bit(paf.bitvector)
            elif paf.where == TO_RESIST:
                self.res_flags.set_bit(paf.bitvector)
            elif paf.where == TO_VULN:
                self.vuln_flags.set_bit(paf.bitvector)
        else:
            if paf.where == TO_AFFECTS:
                self.affected_by.rem_bit(paf.bitvector)
            elif paf.where == TO_IMMUNE:
                self.imm_flags.rem_bit(paf.bitvector)
            elif paf.where == TO_RESIST:
                self.res_flags.rem_bit(paf.bitvector)
            elif paf.where == TO_VULN:
                self.vuln_flags.rem_bit(paf.bitvector)
            mod = 0 - mod

        if paf.location == APPLY_NONE:
            pass
        elif paf.location == APPLY_STR:
            self.mod_stat[STAT_STR] += mod
        elif paf.location == APPLY_DEX:
            self.mod_stat[STAT_DEX] += mod
        elif paf.location == APPLY_INT:
            self.mod_stat[STAT_INT] += mod
        elif paf.location == APPLY_WIS:
            self.mod_stat[STAT_WIS] += mod
        elif paf.location == APPLY_CON:
            self.mod_stat[STAT_CON] += mod
        elif paf.location == APPLY_SEX:
            self.sex += mod
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
            self.max_mana += mod
        elif paf.location == APPLY_HIT:
            self.max_hit += mod
        elif paf.location == APPLY_MOVE:
            self.max_move += mod
        elif paf.location == APPLY_GOLD:
            pass
        elif paf.location == APPLY_EXP:
            pass
        elif paf.location == APPLY_AC:
            for i in range(4):
                self.armor[i] += mod
        elif paf.location == APPLY_HITROLL:
            self.hitroll += mod
        elif paf.location == APPLY_DAMROLL:
            self.damroll += mod
        elif paf.location == APPLY_SAVES:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_ROD:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_PETRI:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_BREATH:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_SPELL:
            self.saving_throw += mod
        elif paf.location == APPLY_SPELL_AFFECT:
            pass
        else:
            logger.error("Affect_modify: unknown location %d." % paf.location)
            return
        #
        # * Check for weapon wielding.
        # * Guard against recursion (for weapons with affects).
        wield = self.get_eq(WEAR_WIELD)
        if not self.is_npc() and wield \
                and wield.get_weight() > (str_app[self.stat(STAT_STR)].wield * 10):
            global depth

            if depth == 0:
                depth += 1
                handler_game.act("You drop $p.", self, wield, None, TO_CHAR)
                handler_game.act("$n drops $p.", self, wield, None, TO_ROOM)
                wield.from_char()
                wield.to_room(self.in_room)
                depth -= 1
        return

class Communication:
    def __init__(self):
        super().__init__()
        self.reply = None
        self.comm = Bit(COMM_COMBINE | COMM_PROMPT, comm_flags)

class Container:
    def __init__(self):
        super().__init__()
        self.contents = []
        self.carry_weight = 0
        self.carry_number = 0

class Living(Immortal, Fight, CharInteract, Physical,
                Location, Effects, Communication, Container):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.version = 5
        self.level = 0
        self.act = Bit(PLR_NOSUMMON, act_flags)
        self._race = 'human'
        self._guild = None
        self.sex = 0
        self.level = 0
        # stats */
        self.perm_stat = [13 for x in range(MAX_STATS)]
        self.mod_stat = [0 for x in range(MAX_STATS)]
        self.mana = 100
        self.max_mana = 100
        self.move = 100
        self.max_move = 100
        self.gold = 0
        self.silver = 0
        self.exp = 0
        self.position = 0
        self.alignment = 0
    def is_npc(self):
        return self.act.is_set(ACT_IS_NPC)
    def is_good(self):
        return self.alignment >= 350
    def is_evil(self):
        return self.alignment <= -350
    def is_neutral(self):
        return not self.is_good() and not self.is_evil()
    def is_awake(self):
        return self.position > POS_SLEEPING

    def check_blind(self):
        if not self.is_npc() and self.act.is_set(PLR_HOLYLIGHT):
            return True

        if self.is_affected(AFF_BLIND):
            self.send("You can't see a thing!\n\r")
            return False
        return True


    #/* command for retrieving stats */
    def stat(self, stat):
        stat_max = 0
        if self.is_npc() or self.level > LEVEL_IMMORTAL:
            stat_max = 25
        else:
            stat_max = pc_race_table[self.race.name].max_stats[stat] + 4

            if self.guild.attr_prime == stat:
                stat_max += 2
            if self.race == race_table["human"]:
                stat_max += 1
            stat_max = min(stat_max, 25);
        return max(3, min(self.perm_stat[stat] + self.mod_stat[stat], stat_max))

    # Find a piece of eq on a character.
    def get_eq(self, iWear):
        if not self:
            return None
        obj = [obj for obj in self.contents if obj.wear_loc == iWear]
        if not obj:
            return None
        return obj[0]
    # * Equip a char with an obj.
    def equip(self, obj, iWear):
        if self.get_eq(iWear):
            logger.warning("Equip_char: already equipped (%d)." % iWear)
            return

        if (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_EVIL) and self.is_evil()) \
                or (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_GOOD) and self.is_good()) \
                or (state_checks.IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) and self.is_neutral()):
            # Thanks to Morgenes for the bug fix here!
            handler_game.act("You are zapped by $p and drop it.", self, obj, None, TO_CHAR)
            handler_game.act("$n is zapped by $p and drops it.", self, obj, None, TO_ROOM)
            obj.from_char()
            obj.to_room(self.in_room)
            return

        for i in range(4):
            self.armor[i] -= obj.apply_ac(iWear, i)
        obj.wear_loc = iWear

        if not obj.enchanted:
            for paf in obj.pIndexData.affected:
                if paf.location != APPLY_SPELL_AFFECT:
                    self.affect_modify(paf, True)

        for paf in obj.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                self.affect_add(self, paf)
            else:
                self.affect_modify(paf, True)

        if obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and self.in_room is not None:
            self.in_room.light += 1
        return

    # * Unequip a char with an obj.
    def unequip(self, obj):
        if obj.wear_loc == WEAR_NONE:
            logger.warning("Unequip_char: already unequipped.")
            return

        for i in range(4):
            self.armor[i] += obj.apply_ac(obj.wear_loc, i)
        obj.wear_loc = -1

        if not obj.enchanted:
            for paf in obj.pIndexData.affected:
                if paf.location == APPLY_SPELL_AFFECT:
                    for lpaf in self.affected[:]:
                        if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                            self.affect_remove(lpaf)
                            break
                else:
                    self.affect_modify(paf, False)
                    self.affect_check(paf.where, paf.bitvector)

        for paf in obj.affected:
            if paf.location == APPLY_SPELL_AFFECT:
                logger.error("Bug: Norm-Apply")
                for lpaf in self.affected:
                    if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == APPLY_SPELL_AFFECT:
                        logger.error("bug: location = %d" % lpaf.location)
                        logger.error("bug: type = %d" % lpaf.type)
                        self.affect_remove(lpaf)
                        break
            else:
                self.affect_modify(paf, False)
                self.affect_check(paf.where, paf.bitvector)

        if obj.item_type == ITEM_LIGHT \
                and obj.value[2] != 0 \
                and self.in_room \
                and self.in_room.light > 0:
            self.in_room.light -= 1
        return


    def exp_per_level(self, points):
        if self.is_npc():
            return 1000
        expl = 1000
        inc = 500

        if points < 40:
            return 1000 * pc_race_table[self.race.name].class_mult[self.guild.name] // 100 if \
                pc_race_table[self.race.name].class_mult[self.guild.name] else 1
        # processing */
        points -= 40

        while points > 9:
            expl += inc
            points -= 10
            if points > 9:
                expl += inc
                inc *= 2
                points -= 10
        expl += points * inc // 10
        return expl * pc_race_table[self.race.name].class_mult[self.guild.name] // 100

    @property
    def guild(self):
        return guild_table.get(self._guild, None)
    @guild.setter
    def guild(self, value):
        if isinstance(value, guild_type):
            self._guild = value.name
        else:
            self._guild = value
    @property
    def pcdata(self):
        return self

    def reset(self):
        if self.is_npc():
            return

        if self.perm_hit == 0 \
                or self.perm_mana == 0 \
                or self.perm_move == 0 \
                or self.last_level == 0:
            # do a FULL reset */
            for loc in range(MAX_WEAR):
                obj = self.get_eq(loc)
                if not obj:
                    continue
                affected = obj.affected
                if not obj.enchanted:
                    affected.extend(obj.pIndexData.affected)
                for af in affected:
                    mod = af.modifier
                    if af.location == APPLY_SEX:
                        self.sex -= mod
                        if self.sex < 0 or self.sex > 2:
                            self.sex = 0 if self.is_npc() else self.true_sex
                    elif af.location == APPLY_MANA:
                        self.max_mana -= mod
                    elif af.location == APPLY_HIT:
                        self.max_hit -= mod
                    elif af.location == APPLY_MOVE:
                        self.max_move -= mod
            # now reset the permanent stats */
            self.perm_hit = self.max_hit
            self.perm_mana = self.max_mana
            self.perm_move = self.max_move
            self.last_level = self.played // 3600
            if self.true_sex < 0 or self.true_sex > 2:
                if 0 < self.sex < 3:
                    self.true_sex = self.sex
                else:
                    self.true_sex = 0

        # now restore the character to his/her true condition */
        for stat in range(MAX_STATS):
            self.mod_stat[stat] = 0

        if self.true_sex < 0 or self.true_sex > 2:
            self.true_sex = 0
        self.sex = self.true_sex
        self.max_hit = self.perm_hit
        self.max_mana = self.perm_mana
        self.max_move = self.perm_move

        for i in range(4):
            self.armor[i] = 100

        self.hitroll = 0
        self.damroll = 0
        self.saving_throw = 0

        # now start adding back the effects */
        for loc in range(MAX_WEAR):
            obj = self.get_eq(loc)
            if not obj:
                continue
            for i in range(4):
                self.armor[i] -= obj.apply_ac(loc, i)
            affected = obj.affected
            if not obj.enchanted:
                affected.extend(obj.pIndexData.affected)

            for af in affected:
                mod = af.modifier
                if af.location == APPLY_STR:
                    self.mod_stat[STAT_STR] += mod
                elif af.location == APPLY_DEX:
                    self.mod_stat[STAT_DEX] += mod
                elif af.location == APPLY_INT:
                    self.mod_stat[STAT_INT] += mod
                elif af.location == APPLY_WIS:
                    self.mod_stat[STAT_WIS] += mod
                elif af.location == APPLY_CON:
                    self.mod_stat[STAT_CON] += mod
                elif af.location == APPLY_SEX:
                    self.sex += mod
                elif af.location == APPLY_MANA:
                    self.max_mana += mod
                elif af.location == APPLY_HIT:
                    self.max_hit += mod
                elif af.location == APPLY_MOVE:
                    self.max_move += mod
                elif af.location == APPLY_AC:
                    self.armor = [i + mod for i in self.armor]
                elif af.location == APPLY_HITROLL:
                    self.hitroll += mod
                elif af.location == APPLY_DAMROLL:
                    self.damroll += mod
                elif af.location == APPLY_SAVES:
                    self.saving_throw += mod
                elif af.location == APPLY_SAVING_ROD:
                    self.saving_throw += mod
                elif af.location == APPLY_SAVING_PETRI:
                    self.saving_throw += mod
                elif af.location == APPLY_SAVING_BREATH:
                    self.saving_throw += mod
                elif af.location == APPLY_SAVING_SPELL:
                    self.saving_throw += mod

        # now add back spell effects */
        for af in self.affected:
            mod = af.modifier
            if af.location == APPLY_STR:
                self.mod_stat[STAT_STR] += mod
            elif af.location == APPLY_DEX:
                self.mod_stat[STAT_DEX] += mod
            elif af.location == APPLY_INT:
                self.mod_stat[STAT_INT] += mod
            elif af.location == APPLY_WIS:
                self.mod_stat[STAT_WIS] += mod
            elif af.location == APPLY_CON:
                self.mod_stat[STAT_CON] += mod
            elif af.location == APPLY_SEX:
                self.sex += mod
            elif af.location == APPLY_MANA:
                self.max_mana += mod
            elif af.location == APPLY_HIT:
                self.max_hit += mod
            elif af.location == APPLY_MOVE:
                self.max_move += mod
            elif af.location == APPLY_AC:
                self.armor = [i + mod for i in self.armor]
            elif af.location == APPLY_HITROLL:
                self.hitroll += mod
            elif af.location == APPLY_DAMROLL:
                self.damroll += mod
            elif af.location == APPLY_SAVES:
                self.saving_throw += mod
            elif af.location == APPLY_SAVING_ROD:
                self.saving_throw += mod
            elif af.location == APPLY_SAVING_PETRI:
                self.saving_throw += mod
            elif af.location == APPLY_SAVING_BREATH:
                self.saving_throw += mod
            elif af.location == APPLY_SAVING_SPELL:
                self.saving_throw += mod
        # make sure sex is RIGHT!!!! */
        if self.sex < 0 or self.sex > 2:
            self.sex = self.true_sex

    # * True if char can see victim.
    def can_see(self, victim):
        # RT changed so that WIZ_INVIS has levels */
        if self == victim:
            return True
        if self.trust < victim.invis_level:
            return False
        if self.trust < victim.incog_level and self.in_room != victim.in_room:
            return False
        if (not self.is_npc()
            and self.act.is_set(PLR_HOLYLIGHT)) \
                or (self.is_npc()
                    and self.is_immortal()):
            return True
        if self.is_affected(AFF_BLIND):
            return False
        if self.in_room.is_dark() and not self.is_affected(AFF_INFRARED):
            return False
        if victim.is_affected(AFF_INVISIBLE) \
                and not self.is_affected(AFF_DETECT_INVIS):
            return False
        # sneaking */

        if victim.is_affected(AFF_SNEAK) \
                and not self.is_affected(AFF_DETECT_HIDDEN) \
                and victim.fighting is None:
            chance = victim.get_skill("sneak")
            chance += victim.stat(STAT_DEX) * 3 // 2
            chance -= self.stat(STAT_INT) * 2
            chance -= self.level - victim.level * 3 // 2

            if random.randint(1, 99) < chance:
                return False

        if victim.is_affected(AFF_HIDE) \
                and not self.is_affected(AFF_DETECT_HIDDEN) \
                and victim.fighting is None:
            return False

        return True

    # * True if char can see obj.
    def can_see_obj(self, obj):
        if not self.is_npc() \
                and self.act.is_set(PLR_HOLYLIGHT):
            return True
        if state_checks.IS_SET(obj.extra_flags, ITEM_VIS_DEATH):
            return False
        if self.is_affected(AFF_BLIND) \
                and obj.item_type != ITEM_POTION:
            return False
        if obj.item_type == ITEM_LIGHT \
                and obj.value[2] != 0:
            return True
        if state_checks.IS_SET(obj.extra_flags, ITEM_INVIS) \
                and not self.is_affected(AFF_DETECT_INVIS):
            return False
        if state_checks.IS_OBJ_STAT(obj, ITEM_GLOW):
            return True
        if self.in_room.is_dark() \
                and not self.is_affected(AFF_DARK_VISION):
            return False
        return True

    def can_see_room(self, pRoomIndex):
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_IMP_ONLY) and self.trust < MAX_LEVEL:
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_GODS_ONLY) and not self.is_immortal():
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags, ROOM_HEROES_ONLY) and not self.is_immortal():
            return False
        if state_checks.IS_SET(pRoomIndex.room_flags,
                               ROOM_NEWBIES_ONLY) and self.level > 5 and not self.is_immortal():
            return False
        if not self.is_immortal() and pRoomIndex.clan and self.clan != pRoomIndex.clan:
            return False
        return True



class Mobile(Living):
    def __init__(self):
        super().__init__()
        self.memory = None
        self.spec_fun = None
        self.pIndexData = None
        self.off_flags = Bit(flags=off_flags)
        self.damage = [0, 0, 0]
        self.dam_type = 17
        self.start_pos = 0
        self.default_pos = 0

class Character(Living):
    def __init__(self):
        super().__init__()
        self.buffer = None
        self.valid = False
        self.pwd = ""
        self.bamfin = ""
        self.bamfout = ""
        self._title = ""
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
        self.desc = None
        self.gen_data = None
        self.prompt = "<%hhp %mm %vmv>"
        self.prefix = ""
        self.lines = 22
        self.played = 0
        self.logon = 0
        self.practice = 0
        self.train = 0
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        if self.is_npc():
            return
        nospace = ['.', ',', '!', '?']
        if title[0] in nospace:
            self._title = title
        else:
            self._title = ' ' + title

    # recursively adds a group given its number -- uses group_add */
    def gn_add(self, gn):
        self.group_known[gn.name] = True
        for i in gn.spells:
            if not i:
                break
            self.group_add(i,False)

    # recursively removes a group given its number -- uses group_remove */
    def gn_remove(self, gn):
        if gn.name in self.group_known:
            del self.group_known[gn.name]

        for i in gn.spells:
            if not i:
                return
            self.group_remove(i)

    # use for processing a skill or group for addition  */
    def group_add(self, name, deduct):
        if self.is_npc(): # NPCs do not have skills */
            return

        if name in skill_table:
            sn = skill_table[name]
            if sn.name not in self.pcdata.learned: # i.e. not known */
                self.learned[sn.name] = 1
            if deduct:
                self.points += sn.rating[self.guild.name]
            return

        # now check groups */

        if name in group_table:
            gn = group_table[name]
            if gn.name not in self.group_known:
                self.group_known[gn.name] = True
            if deduct:
                self.points += gn.rating[self.guild.name]

            self.gn_add(gn) # make sure all skills in the group are known */


    # used for processing a skill or group for deletion -- no points back! */

    def group_remove(self, name):
        if name in skill_table:
            sn = skill_table[name]
            if sn.name in self.learned:
                del self.learned[sn.name]
                return

        # now check groups */
        if name in group_table:
            gn = group_table[name]

            if gn.name in self.group_known:
                del self.group_known[gn.name]
                self.gn_remove(gn) # be sure to call gn_add on all remaining groups */

    # shows skills, groups and costs (only if not bought) */
    def list_group_costs(self):
        if self.is_npc():
            return
        col = 0
        self.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("group","cp","group","cp","group","cp"))

        for gn, group in group_table.items():
            if gn not in self.gen_data.group_chosen and gn not in self.group_known and group.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (group_table[gn].name, group.rating[self.guild.name]))
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send("\n")
        self.send("\n")
        col = 0

        self.send("%-18s %-5s %-18s %-5s %-18s %-5s\n" % ("skill","cp","skill","cp","skill","cp"))

        for sn, skill in skill_table.items():
            if sn not in self.gen_data.skill_chosen \
            and sn not in self.learned \
            and  skill.spell_fun == None \
            and  skill.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (skill.name, skill.rating[self.guild.name]))
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if  col % 3 != 0:
            self.send( "\n" )
        self.send("\n")

        self.send("Creation points: %d\n" % self.pcdata.points)
        self.send("Experience per level: %d\n" % self.exp_per_level(self.gen_data.points_chosen))
        return

    def list_group_chosen(self):
        if self.is_npc():
            return
        col = 0
        self.send("%-18s %-5s %-18s %-5s %-18s %-5s" % ("group","cp","group","cp","group","cp\n"))

        for gn, group in group_table.items():
            if gn in self.gen_data.group_chosen and group.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (group.name, group.rating[self.guild.name]) )
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send( "\n" )
        self.send("\n")

        col = 0

        self.send("%-18s %-5s %-18s %-5s %-18s %-5s" % ("skill","cp","skill","cp","skill","cp\n"))

        for sn, skill in skill_table.items():
            if sn in self.gen_data.skill_chosen and skill.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (skill.name, skill.rating[self.guild.name]) )
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send( "\n" )
        self.send("\n")

        self.send("Creation points: %d\n" % self.gen_data.points_chosen)
        self.send("Experience per level: %d\n" % self.exp_per_level(self.gen_data.points_chosen))
        return

    # this procedure handles the input parsing for the skill generator */
    def parse_gen_groups(self, argument):
        if not argument.strip():
            return False

        argument, arg = game_utils.read_word(argument)
        if "help".startswith(arg):
            if not argument:
                self.do_help("group help")
                return True

            self.do_help(argument)
            return True

        if "add".startswith(arg):
            if not argument:
                self.send("You must provide a skill name.\n")
                return True
            argument = argument.lower()
            if argument in group_table:
                gn = group_table[argument]
                if gn.name in self.gen_data.group_chosen or gn.name in self.group_known:
                    self.send("You already know that group!\n")
                    return True

                if gn.rating[self.guild.name] < 1:
                    self.send("That group is not available.\n")
                    return True

                # Close security hole */
                if self.gen_data.points_chosen + gn.rating[self.guild.name] > 300:
                    self.send("You cannot take more than 300 creation points.\n")
                    return True

                self.send("%s group added\n" % gn.name)
                self.gen_data.group_chosen[gn.name] = True
                self.gen_data.points_chosen += gn.rating[self.guild.name]
                self.gn_add(gn)
                self.points += gn.rating[self.guild.name]
                return True

            if argument in skill_table:
                sn = skill_table[argument]
                if sn.name in self.gen_data.skill_chosen or sn.name in self.learned:
                    self.send("You already know that skill!\n")
                    return True

                if sn.rating[self.guild.name] < 1 or sn.spell_fun != None:
                    self.send("That skill is not available.\n")
                    return True
                # Close security hole */
                if self.gen_data.points_chosen + sn.rating[self.guild.name] > 300:
                    self.send("You cannot take more than 300 creation points.\n")
                    return True

                self.send("%s skill added\n" % sn.name)
                self.gen_data.skill_chosen[sn.name] = True
                self.gen_data.points_chosen += sn.rating[self.guild.name]
                self.pcdata.learned[sn] = 1
                self.pcdata.points += sn.rating[self.guild.name]
                return True

            self.send("No skills or groups by that name...\n")
            return True

        if "drop".startswith(arg):
            if not argument:
                self.send("You must provide a skill to drop.\n")
                return True

            argument = argument.lower()
            if argument in group_table and argument in self.gen_data.group_chosen:
                gn = group_table[argument]
                self.send("Group dropped.\n")
                del self.gen_data.group_chosen[gn.name]
                self.gen_data.points_chosen -= gn.rating[self.guild.name]
                self.gn_remove(gn)
                for k,v in self.gen_data.group_chosen:
                    self.gn_add(group_table[k])
                self.points -= gn.rating[self.guild.name]
                return True

            if argument in skill_table and argument in self.gen_data.skill_chosen:
                sn = skill_table[argument]
                self.send("Skill dropped.\n")
                del self.gen_data.skill_chosen[sn.name]
                self.gen_data.points_chosen -= sn.rating[self.guild.name]
                del self.learned[sn]
                self.points -= sn.rating[self.guild.name]
                return True

            self.send("You haven't bought any such skill or group.\n")
            return True

        if "premise".startswith(arg):
            self.do_help("premise")
            return True

        if "list".startswith(arg):
            self.list_group_costs()
            return True

        if "learned".startswith(arg):
            self.list_group_chosen()
            return True

        if "info".startswith(arg):
            self.do_groups(argument)
            return True

        return False

    # shows all groups, or the sub-members of a group */
    # checks for skill improvement */
    def check_improve(self, sn, success, multiplier):
        if self.is_npc():
            return
        if type(sn) == str:
            sn = skill_table[sn]

        if self.level < sn.skill_level[self.guild.name] \
        or sn.rating[self.guild.name] == 0 \
        or sn.name not in self.learned \
        or self.learned[sn.name] == 100:
            return  # skill is not known */

        # check to see if the character has a chance to learn */
        chance = 10 * int_app[self.get_curr_stat(STAT_INT)].learn
        chance //= (multiplier * sn.rating[self.guild.name] * 4)
        chance += self.level

        if random.randint(1,1000) > chance:
            return

        # now that the character has a CHANCE to learn, see if they really have */

        if success:
            chance = max(5, min(100 - self.learned[sn.name], 95))
            if random.randint(1,99) < chance:
                self.send("You have become better at %s!\n" % sn.name)
                self.learned[sn.name] += 1
                gain_exp(self,2 * sn.rating[self.guild.name])
        else:
            chance = max(5, min(self.learned[sn.name]/2,30))
            if random.randint(1,99) < chance:
                self.send("You learn from your mistakes, and your %s skill improves.\n" % sn.name)
                self.learned[sn.name] += random.randint(1,3)
                self.learned[sn.name] = min(self.learned[sn.name],100)
                gain_exp(self,2 * sn.rating[self.guild.name])
