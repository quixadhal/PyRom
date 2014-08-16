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
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import logging

import object_creator
from world_classes import Gen


logger = logging.getLogger()

import hashlib
import const

import game_utils
import handler_game
import comm
import merc
import save
import settings
import state_checks


def licheck(c):
    if c.lower() == 'l':
        return False
    if c.lower() == 'i':
        return False
    return True


def check_parse_name(name):
    bad_names = ['All', 'Auto', 'Immortal', 'Self', 'Someone', 'Something', 'The', 'You', 'Loner', 'Alander']
    if name in bad_names:
        return False
    
    if 2 > len(name) > 12:
        return False
    
    if not name.isalpha():
        return False
    checked = [licheck(c) for c in name]
    
    if True not in checked:
        return False
    return True


def con_get_name(self):
    argument = self.get_command()
    name = argument.title()

    if not check_parse_name(name):
        self.send("Illegal name, try another.\nName:")

    found, ch = save.load_char_obj(self, name)

    if ch.act.is_set(merc.PLR_DENY):
        logger.info("Denying access to %s@%s" % (ch.name, self.addrport()))
        self.send("You have been denied access.")
        self.deactivate()
        return

    if comm.is_reconnecting(self, name):
        found = True
    
    if settings.WIZLOCK and not ch.is_immortal():
        ch.send("Game is wizlocked")
        self.deactivate()
        return

    if not found and settings.NEWLOCK:
        ch.send("Game is newlocked")
        self.deactivate()
        return

    if found:
        ch.send("Password: ")
        ch.desc.password_mode_on()
        self.set_connected(con_get_old_password)
        return

    ch.send("Did I get that right, %s (Y/N)? " % ch.name)
    self.set_connected(con_confirm_new_name)
    return


def con_confirm_new_name(self):
    argument = self.get_command()[:1].lower()
    ch = self.character
    if argument == 'y':
        ch.send("New character.\nGive me a password for %s: " % ch.name)
        ch.desc.password_mode_on()
        self.set_connected(con_get_new_password)
    elif argument == 'n':
        ch.send("Ok, what IS it, then? ")
        del ch
        self.character = None
        self.set_connected(con_get_name)
    else:
        ch.send("Please type Yes or No? ")


def con_get_new_password(self):
    argument = self.get_command()
    ch = self.character
    if len(argument) < 5:
        ch.send("Password must be at least five characters long.\nPassword: ")
        return
    if settings.ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        pwdnew = hashlib.sha512(argument).hexdigest()
    else:
        pwdnew = argument

    ch.pwd = pwdnew
    
    ch.send("Please retype password: ")
    ch.desc.password_mode_on()
    self.set_connected(con_confirm_new_password)


def con_confirm_new_password(self):
    argument = self.get_command()
    ch = self.character

    if settings.ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        argument = hashlib.sha512(argument).hexdigest()

    if argument != ch.pwd:
        ch.send("Passwords don't match.\nRetype password: ")
        ch.desc.password_mode_on()
        self.set_connected(con_get_new_password)
        return

    ch.desc.password_mode_off()
    ch.send("The following races are available:\n  ")
    for race in const.pc_race_table:
        ch.send("%s " % const.race_table[race].name)
        
    ch.send("\nWhat is your race (help for more information)? ")
    self.set_connected(con_get_new_race)


def con_get_new_race(self):
    argument = self.get_command().lower()
    ch = self.character
    if argument.startswith("help"):
        argument, arg = game_utils.read_word(argument)
        if not argument:
            ch.do_help('race help')
        else:
            ch.do_help(argument)
        ch.send("\nWhat is your race (help for more information)? ")
        return

    race = state_checks.prefix_lookup(const.pc_race_table, argument)

    if not race:
        ch.send("That is not a valid race.\n")
        ch.send("The following races are available:\n  ")
        for race in const.pc_race_table:
            ch.send("%s " % const.race_table[race].name)
        ch.send("\nWhat is your race? (help for more information) ")
        return
    
    ch.race = const.race_table[race.name]
    #initialize stats */
    for i in range(merc.MAX_STATS):
        ch.perm_stat[i] = race.stats[i]
    ch.affected_by.set_bit(const.race_table[race.name].aff)
    ch.imm_flags.set_bit(const.race_table[race.name].imm)
    ch.res_flags.set_bit(const.race_table[race.name].res)
    ch.vuln_flags.set_bit(const.race_table[race.name].vuln)
    ch.form.set_bit(const.race_table[race.name].form)
    ch.parts.set_bit(const.race_table[race.name].parts)

    # add skills */
    for i in race.skills:
        ch.group_add(i, False)

    # add cost */
    ch.points = race.points
    ch.size = race.size

    ch.send("What is your sex (M/F)? ")
    self.set_connected(con_get_new_sex)
    return
        

def con_get_new_sex(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    if argument == 'm':
        ch.sex = merc.SEX_MALE
        ch.true_sex = merc.SEX_MALE
    elif argument == 'f':
        ch.sex = merc.SEX_FEMALE
        ch.true_sex = merc.SEX_FEMALE
    else:
        ch.send("That's not a sex.\nWhat IS your sex? ")
        return

    ch.send("Select a class [[")
    for name, guild in const.guild_table.items():
        ch.send("%s " % guild.name)
    ch.send("]]: ")
    self.set_connected(con_get_new_class)
    return


def con_get_new_class(self):
    argument = self.get_command()
    ch = self.character

    guild = state_checks.prefix_lookup(const.guild_table, argument)

    if not guild:
        ch.send("That's not a class.\nWhat IS your class? ")
        return

    ch.guild = guild

    log_buf = "%s@%s new player." % (ch.name, self.addrport())
    logger.info(log_buf)
    handler_game.wiznet("Newbie alert!  $N sighted.", ch, None, merc.WIZ_NEWBIE, 0, 0)
    handler_game.wiznet(log_buf, None, None, merc.WIZ_SITES, 0, ch.trust)

    ch.send("\nYou may be good, neutral, or evil.\n")
    ch.send("Which alignment (G/N/E)? ")
    self.set_connected(con_get_alignment)
    return


def con_get_alignment(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    if argument == 'g':
        ch.alignment = 750
    elif argument == 'n':
        ch.alignment = 0
    elif argument == 'e':
        ch.alignment = -750
    else:
        ch.send("That's not a valid alignment.\n")
        ch.send("Which alignment (G/N/E)? ")
        return

    ch.send("\n")
    ch.group_add("rom basics", False)
    ch.group_add(ch.guild.base_group, False)
    ch.learned['recall'] = 50
    ch.send("Do you wish to customize this character?\n")
    ch.send("Customization takes time, but allows a wider range of skills and abilities.\n")
    ch.send("Customize (Y/N)? ")
    self.set_connected(con_default_choice)


def con_default_choice(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    ch.send("\n")
    if argument == 'y':
        ch.gen_data = Gen()
        ch.gen_data.points_chosen = ch.points
        ch.do_help("group header")
        ch.list_group_costs()
        ch.send("You already have the following skills:\n")
        ch.do_skills("")
        ch.do_help("menu choice")
        self.set_connected(con_gen_groups)
    elif argument == 'n':
        ch.group_add(ch.guild.default_group, True)
        ch.send("Please pick a weapon from the following choices:\n")
        
        for k, weapon in const.weapon_table.items():
            if weapon.gsn in ch.learned:
                ch.send("%s " % weapon.name)

        ch.send("\nYour choice? ")
        self.set_connected(con_pick_weapon)

    else:
        ch.send("Please answer (Y/N)? ")


def con_pick_weapon(self):
    argument = self.get_command()
    ch = self.character
    weapon = state_checks.prefix_lookup(const.weapon_table, argument)
    if not weapon or ch.learned[weapon.gsn] <= 0:
        ch.send("That's not a valid selection. Choices are:\n")
        for k, weapon in const.weapon_table.items():
            if weapon.gsn in ch.learned:
                ch.send("%s " % weapon.name)

            ch.send("\nYour choice? ")
        return

    ch.learned[weapon.gsn] = 40
    ch.do_help("motd")
    self.set_connected(con_read_motd)


def con_gen_groups(self):
    argument = self.get_command().lower()
    ch = self.character

    if argument == "done":
        if ch.points == const.pc_race_table[ch.race.name].points:
            ch.send("You didn't pick anything.\n")
            return
        if ch.points < 40 + const.pc_race_table[ch.race.name].points:
            ch.send("You must take at least %d points of skills and groups" %
                    (40 + const.pc_race_table[ch.race.name].points))
            return

        ch.send("Creation points: %d\n" % ch.points)
        ch.send("Experience per level: %d\n" % ch.exp_per_level(ch.gen_data.points_chosen))
        if ch.points < 40:
            ch.train = (40 - ch.points + 1) / 2
        del ch.gen_data
        ch.gen_data = None
        ch.send("Please pick a weapon from the following choices:\n")
        
        for w, weapon in const.weapon_table.items():
            if weapon.gsn in ch.learned and ch.learned[weapon.gsn] > 0:
                ch.send("%s " % weapon.name)

        ch.send("\nYour choice? ")
        self.set_connected(con_pick_weapon)
        return

    if not ch.parse_gen_groups(argument):
        ch.send("Choices are: list,learned,premise,add,drop,info,help, and done.\n")
        ch.do_help("menu choice")
        return


def con_get_old_password(self):
    argument = self.get_command()
    ch = self.character
    ch.desc.password_mode_off()
    if settings.ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        pwdcmp = hashlib.sha512(argument).hexdigest()
    else:
        pwdcmp = argument
    if pwdcmp != ch.pwd:
        ch.send("\nWrong password.\n")
        ch.failed_attempts += 1
        if ch.failed_attempts > 3:
            comm.close_socket(self)
        else:
            ch.send("Password: ")
            ch.desc.password_mode_on()
            self.set_connected(con_get_old_password)
        return
    #write_to_buffer( d, echo_on_str, 0 );

    if ch.auth:
        ch.failed_attempts = 0
        ch.send('\nAuthenticator code: ')
        self.set_connected(con_get_timecode)
        return

    ch.send("\n")
    if comm.check_playing(self, ch.name):
        return

    if comm.check_reconnect(self, ch.name, True):
        return

    log_buf = "%s@%s has connected." % (ch.name, self.addrport())
    logger.info(log_buf)
    handler_game.wiznet(log_buf, None, None, merc.WIZ_SITES, 0, ch.trust)
    if ch.is_immortal():
        ch.do_help("imotd")
        self.set_connected(con_read_imotd)
    else:
        ch.do_help("motd")
        self.set_connected(con_read_motd)
    return


def con_get_timecode(self):
    argument = self.get_command()
    ch = self.character

    if not ch.auth.verify(argument):
        ch.send('\nWrong timecode.\n')
        ch.failed_attempts += 1
        if ch.failed_attempts > 3:
            comm.close_socket(self)
        else:
            ch.send('Authenticator code: ')
            self.set_connected(con_get_timecode)
        return

    ch.send("\n")
    if comm.check_playing(self, ch.name):
        return

    if comm.check_reconnect(self, ch.name, True):
        return

    log_buf = "%s@%s has connected." % (ch.name, self.addrport())
    logger.info(log_buf)
    handler_game.wiznet(log_buf, None, None, merc.WIZ_SITES, 0, ch.trust)
    if ch.is_immortal():
        ch.do_help("imotd")
        self.set_connected(con_read_imotd)
    else:
        ch.do_help("motd")
        self.set_connected(con_read_motd)
    return


# RT code for breaking link */
def con_break_connect(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    if argument == 'y':
        for d_old in merc.descriptor_list[:]:
            if d_old == self or not d_old.character:
                continue
            chname = d_old.original if d_old.original else d_old.character
            if ch.name != chname:
                continue
            comm.close_socket(d_old)
        if comm.check_reconnect(self, ch.name, True):
            return
        self.send("Reconnect attempt failed.\nName: ")
        if self.character:
            del self.character
            self.character = None
        self.set_connected(con_get_name)
        return
    if argument == 'n':
        self.send("Name: ")
        if self.character:
            del self.character
            self.character = None
        self.set_connected(con_get_name)
        return

    self.send("Please type Y or N? ")
    return


def con_read_imotd(self):
    ch = self.character
    ch.do_help("motd")
    self.set_connected(con_read_motd)
    

def con_read_motd(self):
    ch = self.character
    if not ch.pwd:
        ch.send("Warning! Null password!\n")
        ch.send("Please report old password with bug.\n")
        ch.send("Type 'password null <new password>' to fix.\n")

    ch.send("\nWelcome to ROM 2.4.  Please do not feed the mobiles.\n")
    ch.reset()
    self.set_connected(con_playing)

    if ch.level == 0:
        ch.perm_stat[ch.guild.attr_prime] += 3
        ch.position = merc.POS_STANDING
        ch.level = 1
        ch.exp = ch.exp_per_level(ch.points)
        ch.hit = ch.max_hit
        ch.mana = ch.max_mana
        ch.move = ch.max_move
        ch.train = 3
        ch.practice = 5
        buf = "the %s" % const.title_table[ch.guild.name][ch.level][ch.sex - 1]
        ch.title = buf

        ch.do_outfit("")
        ch.put(object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_MAP], 0))
        school_id = merc.instances_by_room[merc.ROOM_VNUM_SCHOOL][0]
        school = merc.rooms[school_id]
        school.put(ch)
        ch.do_help("newbie info")

    elif ch.in_room:
        ch.in_room.put(ch)
    elif ch.is_immortal():
        to_instance_id = merc.instances_by_room[merc.ROOM_VNUM_CHAT][0]
        to_instance = merc.rooms[to_instance_id]
        to_instance.put(ch)
    else:
        to_instance_id = merc.instances_by_room[merc.ROOM_VNUM_TEMPLE][0]
        to_instance = merc.rooms[to_instance_id]
        to_instance.put(ch)

    handler_game.act("$n has entered the game.", ch, None, None, merc.TO_ROOM)
    ch.do_look("auto")
    ch.send("\n\n")
    ch.do_term("")

    handler_game.wiznet("$N has left real life behind.", ch, None, merc.WIZ_LOGINS, merc.WIZ_SITES, ch.trust)
    if ch.pet:
        ch.in_room.put(ch.pet)
        handler_game.act("$n has entered the game.", ch.pet, None, None, merc.TO_ROOM)


def con_playing(self):
    command = self.get_command()
    if not command.strip():
        return
    handler_game.substitute_alias(self, command)

