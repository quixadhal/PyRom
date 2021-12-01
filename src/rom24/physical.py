import logging

logger = logging.getLogger(__name__)

from rom24 import bit
from rom24 import tables


class Physical:
    def __init__(self):
        super().__init__()
        self.name = ""
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.form = bit.Bit(flags=tables.form_flags)
        self.parts = bit.Bit(flags=tables.part_flags)
        self.size = 0
        self.material = ""
        self.weight = 0
