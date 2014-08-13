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
