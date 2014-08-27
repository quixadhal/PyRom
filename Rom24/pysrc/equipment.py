__author__ = 'syn'

import sys
import json
import collections
import logging

logger = logging.getLogger()

import instance


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


class Equipped:
    def __init__(self, equip_dict: dict=None):
        self._equipped = collections.OrderedDict([('light', None),
                                                ('left_finger', None),
                                                ('right_finger', None),
                                                ('neck', None),
                                                ('collar', None),
                                                ('body', None),
                                                ('head', None),
                                                ('legs', None),
                                                ('feet', None),
                                                ('hands', None),
                                                ('arms', None),
                                                ('about_body', None),
                                                ('waist', None),
                                                ('left_wrist', None),
                                                ('right_wrist', None),
                                                ('main_hand', None),
                                                ('off_hand', None),
                                                ('held', None),
                                                ('float', None)])
        if equip_dict:
            for k, v in equip_dict.items():
                self._equipped[k] = v

    @property
    def available(self):
        return {slot for slot in self._equipped.keys() if not self._equipped[slot]}

    @property
    def light(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def head(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)


    @property
    def neck(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def collar(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def left_finger(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def right_finger(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def body(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def waist(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def arms(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def legs(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def left_wrist(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def right_wrist(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def hands(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def feet(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def about(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def main_hand(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def off_hand(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def held(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    @property
    def float(self):
        func_name = sys._getframe().f_code.co_name
        return instance.global_instances.get(self._equipped[func_name], None)

    # Serialization
    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return{cls_name: {'equipped': outer_encoder(self._equipped)}}

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            return cls(equip_dict=outer_decoder(data[cls_name]['equipped']))
        return data
