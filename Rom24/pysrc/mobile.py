from bit import Bit
from living import Living
import pyprogs
from tables import off_flags


class Mobile(Living):
    def __init__(self):
        super().__init__()
        self.memory = None
        self.spec_fun = None
        self.pIndexData = None
        self.off_flags = Bit(flags=off_flags)
        self.damage = [0, 0, 0]
        self.start_pos = 0
        self.default_pos = 0
        self.listeners = {}

    register_signal = pyprogs.register_signal
    absorb = pyprogs.absorb