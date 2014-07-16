import logging
import random
import container

import handler_game
import physical


logger = logging.getLogger()

import merc
import tables
import affects
import bit
import const
import fight
import game_utils
import immortal
import location
import state_checks
import handler

class Grouping:
    def __init__(self):
        super().__init__()
        self.master = None
        self.leader = None
        self.pet = None
        self.group = None
        self._clan = ""
    # * It is very important that this be an equivalence relation:
    # * (1) A ~ A
    # * (2) if A ~ B then B ~ A
    # * (3) if A ~ B  and B ~ C, then A ~ C
    def is_same_group(self, bch):
        if self is None or bch is None:
            return False

        if self.leader is not None:
            self = merc.characters[self.leader]
        if bch.leader is not None:
            bch = merc.characters[bch.leader]
        return self == bch

    @property
    def clan(self):
        try:
            return tables.clan_table[self._clan]
        except KeyError as e:
            return tables.clan_table[""]

    @clan.setter
    def clan(self, value):
        if value not in tables.clan_table:
            return
        self._clan = value

    def stop_follower(self):
        if not self.master:
            logger.error("BUG: Stop_follower: null master.")
            return

        if self.is_affected(merc.AFF_CHARM):
            self.affected_by.rem_bit(merc.AFF_CHARM)
            self.affect_strip('charm person')

        if merc.characters[self.master].can_see(self) and self.in_room:
            handler_game.act("$n stops following you.", self, None, self.master, merc.TO_VICT)
            handler_game.act("You stop following $N.", self, None, self.master, merc.TO_CHAR)
        if merc.characters[self.master].pet == self.instance_id:
            merc.characters[self.master].pet = None
        self.master = None
        self.leader = None
        return

    def is_clan(ch):
        return ch.clan.name != ""

    def is_same_clan(ch, victim):
        if ch.clan.independent:
            return False
        else:
            return ch.clan == victim.clan

    def can_loot(ch, item):
        if ch.is_immortal():
            return True
        if not item.owner or item.owner is None:
            return True
        owner = None
        for wch in merc.characters.values():
            if wch.name == item.owner:
                owner = wch
        if owner is None:
            return True
        if ch.name == owner.name:
            return True
        if not owner.is_npc() and owner.act.is_set(merc.PLR_CANLOOT):
            return True
        if ch.is_same_group(owner):
            return True
        return False


class Fight:
    def __init__(self):
        super().__init__()
        self._fighting = None
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
        self.imm_flags = bit.Bit(flags=tables.imm_flags)
        self.res_flags = bit.Bit(flags=tables.imm_flags)
        self.vuln_flags = bit.Bit(flags=tables.imm_flags)
    @property
    def fighting(self):
        return merc.characters.get(self._fighting, None)

    @fighting.setter
    def fighting(self, value):
        if type(value) is int:
            value = merc.characters.get(value, None) #Ensure fighting exists.
        if value and not isinstance(value, Fight):
            logger.error("Instance fighting non combat. %s fighting %s", self.name, value.name)
            return
        if value:
            value = value.instance_id
        self._fighting = value #None or instance_id

    def check_immune(self, dam_type):
        immune = -1
        defence = merc.IS_NORMAL

        if dam_type is merc.DAM_NONE:
            return immune

        if dam_type <= 3:
            if self.imm_flags.is_set(merc.IMM_WEAPON):
                defence = merc.IS_IMMUNE
            elif self.res_flags.is_set(merc.RES_WEAPON):
                defence = merc.IS_RESISTANT
            elif self.vuln_flags.is_set(merc.VULN_WEAPON):
                defence = merc.IS_VULNERABLE
        else:  # magical attack */
            if self.imm_flags.is_set(merc.IMM_MAGIC):
                defence = merc.IS_IMMUNE
            elif self.res_flags.is_set(merc.RES_MAGIC):
                defence = merc.IS_RESISTANT
            elif self.vuln_flags.is_set(merc.VULN_MAGIC):
                defence = merc.IS_VULNERABLE

        bit = {merc.DAM_BASH: merc.IMM_BASH,
               merc.DAM_PIERCE: merc.IMM_PIERCE,
               merc.DAM_SLASH: merc.IMM_SLASH,
               merc.DAM_FIRE: merc.IMM_FIRE,
               merc.DAM_COLD: merc.IMM_COLD,
               merc.DAM_LIGHTNING: merc.IMM_LIGHTNING,
               merc.DAM_ACID: merc.IMM_ACID,
               merc.DAM_POISON: merc.IMM_POISON,
               merc.DAM_NEGATIVE: merc.IMM_NEGATIVE,
               merc.DAM_HOLY: merc.IMM_HOLY,
               merc.DAM_ENERGY: merc.IMM_ENERGY,
               merc.DAM_MENTAL: merc.IMM_MENTAL,
               merc.DAM_DISEASE: merc.IMM_DISEASE,
               merc.DAM_DROWNING: merc.IMM_DROWNING,
               merc.DAM_LIGHT: merc.IMM_LIGHT,
               merc.DAM_CHARM: merc.IMM_CHARM,
               merc.DAM_SOUND: merc.IMM_SOUND}
        if dam_type not in bit:
            return defence
        bit = bit[dam_type]

        if self.imm_flags.is_set(bit):
            immune = merc.IS_IMMUNE
        elif self.res_flags.is_set(bit) and immune is not merc.IS_IMMUNE:
            immune = merc.IS_RESISTANT
        elif self.vuln_flags.is_set(bit):
            if immune == merc.IS_IMMUNE:
                immune = merc.IS_RESISTANT
            elif immune == merc.IS_RESISTANT:
                immune = merc.IS_NORMAL
        else:
            immune = merc.IS_VULNERABLE

        if immune == -1:
            return defence
        else:
            return immune
            # * Retrieve a character's trusted level for permission checking.


class Communication:
    def __init__(self):
        super().__init__()
        self.reply = 0
        self.comm = bit.Bit(merc.COMM_COMBINE | merc.COMM_PROMPT, tables.comm_flags)


class Living(immortal.Immortal, Fight, Grouping, physical.Physical,
             location.Location, affects.Affects, Communication,
             container.Container, handler.Instancer):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.version = 5
        self.level = 0
        self.act = bit.Bit(merc.PLR_NOSUMMON, [tables.act_flags, tables.plr_flags])
        self._race = 'human'
        self._guild = None
        self.sex = 0
        self.level = 0
        # stats */
        self.perm_stat = [13 for x in range(merc.MAX_STATS)]
        self.mod_stat = [0 for x in range(merc.MAX_STATS)]
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

    @property
    def race(self):
        try:
            return const.race_table[self._race]
        except KeyError:
            return const.race_table['human']

    @race.setter
    def race(self, value):
        if isinstance(value, const.race_type):
            self._race = value.name
        elif value in const.race_table:
            self._race = value

    @property
    def guild(self):
        return const.guild_table.get(self._guild, None)

    @guild.setter
    def guild(self, value):
        if isinstance(value, const.guild_type):
            self._guild = value.name
        else:
            self._guild = value

    def send(self, pstr):
        pass

    def is_npc(self):
        return self.act.is_set(merc.ACT_IS_NPC)

    def is_good(self):
        return self.alignment >= 350

    def is_evil(self):
        return self.alignment <= -350

    def is_neutral(self):
        return not self.is_good() and not self.is_evil()

    def is_awake(self):
        return self.position > merc.POS_SLEEPING

    def check_blind(self):
        if not self.is_npc() and self.act.is_set(merc.PLR_HOLYLIGHT):
            return True

        if self.is_affected(merc.AFF_BLIND):
            self.send("You can't see a thing!\n\r")
            return False
        return True

    #/* command for retrieving stats */
    def stat(self, stat):
        stat_max = 0
        if self.is_npc() or self.level > merc.LEVEL_IMMORTAL:
            stat_max = 25
        else:
            stat_max = const.pc_race_table[self.race.name].max_stats[stat] + 4

            if self.guild.attr_prime == stat:
                stat_max += 2
            if self.race == const.race_table["human"]:
                stat_max += 1
            stat_max = min(stat_max, 25);
        return max(3, min(self.perm_stat[stat] + self.mod_stat[stat], stat_max))

    # Find a piece of eq on a character.
    def get_eq(self, iWear):
        if not self:
            return None
        item_id = [eid for eid in self.contents if merc.items[eid].wear_loc == iWear]
        if not item_id:
            return None
        return item_id[0]
    # * Equip a char with an obj.

    def equip(self, item_id, iWear):
        if self.get_eq(iWear):
            logger.warning("Equip_char: already equipped (%d)." % iWear)
            return
        item = merc.items.get(item_id, None)
        if (state_checks.is_item_stat(item, merc.ITEM_ANTI_EVIL) and self.is_evil()) \
                or (state_checks.is_item_stat(item, merc.ITEM_ANTI_GOOD) and self.is_good()) \
                or (state_checks.is_item_stat(item, merc.ITEM_ANTI_NEUTRAL) and self.is_neutral()):
            # Thanks to Morgenes for the bug fix here!
            handler_game.act("You are zapped by $p and drop it.", self, item, None, merc.TO_CHAR)
            handler_game.act("$n is zapped by $p and drops it.", self, item, None, merc.TO_ROOM)
            item.from_environment()
            item.to_environment(self.in_room)
            return

        for i in range(4):
            self.armor[i] -= item.apply_ac(iWear, i)
        item.wear_loc = iWear

        if not item.enchanted:
            for paf in item.affected:
                if paf.location != merc.APPLY_SPELL_AFFECT:
                    self.affect_modify(paf, True)

        for paf in item.affected:
            if paf.location == merc.APPLY_SPELL_AFFECT:
                self.affect_add(self, paf)
            else:
                self.affect_modify(paf, True)

        if item.item_type == merc.ITEM_LIGHT and item.value[2] != 0 and self.in_room is not None:
            self.in_room.light += 1
        return

    # * Unequip a char with an obj.
    def unequip(self, item_id):
        item = merc.items.get(item_id, None)
        if item.wear_loc == merc.WEAR_NONE:
            logger.warning("Unequip_char: already unequipped.")
            return

        for i in range(4):
            self.armor[i] += item.apply_ac(item.wear_loc, i)
        item.wear_loc = -1

        if not item.enchanted:
            for paf in item.affected:
                if paf.location == merc.APPLY_SPELL_AFFECT:
                    for lpaf in self.affected[:]:
                        if lpaf.type == paf.type and lpaf.level == paf.level \
                                and lpaf.location == merc.APPLY_SPELL_AFFECT:
                            self.affect_remove(lpaf)
                            break
                else:
                    self.affect_modify(paf, False)
                    self.affect_check(paf.where, paf.bitvector)

        for paf in item.affected:
            if paf.location == merc.APPLY_SPELL_AFFECT:
                logger.error("Bug: Norm-Apply")
                for lpaf in self.affected:
                    if lpaf.type == paf.type and lpaf.level == paf.level and lpaf.location == merc.APPLY_SPELL_AFFECT:
                        logger.error("bug: location = %d" % lpaf.location)
                        logger.error("bug: type = %d" % lpaf.type)
                        self.affect_remove(lpaf)
                        break
            else:
                self.affect_modify(paf, False)
                self.affect_check(paf.where, paf.bitvector)

        if item.item_type == merc.ITEM_LIGHT \
                and item.value[2] != 0 \
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
            return 1000 * const.pc_race_table[self.race.name].class_mult[self.guild.name] // 100 if \
                const.pc_race_table[self.race.name].class_mult[self.guild.name] else 1
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
        return expl * const.pc_race_table[self.race.name].class_mult[self.guild.name] // 100

    def reset(self):
        if self.is_npc():
            return

        if self.perm_hit == 0 \
                or self.perm_mana == 0 \
                or self.perm_move == 0 \
                or self.last_level == 0:
            # do a FULL reset */
            for loc in range(merc.MAX_WEAR):
                item = merc.items.get(self.get_eq(loc), None)
                if not item:
                    continue
                affected = item.affected
                if not item.enchanted:
                    affected.extend(merc.global_instances[item.instance_id].affected)
                for af in affected:
                    mod = af.modifier
                    if af.location == merc.APPLY_SEX:
                        self.sex -= mod
                        if self.sex < 0 or self.sex > 2:
                            self.sex = 0 if self.is_npc() else self.true_sex
                    elif af.location == merc.APPLY_MANA:
                        self.max_mana -= mod
                    elif af.location == merc.APPLY_HIT:
                        self.max_hit -= mod
                    elif af.location == merc.APPLY_MOVE:
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
        for stat in range(merc.MAX_STATS):
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
        for loc in range(merc.MAX_WEAR):
            item = merc.items.get(self.get_eq(loc), None)
            if not item:
                continue
            for i in range(4):
                self.armor[i] -= item.apply_ac(loc, i)
            affected = item.affected
            if not item.enchanted:
                affected.extend(merc.global_instances[item.instance_id].affected)

            for af in affected:
                mod = af.modifier
                if af.location == merc.APPLY_STR:
                    self.mod_stat[merc.STAT_STR] += mod
                elif af.location == merc.APPLY_DEX:
                    self.mod_stat[merc.STAT_DEX] += mod
                elif af.location == merc.APPLY_INT:
                    self.mod_stat[merc.STAT_INT] += mod
                elif af.location == merc.APPLY_WIS:
                    self.mod_stat[merc.STAT_WIS] += mod
                elif af.location == merc.APPLY_CON:
                    self.mod_stat[merc.STAT_CON] += mod
                elif af.location == merc.APPLY_SEX:
                    self.sex += mod
                elif af.location == merc.APPLY_MANA:
                    self.max_mana += mod
                elif af.location == merc.APPLY_HIT:
                    self.max_hit += mod
                elif af.location == merc.APPLY_MOVE:
                    self.max_move += mod
                elif af.location == merc.APPLY_AC:
                    self.armor = [i + mod for i in self.armor]
                elif af.location == merc.APPLY_HITROLL:
                    self.hitroll += mod
                elif af.location == merc.APPLY_DAMROLL:
                    self.damroll += mod
                elif af.location == merc.APPLY_SAVES:
                    self.saving_throw += mod
                elif af.location == merc.APPLY_SAVING_ROD:
                    self.saving_throw += mod
                elif af.location == merc.APPLY_SAVING_PETRI:
                    self.saving_throw += mod
                elif af.location == merc.APPLY_SAVING_BREATH:
                    self.saving_throw += mod
                elif af.location == merc.APPLY_SAVING_SPELL:
                    self.saving_throw += mod

        # now add back spell effects */
        for af in self.affected:
            mod = af.modifier
            if af.location == merc.APPLY_STR:
                self.mod_stat[merc.STAT_STR] += mod
            elif af.location == merc.APPLY_DEX:
                self.mod_stat[merc.STAT_DEX] += mod
            elif af.location == merc.APPLY_INT:
                self.mod_stat[merc.STAT_INT] += mod
            elif af.location == merc.APPLY_WIS:
                self.mod_stat[merc.STAT_WIS] += mod
            elif af.location == merc.APPLY_CON:
                self.mod_stat[merc.STAT_CON] += mod
            elif af.location == merc.APPLY_SEX:
                self.sex += mod
            elif af.location == merc.APPLY_MANA:
                self.max_mana += mod
            elif af.location == merc.APPLY_HIT:
                self.max_hit += mod
            elif af.location == merc.APPLY_MOVE:
                self.max_move += mod
            elif af.location == merc.APPLY_AC:
                self.armor = [i + mod for i in self.armor]
            elif af.location == merc.APPLY_HITROLL:
                self.hitroll += mod
            elif af.location == merc.APPLY_DAMROLL:
                self.damroll += mod
            elif af.location == merc.APPLY_SAVES:
                self.saving_throw += mod
            elif af.location == merc.APPLY_SAVING_ROD:
                self.saving_throw += mod
            elif af.location == merc.APPLY_SAVING_PETRI:
                self.saving_throw += mod
            elif af.location == merc.APPLY_SAVING_BREATH:
                self.saving_throw += mod
            elif af.location == merc.APPLY_SAVING_SPELL:
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
            and self.act.is_set(merc.PLR_HOLYLIGHT)) \
                or (self.is_npc()
                    and self.is_immortal()):
            return True
        if self.is_affected(merc.AFF_BLIND):
            return False
        if self.in_room.is_dark() and not self.is_affected(merc.AFF_INFRARED):
            return False
        if victim.is_affected(merc.AFF_INVISIBLE) \
                and not self.is_affected(merc.AFF_DETECT_INVIS):
            return False
        # sneaking */

        if victim.is_affected(merc.AFF_SNEAK) \
                and not self.is_affected(merc.AFF_DETECT_HIDDEN) \
                and victim.fighting is None:
            chance = victim.get_skill("sneak")
            chance += victim.stat(merc.STAT_DEX) * 3 // 2
            chance -= self.stat(merc.STAT_INT) * 2
            chance -= self.level - victim.level * 3 // 2

            if random.randint(1, 99) < chance:
                return False

        if victim.is_affected(merc.AFF_HIDE) \
                and not self.is_affected(merc.AFF_DETECT_HIDDEN) \
                and victim.fighting is None:
            return False

        return True

    # * True if char can see obj.
    def can_see_item(self, item):
        if not self.is_npc() \
                and self.act.is_set(merc.PLR_HOLYLIGHT):
            return True
        if type(item) == int:
            item = merc.items.get(item, None)
        if state_checks.IS_SET(item.extra_flags, merc.ITEM_VIS_DEATH):
            return False
        if self.is_affected(merc.AFF_BLIND) \
                and item.item_type != merc.ITEM_POTION:
            return False
        if item.item_type == merc.ITEM_LIGHT \
                and item.value[2] != 0:
            return True
        if state_checks.IS_SET(item.extra_flags, merc.ITEM_INVIS) \
                and not self.is_affected(merc.AFF_DETECT_INVIS):
            return False
        if state_checks.is_item_stat(item, merc.ITEM_GLOW):
            return True
        if self.in_room.is_dark() \
                and not self.is_affected(merc.AFF_DARK_VISION):
            return False
        return True

    def can_see_room(self, room_id):
        room = merc.rooms[room_id]
        if state_checks.IS_SET(room.room_flags, merc.ROOM_IMP_ONLY) and self.trust < merc.MAX_LEVEL:
            return False
        if state_checks.IS_SET(room.room_flags, merc.ROOM_GODS_ONLY) and not self.is_immortal():
            return False
        if state_checks.IS_SET(room.room_flags, merc.ROOM_HEROES_ONLY) and not self.is_immortal():
            return False
        if state_checks.IS_SET(room.room_flags,
                               merc.ROOM_NEWBIES_ONLY) and self.level > 5 and not self.is_immortal():
            return False
        if not self.is_immortal() and room.clan and self.clan != room.clan:
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

        for item_id in self.contents[:]:
            item = merc.items[item_id]
            item.extract()

        if self.in_room:
            self.from_environment()

        # Death room is set in the clan tabe now */
        if not fPull:
            room_id = merc.instances_by_room[self.clan.hall][0]
            self.to_environment(room_id)
            return

        if self.desc and self.desc.original:
            self.do_return("")
            self.desc = None

        for wch in merc.player_characters.values():
            if wch.reply == self:
                wch.reply = None

        if self.instance_id not in merc.characters:
            logger.error("Extract_char: char not found.")
            return

        if self.desc:
            self.desc.character = None
        return

    # * Find a char in the room.
    def get_char_room(ch, argument):
        number, word = game_utils.number_argument(argument)
        count = 0
        word = word.lower()
        if word == "self":
            return ch
        for rch_id in ch.in_room.people:
            rch = merc.characters[rch_id]
            if not ch.can_see(rch):
                continue
            if not rch.is_npc() and not rch.name.lower().startswith(word):
                continue
            if rch.is_npc() and not game_utils.is_name(word, rch.name):
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
        for wch in merc.characters.values():
            if wch.in_room is 0 or not ch.can_see(wch):
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
    def get_item_list(ch, argument, contents):
        #TODO check if this should be returning object pointer or id
        number, arg = game_utils.number_argument(argument)
        count = 0
        for item_id in contents:
            item = merc.items[item_id]
            if ch.can_see_item(item) and game_utils.is_name(arg, item.name.lower()):
                count += 1
                if count == number:
                    return item
        return None

    # * Find an obj in player's inventory.
    def get_item_carry(ch, argument, viewer):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for item_id in ch.items:
            item = merc.items.get(item_id, None)
            if item.wear_loc == merc.WEAR_NONE and viewer.can_see_item(item) \
                    and game_utils.is_name(arg, item.name.lower()):
                count += 1
                if count == number:
                    return item
        return None

    # * Find an obj in player's equipment.
    def get_item_wear(ch, argument):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for item_id in ch.items:
            item = merc.items.get(item_id, None)
            if item.wear_loc != merc.WEAR_NONE and ch.can_see_item(item) \
                    and game_utils.is_name(arg, item.name.lower()):
                count += 1
                if count == number:
                    return found
        return None

    # * Find an obj in the room or in inventory.
    def get_item_here(ch, argument):
        item = ch.get_item_list(argument, ch.in_room.items)
        if item:
            return item
        item = ch.get_item_carry(argument, ch)
        if item:
            return item
        item = ch.get_item_wear(argument)
        if item:
            return item
        return None

    # * Find an obj in the world.
    def get_item_world(ch, argument):
        item_id = ch.get_item_here(argument)
        if item_id:
            return item_id
        number, arg = game_utils.number_argument(argument)
        arg = arg.lower()
        count = 0
        item_ids = sorted(merc.items.keys())
        for item_id in item_ids:
            item = merc.items[item_id]
            if ch.can_see_item(item) and game_utils.is_name(arg, item.name.lower()):
                count += 1
                if count == number:
                    return item
        return None


    # * True if char can drop obj.
    def can_drop_item(self, item):
        if type(item) is int:
            item = merc.items.get(item, None)
        if not state_checks.IS_SET(item.extra_flags, merc.ITEM_NODROP):
            return True
        if not self.is_npc() \
                and self.level >= merc.LEVEL_IMMORTAL:
            return True
        return False

    def get_skill(self, sn):
        if sn == -1:  # shorthand for level based skills */
            skill = self.level * 5 // 2
        elif sn not in const.skill_table:
            logger.error("BUG: Bad sn %s in get_skill." % sn)
            skill = 0
        elif not self.is_npc():
            if self.level < const.skill_table[sn].skill_level[self.guild.name] \
                    or sn not in self.learned:
                skill = 0
            else:
                skill = self.learned[sn]
        else:  # mobiles */
            if const.skill_table[sn].spell_fun is not None:
                skill = 40 + 2 * self.level
            elif sn == 'sneak' or sn == 'hide':
                skill = self.level * 2 + 20
            elif (sn == 'dodge' and self.off_flags.is_set(merc.OFF_DODGE)) \
                    or (sn == 'parry' and self.off_flags.is_set(merc.OFF_PARRY)):
                skill = self.level * 2
            elif sn == 'shield block':
                skill = 10 + 2 * self.level
            elif sn == 'second attack' \
                    and (self.act.is_set(merc.ACT_WARRIOR)
                         or self.act.is_set(merc.ACT_THIEF)):
                skill = 10 + 3 * self.level
            elif sn == 'third attack' and self.act.is_set(merc.ACT_WARRIOR):
                skill = 4 * self.level - 40
            elif sn == 'hand to hand':
                skill = 40 + 2 * self.level
            elif sn == "trip" and self.off_flags.is_set(merc.OFF_TRIP):
                skill = 10 + 3 * self.level
            elif sn == "bash" and self.off_flags.is_set(merc.OFF_BASH):
                skill = 10 + 3 * self.level
            elif sn == "disarm" and (self.off_flags.is_set(merc.OFF_DISARM)
                                     or self.act.is_set(merc.ACT_WARRIOR)
                                     or self.act.is_set(merc.ACT_THIEF)):
                skill = 20 + 3 * self.level
            elif sn == "berserk" and self.off_flags.is_set(merc.OFF_BERSERK):
                skill = 3 * self.level
            elif sn == "kick":
                skill = 10 + 3 * self.level
            elif sn == "backstab" and self.act.is_set(merc.ACT_THIEF):
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
            if const.skill_table[sn].spell_fun is not None:
                skill //= 2
            else:
                skill = 2 * skill // 3
        if not self.is_npc() \
                and self.condition[merc.COND_DRUNK] > 10:
            skill = 9 * skill // 10

        return max(0, min(skill, 100))

    # for returning weapon information */
    def get_weapon_sn(self):
        wield = merc.items.get(self.get_eq(merc.WEAR_WIELD), None)
        if not wield or wield.item_type != merc.ITEM_WEAPON:
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


    # * Wear one object.
    # * Optional replacement of existing objects.
    # * Big repetitive code, ick.
    def wear_item(self, item, fReplace):
        if self.level < item.level:
            self.send("You must be level %d to use this object.\n" % item.level)
            handler_game.act("$n tries to use $p, but is too inexperienced.", self, item, None, merc.TO_ROOM)
            return
        if item.item_type == merc.ITEM_LIGHT:
            if not self.remove_item(merc.WEAR_LIGHT, fReplace):
                return
            handler_game.act("$n lights $p and holds it.", self, item, None, merc.TO_ROOM)
            handler_game.act("You light $p and hold it.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_LIGHT)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FINGER):
            if merc.items.get(self.get_eq(merc.WEAR_FINGER_L), None) and merc.items.get(self.get_eq(merc.WEAR_FINGER_R), None) \
                    and not self.remove_item(merc.WEAR_FINGER_L, fReplace) \
                    and not self.remove_item(merc.WEAR_FINGER_R, fReplace):
                return
            if not merc.items.get(self.get_eq(merc.WEAR_FINGER_L), None):
                handler_game.act("$n wears $p on $s left finger.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p on your left finger.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_FINGER_L)
                return
            if not merc.items.get(self.get_eq(merc.WEAR_FINGER_R), None):
                handler_game.act("$n wears $p on $s right finger.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p on your right finger.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_FINGER_R)
                return
            logger.error("BUG: Wear_obj: no free finger.")
            self.send("You already wear two rings.\n")
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_NECK):
            if merc.items.get(self.get_eq(merc.WEAR_NECK_1), None) and merc.items.get(self.get_eq(merc.WEAR_NECK_2), None) \
                    and not self.remove_item(merc.WEAR_NECK_1, fReplace) \
                    and not self.remove_item(merc.WEAR_NECK_2, fReplace):
                return
            if not merc.items.get(self.get_eq(merc.WEAR_NECK_1), None):
                handler_game.act("$n wears $p around $s neck.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p around your neck.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_NECK_1)
                return
            if not merc.items.get(self.get_eq(merc.WEAR_NECK_2), None):
                handler_game.act("$n wears $p around $s neck.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p around your neck.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_NECK_2)
                return
            logger.error("BUG: Wear_obj: no free neck.")
            self.send("You already wear two neck items.\n")
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_BODY):
            if not self.remove_item(merc.WEAR_BODY, fReplace):
                return
            handler_game.act("$n wears $p on $s torso.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your torso.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_BODY)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_HEAD):
            if not self.remove_item(merc.WEAR_HEAD, fReplace):
                return
            handler_game.act("$n wears $p on $s head.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your head.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_HEAD)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_LEGS):
            if not self.remove_item(merc.WEAR_LEGS, fReplace):
                return
            handler_game.act("$n wears $p on $s legs.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your legs.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_LEGS)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FEET):
            if not self.remove_item(merc.WEAR_FEET, fReplace):
                return
            handler_game.act("$n wears $p on $s feet.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your feet.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_FEET)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_HANDS):
            if not self.remove_item(merc.WEAR_HANDS, fReplace):
                return
            handler_game.act("$n wears $p on $s hands.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your hands.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_HANDS)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_ARMS):
            if not self.remove_item(merc.WEAR_ARMS, fReplace):
                return
            handler_game.act("$n wears $p on $s arms.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your arms.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_ARMS)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_ABOUT):
            if not self.remove_item(merc.WEAR_ABOUT, fReplace):
                return
            handler_game.act("$n wears $p about $s torso.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p about your torso.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_ABOUT)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_WAIST):
            if not self.remove_item(merc.WEAR_WAIST, fReplace):
                return
            handler_game.act("$n wears $p about $s waist.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p about your waist.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_WAIST)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_WRIST):
            if merc.items.get(self.get_eq(merc.WEAR_WRIST_L), None) and merc.items.get(self.get_eq(merc.WEAR_WRIST_R), None) \
                    and not self.remove_item(merc.WEAR_WRIST_L, fReplace) and not self.remove_item(merc.WEAR_WRIST_R, fReplace):
                return
            if not merc.items.get(self.get_eq(merc.WEAR_WRIST_L), None):
                handler_game.act("$n wears $p around $s left wrist.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p around your left wrist.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_WRIST_L)
                return
            if not merc.items.get(self.get_eq(merc.WEAR_WRIST_R), None):
                handler_game.act("$n wears $p around $s right wrist.", self, item, None, merc.TO_ROOM)
                handler_game.act("You wear $p around your right wrist.", self, item, None, merc.TO_CHAR)
                self.equip(item, merc.WEAR_WRIST_R)
                return

            logger.error("BUG: Wear_obj: no free wrist.")
            self.send("You already wear two wrist items.\n")
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_SHIELD):
            if not self.remove_item(merc.WEAR_SHIELD, fReplace):
                return
            weapon = merc.items.get(self.get_eq(merc.WEAR_WIELD), None)
            if weapon and self.size < merc.SIZE_LARGE and state_checks.IS_WEAPON_STAT(weapon, merc.WEAPON_TWO_HANDS):
                self.send("Your hands are tied up with your weapon!\n")
                return
            handler_game.act("$n wears $p as a shield.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p as a shield.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_SHIELD)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WIELD):
            if not self.remove_item(merc.WEAR_WIELD, fReplace):
                return
            if not self.is_npc() and item.get_weight() > (const.str_app[self.stat(merc.STAT_STR)].wield * 10):
                self.send("It is too heavy for you to wield.\n")
                return
            if not self.is_npc() and self.size < merc.SIZE_LARGE \
                    and state_checks.IS_WEAPON_STAT(item, merc.WEAPON_TWO_HANDS) \
                    and merc.items.get(self.get_eq(merc.WEAR_SHIELD), None) is not None:
                self.send("You need two hands free for that weapon.\n")
                return
            handler_game.act("$n wields $p.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wield $p.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_WIELD)

            sn = self.get_weapon_sn()

            if sn == "hand to hand":
                return

            skill = self.get_weapon_skill(sn)
            if skill >= 100:
                handler_game.act("$p feels like a part of you!", self, item, None, merc.TO_CHAR)
            elif skill > 85:
                handler_game.act("You feel quite confident with $p.", self, item, None, merc.TO_CHAR)
            elif skill > 70:
                handler_game.act("You are skilled with $p.", self, item, None, merc.TO_CHAR)
            elif skill > 50:
                handler_game.act("Your skill with $p is adequate.", self, item, None, merc.TO_CHAR)
            elif skill > 25:
                handler_game.act("$p feels a little clumsy in your hands.", self, item, None, merc.TO_CHAR)
            elif skill > 1:
                handler_game.act("You fumble and almost drop $p.", self, item, None, merc.TO_CHAR)
            else:
                handler_game.act("You don't even know which end is up on $p.", self, item, None, merc.TO_CHAR)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_HOLD):
            if not self.remove_item(merc.WEAR_HOLD, fReplace):
                return
            handler_game.act("$n holds $p in $s hand.", self, item, None, merc.TO_ROOM)
            handler_game.act("You hold $p in your hand.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_HOLD)
            return
        if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FLOAT):
            if not self.remove_item(merc.WEAR_FLOAT, fReplace):
                return
            handler_game.act("$n releases $p to float next to $m.", self, item, None, merc.TO_ROOM)
            handler_game.act("You release $p and it floats next to you.", self, item, None, merc.TO_CHAR)
            self.equip(item, merc.WEAR_FLOAT)
            return
        if fReplace:
            self.send("You can't wear, wield, or hold that.\n")
        return

    def remove_item(self, iWear, fReplace):
        item = merc.items.get(self.get_eq(iWear), None)
        if not item:
            return True
        if not fReplace:
            return False
        if state_checks.IS_SET(item.extra_flags, merc.ITEM_NOREMOVE):
            handler_game.act("You can't remove $p.", self, item, None, merc.TO_CHAR)
            return False
        self.unequip(item)
        handler_game.act("$n stops using $p.", self, item, None, merc.TO_ROOM)
        handler_game.act("You stop using $p.", self, item, None, merc.TO_CHAR)
        return True

