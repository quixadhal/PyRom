__author__ = 'syn'

import logging

logger = logging.getLogger()

class ObjectType:
    def __init__(self):
        super().__init__()
        self.is_item = False
        self.is_room = False
        self.is_living = False
        self.is_area = False
        #self.is_npc = False
        #self.is_pc = False
