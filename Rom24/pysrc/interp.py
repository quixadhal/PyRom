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
from collections import OrderedDict
import logging
logger = logging.getLogger()

from alias import *
from healing import do_heal
from fight import *
from skills import do_groups, do_skills, do_spells, do_gain
from settings import LOGALL

class cmd_type:
    def __init__(self, name, do_fun, position, level, log, show, default_arg=None):
        self.name = name
        self.do_fun = do_fun
        self.position = position
        self.level = level
        self.log = log
        self.show = show
        self.default_arg = default_arg
        setattr(CHAR_DATA, self.do_fun.__name__, self.do_fun)

# These commands don't need to be here but are, for order. These will always match first with prefixes.
cmd_table = OrderedDict()

cmd_table['north'] = None
cmd_table['east'] = None
cmd_table['south'] = None
cmd_table['west'] = None
cmd_table['up'] = None
cmd_table['down'] = None
cmd_table['at'] = None
cmd_table['buy'] = None
cmd_table['cast'] = None
cmd_table['follow'] = None
cmd_table['goto'] = None
cmd_table['group'] = None
cmd_table['hit'] = cmd_type('hit', do_kill, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['inventory'] = None
cmd_table['kill'] = cmd_type('kill', do_kill, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['look'] = None
cmd_table['who'] = None
cmd_table['autolist'] = None
# Common other commands.
# Placed here so one and two letter abbreviations work.

# Informational commands.

cmd_table['info'] = cmd_type('info', do_groups, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['skills'] = cmd_type('skills', do_skills, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['spells'] = cmd_type('spells', do_spells, POS_DEAD, 0, LOG_NORMAL, 1)

# Configuration commands.
cmd_table['alia'] = cmd_type('alia', do_alia, POS_DEAD, 0, LOG_NORMAL, 0)
cmd_table['alias'] = cmd_type('alias', do_alias, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['unalias'] = cmd_type('unalias', do_unalias, POS_DEAD, 0, LOG_NORMAL, 1)

# Communication commands.

# Object manipulation commands.

cmd_table['heal'] = cmd_type('heal', do_heal, POS_RESTING, 0, LOG_NORMAL, 1)

# Combat commands.
cmd_table['backstab'] = cmd_type('backstab', do_backstab, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['bash'] = cmd_type('bash', do_bash, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['bs'] = cmd_type('bs', do_backstab, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['berserk'] = cmd_type('berserk', do_berserk, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['dirt'] = cmd_type('dirt', do_dirt, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['disarm'] = cmd_type('disarm', do_disarm, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['flee'] = cmd_type('flee', do_flee, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['kick'] = cmd_type('kick', do_kick, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['murde'] = cmd_type('murde', do_murde, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['murder'] = cmd_type('murder', do_murder, POS_FIGHTING, 5, LOG_ALWAYS, 1)
cmd_table['rescue'] = cmd_type('rescue', do_rescue, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['trip'] = cmd_type('trip', do_trip, POS_FIGHTING, 0, LOG_NORMAL, 1)

# Miscellaneous commands.

cmd_table['gain'] = cmd_type('gain', do_gain, POS_STANDING, 0, LOG_NORMAL, 1)
cmd_table['groups'] = cmd_type('groups', do_groups, POS_SLEEPING, 0, LOG_NORMAL, 1)

# Immortal commands.

cmd_table['sla'] = cmd_type('sla', do_sla, POS_DEAD, L3, LOG_NORMAL, 0)
cmd_table['slay'] = cmd_type('slay', do_slay, POS_DEAD, L3, LOG_ALWAYS, 1)

logger.info('Command table initialized.')

def register_command(entry:cmd_type):
    cmd_table[entry.name] = entry
    logger.debug('    %s registered in command table.', entry.name)

def interpret(ch, argument):
    # Strip leading spaces.
    argument = argument.lstrip()
    command = ''

    # No hiding.
    REMOVE_BIT(ch.affected_by, AFF_HIDE)

    # Implement freeze command.
    if not IS_NPC(ch) and IS_SET(ch.act, PLR_FREEZE):
        ch.send("You're totally frozen!\n")
        return
    # Grab the command word.
    # Special parsing so ' can be a command,
    #   also no spaces needed after punctuation.
    logline = argument
    if not argument[0].isalpha() and not argument[0].isdigit():
        command = argument[0]
        argument = argument[:1].lstrip()
    else:
        argument, command = read_word(argument)
    # Look for command in command table.
    trust = ch.get_trust()
    cmd = prefix_lookup(cmd_table, command)
    if cmd != None:
        if cmd.level > trust:
            cmd = None

    #* Log and snoop.
    if (not IS_NPC(ch) and IS_SET(ch.act, PLR_LOG)) or LOGALL or (cmd and cmd.log == LOG_ALWAYS):
        if cmd and cmd.log != LOG_NEVER:
            log_buf = "Log %s: %s" % (ch.name, logline)
            wiznet(log_buf, ch, None, WIZ_SECURE, 0, ch.get_trust())
            logger.info(log_buf)
    if ch.desc and ch.desc.snoop_by:
        ch.desc.snoop_by.send("% ")
        ch.desc.snoop_by.send(logline)
        ch.desc.snoop_by.send("\n")
    if not cmd:
        #* Look for command in socials table.
        if not check_social(ch, command, argument):
            ch.send("Huh?\n")
        return
    #* Character not in position for command?
    if ch.position < cmd.position:
        if ch.position == POS_DEAD:
            ch.send("Lie still; you are DEAD.\n")
        elif ch.position == POS_MORTAL \
                or ch.position == POS_INCAP:
            ch.send("You are hurt far too bad for that.\n")
        elif ch.position == POS_STUNNED:
            ch.send("You are too stunned to do that.\n")
        elif ch.position == POS_SLEEPING:
            ch.send("In your dreams, or what?\n")
        elif ch.position == POS_RESTING:
            ch.send("Nah... You feel too relaxed...\n")
        elif ch.position == POS_SITTING:
            ch.send("Better stand up first.\n")
        elif ch.position == POS_FIGHTING:
            ch.send("No way!  You are still fighting!\n")
        return

    # Dispatch the command.
    if cmd.default_arg:
        cmd.do_fun(ch, cmd.default_arg)
        return
    cmd.do_fun(ch, argument)


def check_social(ch, command, argument):
    cmd = None
    for social in social_list:
        if social.name.lower().startswith(command):
            cmd = social
    if not cmd:
        return False
    if not IS_NPC(ch) and IS_SET(ch.comm, COMM_NOEMOTE):
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
    holder, arg = read_word(argument)
    victim = ch.get_char_room(arg)
    if not arg:
        act(cmd.others_no_arg, ch, None, victim, TO_ROOM)
        act(cmd.char_no_arg, ch, None, victim, TO_CHAR)
    elif not victim:
        ch.send("They aren't here.\n")
    elif victim == ch:
        act(cmd.others_auto, ch, None, victim, TO_ROOM)
        act(cmd.char_auto, ch, None, victim, TO_CHAR)
    else:
        act(cmd.others_found, ch, None, victim, TO_NOTVICT)
        act(cmd.char_found, ch, None, victim, TO_CHAR)
        act(cmd.vict_found, ch, None, victim, TO_VICT)

        if not IS_NPC(ch) and IS_NPC(victim) \
                and not IS_AFFECTED(victim, AFF_CHARM) \
                and IS_AWAKE(victim) and victim.desc is None:
            num = random.randint(0, 12)
            if num in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                act(cmd.others_found, victim, None, ch, TO_NOTVICT)
                act(cmd.char_found, victim, None, ch, TO_CHAR)
                act(cmd.vict_found, victim, None, ch, TO_VICT)

            elif num in [9, 10, 11, 12]:
                act("$n slaps $N.", victim, None, ch, TO_NOTVICT)
                act("You slap $N.", victim, None, ch, TO_CHAR)
                act("$n slaps you.", victim, None, ch, TO_VICT)
    return True
