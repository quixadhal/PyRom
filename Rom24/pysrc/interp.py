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
import logging
import character

logger = logging.getLogger()

from collections import OrderedDict

import game_utils
import handler_game
import handler_ch
from fight import *
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
        setattr(handler_ch.CHAR_DATA, self.do_fun.__name__, self.do_fun)
        setattr(character.Living, self.do_fun.__name__, self.do_fun)

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
cmd_table['hit'] = None
cmd_table['inventory'] = None
cmd_table['kill'] = None
cmd_table['look'] = None
cmd_table['who'] = None
cmd_table['autolist'] = None


def register_command(entry: cmd_type):
    cmd_table[entry.name] = entry
    logger.debug('    %s registered in command table.', entry.name)


#hotfix.init_directory(os.path.join('commands'))


def interpret(ch, argument):
    # Strip leading spaces.
    argument = argument.lstrip()

    # No hiding.
    state_checks.REMOVE_BIT(ch.affected_by, AFF_HIDE)

    # Implement freeze command.
    if not ch.is_npc() and state_checks.IS_SET(ch.act, PLR_FREEZE):
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
        argument, command = game_utils.read_word(argument)
    # Look for command in command table.
    trust = ch.get_trust()
    cmd = state_checks.prefix_lookup(cmd_table, command)
    if cmd is not None:
        if cmd.level > trust:
            cmd = None

    #* Log and snoop.
    if (not ch.is_npc() and state_checks.IS_SET(ch.act, PLR_LOG)) or LOGALL or (cmd and cmd.log == LOG_ALWAYS):
        if cmd and cmd.log != LOG_NEVER:
            log_buf = "Log %s: %s" % (ch.name, logline)
            handler_game.wiznet(log_buf, ch, None, WIZ_SECURE, 0, ch.get_trust())
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
    if not ch.is_npc() and state_checks.IS_SET(ch.comm, COMM_NOEMOTE):
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

        if not ch.is_npc() and state_checks.IS_NPC(victim) \
                and not state_checks.IS_AFFECTED(victim, AFF_CHARM) \
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
