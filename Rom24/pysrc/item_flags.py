import collections

__author__ = 'venom'

import logging

logger = logging.getLogger()
import equipment
import sys


class ItemFlags(equipment.Equipment):
    def __init__(self):
        super().__init__()
        # Wear Flags
        self._light = False
        self._head = False
        self._neck = False
        self._collar = False
        self._left_finger = False
        self._right_finger = False
        self._about_body = False
        self._waist = False
        self._arms = False
        self._legs = False
        self._feet = False
        self._hands = False
        self._left_wrist = False
        self._right_wrist = False
        self._off_hand = False
        self._main_hand = False
        self._float = False
        self._body = False
        # Item Attribute Flags
        self._melt_drop = False
        self._rot_death = False
        self._vis_death = False
        self._sell_extract = False
        self._magic = False
        self._glow = False
        self._hum = False
        self._dark = False
        self._lock = False
        self._evil = False
        self._invis = False
        self._bless = False
        self._non_metal = False
        self._had_timer = False
        self._burn_proof = False
        self._take = False
        # Item Restriction Flags
        self._no_drop = False
        self._no_remove = False
        self._no_uncurse = False
        self._no_purge = False
        self._anti_good = False
        self._anti_evil = False
        self._anti_neutral = False
        self._inventory = False
        self._no_locate = False
        # Weapon Attributes
        self._two_handed = False
        self._flaming = False
        self._sharp = False
        self._frost = False
        self._vampiric = False
        self._vorpal = False
        self._shocking = False
        self._poison = False

    @property
    def head(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @head.setter
    def head(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def legs(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @legs.setter
    def legs(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def feet(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @feet.setter
    def feet(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def hands(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @hands.setter
    def hands(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def float(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @float.setter
    def float(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def left_finger(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @left_finger.setter
    def left_finger(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def right_finger(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @right_finger.setter
    def right_finger(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def right_wrist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @right_wrist.setter
    def right_wrist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def left_wrist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @left_wrist.setter
    def left_wrist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def waist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @waist.setter
    def waist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def about_body(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @about_body.setter
    def about_body(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def light(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @light.setter
    def light(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def body(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @body.setter
    def body(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def neck(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @neck.setter
    def neck(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def collar(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @collar.setter
    def collar(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def arms(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @arms.setter
    def arms(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def off_hand(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @off_hand.setter
    def off_hand(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    @property
    def main_hand(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.equips_to.set else False

    @main_hand.setter
    def main_hand(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self.equips_to.set.add(func_name)
        else:
            self.equips_to.set.discard(func_name)

    # Item Attribute Flags
    @property
    def melt_drop(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @melt_drop.setter
    def melt_drop(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def rot_death(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @rot_death.setter
    def rot_death(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def vis_death(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @vis_death.setter
    def vis_death(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def sell_extract(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @sell_extract.setter
    def sell_extract(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def magic(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @magic.setter
    def magic(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def glow(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @glow.setter
    def glow(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def hum(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @hum.setter
    def hum(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def dark(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @dark.setter
    def dark(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def lock(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @lock.setter
    def lock(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def evil(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @evil.setter
    def evil(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def invis(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @invis.setter
    def invis(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def bless(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @bless.setter
    def bless(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def non_metal(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @non_metal.setter
    def non_metal(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def had_timer(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @had_timer.setter
    def had_timer(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def burn_proof(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @burn_proof.setter
    def burn_proof(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    @property
    def take(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_attributes.set else False

    @take.setter
    def take(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self.item_attributes.set.add(func_name)
        else:
            self.item_attributes.set.discard(func_name)

    # Item Restriction Flags
    @property
    def no_remove(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_remove.setter
    def no_remove(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def no_uncurse(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_uncurse.setter
    def no_uncurse(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def no_purge(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_purge.setter
    def no_purge(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def anti_good(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @anti_good.setter
    def anti_good(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def anti_evil(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @anti_evil.setter
    def anti_evil(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def anti_neutral(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @anti_neutral.setter
    def anti_neutral(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def inventory(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @inventory.setter
    def inventory(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def no_locate(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_locate.setter
    def no_locate(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    # Weapon Attributes
    @property
    def no_remove(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_remove.setter
    def no_remove(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def no_uncurse(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_uncurse.setter
    def no_uncurse(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)

    @property
    def no_purge(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.item_restrictions.set else False

    @no_purge.setter
    def no_purge(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self.item_restrictions.set.add(func_name)
        else:
            self.item_restrictions.set.discard(func_name)
    
    @property
    def two_handed(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @two_handed.setter
    def two_handed(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def flaming(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
    
    @flaming.setter
    def flaming(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def sharp(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @sharp.setter
    def sharp(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def frost(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @frost.setter
    def frost(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def vampiric(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @vampiric.setter
    def vampiric(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def vorpal(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @vorpal.setter
    def vorpal(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def shocking(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @shocking.setter
    def shocking(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
        
    @property
    def poison(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return True if func_name in self.weapon_attributes.set else False
        
    @poison.setter
    def poison(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self.weapon_attributes.set.add(func_name)
        else:
            self.weapon_attributes.set.discard(func_name)
