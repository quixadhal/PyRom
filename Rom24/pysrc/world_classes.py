import os
import hashlib
import json
import logging
import tables

logger = logging.getLogger()

import merc
import instance
import settings
import type_bypass
import bit

__author__ = 'syn'


class Area(instance.Instancer, type_bypass.ObjectType):
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
            self.nplayer = 0
            self.reset_list = []
            self.file_name = ""
            self.credits = ""
            self.age = 15
            self.character = 0
            self.low_range = 0
            self.high_range = 0
            self.min_vnum = 0
            self.max_vnum = 0
            self.empty = False

    def __del__(self):
        self.save()
        if self.instance_id:
            self.instance_destructor()

    def __repr__(self):
        return "<%d %s(%s): %d-%d>" % (self.index, self.name,
                                       self.file_name,
                                       self.min_vnum,
                                       self.max_vnum)

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
                filename = os.path.join(pathname, '%d.json' % (self.instance_id))
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
    def __init__(self):
        self.keyword = "" # Keyword in look/examine
        self.description = ""


class Exit:
    def __init__(self, template=None):
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            if self.to_room_vnum != -1 and not None:
                self.to_room = merc.instances_by_room[self.to_room_vnum][0]
            else:
                self.to_room = None
            if self.key <= 0:
                self.key = None
        else:
            self.name = ""
            self.to_room_vnum = None
            self.to_room = None
            self.exit_info = bit.Bit(flags=tables.exit_flags)
            self.key = None
            self.key_vnum = None
            self.keyword = ""
            self.description = ""


class Reset:
    def __init__(self, template=None):
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            self.room = merc.instances_by_room[self.room][0]
        else:
            self.name = ""
            self.area = ""
            self.instance_id = None
            self.room = None
            self.command = ""
            self.arg1 = 0
            self.arg2 = 0
            self.arg3 = 0
            self.arg4 = 0

    def __repr__(self):
        if not self.instance_id:
            return "Reset Area: %s Room: %d Type: %s" % (merc.roomTemplate[self.room].area,
                                                         self.room, self.command )

class Shop:
    def __init__(self, template=None):
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
        else:
            self.keeper = None
            self.keeperTemplate = None
            self.room = None
            self.buy_type = {}
            self.profit_buy = 0
            self.profit_sell = 0
            self.open_hour = 0
            self.close_hour = 0

    def __repr__(self):
            return "Shop Mob: %s Room: %d" % (merc.characters[self.keeper].name, self.room)


class Gen:
    def __init__(self):
        self.valid = False
        self.skill_chosen = {}
        self.group_chosen = {}
        self.points_chosen = 0
