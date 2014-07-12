import game_utils
import handler
import merc

__author__ = 'venom'

class Area:
    def __init__(self, template=None):
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            handler.Instancer.id_generator(self)
        else:
            self.instance_id = None
            self.nplayer = 0
            self.reset_list = []
            self.file_name = ""
            self.name = ""
            self.credits = ""
            self.age = 15
            self.character = 0
            self.low_range = 0
            self.high_range = 0
            self.min_vnum = 0
            self.max_vnum = 0
            self.empty = False

    def __repr__(self):
        return "<%s(%s): %d-%d>" % (self.name,
                                    self.file_name,
                                    self.min_vnum,
                                    self.max_vnum)

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
            self.room = merc.instances_by_room[self.roomTemplate][0]
        else:
            self.instance_id = None
            self.room = None
            self.command = ""
            self.arg1 = 0
            self.arg2 = 0
            self.arg3 = 0
            self.arg4 = 0

    def __repr__(self):
        if not self.instance_id:
            return "Reset Area: %s Room: %d Type: %s" % (merc.roomTemplate[self.roomTemplate].area,
                                                         self.roomTemplate, self.command )

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
