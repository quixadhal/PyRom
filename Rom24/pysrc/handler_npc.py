import logging


logger = logging.getLogger()


from bit import Bit
import living
import merc
import pyprogs
from tables import off_flags


class Npc(living.Living):
    def __init__(self):
        super().__init__()
        self.vnum = 0  # Needs to come before the template to setup the instance
        self.memory = None
        self.spec_fun = None
        self.new_format = True
        self.area = ""
        self.off_flags = Bit(flags=off_flags)
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

    def __del__(self):
        logger.trace("Freeing %s" % str(self))

    def __repr__(self):
        if self.instance_id:
            return "<NPC Instance: %s ID %d template %d>" % (self.short_descr, self.instance_id, self.vnum)
        else:
            return "<NPC Template: %s:%s>" % (self.short_descr, self.vnum)

    def instance_setup(self):
        merc.global_instances[self.instance_id] = self
        merc.characters[self.instance_id] = merc.global_instances[self.instance_id]
        if self.vnum not in merc.instances_by_character.keys():
            merc.instances_by_character[self.vnum] = [self.instance_id]
        else:
            merc.instances_by_character[self.vnum].append(self.instance_id)

    def instance_destructor(self):
        if self.vnum in merc.instances_by_character:
            instance_list = merc.instances_by_character[self.vnum]
            if self.instance_id in instance_list:
                instance_list.remove(self.instance_id)
        if self.instance_id in merc.characters:
            del merc.characters[self.instance_id]
        if self.instance_id in merc.global_instances:
            del merc.global_instances[self.instance_id]

    register_signal = pyprogs.register_signal
    absorb = pyprogs.absorb
