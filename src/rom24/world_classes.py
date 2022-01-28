import os
import json
import copy
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

from rom24 import environment
from rom24 import tables
from rom24 import instance
from rom24 import settings
from rom24 import type_bypass
from rom24 import bit

__author__ = "syn"


class Area(instance.Instancer, type_bypass.ObjectType, environment.Environment):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None, **kwargs):
        super().__init__()
        self.is_area = True
        self.index = 0
        self.name = ""
        self.no_save = False  # TODO: This should be true for instances
        self.instance_id = None
        self.reset_list = []
        self.file_name = ""
        self.credits = ""
        self.age = 15
        self.character = 0
        self.low_range = 0
        self.high_range = 0
        self.min_vnum = 0
        self.max_vnum = 0
        # Empty is a check for if the area contains player_characters or not for use in resets, should default True
        # As in, this area is just loaded and has no PC objects, True
        self.empty = False
        self.player_chars = []
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]
        if template:
            [
                setattr(self, k, copy.deepcopy(v))
                for k, v in template.__dict__.items()
                if k not in instance.not_to_instance
            ]
            self.instancer()
        if self.instance_id:
            self.instance_setup()
            Area.instance_count += 1
        else:
            Area.template_count += 1
        self._last_saved = None
        self._md5 = None

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                Area.instance_count -= 1
                if instance.areas.get(self.instance_id, None):
                    self.instance_destructor()
            else:
                Area.template_count -= 1
                del instance.area_templates[self.name]
        except:
            return

    def __repr__(self):
        if self.instance_id:
            return "<Instance: %d %d %s(%s): %d-%d>" % (
                self.instance_id,
                self.index,
                self.name,
                self.file_name,
                self.min_vnum,
                self.max_vnum,
            )
        else:
            return "<Template: %d %s(%s): %d-%d>" % (
                self.index,
                self.name,
                self.file_name,
                self.min_vnum,
                self.max_vnum,
            )

    @property
    def player_count(self):
        return len(self.player_chars)

    def add_pc(self, player_char):
        if player_char.is_living and not player_char.is_npc():
            if not player_char.instance_id in self.player_chars:
                # Transition an empty area, to an occupied one, for Resets
                if self.empty:
                    self.empty = False
                    self.age = 0
                self.player_chars += [player_char.instance_id]
            else:
                raise ValueError(
                    "Player Character already in player_chars list! %d"
                    % player_char.instance_id
                )
        else:
            raise KeyError(
                "Entity not a player character, or is an NPC on area addition! %r"
                % type(player_char)
            )

    def remove_pc(self, player_char):
        if player_char.is_living and not player_char.is_npc():
            if player_char.instance_id in self.player_chars:
                self.player_chars.remove(player_char.instance_id)
            else:
                raise ValueError(
                    "Player Character not in player_chars list! %d"
                    % player_char.instance_id
                )
        else:
            raise KeyError(
                "Entity not a player character, or is an NPC on area removal! %r"
                % type(player_char)
            )

    def instance_setup(self):
        instance.global_instances[self.instance_id] = self
        instance.areas[self.instance_id] = self
        if self.name not in instance.instances_by_area.keys():
            instance.instances_by_area[self.name] = [self.instance_id]
        else:
            instance.instances_by_area[self.name] += [self.instance_id]

    def instance_destructor(self):
        instance.instances_by_area[self.name].remove(self.instance_id)
        del instance.areas[self.instance_id]
        del instance.global_instances[self.instance_id]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            elif str(k) in ("_last_saved", "_md5"):
                continue
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
            number = self.index
        pathname = os.path.join(top_dir, "%d-%s" % (number, self.name))

        os.makedirs(pathname, 0o755, True)
        filename = os.path.join(pathname, "%d-area.json" % number)
        # logger.info('Saving %s', filename)
        js = json.dumps(self, default=instance.to_json, indent=4, sort_keys=True)
        md5 = hashlib.md5(js.encode("utf-8")).hexdigest()
        if self._md5 != md5:
            self._md5 = md5
            with open(filename, "w") as fp:
                fp.write(js)

    @classmethod
    def load(cls, index: int = None, instance_id: int = None):
        if instance_id and instance_id in instance.characters:
            logger.warn("Instance %d of npc already loaded!", instance_id)
            return

        if instance_id:
            top_dir = settings.INSTANCE_DIR
            number = instance_id
        elif index:
            top_dir = settings.AREA_DIR
            number = index
        else:
            raise ValueError(
                "Must have an instance_id that's in characters, an instance_id, or an index."
            )

        target_file = "%d-area.json" % number
        filename = None
        for a_path, a_directory, i_files in os.walk(top_dir):
            if target_file in i_files:
                filename = os.path.join(a_path, target_file)
                break
        if not filename:
            raise ValueError("Cannot find %s" % target_file)

        with open(filename, "r") as fp:
            obj = json.load(fp, object_hook=instance.from_json)
        if isinstance(obj, Area):
            return obj
        else:
            logger.error("Could not load area data for %d", number)
            return None


class ExtraDescrData:
    def __init__(self, **kwargs):
        self.keyword = ""  # Keyword in look/examine
        self.description = ""
        if kwargs:
            import copy

            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
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


class Exit:
    def __init__(self, template=None, **kwargs):
        self.name = ""
        self.to_room_vnum = None
        self.to_room = None
        self.exit_info = bit.Bit(flags=tables.exit_flags)
        self.key = None
        self.key_vnum = None
        self.keyword = ""
        self.description = ""
        self.is_broken = False
        if template:
            import copy

            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
            if (
                self.to_room_vnum != -1
                and not None
                and self.to_room_vnum in instance.instances_by_room
            ):
                self.to_room = instance.instances_by_room[self.to_room_vnum][0]
            elif self.to_room_vnum not in instance.instances_by_room:
                self.is_broken = True
                logger.error("Exit(): bad to_room_vnum %d.", self.to_room_vnum)
            else:
                self.to_room = None
            if self.key <= 0:
                self.key = None
        if kwargs:
            import copy

            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
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


class Reset:
    load_count = 0

    def __init__(self, template=None, **kwargs):
        Reset.load_count += 1
        self.name = ""
        self.area = ""
        self.instance_id = None
        self.room = None
        self.command = ""
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0
        self.arg4 = 0
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
            self.room = instance.instances_by_room[self.room][0]
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def __repr__(self):
        if not self.instance_id:
            return "Reset Area: %s Room: %d Type: %s" % (
                instance.room_templates[self.room].area,
                self.room,
                self.command,
            )

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
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


class Shop:
    def __init__(self, template=None, **kwargs):
        self.keeper = None
        self.keeperTemplate = None
        self.room = None
        self.buy_type = {}
        self.profit_buy = 0
        self.profit_sell = 0
        self.open_hour = 0
        self.close_hour = 0
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def __repr__(self):
        return "Shop Mob: %s Room: %d" % (
            instance.characters[self.keeper].name,
            self.room,
        )

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
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


class Gen:
    def __init__(self, **kwargs):
        self.valid = False
        self.skill_chosen = {}
        self.group_chosen = {}
        self.points_chosen = 0
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
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
