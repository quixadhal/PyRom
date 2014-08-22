"""
 #**************************************************************************
 *  Original Diku Mud copyright(C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright(C) 1992, 1993 by Michael           *
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
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                            *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/ 
 ************/
"""
import random
import logging

logger = logging.getLogger()

import merc
import handler_game
import instance
import environment
import state_checks
import inventory
import type_bypass


class Room(instance.Instancer, environment.Environment, inventory.Inventory, type_bypass.ObjectType):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None):
        super().__init__()
        self.is_room = True
        self.vnum = 0
        self.extra_descr = []
        self.area = ""
        self.exit = [None, None, None, None, None, None]
        self.old_exit = [None, None, None, None, None, None]
        self.name = ""
        self.description = ""
        self.owner = ""
        self.room_flags = 0
        self.available_light = 0
        self.sector_type = 0
        self.heal_rate = 100
        self.mana_rate = 100
        self.clan = None
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            self.instancer()
            self.instance_setup()
        if self.instance_id:
            Room.instance_count += 1
        else:
            Room.template_count += 1

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                self.instance_destructor()
        except:
            return

    def __repr__(self):
        if not self.instance_id:
            return "<Room Template: %d>" % self.vnum
        else:
            return "<Room Instance ID: %d - Template: %d >" % (self.instance_id, self.vnum)

    def put(self, instance_object):
        if not instance_object.instance_id in self.inventory:
            self.inventory += [instance_object.instance_id]
            instance_object._room_vnum = self.vnum
        else:
            raise ValueError('Instance already present in room inventory %d' % instance_object.instance_id)
        if instance_object.is_living:
            if not instance_object.is_npc():
                    self.in_area.add_pc(instance_object)
            if instance_object.slots.light and instance_object.slots.light.value[2] != 0:
                self.available_light += 1
            if instance_object.is_affected(merc.AFF_PLAGUE):
                self.spread_plague(instance_object)
        if instance_object.is_item:
            if instance_object.flags.light and instance_object.value[2] != 0:
                self.available_light += 1
        try:
            self.carry_number += instance_object.get_number()
            self.carry_weight += instance_object.get_weight()
        except:
            pass
        instance_object.environment = self.instance_id
        return instance_object

    def get(self, instance_object):
        if instance_object.instance_id in self.inventory:
            self.inventory.remove(instance_object.instance_id)
            instance_object._room_vnum = None
        else:
            raise KeyError('Instance is not in room inventory, trying to be removed %d' % instance_object.instance_id)
        if instance_object.is_living:
            if not instance_object.is_npc():
                self.in_area.remove_pc(instance_object)
            if instance_object.slots.light and instance_object.slots.light.value[2] != 0 and self.available_light > 0:
                self.available_light -= 1
        elif instance_object.is_item:
            if instance_object.flags.light and instance_object.value[2] != 0 and self.available_light > 0:
                self.available_light -= 1
        else:
            raise TypeError('Unknown instance type trying to be removed from Room %r' % type(instance_object))
        if instance_object.on:
            instance_object.on = None
        instance_object.environment = None
        try:
            self.carry_number -= instance_object.get_number()
            self.carry_weight -= instance_object.get_weight()
        except:
            pass
        return instance_object

    def instance_setup(self):
        merc.global_instances[self.instance_id] = self
        merc.rooms[self.instance_id] = merc.global_instances[self.instance_id]
        if self.vnum not in merc.instances_by_room.keys():
            merc.instances_by_room[self.vnum] = [self.instance_id]
        else:
            merc.instances_by_room[self.vnum].append(self.instance_id)

    def instance_destructor(self):
        merc.instances_by_room[self.vnum].remove(self.instance_id)
        del merc.rooms[self.instance_id]
        del merc.global_instances[self.instance_id]

    def is_dark(room_instance):
        if room_instance.available_light > 0:
            return False
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_DARK):
            return True
        if room_instance.sector_type == merc.SECT_INSIDE or room_instance.sector_type == merc.SECT_CITY:
            return False
        if handler_game.weather_info.sunlight == merc.SUN_SET or handler_game.weather_info.sunlight == merc.SUN_DARK:
            return True
        return False

    # * True if room is private.
    def is_private(room_instance):
        if room_instance.owner:
            return True
        count = len(room_instance.people)
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_PRIVATE) and count >= 2:
            return True
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_SOLITARY) and count >= 1:
            return True
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_IMP_ONLY):
            return True
        return False

def get_room_by_vnum(vnum):
    room_id = merc.instances_by_room[vnum][0]
    return merc.rooms[room_id]

def get_random_room(ch):
    room = None
    while True:
        room = random.choice(merc.rooms.values())
        if ch.can_see_room(room) and not room.is_private() \
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_PRIVATE) \
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_SOLITARY) \
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_SAFE) \
            and (ch.is_npc() or ch.act.is_set(merc.ACT_AGGRESSIVE)
                 or not state_checks.IS_SET(room.room_flags, merc.ROOM_LAW)):
            break
    return room

def number_door(self=None):
    return random.randint(0, 5)

def find_door(ch, arg):
    if arg == "n" or arg == "north":
        door = 0
    elif arg == "e" or arg == "east":
        door = 1
    elif arg == "s" or arg == "south":
        door = 2
    elif arg == "w" or arg == "west":
        door = 3
    elif arg == "u" or arg == "up":
        door = 4
    elif arg == "d" or arg == "down":
        door = 5
    else:
        for door in range(0, 5):
            pexit = ch.in_room.exit[door]
            if pexit and pexit.exit_info.is_set(merc.EX_ISDOOR) and pexit.keyword \
                    and arg in pexit.keyword:
                return door
        handler_game.act("I see no $T here.", ch, None, arg, merc.TO_CHAR)
        return -1
    pexit = ch.in_room.exit[door]
    if not pexit:
        handler_game.act("I see no door $T here.", ch, None, arg, merc.TO_CHAR)
        return -1
    if not pexit.exit_info.is_set(merc.EX_ISDOOR):
        ch.send("You can't do that.\n")
        return -1
    return door
