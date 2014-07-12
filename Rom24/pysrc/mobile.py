from bit import Bit
from living import Living
import pyprogs
import merc
from tables import off_flags


class Mobile(Living):
    def __init__(self, template=None):
        super().__init__(template)
        self.memory = None
        self.spec_fun = None
        self.new_format = True
        self.area = ""
        self.vnum = 0
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

    def __repr__(self):
        return "<MobIndex: %s:%s>" % (self.short_descr, self.vnum)

    register_signal = pyprogs.register_signal
    absorb = pyprogs.absorb
