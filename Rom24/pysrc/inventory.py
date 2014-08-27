import logging

logger = logging.getLogger()

import const
import merc
import instance


class Inventory:
    def __init__(self):
        super().__init__()
        self.inventory = []
        self.carry_weight = 0
        self.carry_number = 0

    @property
    def people(self):
            return tuple(char_id for char_id in self.inventory if char_id in instance.characters)

    @property
    def items(self):
            return tuple(item_id for item_id in self.inventory if item_id in instance.items)

    def can_carry_n(self):
        if not self.is_npc() and self.level >= merc.LEVEL_IMMORTAL:
            return 1000
        if self.is_npc() and self.act.is_set(merc.ACT_PET):
            return 0
        return merc.MAX_WEAR + 2 * self.stat(merc.STAT_DEX) + self.level

    # * Retrieve a character's carry capacity.
    def can_carry_w(self):
        if not self.is_npc() and self.level >= merc.LEVEL_IMMORTAL:
            return 10000000
        if self.is_npc() and self.act.is_set(merc.ACT_PET):
            return 0
        return const.str_app[self.stat(merc.STAT_STR)].carry * 10 + self.level * 25
