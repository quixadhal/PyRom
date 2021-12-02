import random
import copy
import os
import json
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import instance
from rom24 import environment
from rom24 import state_checks
from rom24 import inventory
from rom24 import type_bypass
from rom24 import settings


class Room(
    instance.Instancer,
    environment.Environment,
    inventory.Inventory,
    type_bypass.ObjectType,
):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None, **kwargs):
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
        self.special_inventory = []
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
            self.instancer()
        if self.environment:
            if self._environment not in instance.global_instances.keys():
                self.environment = None
        if self.special_inventory:
            for t in self.special_inventory[:]:
                self.inventory += t[0]
                import importlib

                words = t[1].split(".")
                class_name = words[-1]
                module_name = ".".join(words[0:-1])
                if module_name != "" and class_name != "":
                    module_ref = importlib.import_module(module_name)
                    class_ref = getattr(module_ref, class_name)
                    if hasattr(class_ref, "load"):
                        return class_ref.load(t[0])
            del self.special_inventory
        if self.instance_id:
            self.instance_setup()
            Room.instance_count += 1
        else:
            Room.template_count += 1
        self._last_saved = None
        self._md5 = None

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                Room.instance_count -= 1
                if instance.rooms.get(self.instance_id, None):
                    self.instance_destructor()
            else:
                Room.template_count -= 1
        except:
            return

    def __repr__(self):
        if not self.instance_id:
            return "<Room Template: %d>" % self.vnum
        else:
            return "<Room Instance ID: %d - Template: %d >" % (
                self.instance_id,
                self.vnum,
            )

    def put(self, instance_object):
        if not instance_object.instance_id in self.inventory:
            self.inventory += [instance_object.instance_id]
            instance_object._room_vnum = self.vnum
        else:
            raise ValueError(
                "Instance already present in room inventory %d"
                % instance_object.instance_id
            )
        if instance_object.is_living:
            if not instance_object.is_npc():
                self.in_area.add_pc(instance_object)
            if (
                instance_object.slots.light
                and instance_object.slots.light.value[2] != 0
            ):
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
            raise KeyError(
                "Instance is not in room inventory, trying to be removed %d"
                % instance_object.instance_id
            )
        if instance_object.is_living:
            if not instance_object.is_npc():
                self.in_area.remove_pc(instance_object)
            if (
                instance_object.slots.light
                and instance_object.slots.light.value[2] != 0
                and self.available_light > 0
            ):
                self.available_light -= 1
        elif instance_object.is_item:
            if (
                instance_object.flags.light
                and instance_object.value[2] != 0
                and self.available_light > 0
            ):
                self.available_light -= 1
        else:
            raise TypeError(
                "Unknown instance type trying to be removed from Room %r"
                % type(instance_object)
            )
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
        instance.global_instances[self.instance_id] = self
        instance.rooms[self.instance_id] = self
        if self.vnum not in instance.instances_by_room.keys():
            instance.instances_by_room[self.vnum] = [self.instance_id]
        else:
            instance.instances_by_room[self.vnum] += [self.instance_id]

    def instance_destructor(self):
        instance.instances_by_room[self.vnum].remove(self.instance_id)
        del instance.rooms[self.instance_id]
        del instance.global_instances[self.instance_id]

    def is_dark(room_instance):
        if room_instance.available_light > 0:
            return False
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_DARK):
            return True
        if (
            room_instance.sector_type == merc.SECT_INSIDE
            or room_instance.sector_type == merc.SECT_CITY
        ):
            return False
        if (
            handler_game.weather_info.sunlight == merc.SUN_SET
            or handler_game.weather_info.sunlight == merc.SUN_DARK
        ):
            return True
        return False

    # * True if room is private.
    def is_private(room_instance):
        if room_instance.owner:
            return True
        count = len(room_instance.people)
        if (
            state_checks.IS_SET(room_instance.room_flags, merc.ROOM_PRIVATE)
            and count >= 2
        ):
            return True
        if (
            state_checks.IS_SET(room_instance.room_flags, merc.ROOM_SOLITARY)
            and count >= 1
        ):
            return True
        if state_checks.IS_SET(room_instance.room_flags, merc.ROOM_IMP_ONLY):
            return True
        return False

    # Serialization
    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            elif str(k) in ("_last_saved", "_md5"):
                continue
            elif str(k) == "inventory" and v is not None:
                # We need to save the inventory special to keep the type data with it.
                t = "special_inventory"
                tmp_dict[t] = []
                for i in v:
                    if i in instance.players:
                        pass
                    elif i in instance.rooms:
                        pass
                    elif i in instance.areas:
                        pass
                    else:
                        tmp_dict[t].append(
                            tuple(
                                (
                                    i,
                                    instance.global_instances[i].__module__
                                    + "."
                                    + instance.global_instances[i].__class__.__name__,
                                )
                            )
                        )
            else:
                tmp_dict[k] = v

        cls_name = "__class__/" + __name__ + "." + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = "__class__/" + __name__ + "." + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data

    def save(self, force: bool = False):
        if self._last_saved is None:
            self._last_saved = time.time() - settings.SAVE_LIMITER - 2
        if not force and time.time() < self._last_saved + settings.SAVE_LIMITER:
            return

        if self.instance_id:
            top_dir = settings.INSTANCE_DIR
            number = self.instance_id
        else:
            top_dir = settings.AREA_DIR
            number = self.vnum
        if self.in_area.instance_id:
            area_number = self.in_area.instance_id
        else:
            area_number = self.in_area.index
        pathname = os.path.join(
            top_dir, "%d-%s" % (area_number, self.in_area.name), "rooms"
        )

        os.makedirs(pathname, 0o755, True)
        filename = os.path.join(pathname, "%d-room.json" % number)
        # logger.info('Saving %s', filename)
        js = json.dumps(self, default=instance.to_json, indent=4, sort_keys=True)
        md5 = hashlib.md5(js.encode("utf-8")).hexdigest()
        if self._md5 != md5:
            self._md5 = md5
            with open(filename, "w") as fp:
                fp.write(js)

        if self.inventory:
            for item_id in self.inventory[:]:
                if item_id not in instance.items:
                    # logger.error('Item %d is in Room %d\'s inventory, but does not exist?', item_id, self.instance_id)
                    continue
                item = instance.items[item_id]
                item.save(in_inventory=True, force=force)

    @classmethod
    def load(cls, vnum: int = None, instance_id: int = None):
        if instance_id:
            if instance_id in instance.rooms:
                logger.warn("Instance %d of room already loaded!", instance_id)
                return
            pathname = settings.INSTANCE_DIR
            number = instance_id
        elif vnum:
            pathname = settings.AREA_DIR
            number = vnum
        else:
            raise ValueError(
                "To load a Room, you must provide either a VNUM or an Instance_ID!"
            )

        target_file = "%d-room.json" % number
        filename = None
        for a_path, a_directory, i_files in os.walk(pathname):
            if target_file in i_files:
                filename = os.path.join(a_path, target_file)
                break
        if not filename:
            raise ValueError("Cannot find %s" % target_file)

        with open(filename, "r") as fp:
            obj = json.load(fp, object_hook=instance.from_json)
        if isinstance(obj, Room):
            # Inventory is already loaded by Room's __init__ function.
            return obj
        else:
            logger.error("Could not load room data for %d", number)
            return None


def get_room_by_vnum(vnum):
    room_id = instance.instances_by_room[vnum][0]
    return instance.rooms[room_id]


def get_random_room(ch):
    room = None
    while True:
        room = random.choice(instance.rooms.values())
        if (
            ch.can_see_room(room)
            and not room.is_private()
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_PRIVATE)
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_SOLITARY)
            and not state_checks.IS_SET(room.room_flags, merc.ROOM_SAFE)
            and (
                ch.is_npc()
                or ch.act.is_set(merc.ACT_AGGRESSIVE)
                or not state_checks.IS_SET(room.room_flags, merc.ROOM_LAW)
            )
        ):
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
            if (
                pexit
                and pexit.exit_info.is_set(merc.EX_ISDOOR)
                and pexit.keyword
                and arg in pexit.keyword
            ):
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
