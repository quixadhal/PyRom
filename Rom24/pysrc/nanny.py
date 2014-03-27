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
from save import load_char_obj

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
        print "Denying access to %s@%s" % (ch.name, self.addrport())
        self.send("You have been denied access.")
        self.deactivate()
        return





