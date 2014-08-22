__author__ = 'syn'
import sys
import json
import logging

logger = logging.getLogger()


class ItemFlags:
    def __init__(self, et_data: set=None, iaf_data: set=None, ir_data: set=None, wa_data: set=None):
        self._equips_to = set({})
        if et_data:
            self._equips_to |= set(et_data)

        self._item_attributes = set({})
        if iaf_data:
            self._item_attributes |= set(iaf_data)

        self._item_restrictions = set({})
        if ir_data:
            self._item_restrictions |= set(ir_data)

        self._weapon_attributes = set({})
        if wa_data:
            self._weapon_attributes |= set(wa_data)

    @property
    def head(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @head.setter
    def head(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def legs(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @legs.setter
    def legs(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def feet(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @feet.setter
    def feet(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def hands(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @hands.setter
    def hands(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def float(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @float.setter
    def float(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def left_finger(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @left_finger.setter
    def left_finger(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def right_finger(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @right_finger.setter
    def right_finger(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def right_wrist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @right_wrist.setter
    def right_wrist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def left_wrist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @left_wrist.setter
    def left_wrist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def waist(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @waist.setter
    def waist(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def about_body(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @about_body.setter
    def about_body(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def light(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @light.setter
    def light(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def body(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @body.setter
    def body(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def neck(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @neck.setter
    def neck(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def collar(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @collar.setter
    def collar(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def arms(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @arms.setter
    def arms(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def off_hand(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @off_hand.setter
    def off_hand(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def main_hand(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @main_hand.setter
    def main_hand(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    @property
    def held(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._equips_to else False

    @held.setter
    def held(self, is_equippable):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if is_equippable:
            self._equips_to |= {func_name}
        else:
            self._equips_to -= {func_name}

    # Item Attribute Flags
    @property
    def melt_drop(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @melt_drop.setter
    def melt_drop(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def rot_death(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @rot_death.setter
    def rot_death(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def vis_death(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @vis_death.setter
    def vis_death(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def sell_extract(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @sell_extract.setter
    def sell_extract(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def magic(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @magic.setter
    def magic(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def glow(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @glow.setter
    def glow(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def hum(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @hum.setter
    def hum(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def dark(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @dark.setter
    def dark(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def lock(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @lock.setter
    def lock(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def evil(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @evil.setter
    def evil(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def invis(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @invis.setter
    def invis(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def bless(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @bless.setter
    def bless(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def non_metal(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @non_metal.setter
    def non_metal(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def had_timer(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @had_timer.setter
    def had_timer(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def burn_proof(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @burn_proof.setter
    def burn_proof(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def take(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @take.setter
    def take(self, has_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_attr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    @property
    def shop_inventory(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_attributes else False

    @shop_inventory.setter
    def shop_inventory(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_attributes |= {func_name}
        else:
            self._item_attributes -= {func_name}

    # Item Restriction Flags
    @property
    def no_drop(self):
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_drop.setter
    def no_drop(self, has_restr):
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_sac(self):
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_sac.setter
    def no_sac(self, has_restr):
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_remove(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_remove.setter
    def no_remove(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_uncurse(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_uncurse.setter
    def no_uncurse(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_purge(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_purge.setter
    def no_purge(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def anti_good(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @anti_good.setter
    def anti_good(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def anti_evil(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @anti_evil.setter
    def anti_evil(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def anti_neutral(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @anti_neutral.setter
    def anti_neutral(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_locate(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_locate.setter
    def no_locate(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    # Weapon Attributes
    @property
    def no_remove(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_remove.setter
    def no_remove(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_uncurse(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_uncurse.setter
    def no_uncurse(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}

    @property
    def no_purge(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._item_restrictions else False

    @no_purge.setter
    def no_purge(self, has_restr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if has_restr:
            self._item_restrictions |= {func_name}
        else:
            self._item_restrictions -= {func_name}
    
    @property
    def two_handed(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @two_handed.setter
    def two_handed(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def flaming(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
    
    @flaming.setter
    def flaming(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def sharp(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @sharp.setter
    def sharp(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def frost(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @frost.setter
    def frost(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def vampiric(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @vampiric.setter
    def vampiric(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def vorpal(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @vorpal.setter
    def vorpal(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def shocking(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @shocking.setter
    def shocking(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}
        
    @property
    def poison(self):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        return func_name if func_name in self._weapon_attributes else False
        
    @poison.setter
    def poison(self, weap_attr):
        """
       TODO: write documentation
       """
        func_name = sys._getframe().f_code.co_name
        if weap_attr:
            self._weapon_attributes |= {func_name}
        else:
            self._weapon_attributes -= {func_name}

    # Serialization
    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {
            cls_name: {
                'equips_to': outer_encoder(self._equips_to),
                'item_attributes': outer_encoder(self._item_attributes),
                'item_restrictions': outer_encoder(self._item_restrictions),
                'weapon_attributes': outer_encoder(self._weapon_attributes),
            }
        }

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            return cls(et_data=outer_decoder(data[cls_name]['equips_to']),
                       iaf_data=outer_decoder(data[cls_name]['item_attributes']),
                       ir_data=outer_decoder(data[cls_name]['item_restrictions']),
                       wa_data=outer_decoder(data[cls_name]['weapon_attributes']))
        return data
