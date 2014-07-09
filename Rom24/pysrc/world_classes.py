import game_utils
import handler
import merc

__author__ = 'venom'

class AREA_DATA:
    def __init__(self, template=None):
        if template:
            copy = template.__dict__.copy()
            for k, v in copy.items():
                setattr(self, k, v)
            self.instance_id = handler.global_instance_generator()
            merc.global_instances[self.instance_id] = self
            merc.area_instances[self.instance_id] = merc.global_instances[self.instance_id]
            copy = None
        else:
            self.instance_id = None
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

class EXTRA_DESCR_DATA:
    def __init__(self):
        self.keyword = "" # Keyword in look/examine
        self.description = ""


class EXIT_DATA:
    def __init__(self, template=None):
        if template:
            copy = template.__dict__.copy()
            for k, v in copy.items():
                setattr(self, k, v)
            self.instance_id = handler.global_instance_generator()
            merc.global_instances[self.instance_id] = self
            merc.exit_instances[self.instance_id] = merc.global_instances[self.instance_id]
            self.to_room_instance = game_utils.find_vnum_instance('room', 1, self.roomTemplate)
            if self.key <= 0:
                self.key = None
            else:
                self.key = game_utils.find_vnum_instance('obj', 1, self.key)
            copy = None
        else:
            self.name = ""
            self.to_room_template = 0
            self.to_room_instance = 0
            self.instance_id = None
            self.exitTemplate = 0
            self.roomTemplate = 0
            self.exit_info = 0
            self.key = 0
            self.keyword = ""
            self.description = ""

class RESET_DATA:
    def __init__(self, template=None):
        if template:
            copy = template.__dict__.copy()
            for k, v in copy.items():
                setattr(self, k, v)
            self.instance_id = handler.global_instance_generator()
            merc.global_instances[self.instance_id] = self
            merc.reset_instances[self.instance_id] = merc.global_instances[self.instance_id]
            self.room = game_utils.find_vnum_instance('room', 1, self.room)
            copy = None
        else:
            self.instance_id = None
            self.roomTemplate = None
            self.room = None
            self.command = ""
            self.arg1 = 0
            self.arg2 = 0
            self.arg3 = 0
            self.arg4 = 0

    def __repr__(self):
        if not self.instance_id:
            return "Reset Area: %s Room: %d Type: %s" % (merc.room_templates[self.roomTemplate].area,
                                                         self.roomTemplate, self.command )
        else:
            return "Reset %d Area: %s Room: %d Type: %s" % (self.instance_id, merc.room_instances[self.room].area,
                                                            self.room, self.command)

class SHOP_DATA:
    def __init__(self, template=None):
        if template:
            copy = template.__dict__.copy()
            for k, v in copy.items():
                setattr(self, k, v)
            self.instance_id = handler.global_instance_generator()
            merc.global_instances[self.instance_id] = self
            merc.shops_instances[self.instance_id] = merc.global_instances[self.instance_id]
            self.room = game_utils.find_vnum_instance('room', 1, self.room)
            self.keeper = game_utils.find_vnum_instance('mob', 1, self.keeperTemplate)
            copy = None
        else:
            self.instance_id = None
            self.keeper = None
            self.keeperTemplate = None
            self.room = None
            self.buy_type = {}
            self.profit_buy = 0
            self.profit_sell = 0
            self.open_hour = 0
            self.close_hour = 0

    def __repr__(self):
        if not self.instance_id:
            return "Shop Mob: %s Room: %d" % (merc.mob_instances[self.keeper].name, self.room)
        else:
            return "Instance ID: %d Shop Mob: %s Room: %d" % (self.instance_id, merc.mob_instances[self.keeper].name,
                                                              self.room)


class GEN_DATA:
    def __init__(self):
        self.valid = False
        self.skill_chosen = {}
        self.group_chosen = {}
        self.points_chosen = 0
