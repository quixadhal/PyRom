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
*	ROM 2.4 is copyright 1993-1998 Russ Taylor			                   *
*	ROM has been brought to you by the ROM consortium		               *
*	    Russ Taylor (rtaylor@hypercube.org)				                   *
*	    Gabrielle Taylor (gtaylor@hypercube.org)			               *
*	    Brian Moore (zump@rom.org)					                       *
*	By using this code, you have agreed to follow the terms of the	       *
*	ROM license, in the file Rom24/doc/rom.license			               *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import os
import sys
import logging
#import pdb


def boot_log(self, message, *args, **kws):
    if self.level <= 21:
        self._log(21, message, args, **kws)


def trace_log(self, message, *args, **kws):
    if self.level <= 5:
        self._log(5, message, args, **kws)


sys.path.append(os.getcwd())
logging.addLevelName(21, 'BOOT')
logging.Logger.boot = boot_log
logging.addLevelName(5, 'TRACE')
logging.Logger.trace = trace_log
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(module)16s| %(message)s', level=21)
logger = logging.getLogger()

from miniboa import TelnetServer
from settings import PORT
from comm import game_loop, init_descriptor, close_socket
from hotfix import init_monitoring
import time

startup_time = time.time()


def Pyom():
    sys.path.append(os.getcwd())
    logger.boot('Logging system initialized.')
    server = TelnetServer(port=PORT)
    server.on_connect = init_descriptor
    server.on_disconnect = close_socket

    init_monitoring()
    logger.boot('Entering Game Loop')
    game_loop(server)
    logger.critical('System halted.')

if __name__ == "__main__":
    Pyom()
