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
import copy

import logging

logger = logging.getLogger()

import living
import merc
import pyprogs
import bit
import tables


class Npc(living.Living):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None):
        super().__init__()
        self.vnum = 0  # Needs to come before the template to setup the instance
        self.memory = None
        self.spec_fun = None
        self.new_format = True
        self.area = ""
        self.off_flags = bit.Bit(flags=tables.off_flags)
        self.damage = [0, 0, 0]
        self.start_pos = 0
        self.default_pos = 0
        self.hit_dice = [0, 0, 0]
        self.mana_dice = [0, 0, 0]
        self.dam_dice = [0, 0, 0]
        self.template_wealth = 0
        self.count = 0
        self.killed = 0
        self.pShop = None
        self.listeners = {}
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
            self.instancer()
            self.instance_setup()
        if self.instance_id:
            Npc.instance_count += 1
        else:
            Npc.template_count += 1

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                Npc.instance_count -= 1
                if merc.characters.get(self.instance_id, None):
                    self.instance_destructor()
            else:
                Npc.template_count -= 1
        except:
            return

    def __repr__(self):
        if self.instance_id:
            return "<NPC Instance: %s ID %d template %d>" % (self.short_descr, self.instance_id, self.vnum)
        else:
            return "<NPC Template: %s:%s>" % (self.short_descr, self.vnum)

    def instance_setup(self):
        merc.global_instances[self.instance_id] = self
        merc.characters[self.instance_id] = self
        if self.vnum not in merc.instances_by_character.keys():
            merc.instances_by_character[self.vnum] = [self.instance_id]
        else:
            merc.instances_by_character[self.vnum] += [self.instance_id]

    def instance_destructor(self):
        merc.instances_by_character[self.vnum].remove(self.instance_id)
        del merc.characters[self.instance_id]
        del merc.global_instances[self.instance_id]

    register_signal = pyprogs.register_signal
    absorb = pyprogs.absorb
