import random
import logging
import time

logger = logging.getLogger()

import game_utils
import handler_game
import handler_log
from interp import cmd_table

from living import Living
from settings import LOGALL
import state_checks
from const import group_table, skill_table, \
    int_app
from merc import STAT_INT, TO_CHAR, TO_VICT, TO_NOTVICT, AFF_CHARM, TO_ROOM, POS_SLEEPING, POS_STUNNED, POS_MORTAL, \
    POS_INCAP, POS_DEAD, COMM_NOEMOTE, social_list, POS_FIGHTING, POS_SITTING, POS_RESTING, WIZ_SECURE, LOG_NEVER, \
    LOG_ALWAYS, PLR_LOG, PLR_FREEZE, AFF_HIDE, gdf
from update import gain_exp


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

    def get_age(self):
            return 17 + (self.played + int(time.time() - self.logon)) // 72000

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
            if sn.name not in self.learned: # i.e. not known */
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

        self.send("Creation points: %d\n" % self.points)
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
        from game_utils import read_word
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

    logged = handler_log.logged("Debug", True) if gdf is True else handler_log.logged("Debug", False)

    @logged
    def interpret(self, argument):
        # Strip leading spaces.
        argument = argument.lstrip()

        # No hiding.
        self.affected_by.rem_bit(AFF_HIDE)

        # Implement freeze command.
        if not self.is_npc() and self.act.is_set(PLR_FREEZE):
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
        cmd = state_checks.prefix_lookup(cmd_table, command)
        if cmd is not None:
            if cmd.level > trust:
                cmd = None

        #* Log and snoop.
        if (not self.is_npc() and self.act.is_set(PLR_LOG)) or LOGALL or (cmd and cmd.log == LOG_ALWAYS):
            if cmd and cmd.log != LOG_NEVER:
                log_buf = "Log %s: %s" % (self.name, logline)
                handler_game.wiznet(log_buf, self, None, WIZ_SECURE, 0, self.trust)
                logger.info(log_buf)
        if self.desc and self.desc.snoop_by:
            self.desc.snoop_by.send("% ")
            self.desc.snoop_by.send(logline)
            self.desc.snoop_by.send("\n")
        if not cmd:
            #* Look for command in socials table.
            if not check_social(self, command, argument):
                self.send("Huh?\n")
            return
        #* Character not in position for command?
        if self.position < cmd.position:
            if self.position == POS_DEAD:
                self.send("Lie still; you are DEAD.\n")
            elif self.position == POS_MORTAL \
                    or self.position == POS_INCAP:
                self.send("You are hurt far too bad for that.\n")
            elif self.position == POS_STUNNED:
                self.send("You are too stunned to do that.\n")
            elif self.position == POS_SLEEPING:
                self.send("In your dreams, or what?\n")
            elif self.position == POS_RESTING:
                self.send("Nah... You feel too relaxed...\n")
            elif self.position == POS_SITTING:
                self.send("Better stand up first.\n")
            elif self.position == POS_FIGHTING:
                self.send("No way!  You are still fighting!\n")
            return

        # Dispatch the command.
        if cmd.default_arg:
            cmd.do_fun(self, cmd.default_arg)
            return
        cmd.do_fun(self, argument)


    def check_social(ch, command, argument):
        cmd = None
        for social in social_list:
            if social.name.lower().startswith(command):
                cmd = social
        if not cmd:
            return False
        if not ch.is_npc() and ch.comm.is_set(COMM_NOEMOTE):
            ch.send("You are anti-social!\n")
            return True

        if ch.position == POS_DEAD:
            ch.send("Lie still; you are DEAD.\n")
            return True
        if ch.position == POS_INCAP or ch.position == POS_MORTAL:
            ch.send("You are hurt far too bad for that.\n")
            return True
        if ch.position == POS_STUNNED:
            ch.send("You are too stunned to do that.\n")
            return True
        if ch.position == POS_SLEEPING:
            # I just know this is the path to a 12" 'if' statement.  :(
            # But two players asked for it already!  -- Furey
            if cmd.name != "snore":
                ch.send("In your dreams, or what?\n")
                return True
        holder, arg = game_utils.read_word(argument)
        victim = ch.get_char_room(arg)
        if not arg:
            handler_game.act(cmd.others_no_arg, ch, None, victim, TO_ROOM)
            handler_game.act(cmd.char_no_arg, ch, None, victim, TO_CHAR)
        elif not victim:
            ch.send("They aren't here.\n")
        elif victim == ch:
            handler_game.act(cmd.others_auto, ch, None, victim, TO_ROOM)
            handler_game.act(cmd.char_auto, ch, None, victim, TO_CHAR)
        else:
            handler_game.act(cmd.others_found, ch, None, victim, TO_NOTVICT)
            handler_game.act(cmd.char_found, ch, None, victim, TO_CHAR)
            handler_game.act(cmd.vict_found, ch, None, victim, TO_VICT)

            if not ch.is_npc() and victim.is_npc() \
                    and not victim.is_affected( AFF_CHARM) \
                    and state_checks.IS_AWAKE(victim) and victim.desc is None:
                num = random.randint(0, 12)
                if num in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                    handler_game.act(cmd.others_found, victim, None, ch, TO_NOTVICT)
                    handler_game.act(cmd.char_found, victim, None, ch, TO_CHAR)
                    handler_game.act(cmd.vict_found, victim, None, ch, TO_VICT)

                elif num in [9, 10, 11, 12]:
                    handler_game.act("$n slaps $N.", victim, None, ch, TO_NOTVICT)
                    handler_game.act("You slap $N.", victim, None, ch, TO_CHAR)
                    handler_game.act("$n slaps you.", victim, None, ch, TO_VICT)
        return True
