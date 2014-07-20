__author__ = 'venom'

wear_location_map = {-1: 'Nothing',
                     0: 'Light',
                     1: 'Left Finger',
                     2: 'Right Finger',
                     3: 'Neck 1',
                     4: 'Neck 2',
                     5: 'Body',
                     6: 'Head',
                     7: 'Legs',
                     8: 'Feet',
                     9: 'Hands',
                     10: 'Arms',
                     11: 'Shield',
                     12: 'About',
                     13: 'Waist',
                     14: 'Left Wrist',
                     15: 'Right Wrist',
                     16: 'Wield',
                     17: 'Hold',
                     18: 'Float',
                     19: 'Max Wear'}

item_attribute_map = {'None': [0, True],
                      'Glow': [1, False],
                      'Hum': [2, False],
                      'Dark': [3, False],
                      'Lock': [4, False],
                      'Evil': [5, False],
                      'Invis': [6, False],
                      'Magic': [7, False],
                      'No Drop': [8, False],
                      'Bless': [9, False],
                      'Anti-Good': [10, False],
                      'Anti-Evil': [11, False],
                      'Anti-Neutral': [12, False],
                      'No Remove': [13, False],
                      'Inventory': [14, False],
                      'No Purge': [15, False],
                      'Rot Death': [16, False],
                      'Vis Death': [17, False],
                      'Non Metal': [18, False],
                      'Melt Drop': [19, False],
                      'Had Timer': [20, False],
                      'Sell Extract': [21, False],
                      'Burn-Proof': [22, False],
                      'No Uncurse': [23, False]}

class Equipment:
    def __init__(self):
        super().__init__()
        self._worn = {}
        self._wear_loc = {}
        self._wear_flags = {}

    def __repr__(self):
        if self.worn.items():
            return 'Wearing {worn.keys()} items as equipment.'.format(worn=self.worn)
        elif self.wearable:
            where = {position for position in self.wearable.keys()}
            can_wear_on = ', '.join(str(item) for item in where)
            return 'Can be worn on {can_wear_on}.'.format(can_wear_on=can_wear_on)
        else:
            pass

    def equip(self):
        pass

    def unequip(self):
        pass

    def apply_paf(self):
        pass

    def remove_paf(self):
        pass

    @property
    def wear_loc(self, print_string=False):
        where_set = {where for where, truth in self._wear_loc.items() if self._wear_loc[where] is True}
        if where_set:
            if print_string is False:
                return where_set
            elif print_string is True:
                clean_string = ', '.join(str(item) for item in where_set)
                return '{self.short_descr} can be worn on {clean_string}.'.format(self=self, clean_string=clean_string)
        else:
            return None

    @wear_loc.setter
    def wear_loc(self, object=None, location=None):
        if type(location) == str:
            if location in wear_location_map.values():
                if object:
                    self._wear_loc[location] = {True, object.instance_id]
                else:


