import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import equipment
from rom24 import instance
from rom24 import type_bypass
from rom24 import inventory
from rom24 import handler_game
from rom24 import physical
from rom24 import tables
from rom24 import affects
from rom24 import bit
from rom24 import const
from rom24 import fight
from rom24 import game_utils
from rom24 import immortal
from rom24 import environment
from rom24 import state_checks


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
            self = instance.characters[self.leader]
        if bch.leader is not None:
            bch = instance.characters[bch.leader]
        return self == bch

    @property
    def clan(self):
        try:
            return tables.clan_table[self._clan]
        except KeyError as e:
            return tables.clan_table[""]

    @clan.setter
    def clan(self, value):
        if value not in tables.clan_table.keys():
            return
        self._clan = value

    def stop_follower(self):
        if not self.master:
            logger.error("BUG: Stop_follower: null master.")
            return

        if self.is_affected(merc.AFF_CHARM):
            self.affected_by.rem_bit(merc.AFF_CHARM)
            self.affect_strip("charm person")

        if instance.characters[self.master].can_see(self) and self.in_room:
            handler_game.act(
                "$n stops following you.", self, None, self.master, merc.TO_VICT
            )
            handler_game.act(
                "You stop following $N.", self, None, self.master, merc.TO_CHAR
            )
        if instance.characters[self.master].pet == self.instance_id:
            instance.characters[self.master].pet = None
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
        for wch in instance.characters.values():
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
        self.armor = [100] * 4
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
        return instance.characters.get(self._fighting, None)

    @fighting.setter
    def fighting(self, value):
        if type(value) is int:
            value = instance.characters.get(value, None)  # Ensure fighting exists.
        if value and not isinstance(value, Fight):
            logger.error(
                "Instance fighting non combat. %s fighting %s", self.name, value.name
            )
            return
        if value:
            value = value.instance_id
        if type(value) is None:
            value = None
        self._fighting = value  # None or instance_id

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

        bit = {
            merc.DAM_BASH: merc.IMM_BASH,
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
            merc.DAM_SOUND: merc.IMM_SOUND,
        }

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


class Living(
    immortal.Immortal,
    Fight,
    Grouping,
    physical.Physical,
    environment.Environment,
    affects.Affects,
    Communication,
    inventory.Inventory,
    instance.Instancer,
    type_bypass.ObjectType,
    equipment.Equipment,
):
    def __init__(self):
        super().__init__()
        self.is_living = True
        self.id = 0
        self.version = 5
        self.level = 0
        self.act = bit.Bit(merc.PLR_NOSUMMON, [tables.act_flags, tables.plr_flags])
        self._race = "human"
        self._guild = None
        self.sex = 0
        self.level = 0
        # stats */
        self.perm_stat = [13] * merc.MAX_STATS
        self.mod_stat = [0] * merc.MAX_STATS
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
        self.slots = equipment.Equipped()

    @property
    def equipped(self):
        if self.is_living:
            return self.slots._equipped
        else:
            return None

    @property
    def race(self):
        try:
            return const.race_table[self._race]
        except KeyError:
            return const.race_table["human"]

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

    def get(self, instance_object):
        if instance_object.is_item and instance_object.instance_id in self.inventory:
            self.inventory.remove(instance_object.instance_id)
            self.carry_number -= instance_object.get_number()
            self.carry_weight -= instance_object.get_weight()
            instance_object.environment = None
            return instance_object
        elif (
            instance_object.is_item
            and instance_object.instance_id in self.equipped.values()
        ):
            raise KeyError(
                "Item is in equipped dict, not inventory! %d"
                % instance_object.instance_id
            )
        else:
            if not instance_object.is_item:
                raise TypeError(
                    "Non-item object attempted "
                    "to be removed from character object - %s" % type(instance_object)
                )

    def put(self, instance_object):
        # if instance_object.is_item:
        self.inventory += [instance_object.instance_id]
        instance_object.environment = self.instance_id
        if not instance_object.instance_id in self.equipped.values():
            self.carry_number += instance_object.get_number()
            self.carry_weight += instance_object.get_weight()
            return instance_object
        else:
            raise KeyError(
                "Item is in equipped dict, run, screaming! %d"
                % instance_object.instance_id
            )

    def send(self, pstr):
        pass

    def is_npc(self):
        return self.act.is_set(merc.ACT_IS_NPC)

    @property
    def is_pc(self):
        return not self.act.is_set(merc.ACT_IS_NPC)

    @is_pc.setter
    def is_pc(self, val):
        if val is True:
            self.act.rem_bit(merc.ACT_IS_NPC)
        elif val is False:
            self.act.set_bit(merc.ACT_IS_NPC)
        else:
            raise ValueError(
                f"Invalid bit set for is_pc: {val}.  Values can only be true or false."
            )

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

    # /* command for retrieving stats */
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
            stat_max = min(stat_max, 25)
        return max(3, min(self.perm_stat[stat] + self.mod_stat[stat], stat_max))

    def exp_per_level(self, points):
        if self.is_npc():
            return 1000
        expl = 1000
        inc = 500

        if points < 40:
            return (
                1000
                * const.pc_race_table[self.race.name].class_mult[self.guild.name]
                // 100
                if const.pc_race_table[self.race.name].class_mult[self.guild.name]
                else 1
            )
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
        return (
            expl
            * const.pc_race_table[self.race.name].class_mult[self.guild.name]
            // 100
        )

    def reset(self):
        if self.is_npc():
            return

        if (
            self.perm_hit == 0
            or self.perm_mana == 0
            or self.perm_move == 0
            or self.last_level == 0
        ):
            # do a FULL reset */
            for loc in self.equipped.keys():
                item = self.get_eq(loc)
                if not item:
                    continue
                affected = item.affected
                # This was causing a massive bug, where items would multiply affects because json doesnt operate
                # the way that the flat files did.
                # if not item.enchanted: - this is unnecessary as we load all affects directly with the json
                # affected(merc.itemTemplate[item.vnum].affected)
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
        for loc in self.equipped.keys():
            item = self.get_eq(loc)
            if not item:
                continue
            for i in range(4):
                self.armor[i] -= item.apply_ac(i)
            affected = item.affected
            # this is unnecessary as we load all affects directly with the json
            # if not item.enchanted:
            #     affected.extend(merc.itemTemplate[item.vnum].affected)

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
        if type(victim) is int:
            victim = instance.characters[victim]
        if self == victim:
            return True
        if self.trust < victim.invis_level:
            return False
        if self.trust < victim.incog_level and self.in_room != victim.in_room:
            return False
        if (not self.is_npc() and self.act.is_set(merc.PLR_HOLYLIGHT)) or (
            self.is_npc() and self.is_immortal()
        ):
            return True
        if self.is_affected(merc.AFF_BLIND):
            return False
        if self.in_room.is_dark() and not self.is_affected(merc.AFF_INFRARED):
            return False
        if victim.is_affected(merc.AFF_INVISIBLE) and not self.is_affected(
            merc.AFF_DETECT_INVIS
        ):
            return False
        # sneaking */

        if (
            victim.is_affected(merc.AFF_SNEAK)
            and not self.is_affected(merc.AFF_DETECT_HIDDEN)
            and victim.fighting is None
        ):
            chance = victim.get_skill("sneak")
            chance += victim.stat(merc.STAT_DEX) * 3 // 2
            chance -= self.stat(merc.STAT_INT) * 2
            chance -= self.level - victim.level * 3 // 2

            if random.randint(1, 99) < chance:
                return False

        if (
            victim.is_affected(merc.AFF_HIDE)
            and not self.is_affected(merc.AFF_DETECT_HIDDEN)
            and victim.fighting is None
        ):
            return False

        return True

    # * True if char can see obj.
    def can_see_item(self, item):
        if not self.is_npc() and self.act.is_set(merc.PLR_HOLYLIGHT):
            return True
        if type(item) == int:
            item = instance.items.get(item, None)
        if item.flags.vis_death:
            return False
        if self.is_affected(merc.AFF_BLIND) and item.item_type != merc.ITEM_POTION:
            return False
        if item.flags.light and item.value[2] != 0:
            return True
        if item.flags.invis and not self.is_affected(merc.AFF_DETECT_INVIS):
            return False
        if item.flags.glow:
            return True
        if self.in_room.is_dark() and not self.is_affected(merc.AFF_DARK_VISION):
            return False
        return True

    def can_see_room(self, room_id):
        if self.is_immortal():
            return True
        if not room_id:
            return False
        room = instance.rooms.get(room_id)
        if not room:
            logger.error("No room found for room_id: %s", room_id)
            return False
        if (
            state_checks.IS_SET(room.room_flags, merc.ROOM_IMP_ONLY)
            and self.trust < merc.MAX_LEVEL
        ):
            return False
        if (
            state_checks.IS_SET(room.room_flags, merc.ROOM_GODS_ONLY)
            and not self.is_immortal()
        ):
            return False
        if (
            state_checks.IS_SET(room.room_flags, merc.ROOM_HEROES_ONLY)
            and not self.is_immortal()
        ):
            return False
        if (
            state_checks.IS_SET(room.room_flags, merc.ROOM_NEWBIES_ONLY)
            and self.level > 5
            and not self.is_immortal()
        ):
            return False
        if not self.is_immortal() and room.clan and self.clan != room.clan:
            return False
        return True

    # Extract a char from the world.
    def extract(self, fPull):
        if not self.in_room:
            logger.warn("Character being extracted is not in a room.")

        # nuke_pets(ch)
        self.pet = None  # just in case

        # if fPull:
        #    die_follower( ch )
        fight.stop_fighting(self, True)

        for item_id in self.equipped.values():
            if item_id:
                item = instance.global_instances[item_id]
                self.raw_unequip(item)
        for item_id in self.inventory[:]:
            item = instance.global_instances[item_id]
            item.extract()

        if self.in_room:
            self.in_room.get(self)

        # Death room is set in the clan table now
        if not fPull:
            room_id = instance.instances_by_room[self.clan.hall][0]
            room = instance.rooms[room_id]
            if self.in_room:
                self.in_room.get(self)
                room.put(self)
            else:
                room.put(self)
            return

        if self.desc and self.desc.original:
            self.do_return("")
            self.desc = None

        for wch in instance.players.values():
            if wch.reply == self:
                wch.reply = None

        if self.instance_id not in instance.characters:
            logger.error("Extract_char: char not found.")
            return

        self.instance_destructor()
        if self.desc:
            self.desc.character = None

        return

    # * Find a char in the room.
    def get_char_room(ch, argument):
        number, word = game_utils.number_argument(argument)
        word = word.lower()
        if word == "self":
            return ch
        number, arg = game_utils.number_argument(argument)
        ch_list = [
            instance.characters[rch_id]
            for rch_id in ch.in_room.people[:]
            if game_utils.is_name(word, instance.characters[rch_id].name)
        ]
        if ch_list:
            try:
                if ch.can_see(ch_list[number - 1]):
                    return ch_list[number - 1]
            except:
                return None
        return None

    # * Find a char in the world.
    def get_char_world(ch, argument):
        wch = ch.get_char_room(argument)
        if wch:
            return wch
        number, arg = game_utils.number_argument(argument)
        arg = arg.lower()
        ch_list = [
            instance.characters[wch_id]
            for wch_id in sorted(instance.characters.keys())
            if game_utils.is_name(arg, instance.characters[wch_id].name)
        ]
        if ch_list:
            try:
                if ch.can_see(ch_list[number - 1]):
                    return ch_list[number - 1]
            except:
                return None
        return None

    # * Find an obj in a list.
    def get_item_list(ch, argument, contents):
        number, arg = game_utils.number_argument(argument)
        arg = arg.lower()
        item_list = [
            instance.items[item_id]
            for item_id in contents
            if game_utils.is_name(arg, instance.items[item_id].name)
        ]
        if item_list:
            try:
                if ch.can_see_item(item_list[number - 1]):
                    return item_list[number - 1]
            except:
                return None
        return None

    # * Find an obj in player's inventory.
    def get_item_carry(ch, argument, viewer):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for item_id in ch.items:
            item = instance.items.get(item_id, None)
            if viewer.can_see_item(item) and game_utils.is_name(arg, item.name.lower()):
                count += 1
                if count == number:
                    return item
        return None

    # * Find an obj in player's equipment.
    def get_item_wear(ch, argument):
        number, arg = game_utils.number_argument(argument)
        count = 0
        for loc, item_id in ch.equipped.items():
            if item_id:
                item = instance.items[item_id]
                if ch.can_see_item(item) and game_utils.is_name(arg, item.name.lower()):
                    # print('inside')
                    count += 1
                    if count == number:
                        # print(item.name, '\n')
                        # print(item.instance_id, '\n')
                        # print(ch.equipped['main_hand'])
                        return item
            else:
                continue
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
        item = ch.get_item_here(argument)
        if item:
            return item
        number, arg = game_utils.number_argument(argument)
        arg = arg.lower()
        item_list = [
            instance.items[item_id]
            for item_id in sorted(instance.items.keys())
            if game_utils.is_name(arg, instance.items[item_id].name)
        ]
        if item_list:
            try:
                if ch.can_see_item(item_list[number - 1]):
                    return item_list[number - 1]
            except:
                return None
        return None

    # * True if char can drop obj.
    def can_drop_item(self, item):
        if not item.flags.no_drop:
            return True
        if not self.is_npc() and self.level >= merc.LEVEL_IMMORTAL:
            return True
        return False

    def get_skill(self, sn):
        if sn == -1:  # shorthand for level based skills */
            skill = self.level * 5 // 2
        elif sn not in const.skill_table:
            logger.error("BUG: Bad sn %s in get_skill." % sn)
            skill = 0
        elif self.is_pc:
            if (
                self.level < const.skill_table[sn].skill_level[self.guild.name]
                or sn not in self.learned
            ):
                skill = 0
            else:
                skill = self.learned[sn]
        else:  # mobiles */
            if const.skill_table[sn].spell_fun is not None:
                skill = 40 + 2 * self.level
            elif sn == "sneak" or sn == "hide":
                skill = self.level * 2 + 20
            elif (sn == "dodge" and self.off_flags.is_set(merc.OFF_DODGE)) or (
                sn == "parry" and self.off_flags.is_set(merc.OFF_PARRY)
            ):
                skill = self.level * 2
            elif sn == "shield block":
                skill = 10 + 2 * self.level
            elif sn == "second attack" and (
                self.act.is_set(merc.ACT_WARRIOR) or self.act.is_set(merc.ACT_THIEF)
            ):
                skill = 10 + 3 * self.level
            elif sn == "third attack" and self.act.is_set(merc.ACT_WARRIOR):
                skill = 4 * self.level - 40
            elif sn == "hand to hand":
                skill = 40 + 2 * self.level
            elif sn == "trip" and self.off_flags.is_set(merc.OFF_TRIP):
                skill = 10 + 3 * self.level
            elif sn == "bash" and self.off_flags.is_set(merc.OFF_BASH):
                skill = 10 + 3 * self.level
            elif sn == "disarm" and (
                self.off_flags.is_set(merc.OFF_DISARM)
                or self.act.is_set(merc.ACT_WARRIOR)
                or self.act.is_set(merc.ACT_THIEF)
            ):
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
            elif sn in [
                "sword",
                "dagger",
                "spear",
                "mace",
                "axe",
                "flail",
                "whip",
                "polearm",
            ]:
                skill = 40 + 5 * self.level // 2
            else:
                skill = 0
        if self.daze > 0:
            if const.skill_table[sn].spell_fun is not None:
                skill //= 2
            else:
                skill = 2 * skill // 3
        if self.is_pc and self.condition[merc.COND_DRUNK] > 10:
            skill = 9 * skill // 10

        return max(0, min(skill, 100))

    # for returning weapon information */
    def get_weapon_sn(self):
        wield = self.get_eq("main_hand")
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
        """
        :param cost:
        :type cost:
        :return:
        :rtype:
        """
        silver = min(self.silver, cost)
        gold = 0
        if silver < cost:
            gold = (cost - silver + 99) // 100
            silver = cost - 100 * gold
        self.gold -= gold
        self.silver -= silver

        if self.gold < 0:
            logger.error("Bug: deduct costs: gold %d < 0" % self.gold)
            self.gold = 0
        if self.silver < 0:
            logger.error("BUG: deduct costs: silver %d < 0" % self.silver)
            self.silver = 0

    # Find a piece of eq on a character.
    def get_eq(self, check_loc):
        """
        :param check_loc:
        :type check_loc:
        :return:
        :rtype:
        """
        if not self:
            return None
        found = False
        if self.equipped.get(check_loc, None):
            found = True
        if not found:
            return None
        else:
            item_id = self.equipped[check_loc]
            return instance.items[item_id]

    def apply_affect(self, aff_object):
        """
        This was taken from the equip code, to shorten its length, checks for Affects, and applies as needed

        :param aff_object:
        :type aff_object:
        :return: no return
        :rtype: nothing
        """
        # redundant anc causes bugs!
        # if not aff_object.enchanted:
        #   for paf in merc.itemTemplate[aff_object.vnum].affected:
        #      if paf.location != merc.APPLY_SPELL_AFFECT:
        #         self.affect_modify(paf, True)

        for paf in aff_object.affected:
            if paf.location == merc.APPLY_SPELL_AFFECT:
                self.affect_add(self, paf)
            else:
                self.affect_modify(paf, True)

    def raw_equip(self, item, to_location):
        self.equipped[to_location] = item.instance_id
        item.environment = self.instance_id
        if item.flags.two_handed and "main_hand" in item.equipped_to:
            self.equipped["off_hand"] = item.instance_id
        for i in range(4):
            self.armor[i] -= item.apply_ac(i)
        self.apply_affect(item)
        if item.flags.light and item.value[2] != 0 and self.in_room:
            self.in_room.available_light += 1

    def can_equip(self, item, loc, should_replace=False, wverbose=False):
        # if item.environment:
        #     logger.debug("item.environment: %s", item.environment)
        #     try:
        #         item.environment.get(item)
        #         logger.debug("item.environment: %s", item.environment)
        #         logger.debug("Successfully ran item.environment.get(item)")
        #     except:
        #         logger.debug("item.environment: %s", item.environment)
        #         logger.exception("Encountered an exception trying to get the item from the environment.")
        #         return

        if (
            (item.flags.anti_evil and self.is_evil())
            or (item.flags.anti_good and self.is_good())
            or (item.flags.anti_neutral and self.is_neutral())
        ):
            handler_game.act(
                "You are zapped by $p and drop it.", self, item, None, merc.TO_CHAR
            )
            handler_game.act(
                "$n is zapped by $p and drops it.", self, item, None, merc.TO_ROOM
            )
            self.get(item)
            self.in_room.put(item)
            return False
        if should_replace:
            if not self.unequip(loc):
                return False
        if not self.is_npc():
            if loc == "main_hand":

                if item.get_weight() > (
                    const.str_app[self.stat(merc.STAT_STR)].wield * 10
                ):
                    if wverbose:
                        self.send("That weapon is too heavy for you to wield.\n")
                    return False
                elif item.flags.two_handed:
                    if self.slots.off_hand and self.size < merc.SIZE_LARGE:
                        if wverbose:
                            self.send("You need two hands free for that weapon.\n")

                        return False
                    elif self.size < merc.SIZE_LARGE:

                        if wverbose:
                            self.send("That weapon is too large for you to wield.\n")

                        return False
                    else:
                        return True
                else:
                    return True
            elif loc == "off_hand":
                if (
                    self.slots.main_hand
                    and item.flags.two_handed
                    and self.size < merc.SIZE_LARGE
                ):
                    if wverbose:
                        self.send("Your hands are tied up with your weapon!\n")
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    # * Equip a char with an obj.
    def equip(
        self,
        item,
        replace: bool = False,
        verbose: bool = False,
        verbose_all: bool = False,
        to_loc: str = None,
    ):
        """

        :type item: int or Items
        :type replace: bool
        :type verbose: bool
        :param verbose_all:
        :type to_loc: builtins.NoneType
        :return: :rtype:
        """
        location = None
        if not item.equips_to:
            if verbose:
                self.send("You can't wear, wield, or hold that.\n")
            return

        if to_loc:
            success = self.can_equip(item, to_loc, False, False)
            if not success:
                return
            self.raw_equip(item, to_loc)
            return
        else:
            possible_slots = item.equips_to & self.slots.available
            if len(possible_slots) > 0:
                if not verbose:
                    success = self.can_equip(
                        item, [k for k in possible_slots][0], False, False
                    )
                else:
                    success = self.can_equip(
                        item, [k for k in possible_slots][0], False, True
                    )
                if not success:
                    return
                else:
                    location = [k for k in possible_slots][0]
                    self.raw_equip(item, location)
                    if verbose_all:
                        self.verbose_wear_strings(item, location)
                    return
            else:
                if replace:
                    all_slots = {k for k in self.equipped.keys()}
                    overlap = item.equips_to & all_slots
                    if len(overlap) > 0:
                        if not verbose:
                            success = self.can_equip(
                                item, [k for k in overlap][0], True, False
                            )
                        else:
                            success = self.can_equip(
                                item, [k for k in overlap][0], True, False
                            )
                        if not success:
                            return
                        else:
                            # Get first location for equipping.
                            location = [k for k in overlap][0]
                            self.raw_equip(item, location)
                            if verbose_all:
                                self.verbose_wear_strings(item, location)
                            return
                    else:
                        if verbose:
                            self.send("You can't wear, wield, or hold that.\n")
                        return
                else:
                    if verbose:
                        self.send("You are already wearing something like that!\n")
                    return

    def remove_affect(self, aff_object):
        """
        :param aff_object:
        :type aff_object:
        :return: Nothing
        :rtype: none
        Taken from unequip to shorten it, searches for Affects, and removes as needed
        """
        # if aff_object.is_item and not aff_object.enchanted:
        # No idea why ROM was going back to the template for this one.. but to make it accurate, for now.
        # for paf in merc.itemTemplate[aff_object.vnum].affected:
        #       if paf.location == merc.APPLY_SPELL_AFFECT:
        #          for lpaf in self.affected[:]:
        #             if lpaf.type == paf.type and lpaf.level == paf.level \
        #                    and lpaf.location == merc.APPLY_SPELL_AFFECT:
        #               self.affect_remove(lpaf)
        #              break
        # else:
        #    self.affect_modify(paf, False)
        #   self.affect_check(paf.where, paf.bitvector)
        for paf in aff_object.affected:
            if paf.location == merc.APPLY_SPELL_AFFECT:
                logger.error("Bug: Norm-Apply")
                for lpaf in self.affected:
                    if (
                        lpaf.type == paf.type
                        and lpaf.level == paf.level
                        and lpaf.location == merc.APPLY_SPELL_AFFECT
                    ):
                        logger.error("bug: location = %d" % lpaf.location)
                        logger.error("bug: type = %d" % lpaf.type)
                        self.affect_remove(lpaf)
                        break
            else:
                self.affect_modify(paf, False)
                self.affect_check(paf.where, paf.bitvector)

    # Unequip a char with an obj.
    def unequip(self, unequip_from, forced: bool = True, silent: bool = False):
        """
        :param unequip_from:
        :type unequip_from:
        :param replace:
        :type replace:
        :return:
        :rtype:
        """
        if isinstance(unequip_from, int):
            try:
                item = instance.items[unequip_from]
            except:
                return False
        elif isinstance(unequip_from, str):
            try:
                item = instance.items[self.equipped[unequip_from]]
            except:
                return False
        elif hasattr(unequip_from, "is_item") and unequip_from.is_item:
            item = unequip_from
        else:
            return False

        if not item.is_item:
            raise TypeError("Expected item on unequip, got %r" % type(item))
        if not forced:
            return False
        if item.flags.no_remove:
            handler_game.act("You can't remove $p.", self, item, None, merc.TO_CHAR)
            return False
        # AC Removal preceeds the actual clearing of the item from the character equipped dict, and list
        # This is because, apply_ac relies on the item being equipped to figure out its position on the character
        # To determine what to actually apply, or remove.
        self.raw_unequip(item)
        if not silent:
            handler_game.act("$n stops using $p.", self, item, None, merc.TO_ROOM)
            handler_game.act("You stop using $p.", self, item, None, merc.TO_CHAR)
        return True

    def raw_unequip(self, item):
        if not item or not item.is_item:
            return None
        for i in range(4):
            self.armor[i] += item.apply_ac(i)
        if item.flags.two_handed and self.slots.off_hand:
            self.equipped["off_hand"] = None
        self.equipped[item.equipped_to] = None
        self.inventory += [item.instance_id]
        self.remove_affect(item)
        if (
            item.flags.light
            and item.value[2] != 0
            and self.in_room
            and self.in_room.available_light > 0
        ):
            self.in_room.available_light -= 1
        return

    def verbose_wear_strings(self, item, slot):
        """
        :param item:
        :type item:
        :param slot:
        :type slot:
        :return:
        :rtype:
        """
        if slot == "light":
            handler_game.act(
                "$n lights $p and holds it.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You light $p and hold it.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "left_finger":
            handler_game.act(
                "$n wears $p on $s left finger.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p on your left finger.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "right_finger":
            handler_game.act(
                "$n wears $p on $s right finger.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p on your right finger.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "neck":
            handler_game.act(
                "$n wears $p around $s neck.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p around your neck.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "collar":
            handler_game.act(
                "$n wears $p around $s collar.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p around your collar.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "body":
            handler_game.act("$n wears $p on $s torso.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your torso.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "head":
            handler_game.act("$n wears $p on $s head.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your head.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "legs":
            handler_game.act("$n wears $p on $s legs.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your legs.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "feet":
            handler_game.act("$n wears $p on $s feet.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your feet.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "hands":
            handler_game.act("$n wears $p on $s hands.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your hands.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "arms":
            handler_game.act("$n wears $p on $s arms.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You wear $p on your arms.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "about_body":
            handler_game.act(
                "$n wears $p about $s torso.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p about your torso.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "waist":
            handler_game.act(
                "$n wears $p about $s waist.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p about your waist.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "left_wrist":
            handler_game.act(
                "$n wears $p around $s left wrist.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p around your left wrist.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "right_wrist":
            handler_game.act(
                "$n wears $p around $s right wrist.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You wear $p around your right wrist.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "off_hand":
            handler_game.act("$n wears $p as a shield.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p as a shield.", self, item, None, merc.TO_CHAR)
            return
        elif slot == "main_hand":
            handler_game.act("$n wields $p.", self, item, None, merc.TO_ROOM)
            handler_game.act("You wield $p.", self, item, None, merc.TO_CHAR)
            sn = self.get_weapon_sn()
            if sn == "hand to hand":
                return
            skill = self.get_weapon_skill(sn)
            if skill >= 100:
                handler_game.act(
                    "$p feels like a part of you!", self, item, None, merc.TO_CHAR
                )
            elif skill > 85:
                handler_game.act(
                    "You feel quite confident with $p.", self, item, None, merc.TO_CHAR
                )
            elif skill > 70:
                handler_game.act(
                    "You are skilled with $p.", self, item, None, merc.TO_CHAR
                )
            elif skill > 50:
                handler_game.act(
                    "Your skill with $p is adequate.", self, item, None, merc.TO_CHAR
                )
            elif skill > 25:
                handler_game.act(
                    "$p feels a little clumsy in your hands.",
                    self,
                    item,
                    None,
                    merc.TO_CHAR,
                )
            elif skill > 1:
                handler_game.act(
                    "You fumble and almost drop $p.", self, item, None, merc.TO_CHAR
                )
            else:
                handler_game.act(
                    "You don't even know which end is up on $p.",
                    self,
                    item,
                    None,
                    merc.TO_CHAR,
                )
            return
        elif slot == "held":
            handler_game.act("$n holds $p in $s hand.", self, item, None, merc.TO_ROOM)
            handler_game.act(
                "You hold $p in your hand.", self, item, None, merc.TO_CHAR
            )
            return
        elif slot == "float":
            handler_game.act(
                "$n releases $p to float next to $m.", self, item, None, merc.TO_ROOM
            )
            handler_game.act(
                "You release $p and it floats next to you.",
                self,
                item,
                None,
                merc.TO_CHAR,
            )
            return
        else:
            raise LookupError("Unable to find verbose wear string for %s" % slot)
