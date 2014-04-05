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
import os
import json
from merc import *
from settings import PLAYER_DIR

def save_char_obj( ch ):
    if IS_NPC(ch):
        return

    if ch.desc and ch.desc.original:
        ch = ch.desc.original

    
    pfile = os.path.join(PLAYER_DIR, ch.name+'.js')
    fwrite = ch.__dict__.copy()
    fwrite['in_room'] = ch.in_room.vnum
    fwrite['was_in_room'] = ch.was_in_room.vnum
    del fwrite['desc']
    del fwrite['send']
    fwrite['carrying'] = [ o.__dict__.copy() for o in ch.carrying ]
    for c in fwrite['carrying']:
        c['pIndexData'] = c['pIndexData'].vnum
        del c['carried_by']
        fwrite['carrying'].extend([o.__dict__.copy() for o in c['contains']])

    fwrite['pcdata'] = ch.pcdata.__dict__
    fwrite['guild'] = ch.guild.name
    fwrite['race'] = ch.race.name

    to_write = json.dumps(fwrite, indent=4)
    with open(pfile, 'w') as pf:
        pf.write(to_write)

#    if ( ch.carrying != NULL )
 #       fwrite_obj( ch, ch.carrying, fp, 0 );
 #   /* save the pets */
 #   if (ch.pet != NULL and ch.pet.in_room == ch.in_room)
 #       fwrite_pet(ch.pet,fp);
 #   fprintf( fp, "#END\n" );
 ##   }
  #  fclose( fp );
  #  rename(TEMP_FILE,strsave);
  #  fpReserve = fopen( NULL_FILE, "r" );

def load_char_obj(d, name):
    ch = CHAR_DATA()
    ch.pcdata = PC_DATA()
    ch.name = name
    ch.act = 0
    found = False
    pfile = os.path.join(PLAYER_DIR, name+'.js')
    if os.path.isfile(pfile):
        ch.__dict__ = json.load( open(pfile,'r') )
        found = True

    ch.desc = d
    d.character = ch
    ch.send = d.send
    player_list.append(ch)
    return (found,ch)
    