from handler import Instancer
import merc

__author__ = 'venom'


class Area(Instancer):
    def __init__(self, template=None):
        super().__init__()
        self.name = ""
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
        if self.instance_id:
            self.instance_destructor()

    def __repr__(self):
        return "<%s(%s): %d-%d>" % (self.name,
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
            self.exit_info = 0
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
