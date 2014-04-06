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
 ************/
"""
from merc import *

# does aliasing and other fun stuff */
def substitute_alias(d, argument):
    ch = CH(d)

    # check for prefix */
    if ch.prefix and not "prefix".startswith(argument):
        if len(ch.prefix) + len(argument) > MAX_INPUT_LENGTH:
            ch.send("Line to long, prefix not processed.\r\n")
        else:
            prefix = "%s %s" % (ch.prefix,argument)

    if IS_NPC(ch) or ch.pcdata.alias[0] == None \
    or "alias".startswith(argument) or "unalias".startswith(argument)  \
    or "prefix".startswith(argument):
        interpret(ch,argument)
        return
    remains, sub = read_word(argument)
    if sub not in ch.pcdata.alias:
        interpret(ch, argument)
    buf = "%s %s" % ( ch.pcdata.alias[sub], remains )
    interpret(ch,buf)

def do_alia(self,argument):
    self.send("I'm sorry, alias must be entered in full.\n\r")
    return

def do_alias(self, argument):
    ch = self
    if not ch.desc:
        rch = ch
    else:
        rch = ch.desc.original if ch.desc.original else ch

    if IS_NPC(rch):
        return

    argument, arg = read_word(argument)
    if not arg:
        if not rch.pcdata.alias:
            ch.send("You have no aliases defined.\n\r")
            return
        ch.send("Your current aliases are:\n\r")

        for alias,sub in rch.pcdata.alias.iteritems():
            ch.send("    %s:  %s\n\r" % (alias, sub) )
        return

    if "unalias" ==  arg or "alias" == arg:
        ch.send("Sorry, that word is reserved.\n\r")
        return

    if not argument:
        if arg not in rch.pcdata.alias:
            ch.send("That alias is not defined.\n\r")
            return
        ch.send("%s aliases to '%s'.\n\r" % (arg, rch.pcdata.alias[arg]) )
        return

    if argument.startswith("delete") or argument.startswith("prefix"):
        ch.send("That shall not be done!\n\r")
        return

    if arg in rch.pcdata.alias:
        rch.pcdata.alias[arg] = argument
        ch.send("%s is now realiased to '%s'.\n\r" % (arg,argument) )
        return
    elif len(rch.pcdata.alias) > MAX_ALIAS:
        ch.send("Sorry, you have reached the alias limit.\r\n")
        return
    rch.pcdata.alias[arg] = argument
    ch.send("%s is now aliased to '%s'.\n\r" % (arg,argument) )
    return

def do_unalias(ch, argument):
    ch = self
    if not ch.desc:
        rch = ch
    else:
        rch = ch.desc.original if ch.desc.original else ch

    if IS_NPC(rch):
        return

    argument, arg = read_word(argument)

    if not arg:
        ch.send("Unalias what?\n\r")
        return

    if arg not in ch.pcdata.alias:
        ch.send("No alias of that name to remove.\n\r")
        return
    del ch.pcdata.alias[arg]
    ch.send("Alias removed.\n")
    return