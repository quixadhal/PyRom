import logging


logger = logging.getLogger()

import random
import game_utils
import handler_game
from handler_magic import saves_spell
from merc import ROOM_VNUM_TEMPLE, WEAR_LIGHT, ITEM_LIGHT, AFF_PLAGUE, TO_AFFECTS, APPLY_STR, \
    DAM_DISEASE, TO_ROOM, room_templates, area_templates, room_instances, area_instances


class Location:
    def __init__(self):
        #Location
        super().__init__()
        self.room_template = 0
        self.in_room_instance = 0
        self.was_in_template = 0
        self.was_in_room_instance = 0
        self.on = 0
        self.on_instance = 0
        self.zone_template = ""
        self.zone_instance = 0

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False

    def to_room(self, pRoomInstance):
        if not pRoomInstance:
            logger.error("Char_to_room: %s No instance %d", self.name, pRoomInstance)
            self.to_room(game_utils.find_vnum_instance('room', 1, ROOM_VNUM_TEMPLE))
            return
        room = room_instances[pRoomInstance]
        room.people.append(self)

        if not self.is_npc():
            #TODO change to area instances
            if area_templates[room.area].template_empty:
                area_templates[room.area].template_empty = False
                area_templates[room.area].template_age = 0

            area_templates[room.area].template_nplayer += 1

        obj = self.get_eq(WEAR_LIGHT)

        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            room.light += 1

        if self.is_affected(AFF_PLAGUE):
            af = [af for af in self.affected if af.type == 'plague']
            if not af:
                self.affected_by.rem_bit(AFF_PLAGUE)
                return
            af = af[0]

            if af.level == 1:
                return
            plague = handler_game.AFFECT_DATA()
            plague.where = TO_AFFECTS
            plague.type = "plague"
            plague.level = af.level - 1
            plague.duration = random.randint(1, 2 * plague.level)
            plague.location = APPLY_STR
            plague.modifier = -5
            plague.bitvector = AFF_PLAGUE

            for vch in room.people[:]:
                if not saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not vch.is_immortal() and not vch.is_affected(AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return
    # * Move a char out of a room.
    def from_room(self):
        if not room_instances[self.in_room_instance]:
            logger.error("BUG: Char_from_room: %s No instance %d.", self.name, self.in_room_instance)
            return
        room = room_instances[self.in_room_instance]
        if not self.is_npc():
            area_templates[room.area].nplayer -= 1
        obj = self.get_eq(WEAR_LIGHT)
        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and room.light > 0:
            room.light -= 1

        if self not in room.people:
            logger.error("BUG: Char_from_room: %s ch not found in instance %d.", self.name, room.instance_id)
            return
        room.people.remove(self)
        self.in_room_instance = 0
        self.room_template = 0
        self.on_instance = 0  # sanity check!
        return

    def has_key(self, key):
        for obj in self.contents:
            if obj.pIndexData.vnum == key:
                return True
        return False
