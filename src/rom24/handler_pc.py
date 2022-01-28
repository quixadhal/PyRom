import os
import random
import time
import json
import copy
import hashlib
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import instance
from rom24 import handler_game
from rom24 import merc
from rom24 import const
from rom24 import interp
from rom24 import living
from rom24 import settings
from rom24 import state_checks
from rom24 import update
from rom24 import handler_item


class Pc(living.Living):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None, **kwargs):
        from rom24 import handler_item

        super().__init__()
        self.is_pc = True
        self.buffer = []
        self.valid = False
        self.pwd = ""
        self.trust = 1
        self.auth = None
        self.failed_attempts = 0
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
        self.gen_data = None
        self.prompt = "<%hhp %mm %vmv> "
        self.prefix = ""
        self.lines = 22
        self.played = 0
        self.logon = 0
        self.practice = 0
        self.train = 0
        self.dampen = False
        self._last_login = time.time()
        self._last_logout = None
        self._saved_room_vnum = merc.ROOM_VNUM_TEMPLE
        if template or kwargs:
            if template and not kwargs:
                self.name = template
                self.instancer()
            if kwargs:
                [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]
                if self._fighting:
                    self._fighting = None
                    self.position = merc.POS_STANDING
                if self.environment:
                    if self._environment not in instance.global_instances.keys():
                        self.environment = None
                if self.inventory:
                    for instance_id in self.inventory[:]:
                        handler_item.Items.load(
                            instance_id=instance_id, player_name=self.name
                        )
                for item_id in self.equipped.values():
                    if item_id:
                        handler_item.Items.load(
                            instance_id=item_id, player_name=self.name
                        )
            self.instance_setup()
        if self.instance_id:
            Pc.instance_count += 1
        else:
            Pc.template_count += 1
        self._last_saved = None
        self._md5 = None

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                Pc.instance_count -= 1
                if instance.players.get(self.instance_id, None):
                    self.instance_destructor()
            else:
                Pc.template_count -= 1
        except:
            return

    def __repr__(self):
        return "<PC: %s ID %d>" % (self.name, self.instance_id)

    def instance_setup(self):
        instance.global_instances[self.instance_id] = self
        instance.characters[self.instance_id] = self
        instance.players[self.instance_id] = self
        if self.name not in instance.instances_by_player.keys():
            instance.instances_by_player[self.name] = [self.instance_id]
        else:
            instance.instances_by_player[self.name] += [self.instance_id]

    def instance_destructor(self):
        instance.instances_by_player[self.name].remove(self.instance_id)
        del instance.players[self.instance_id]
        del instance.characters[self.instance_id]
        del instance.global_instances[self.instance_id]

    def absorb(self, *args):
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if self.is_npc():
            return
        nospace = [".", ",", "!", "?"]
        if title[0] in nospace:
            self._title = title
        else:
            self._title = " " + title

    def get_age(self):
        return 17 + (self.played + int(time.time() - self.logon)) // 72000

    # command for returning max training score
    def get_max_train(self, stat):
        max = const.pc_race_table[self.race.name].max_stats[stat]
        if self.guild.attr_prime == stat:
            if self.race.name == "human":
                max += 3
            else:
                max += 2
        return min(max, 25)

    # recursively adds a group given its number -- uses group_add */
    def gn_add(self, gn):
        self.group_known[gn.name] = True
        for i in gn.spells:
            if not i:
                break
            self.group_add(i, False)

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
        if self.is_npc():  # NPCs do not have skills */
            return

        if name in const.skill_table:
            sn = const.skill_table[name]
            if sn.name not in self.learned:  # i.e. not known */
                self.learned[sn.name] = 1
            if deduct:
                self.points += sn.rating[self.guild.name]
            return

        # now check groups */

        if name in const.group_table:
            gn = const.group_table[name]
            if gn.name not in self.group_known:
                self.group_known[gn.name] = True
            if deduct:
                self.points += gn.rating[self.guild.name]

            self.gn_add(gn)  # make sure all skills in the group are known */

    # used for processing a skill or group for deletion -- no points back! */
    def group_remove(self, name):
        if name in const.skill_table:
            sn = const.skill_table[name]
            if sn.name in self.learned:
                del self.learned[sn.name]
                return

        # now check groups */
        if name in const.group_table:
            gn = const.group_table[name]

            if gn.name in self.group_known:
                del self.group_known[gn.name]
                self.gn_remove(gn)  # be sure to call gn_add on all remaining groups */

    # shows skills, groups and costs (only if not bought) */
    def list_group_costs(self):
        if self.is_npc():
            return
        col = 0
        self.send(
            "%-18s %-5s %-18s %-5s %-18s %-5s\n"
            % ("group", "cp", "group", "cp", "group", "cp")
        )

        for gn, group in const.group_table.items():
            if (
                gn not in self.gen_data.group_chosen
                and gn not in self.group_known
                and group.rating[self.guild.name] > 0
            ):
                self.send(
                    "%-18s %-5d "
                    % (const.group_table[gn].name, group.rating[self.guild.name])
                )
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send("\n")
        self.send("\n")
        col = 0

        self.send(
            "%-18s %-5s %-18s %-5s %-18s %-5s\n"
            % ("skill", "cp", "skill", "cp", "skill", "cp")
        )

        for sn, skill in const.skill_table.items():
            if (
                sn not in self.gen_data.skill_chosen
                and sn not in self.learned
                and skill.spell_fun is None
                and skill.rating[self.guild.name] > 0
            ):
                self.send("%-18s %-5d " % (skill.name, skill.rating[self.guild.name]))
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send("\n")
        self.send("\n")

        self.send("Creation points: %d\n" % self.points)
        self.send(
            "Experience per level: %d\n"
            % self.exp_per_level(self.gen_data.points_chosen)
        )
        return

    def list_group_chosen(self):
        if self.is_npc():
            return
        col = 0
        self.send(
            "%-18s %-5s %-18s %-5s %-18s %-5s"
            % ("group", "cp", "group", "cp", "group", "cp\n")
        )

        for gn, group in const.group_table.items():
            if gn in self.gen_data.group_chosen and group.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (group.name, group.rating[self.guild.name]))
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send("\n")
        self.send("\n")

        col = 0

        self.send(
            "%-18s %-5s %-18s %-5s %-18s %-5s"
            % ("skill", "cp", "skill", "cp", "skill", "cp\n")
        )

        for sn, skill in const.skill_table.items():
            if sn in self.gen_data.skill_chosen and skill.rating[self.guild.name] > 0:
                self.send("%-18s %-5d " % (skill.name, skill.rating[self.guild.name]))
                col += 1
                if col % 3 == 0:
                    self.send("\n")
        if col % 3 != 0:
            self.send("\n")
        self.send("\n")

        self.send("Creation points: %d\n" % self.gen_data.points_chosen)
        self.send(
            "Experience per level: %d\n"
            % self.exp_per_level(self.gen_data.points_chosen)
        )
        return

    # this procedure handles the input parsing for the skill generator */
    def parse_gen_groups(self, argument):
        from rom24.game_utils import read_word

        if not argument.strip():
            return False

        argument, arg = read_word(argument)
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
            if argument in const.group_table:
                gn = const.group_table[argument]
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

            if argument in const.skill_table:
                sn = const.skill_table[argument]
                if sn.name in self.gen_data.skill_chosen or sn.name in self.learned:
                    self.send("You already know that skill!\n")
                    return True

                if sn.rating[self.guild.name] < 1 or sn.spell_fun is not None:
                    self.send("That skill is not available.\n")
                    return True
                # Close security hole */
                if self.gen_data.points_chosen + sn.rating[self.guild.name] > 300:
                    self.send("You cannot take more than 300 creation points.\n")
                    return True

                self.send("%s skill added\n" % sn.name)
                self.gen_data.skill_chosen[sn.name] = True
                self.gen_data.points_chosen += sn.rating[self.guild.name]
                self.learned[sn] = 1
                self.points += sn.rating[self.guild.name]
                return True

            self.send("No skills or groups by that name...\n")
            return True

        if "drop".startswith(arg):
            if not argument:
                self.send("You must provide a skill to drop.\n")
                return True

            argument = argument.lower()
            if argument in const.group_table and argument in self.gen_data.group_chosen:
                gn = const.group_table[argument]
                self.send("Group dropped.\n")
                del self.gen_data.group_chosen[gn.name]
                self.gen_data.points_chosen -= gn.rating[self.guild.name]
                self.gn_remove(gn)
                for k, v in self.gen_data.group_chosen:
                    self.gn_add(const.group_table[k])
                self.points -= gn.rating[self.guild.name]
                return True

            if argument in const.skill_table and argument in self.gen_data.skill_chosen:
                sn = const.skill_table[argument]
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
            sn = const.skill_table[sn]

        if (
            self.level < sn.skill_level[self.guild.name]
            or sn.rating[self.guild.name] == 0
            or sn.name not in self.learned
            or self.learned[sn.name] == 100
        ):
            return  # skill is not known */

        # check to see if the character has a chance to learn */
        chance = 10 * const.int_app[self.stat(merc.STAT_INT)].learn
        chance //= multiplier * sn.rating[self.guild.name] * 4
        chance += self.level

        if random.randint(1, 1000) > chance:
            return

        # now that the character has a CHANCE to learn, see if they really have */

        if success:
            chance = max(5, min(100 - self.learned[sn.name], 95))
            if random.randint(1, 99) < chance:
                self.send("You have become better at %s!\n" % sn.name)
                self.learned[sn.name] += 1
                update.gain_exp(self, 2 * sn.rating[self.guild.name])
        else:
            chance = max(5, min(self.learned[sn.name] / 2, 30))
            if random.randint(1, 99) < chance:
                self.send(
                    "You learn from your mistakes, and your %s skill improves.\n"
                    % sn.name
                )
                self.learned[sn.name] += random.randint(1, 3)
                self.learned[sn.name] = min(self.learned[sn.name], 100)
                update.gain_exp(self, 2 * sn.rating[self.guild.name])

    def check_social(ch, command, argument):
        cmd = None
        for social in merc.social_list:
            if social.name.lower().startswith(command):
                cmd = social
        if not cmd:
            return False
        if not ch.is_npc() and ch.comm.is_set(merc.COMM_NOEMOTE):
            ch.send("You are anti-social!\n")
            return True

        if ch.position == merc.POS_DEAD:
            ch.send("Lie still; you are DEAD.\n")
            return True
        if ch.position == merc.POS_INCAP or ch.position == merc.POS_MORTAL:
            ch.send("You are hurt far too bad for that.\n")
            return True
        if ch.position == merc.POS_STUNNED:
            ch.send("You are too stunned to do that.\n")
            return True
        if ch.position == merc.POS_SLEEPING:
            # I just know this is the path to a 12" 'if' statement.  :(
            # But two players asked for it already!  -- Furey
            if cmd.name != "snore":
                ch.send("In your dreams, or what?\n")
                return True
        holder, arg = game_utils.read_word(argument)
        victim = ch.get_char_room(arg)
        if not arg:
            handler_game.act(cmd.others_no_arg, ch, None, victim, merc.TO_ROOM)
            handler_game.act(cmd.char_no_arg, ch, None, victim, merc.TO_CHAR)
        elif not victim:
            ch.send("They aren't here.\n")
        elif victim == ch:
            handler_game.act(cmd.others_auto, ch, None, victim, merc.TO_ROOM)
            handler_game.act(cmd.char_auto, ch, None, victim, merc.TO_CHAR)
        else:
            handler_game.act(cmd.others_found, ch, None, victim, merc.TO_NOTVICT)
            handler_game.act(cmd.char_found, ch, None, victim, merc.TO_CHAR)
            handler_game.act(cmd.vict_found, ch, None, victim, merc.TO_VICT)

            if (
                not ch.is_npc()
                and victim.is_npc()
                and not victim.is_affected(merc.AFF_CHARM)
                and state_checks.IS_AWAKE(victim)
                and victim.desc is None
            ):
                num = random.randint(0, 12)
                if num in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                    handler_game.act(
                        cmd.others_found, victim, None, ch, merc.TO_NOTVICT
                    )
                    handler_game.act(cmd.char_found, victim, None, ch, merc.TO_CHAR)
                    handler_game.act(cmd.vict_found, victim, None, ch, merc.TO_VICT)

                elif num in [9, 10, 11, 12]:
                    handler_game.act("$n slaps $N.", victim, None, ch, merc.TO_NOTVICT)
                    handler_game.act("You slap $N.", victim, None, ch, merc.TO_CHAR)
                    handler_game.act("$n slaps you.", victim, None, ch, merc.TO_VICT)
        return True

    def interpret(self, argument):
        logger.debug("Char %s ran %s", self.name, argument)

        # Strip leading spaces.
        argument = argument.lstrip()

        # No hiding.
        self.affected_by.rem_bit(merc.AFF_HIDE)

        # Implement freeze command.
        if not self.is_npc() and self.act.is_set(merc.PLR_FREEZE):
            self.send("You're totally frozen!\n")
            return
        # Grab the command word.
        # Special parsing so ' can be a command,
        #   also no spaces needed after punctuation.
        logline = argument
        if not argument[0].isalpha() and not argument[0].isdigit():
            command = argument[0]
            argument = argument[:1].lstrip()
        else:
            argument, command = game_utils.read_word(argument)
        # Look for command in command table.
        trust = self.trust
        cmd = state_checks.prefix_lookup(interp.cmd_table, command)
        if cmd is not None:
            if cmd.level > trust:
                cmd = None

        # * Log and snoop.
        if (
            (not self.is_npc() and self.act.is_set(merc.PLR_LOG))
            or settings.LOGALL
            or (cmd and cmd.log == merc.LOG_ALWAYS)
        ):
            if cmd and cmd.log != merc.LOG_NEVER:
                log_buf = "Log %s: %s" % (self.name, logline)
                handler_game.wiznet(log_buf, self, None, merc.WIZ_SECURE, 0, self.trust)
                logger.info(log_buf)
        if self.desc and self.desc.snoop_by:
            self.desc.snoop_by.send("% ")
            self.desc.snoop_by.send(logline)
            self.desc.snoop_by.send("\n")
        if not cmd:
            # * Look for command in socials table.
            if not Pc.check_social(self, command, argument):
                if settings.DETAILED_INVALID_COMMANDS:
                    # TODO: Levenshtein distance over cmd_table, also add a wait_state to prevent horrors
                    self.send("Huh? '%s' is not a valid command." % command)
                else:
                    self.send("Huh?\n")
            return
        # * Pc not in position for command?
        if self.position < cmd.position:
            if self.position == merc.POS_DEAD:
                self.send("Lie still; you are DEAD.\n")
            elif self.position == merc.POS_MORTAL or self.position == merc.POS_INCAP:
                self.send("You are hurt far too bad for that.\n")
            elif self.position == merc.POS_STUNNED:
                self.send("You are too stunned to do that.\n")
            elif self.position == merc.POS_SLEEPING:
                self.send("In your dreams, or what?\n")
            elif self.position == merc.POS_RESTING:
                self.send("Nah... You feel too relaxed...\n")
            elif self.position == merc.POS_SITTING:
                self.send("Better stand up first.\n")
            elif self.position == merc.POS_FIGHTING:
                self.send("No way!  You are still fighting!\n")
            return

        # Dispatch the command.
        if cmd.default_arg:
            cmd.do_fun(self, cmd.default_arg)
            return
        cmd.do_fun(self, argument.lstrip())

    # Serialization
    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            elif str(k) in ("desc", "send"):
                continue
            elif str(k) in ("_last_saved", "_md5"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = "__class__/" + __name__ + "." + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = "__class__/" + __name__ + "." + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data

    def save_stub(self, logout: bool = False):
        if logout:
            self._last_logout = time.time()
        pathname = os.path.join(
            settings.PLAYER_DIR, self.name[0].lower(), self.name.capitalize()
        )
        os.makedirs(pathname, 0o755, True)
        filename = os.path.join(pathname, "login.json")
        stub = dict({})
        stub["name"] = self.name
        stub["pwd"] = self.pwd
        stub["auth"] = self.auth
        stub["is_immortal"] = self.is_immortal()
        stub["is_banned"] = self.act.is_set(merc.PLR_DENY)
        stub["instance_id"] = self.instance_id
        stub["last_login"] = self._last_login
        stub["last_logout"] = self._last_logout
        stub["room"] = self._saved_room_vnum
        js = json.dumps(stub, default=instance.to_json, indent=4, sort_keys=True)
        with open(filename, "w") as fp:
            fp.write(js)

    @classmethod
    def load_stub(cls, player_name: str = None):
        if not player_name:
            raise KeyError("Player name is required to load a player!")

        pathname = os.path.join(
            settings.PLAYER_DIR, player_name[0].lower(), player_name.capitalize()
        )
        filename = os.path.join(pathname, "login.json")

        if os.path.isfile(filename):
            logger.info("Loading %s player stub data", player_name)
            with open(filename, "r") as fp:
                data = json.load(fp, object_hook=instance.from_json)
            if isinstance(data, dict):
                return data
            else:
                logger.error("Could not load player stub file for %s", player_name)
                return None
        else:
            logger.error("Could not open player stub file for %s", player_name)
            return None

    def save(self, logout: bool = False, force: bool = False):
        if self._last_saved is None:
            self._last_saved = time.time() - settings.SAVE_LIMITER - 2
        if not force and time.time() < self._last_saved + settings.SAVE_LIMITER:
            return

        self._last_saved = time.time()
        self.save_stub(logout)
        pathname = os.path.join(
            settings.PLAYER_DIR, self.name[0].lower(), self.name.capitalize()
        )
        os.makedirs(pathname, 0o755, True)
        filename = os.path.join(pathname, "player.json")
        # logger.info('Saving %s', filename)
        js = json.dumps(self, default=instance.to_json, indent=4, sort_keys=True)
        md5 = hashlib.md5(js.encode("utf-8")).hexdigest()
        if self._md5 != md5:
            self._md5 = md5
            with open(filename, "w") as fp:
                fp.write(js)

        if self.inventory:
            for item_id in self.inventory[:]:
                if item_id not in instance.items:
                    # logger.error('Item %d is in Player %s\'s inventory, but does not exist?', item_id, self.name)
                    continue
                item = instance.items[item_id]
                item.save(in_inventory=True, player_name=self.name, force=force)
        for item_id in self.equipped.values():
            if item_id:
                if item_id not in instance.items:
                    # logger.error('Item %d is in Player %s\'s inventory, but does not exist?', item_id, self.name)
                    continue
                item = instance.items[item_id]
                item.save(is_equipped=True, player_name=self.name, force=force)

    @classmethod
    def load(cls, player_name: str = None):
        if not player_name:
            raise KeyError("Player name is required to load a player!")

        pathname = os.path.join(
            settings.PLAYER_DIR, player_name[0].lower(), player_name.capitalize()
        )
        filename = os.path.join(pathname, "player.json")

        if os.path.isfile(filename):
            logger.info("Loading %s player data", player_name)
            with open(filename, "r") as fp:
                obj = json.load(fp, object_hook=instance.from_json)
            if isinstance(obj, Pc):
                obj._last_login = time.time()
                obj._last_logout = None
                # This just ensures that all items the player has are actually loaded.
                if obj.inventory:
                    for item_id in obj.inventory[:]:
                        handler_item.Items.load(
                            instance_id=item_id, player_name=player_name
                        )
                for item_id in obj.equipped.values():
                    if item_id:
                        handler_item.Items.load(
                            instance_id=item_id, player_name=player_name
                        )
                return obj
            else:
                logger.error("Could not load player file for %s", player_name)
                return None
        else:
            logger.error("Could not open player file for %s", player_name)
            return None
