import logging

logger = logging.getLogger(__name__)

from rom24 import bit
from rom24 import const
from rom24 import merc


class Immortal:
    def __init__(self):
        super().__init__()
        # Immortal
        self._trust = 0
        self.invis_level = 0
        self.incog_level = 0
        self.wiznet = bit.Bit(flags=const.wiznet_table)

    def is_immortal(self):
        return self.trust >= merc.LEVEL_IMMORTAL

    @property
    def trust(self):
        if self.is_npc():
            if self.level >= merc.LEVEL_HERO:
                return merc.LEVEL_HERO - 1
            else:
                return self.level
        trust = self._trust
        level = self.level
        if self.desc and self.desc.original:
            trust = self.desc.original._trust
            level = self.desc.original.level
        if trust:
            return trust
        return level

    @trust.setter
    def trust(self, value):
        self._trust = int(value)
