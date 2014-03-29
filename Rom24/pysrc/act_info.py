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
from merc import help_list
from nanny import con_playing, con_gen_groups
from handler import get_trust

def do_help( self, argument ):
    ch = self
    if not argument:
        argument = "summary";

    found = [h for h in help_list if h.level <= get_trust(self) and argument.lower() in h.keyword.lower()]
    nokeyword = ['motd', 'imotd']

    for pHelp in found:
        self.send("\n\r============================================================\n\r")
        if argument not in nokeyword:
            ch.send(pHelp.keyword)
            ch.send("\r\n")
        text = pHelp.text
        if pHelp.text[0] == '.':
            text = pHelp.text[1:]
        ch.send(text)
        # small hack :) */
        if ch.desc and ch.desc.connected != con_playing and ch.desc.connected != con_gen_groups:
            break

    if not found:
        self.send( "No help on that word.\n\r")
