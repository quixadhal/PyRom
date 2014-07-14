import logging

import merc


logger = logging.getLogger()

import random
import game_utils
import handler_game
from handler_magic import saves_spell
from merc import ROOM_VNUM_TEMPLE, WEAR_LIGHT, ITEM_LIGHT, AFF_PLAGUE, TO_AFFECTS, APPLY_STR, \
    DAM_DISEASE, TO_ROOM, areaTemplate, rooms, instances_by_room


class Location:
    def __init__(self):
        #Location
        super().__init__()
        self.room_template = 0
        self.environment = None

        self.in_living = None
        self.in_room = None
        self.in_item = None
        self.was_in_template = 0
        self.was_in_room = None

        self.on_template = 0
        self.on = None
        self.zone_template = ""
        self.zone = 0

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False

    def to_room(self, roomInstanceID):
        if not roomInstanceID:
            logger.error("Char_to_room: %s No instance %d", self.name, roomInstanceID)
            self.to_room(instances_by_room[ROOM_VNUM_TEMPLE][0])
            return
        room = rooms[roomInstanceID]
        room.people.append(self.instance_id)
        self.in_room = room.instance_id

        if not self.is_npc():
            #TODO change to area instances
            if areaTemplate[room.area].empty:
                areaTemplate[room.area].empty = False
                areaTemplate[room.area].age = 0

            areaTemplate[room.area].nplayer += 1

        item = merc.items.get(self.get_eq(WEAR_LIGHT), None)

        if item and item.item_type == ITEM_LIGHT and item.value[2] != 0:
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

            for vch_id in room.people[:]:
                vch = merc.characters[vch_id]
                if not saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not vch.is_immortal() and not vch.is_affected(AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return
    # * Move a char out of a room.
    def from_room(self):
        if not rooms[self.in_room]:
            logger.error("BUG: Char_from_room: %s No instance %d.", self.name, self.in_room)
            return
        room = rooms[self.in_room]
        if not self.is_npc():
            areaTemplate[room.area].nplayer -= 1
        item = merc.items.get(self.get_eq(WEAR_LIGHT), None)
        if item and item.item_type == ITEM_LIGHT and item.value[2] != 0 and room.light > 0:
            room.light -= 1

        if self.instance_id not in room.people:
            logger.error("BUG: Char_from_room: %s ch not found in instance %d.", self.name, room.instance_id)
            return
        room.people.remove(self.instance_id)
        self.in_room = None
        self.room_template = 0
        self.on = None  # sanity check!
        return

    def has_key(self, key):
        instance_id = [item_id for item_id in self.contents if merc.items[item_id] == key]
        if instance_id:
            return True
        return False
