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

import living


class cmd_type:
    def __init__(self, name, do_fun, position, level, log, show, default_arg=None):
        self.name = name
        self.do_fun = do_fun
        self.position = position
        self.level = level
        self.log = log
        self.show = show
        self.default_arg = default_arg
        setattr(living.Living, self.do_fun.__name__, self.do_fun)

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
