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
import hashlib
import time
from merc import *
from settings import *
from const import race_table, pc_race_table, guild_table, weapon_table, title_table
from save import load_char_obj
from db import read_word, create_object
from skills import *
from handler import wiznet
from alias import substitute_alias
import comm

def licheck(c):
    if c.lower() == 'l':
        return False
    if c.lower() == 'i':
        return False
    
    return True
def check_parse_name( name ):
    bad_names = ['All', 'Auto', 'Immortal', 'Self', 'Someone', 'Something', 'The', 'You', 'Loner', 'Alander']
    if name in bad_names:
        return False
    
    if len(name) < 2 or len(name) >12:
        return False
    
    if not name.isalpha():
        return False
    checked = [licheck(c) for c in name ]
    
    if True not in checked:
        return False
    
    return True

def con_get_name( self ):
    argument = self.get_command()

    name = argument.title()

    if not check_parse_name(name):
        self.send("Illegal name, try another.\r\nName:")

    found,ch = load_char_obj(self,name)

    if IS_SET( ch.act, PLR_DENY ):
        print ("Denying access to %s@%s" % (ch.name, self.addrport()))
        self.send("You have been denied access.")
        self.deactivate()
        return

    if comm.is_reconnecting(self, name):
        found = True
    
    if WIZLOCK and not IS_IMMORTAL(ch):
        ch.send("Game is wizlocked")
        self.deactivate()
        return
    if not found and NEWLOCK:
        ch.send("Game is newlocked")
        self.deactivate()
        return

    if found:
        ch.send("Password: ")
        self.set_connected(con_get_old_password)
        return

    ch.send("Did I get that right, %s (Y/N)? " % ch.name )
    self.set_connected(con_confirm_new_name)
    return

def con_confirm_new_name(self):
    argument = self.get_command()[:1].lower()
    ch = self.character
    if argument == 'y':
        ch.send("New character.\nGive me a password for %s: " % ch.name)
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
    if ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        pwdnew = hashlib.sha512( argument ).hexdigest()
    else:
        pwdnew = argument

    ch.pcdata.pwd = pwdnew
    
    ch.send("Please retype password: ")
    self.set_connected(con_confirm_new_password)

def con_confirm_new_password(self):
    argument = self.get_command()
    ch = self.character

    if ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        argument = hashlib.sha512( argument ).hexdigest()

    if argument != ch.pcdata.pwd:
        ch.send("Passwords don't match.\r\nRetype password: ")
        self.set_connected(con_get_new_password)
        return

    ch.send("The following races are available:\n  ")
    for race in pc_race_table:
        ch.send("%s " % race_table[race].name )
        
    ch.send("\nWhat is your race (help for more information)? ")
    self.set_connected(con_get_new_race)

def con_get_new_race(self):
    argument = self.get_command().lower()
    ch = self.character
    if argument.startswith("help"):
        argument, arg = read_word(argument)
        if not argument:
            ch.do_help('race help')
        else:
            ch.do_help(argument)
        ch.send( "\r\nWhat is your race (help for more information)? ")
        return

    race = prefix_lookup(pc_race_table, argument)

    if not race:
        ch.send("That is not a valid race.\n")
        ch.send("The following races are available:\n  ")
        for race in pc_race_table:
            ch.send("%s " % race_table[race].name )
        ch.send("\r\nWhat is your race? (help for more information) ")
        return
    
    ch.race = race_table[race.name]
    #initialize stats */
    for i in range(MAX_STATS):
        ch.perm_stat[i] = race.stats[i]
    ch.affected_by = ch.affected_by|race_table[race.name].aff
    ch.imm_flags   = ch.imm_flags|race_table[race.name].imm
    ch.res_flags   = ch.res_flags|race_table[race.name].res
    ch.vuln_flags  = ch.vuln_flags|race_table[race.name].vuln
    ch.form    = race_table[race.name].form
    ch.parts   = race_table[race.name].parts

    # add skills */
    for i in race.skills:
        group_add(ch,i,False)

    # add cost */
    ch.pcdata.points = race.points
    ch.size = race.size

    ch.send("What is your sex (M/F)? ")
    self.set_connected(con_get_new_sex)
    return
        

def con_get_new_sex(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    if argument == 'm':
        ch.sex = SEX_MALE
        ch.pcdata.true_sex = SEX_MALE
    elif argument == 'f':
        ch.sex = SEX_FEMALE
        ch.pcdata.true_sex = SEX_FEMALE
    else:
        ch.send("That's not a sex.\nWhat IS your sex? ")
        return

    ch.send("Select a class [" )
    for name, guild in guild_table.items():
        ch.send("%s " % guild.name )
    ch.send("]: ")
    self.set_connected(con_get_new_class)
    return

def con_get_new_class(self):
    argument = self.get_command()
    ch = self.character

    guild = prefix_lookup(guild_table, argument)

    if not guild:
        ch.send("That's not a class.\nWhat IS your class? ")
        return

    ch.guild = guild

    log_buf = "%s@%s new player." % ( ch.name, self.addrport() )
    print (log_buf)
    wiznet("Newbie alert!  $N sighted.",ch,None,WIZ_NEWBIE,0,0)
    wiznet(log_buf,None,None,WIZ_SITES,0,ch.get_trust())

    ch.send("\r\nYou may be good, neutral, or evil.\n")
    ch.send("Which alignment (G/N/E)? ")
    self.set_connected(con_get_alignment)
    return

def con_get_alignment(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    if argument == 'g': ch.alignment = 750
    elif argument == 'n': ch.alignment = 0
    elif argument == 'e': ch.alignment = -750
    else:
        ch.send("That's not a valid alignment.\n")
        ch.send("Which alignment (G/N/E)? ")
        return

    ch.send("\n")
    group_add(ch,"rom basics",False)
    group_add(ch,ch.guild.base_group,False)
    ch.pcdata.learned['recall'] = 50
    ch.send("Do you wish to customize this character?\n")
    ch.send("Customization takes time, but allows a wider range of skills and abilities.\n")
    ch.send("Customize (Y/N)? ")
    self.set_connected(con_default_choice)

def con_default_choice(self):
    argument = self.get_command()[:1].lower()
    ch = self.character

    ch.send("\r\n")
    if argument == 'y':
        ch.gen_data = GEN_DATA()
        ch.gen_data.points_chosen = ch.pcdata.points
        ch.do_help("group header")
        list_group_costs(ch)
        ch.send("You already have the following skills:\n")
        ch.do_skills("")
        ch.do_help("menu choice")
        self.set_connected(con_gen_groups)
    elif argument == 'n':
        group_add(ch,ch.guild.default_group,True)
        ch.send("Please pick a weapon from the following choices:\n")
        
        for k,weapon in weapon_table.items():
            if weapon.gsn in ch.pcdata.learned:
                ch.send("%s " % weapon.name)

        ch.send("\nYour choice? ")
        self.set_connected(con_pick_weapon)

    else:
        ch.send("Please answer (Y/N)? ")

def con_pick_weapon(self):
    argument = self.get_command()
    ch = self.character
    weapon = prefix_lookup(weapon_table, argument )
    if not weapon or ch.pcdata.learned[weapon.gsn] <= 0:
        ch.send("That's not a valid selection. Choices are:\n")
        for k,weapon in weapon_table.items():
            if weapon.gsn in ch.pcdata.learned:
                ch.send("%s " % weapon.name)

            ch.send("\nYour choice? ")
        return

    ch.pcdata.learned[weapon.gsn] = 40
    ch.do_help("motd")
    self.set_connected(con_read_motd)

def con_gen_groups(self):
    argument = self.get_command().lower()
    ch = self.character

    if argument == "done":
        if ch.pcdata.points == pc_race_table[ch.race.name].points:
            ch.send("You didn't pick anything.\n")
            return
        if ch.pcdata.points < 40 + pc_race_table[ch.race.name].points:
            ch.send("You must take at least %d points of skills and groups" % (40 + pc_race_table[ch.race.name].points))
            return

        ch.send("Creation points: %d\n" % ch.pcdata.points )
        ch.send("Experience per level: %d\n" % ch.exp_per_level(ch.gen_data.points_chosen))
        if ch.pcdata.points < 40:
            ch.train = (40 - ch.pcdata.points + 1) / 2
        del ch.gen_data
        ch.gen_data = None
        ch.send("Please pick a weapon from the following choices:\n")
        
        for w, weapon in weapon_table.items():
            if ch.pcdata.learned[weapon.gsn] > 0:
                ch.send("%s " % weapon.name)

        ch.send("\nYour choice? ")
        self.set_connected(con_pick_weapon)
        return

    if not parse_gen_groups(ch,argument):
        ch.send("Choices are: list,learned,premise,add,drop,info,help, and done.\n")
        ch.do_help("menu choice")
        return

def con_get_old_password(self):
    argument = self.get_command()
    ch = self.character
    ch.send("\n")
    pwdcmp = ""
    if ENCRYPT_PASSWORD:
        argument = argument.encode('utf8')
        pwdcmp = hashlib.sha512( argument ).hexdigest()
    else:
        pwdcmp = argument
    if pwdcmp != ch.pcdata.pwd:
        ch.send("Wrong password.\n")
        comm.close_socket( self )
        return
    #write_to_buffer( d, echo_on_str, 0 );

    if comm.check_playing(self, ch.name):
        return

    if comm.check_reconnect(self, ch.name, True):
        return

    log_buf = "%s@%s has connected." % (ch.name, self.addrport())
    print (log_buf)
    wiznet(log_buf,None,None,WIZ_SITES,0,ch.get_trust())
    if IS_IMMORTAL(ch):
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
        for d_old in descriptor_list[:]:
            if d_old == self or not d_old.character:
                continue
            chname = d_old.original if d_old.original else d_old.character
            if ch.name != chname:
                continue
            close_socket(d_old)
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
    if not ch.pcdata or not ch.pcdata.pwd:
        ch.send("Warning! Null password!\n")
        ch.send("Please report old password with bug.\n")
        ch.send("Type 'password null <new password>' to fix.\n")

    ch.send("\nWelcome to ROM 2.4.  Please do not feed the mobiles.\n")
    char_list.append(ch)
    ch.reset()
    self.set_connected(con_playing)

    if ch.level == 0:
        ch.perm_stat[ch.guild.attr_prime] += 3
        ch.position = POS_STANDING
        ch.level   = 1
        ch.exp = ch.exp_per_level(ch.pcdata.points)
        ch.hit = ch.max_hit
        ch.mana    = ch.max_mana
        ch.move    = ch.max_move
        ch.train    = 3
        ch.practice = 5
        buf = "the %s" % title_table[ch.guild.name][ch.level][ch.sex-1]
        set_title( ch, buf )

        ch.do_outfit("")
        create_object(obj_index_hash[OBJ_VNUM_MAP],0).to_char(ch)

        ch.to_room(room_index_hash[ROOM_VNUM_SCHOOL]) 
        ch.do_help("newbie info")
    elif ch.in_room:
        ch.to_room(ch.in_room)
    elif IS_IMMORTAL(ch):
        ch.to_room(room_index_hash[ROOM_VNUM_CHAT])
    else:
        ch.to_room(ch, room_index_hash[ROOM_VNUM_TEMPLE])

    act( "$n has entered the game.", ch, None, None, TO_ROOM )
    ch.do_look("auto")

    wiznet("$N has left real life behind.",ch,None, WIZ_LOGINS,WIZ_SITES,ch.get_trust())
    if ch.pet:
        ch.pet.to_room(ch.in_room)
        act("$n has entered the game.",ch.pet,None,None,TO_ROOM)

def con_playing(self):
    command = self.get_command()
    if not command.strip():
        return
    substitute_alias(self, command)

    