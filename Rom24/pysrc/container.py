import const
import merc


class Container:
    def __init__(self):
        super().__init__()
        self.contents = []
        self.carry_weight = 0
        self.carry_number = 0

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