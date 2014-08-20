import os
import hashlib
import json
import logging

logger = logging.getLogger()

import merc
import environment
import tables
import instance
import settings
import type_bypass
import bit

__author__ = 'syn'


class Area(instance.Instancer, type_bypass.ObjectType, environment.Environment):
    def __init__(self, template=None):
        super().__init__()
        self.is_area = True
        self.index = 0
        self.name = ""
        self.no_save = False  # TODO: This should be true for instances
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items() if k not in merc.not_to_instance]
            self.instancer()
            self.instance_setup()
        else:
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
            #Empty is a check for if the area contains player_characters or not for use in resets, should default True
            #As in, this area is just loaded and has no PC objects, True
            self.empty = False
            self.player_chars = []
            self.player_count = len(self.player_chars)

    #def __del__(self):
    #    self.save()
    #    if self.instance_id:
    #        self.instance_destructor()

    def __repr__(self):
        if self.instance_id:
            return "<Instance: %d %d %s(%s): %d-%d>" % (self.instance_id, self.index, self.name,
                                                        self.file_name,
                                                        self.min_vnum,
                                                        self.max_vnum)
        else:
            return "<Template: %d %s(%s): %d-%d>" % (self.index, self.name,
                                                     self.file_name,
                                                     self.min_vnum,
                                                     self.max_vnum)

    def add_pc(self, player_char):
        if player_char.is_living and not player_char.is_npc():
            if not player_char.instance_id in self.player_chars:
                #Transition an empty area, to an occupied one, for Resets
                if self.empty:
                    self.empty = False
                    self.age = 0
                self.player_chars += [player_char.instance_id]
            else:
                raise ValueError('Player Character already in player_chars list! %d' % player_char.instance_id)
        else:
            raise KeyError('Entity not a player character, or is an NPC on area addition! %r' % type(player_char))

    def remove_pc(self, player_char):
        if player_char.is_living and not player_char.is_npc():
            if player_char.instance_id in self.player_chars:
                self.player_chars.remove(player_char.instance_id)
            else:
                raise ValueError('Player Character not in player_chars list! %d' % player_char.instance_id)
        else:
            raise KeyError('Entity not a player character, or is an NPC on area removal! %r' % type(player_char))

    def instance_setup(self):
        merc.global_instances[self.instance_id] = self
        merc.areas[self.instance_id] = merc.global_instances[self.instance_id]
        if self.name not in merc.instances_by_area.keys():
            merc.instances_by_area[self.name] = [self.instance_id]
        else:
            merc.instances_by_area[self.name].append(self.instance_id)

    def instance_destructor(self):
        merc.instances_by_area[self.name].remove(self.instance_id)
        del merc.areas[self.instance_id]
        del merc.global_instances[self.instance_id]

    def to_json(self, obj):
        if isinstance(obj, Area):
            special_keys = []
            result = {k: v for k, v in obj.__dict__.items() if k not in special_keys}
            result['__type__'] = 'Area'
            return result
        return obj

    def save(self):
        if not self.no_save:
            filename = '%03d_%s' % (self.index, self.name.replace(' ', '_'))
            if self.instance_id is None:
                pathname = os.path.join(settings.DUMP_DIR, 'world', 'areas', filename)
                os.makedirs(pathname, 0o755, True)
                filename = os.path.join(pathname, 'area.json')
            else:
                md5 = hashlib.md5(filename.encode()).hexdigest()
                pathname = os.path.join(settings.DUMP_DIR, 'world', 'instances', md5[0:2], md5[2:4])
                os.makedirs(pathname, 0o755, True)
                filename = os.path.join(pathname, '%d.json' % self.instance_id)
            logger.info('Area save file: %s', filename)
            if os.path.isfile(filename):
                os.replace(filename, filename + 'bkp')
            fp = open(filename, 'w')
            json.dump(self, fp, default=self.to_json)
            fp.close()
        return

    def restore(self):
        pass


class ExtraDescrData:
    def __init__(self, **kwargs):
        self.keyword = ""  # Keyword in look/examine
        self.description = ""
        if kwargs:
            [setattr(self, k, v) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
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
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            if self.to_room_vnum != -1 and not None:
                self.to_room = merc.instances_by_room[self.to_room_vnum][0]
            else:
                self.to_room = None
            if self.key <= 0:
                self.key = None
        if kwargs:
            [setattr(self, k, v) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data


class Reset:
    def __init__(self, template=None, **kwargs):
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
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            self.room = merc.instances_by_room[self.room][0]
        if kwargs:
            [setattr(self, k, v) for k, v in kwargs.items()]

    def __repr__(self):
        if not self.instance_id:
            return "Reset Area: %s Room: %d Type: %s" % (merc.roomTemplate[self.room].area,
                                                         self.room, self.command)

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
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
            [setattr(self, k, v) for k, v in template.__dict__.items()]
        if kwargs:
            [setattr(self, k, v) for k, v in kwargs.items()]

    def __repr__(self):
            return "Shop Mob: %s Room: %d" % (merc.characters[self.keeper].name, self.room)

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
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
            [setattr(self, k, v) for k, v in kwargs.items()]

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data
