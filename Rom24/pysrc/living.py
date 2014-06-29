import random
from affects import Affects
from bit import Bit
from const import pc_race_table, race_table, race_type, guild_table, guild_type, skill_table, str_app
import fight
import game_utils
import handler_game
from immortal import Immortal
from location import Location
from merc import PLR_NOSUMMON, MAX_STATS, ACT_IS_NPC, POS_SLEEPING, PLR_HOLYLIGHT, AFF_BLIND, LEVEL_IMMORTAL, \
    ITEM_ANTI_EVIL, ITEM_ANTI_GOOD, ITEM_ANTI_NEUTRAL, TO_CHAR, TO_ROOM, APPLY_SPELL_AFFECT, ITEM_LIGHT, WEAR_NONE, \
    MAX_WEAR, APPLY_SEX, APPLY_MANA, APPLY_HIT, APPLY_MOVE, APPLY_STR, STAT_STR, APPLY_DEX, STAT_DEX, APPLY_INT, \
    STAT_INT, APPLY_WIS, STAT_WIS, APPLY_CON, STAT_CON, APPLY_AC, APPLY_HITROLL, APPLY_DAMROLL, APPLY_SAVES, \
    APPLY_SAVING_ROD, APPLY_SAVING_PETRI, APPLY_SAVING_BREATH, APPLY_SAVING_SPELL, AFF_INFRARED, AFF_INVISIBLE, \
    AFF_DETECT_INVIS, AFF_SNEAK, AFF_DETECT_HIDDEN, AFF_HIDE, ITEM_VIS_DEATH, ITEM_POTION, ITEM_INVIS, ITEM_GLOW, \
    AFF_DARK_VISION, ROOM_IMP_ONLY, MAX_LEVEL, ROOM_GODS_ONLY, ROOM_HEROES_ONLY, ROOM_NEWBIES_ONLY, room_index_hash, \
    player_list, char_list, object_list, OFF_DODGE, OFF_PARRY, ACT_WARRIOR, ACT_THIEF, OFF_TRIP, OFF_BASH, OFF_DISARM, \
    OFF_BERSERK, COND_DRUNK, WEAR_WIELD, COMM_COMBINE, COMM_PROMPT, ACT_PET, IS_NORMAL, ITEM_WEAPON, IS_VULNERABLE, \
    IS_RESISTANT, IS_IMMUNE, IMM_SOUND, DAM_SOUND, IMM_CHARM, DAM_CHARM, IMM_LIGHT, DAM_LIGHT, IMM_DROWNING, \
    DAM_DROWNING, IMM_DISEASE, DAM_DISEASE, IMM_MENTAL, DAM_MENTAL, IMM_ENERGY, DAM_ENERGY, IMM_HOLY, DAM_HOLY, \
    IMM_NEGATIVE, DAM_NEGATIVE, IMM_POISON, DAM_POISON, IMM_ACID, DAM_ACID, IMM_LIGHTNING, DAM_LIGHTNING, IMM_COLD, \
    DAM_COLD, IMM_FIRE, DAM_FIRE, IMM_SLASH, DAM_SLASH, IMM_PIERCE, DAM_PIERCE, IMM_BASH, DAM_BASH, VULN_MAGIC, \
    RES_MAGIC, IMM_MAGIC, VULN_WEAPON, RES_WEAPON, IMM_WEAPON, DAM_NONE
import state_checks
from tables import act_flags, plr_flags, clan_table, form_flags, part_flags, imm_flags, comm_flags


class CharInteract:
    def __init__(self):
        super().__init__()
        self.master = None
        self.leader = None
        self.pet = None
        self.group = 0
        self._clan = ""
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
    @property
    def clan(self):
        try:
            return clan_table[self._clan]
        except KeyError as e:
            return clan_table[""]
    @clan.setter
    def clan(self, value):
        if value not in clan_table:
            return
        self._clan = value
    def stop_follower(self):
        if not self.master:
            logger.error("BUG: Stop_follower: null master.")
            return

        if self.is_affected(AFF_CHARM):
            self.affected_by.rem_bit(AFF_CHARM)
            self.affect_strip('charm person')

        if self.master.can_see(self) and self.in_room:
            handler_game.act("$n stops following you.", self, None, self.master, TO_VICT)
            handler_game.act("You stop following $N.", self, None, self.master, TO_CHAR)
        if self.master.pet == self:
            self.master.pet = None
        self.master = None
        self.leader = None
        return


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
        self.dam_type = 17
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

    def check_immune(self, dam_type):
        immune = -1
        defence = IS_NORMAL

        if dam_type is DAM_NONE:
            return immune

        if dam_type <= 3:
            if self.imm_flags.is_set(IMM_WEAPON):
                defence = IS_IMMUNE
            elif self.res_flags.is_set(RES_WEAPON):
                defence = IS_RESISTANT
            elif self.vuln_flags.is_set(VULN_WEAPON):
                defence = IS_VULNERABLE
        else:  # magical attack */
            if self.imm_flags.is_set(IMM_MAGIC):
                defence = IS_IMMUNE
            elif self.res_flags.is_set(RES_MAGIC):
                defence = IS_RESISTANT
            elif self.vuln_flags.is_set(VULN_MAGIC):
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

        if self.imm_flags.is_set(bit):
            immune = IS_IMMUNE
        elif self.res_flags.is_set(bit) and immune is not IS_IMMUNE:
            immune = IS_RESISTANT
        elif self.vuln_flags.is_set(bit):
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

    def can_carry_n(self):
        if not self.is_npc() and self.level >= LEVEL_IMMORTAL:
            return 1000
        if self.is_npc() and self.act.is_set(ACT_PET):
            return 0
        return MAX_WEAR + 2 * self.stat(STAT_DEX) + self.level

    # * Retrieve a character's carry capacity.
    def can_carry_w(self):
        if not self.is_npc() and self.level >= LEVEL_IMMORTAL:
            return 10000000
        if self.is_npc() and self.act.is_set(ACT_PET):
            return 0
        return str_app[self.stat(STAT_STR)].carry * 10 + self.level * 25


class Living(Immortal, Fight, CharInteract, Physical,
                Location, Affects, Communication, Container):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.version = 5
        self.level = 0
        self.act = Bit(PLR_NOSUMMON, [act_flags, plr_flags])
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
        self.desc = None
    def send(self, str):
        pass
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
    def race(self):
        try:
            return race_table[self._race]
        except KeyError:
            return race_table['human']
    @race.setter
    def race(self, value):
        if isinstance(value, race_type):
            self._race = value.name
        elif value in race_table:
            self._race = value

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

    # * Extract a char from the world.
    def extract(self, fPull):
        # doesn't seem to be necessary
        #if not ch.in_room:
        #    print "Extract_char: None."
        #    return

        #    nuke_pets(ch)
        self.pet = None  # just in case */

        #if fPull:
        #    die_follower( ch )
        fight.stop_fighting(self, True)

        for obj in self.contents[:]:
            obj.extract()

        if self.in_room:
            self.from_room()

        # Death room is set in the clan tabe now */
        if not fPull:
            self.to_room(room_index_hash[self.clan.hall])
            return

        if self.desc and self.desc.original:
            self.do_return("")
            self.desc = None

        for wch in player_list:
            if wch.reply == self:
                wch.reply = None

        if self not in char_list:
            logger.error("Extract_char: char not found.")
            return

        char_list.remove(self)
        if self in player_list:
            player_list.remove(self)

        if self.desc:
            self.desc.character = None
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
            if not rch.is_npc() and not rch.name.lower().startswith(arg):
                continue
            if rch.is_npc() and not game_utils.is_name(arg, rch.name):
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
            if not wch.is_npc() and not game_utils.is_name(arg, wch.name.lower()):
                continue
            if wch.is_npc() and arg not in wch.name:
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
        for obj in ch.contents:
            if obj.wear_loc == WEAR_NONE and viewer.can_see_obj(obj) and game_utils.is_name(arg, obj.name.lower()):
                count += 1
                if count == number:
                    return obj
        return None

    # * Find an obj in player's equipment.
    def get_obj_wear(ch, argument):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for obj in ch.contents:
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
    def get_skill(self, sn):

        if sn == -1:  # shorthand for level based skills */
            skill = self.level * 5 // 2
        elif sn not in skill_table:
            logger.error("BUG: Bad sn %s in get_skill." % sn)
            skill = 0
        elif not self.is_npc():
            if self.level < skill_table[sn].skill_level[self.guild.name] \
                    or sn not in self.learned:
                skill = 0
            else:
                skill = self.learned[sn]
        else:  # mobiles */
            if skill_table[sn].spell_fun is not None:
                skill = 40 + 2 * self.level
            elif sn == 'sneak' or sn == 'hide':
                skill = self.level * 2 + 20
            elif (sn == 'dodge' and self.off_flags.is_set(OFF_DODGE)) \
                    or (sn == 'parry' and self.off_flags.is_set(OFF_PARRY)):
                skill = self.level * 2
            elif sn == 'shield block':
                skill = 10 + 2 * self.level
            elif sn == 'second attack' \
                    and (self.act.is_set(ACT_WARRIOR)
                         or self.act.is_set(ACT_THIEF)):
                skill = 10 + 3 * self.level
            elif sn == 'third attack' and self.act.is_set(ACT_WARRIOR):
                skill = 4 * self.level - 40
            elif sn == 'hand to hand':
                skill = 40 + 2 * self.level
            elif sn == "trip" and self.off_flags.is_set(OFF_TRIP):
                skill = 10 + 3 * self.level
            elif sn == "bash" and self.off_flags.is_set(OFF_BASH):
                skill = 10 + 3 * self.level
            elif sn == "disarm" and (self.off_flags.is_set(OFF_DISARM)
                                     or self.act.is_set(ACT_WARRIOR)
                                     or self.act.is_set(ACT_THIEF)):
                skill = 20 + 3 * self.level
            elif sn == "berserk" and self.off_flags.is_set(OFF_BERSERK):
                skill = 3 * self.level
            elif sn == "kick":
                skill = 10 + 3 * self.level
            elif sn == "backstab" and self.act.is_set(ACT_THIEF):
                skill = 20 + 2 * self.level
            elif sn == "rescue":
                skill = 40 + self.level
            elif sn == "recall":
                skill = 40 + self.level
            elif sn in ["sword", "dagger", "spear", "mace", "axe", "flail", "whip", "polearm"]:
                skill = 40 + 5 * self.level // 2
            else:
                skill = 0
        if self.daze > 0:
            if skill_table[sn].spell_fun is not None:
                skill //= 2
            else:
                skill = 2 * skill // 3
        if not self.is_npc() \
                and self.condition[COND_DRUNK] > 10:
            skill = 9 * skill // 10

        return max(0, min(skill, 100))
    # for returning weapon information */
    def get_weapon_sn(self):
        wield = self.get_eq(WEAR_WIELD)
        if not wield or wield.item_type != ITEM_WEAPON:
            sn = "hand to hand"
            return sn
        else:
            return wield.value[0]

    def get_weapon_skill(self, sn):
        # -1 is exotic */
        skill = 0
        if self.is_npc():
            if sn == -1:
                skill = 3 * self.level
            elif sn == "hand to hand":
                skill = 40 + 2 * self.level
            else:
                skill = 40 + 5 * self.level / 2
        elif sn in self.learned:
            if sn == -1:
                skill = 3 * self.level
            else:
                skill = self.learned[sn]
        return max(0, min(skill, 100))
    # deduct cost from a character */
    def deduct_cost(self, cost):
        silver = min(self.silver, cost)
        gold = 0
        if silver < cost:
            gold = ((cost - silver + 99) // 100)
            silver = cost - 100 * gold
        self.gold -= gold
        self.silver -= silver

        if self.gold < 0:
            logger.error("Bug: deduct costs: gold %d < 0" % self.gold)
            self.gold = 0
        if self.silver < 0:
            logger.error("BUG: deduct costs: silver %d < 0" % self.silver)
            self.silver = 0