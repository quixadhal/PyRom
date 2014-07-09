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
import os
import importlib
import traceback
import logging

logger = logging.getLogger()

# dictionary of files to track. will be key'd by file name and the value will be modified unix timestamp
tracked_files = {}
modified_files = {}


def init_file(path, modules, silent=False):
    #called by init_monitoring to begin tracking a file.
    modules = [importlib.import_module(m) for m in modules]
    tracked_files[path] = [os.path.getmtime(path), modules]
    if not silent:
        logger.info('    Tracking %s', path)
    else:
        logger.debug('    Tracking %s', path)


def init_directory(path, silent=False):
    dir = os.listdir(path)
    files = [f for f in dir if not f.startswith('__')]

    logger.info('Tracking %d files in %s', len(files), path)
    for file in files:
        full_path = os.path.join(path, file)
        module = full_path.split('.')[0].replace(os.sep, '.')
        init_file(full_path, [module], silent)


def init_monitoring():
    #Called in main function to begin tracking files.
    logger.info('Monitoring system initializing...')
    init_file('handler_ch.py', ['handler_ch'])
    init_file('handler_obj.py', ['handler_obj'])
    init_file('handler_room.py', ['handler_room'])
    init_file('handler_log.py', ['handler_log'])
    init_file('pyprogs.py', ['pyprogs'])
    init_directory(os.path.join('commands'))
    init_directory(os.path.join('spells'))
    logger.info('done. (Monitoring system)')


def poll_files():
    #Called in game_loop of program to check if files have been modified.
    for fp, pair in tracked_files.items():
        mod, modules = pair
        if mod != os.path.getmtime(fp):
            #File has been modified.
            logger.warn('%s has been modified', fp)
            tracked_files[fp][0] = os.path.getmtime(fp)
            modified_files[fp] = [os.path.getmtime(fp), modules]


def reload_files(ch):
    for fp, pair in modified_files.copy().items():
        mod, modules = pair
        logger.warn('Reloading %s', fp)
        for m in modules:
            try:
                importlib.reload(m)
            except:
                ch.send(traceback.format_exc())
                logger.exception('Failed to reload %s', fp)

        del modified_files[fp]
