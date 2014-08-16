import sys
import merc

__author__ = 'syn'


class Equipment:
    def __init__(self):
        super().__init__()
        self._equipped = None
        self._equips_to = None
        self._equipped_to = None

    def equip(self, item, replace: bool=False, verbose: bool=True, verbose_all: bool=True, to_loc: str=None):
        pass

    def unequip(self, unequip_from, replace: bool=True):
        pass


class EquipSlotInstance:
    def __init__(self, equip_dict):
        self._slots = equip_dict

    @property
    def available(self):
        return {slot for slot in self._slots.keys() if not self._slots[slot]}

    @property
    def light(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def head(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)


    @property
    def neck(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def collar(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def left_finger(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def right_finger(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def body(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def waist(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def arms(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def legs(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def left_wrist(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def right_wrist(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def hands(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def feet(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def about(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def main_hand(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def off_hand(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def held(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)

    @property
    def float(self):
        func_name = sys._getframe().f_code.co_name
        return merc.global_instances.get(self._slots[func_name], None)
