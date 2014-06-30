import logging


logger = logging.getLogger()

import random
import game_utils
import handler_game
from handler_magic import saves_spell
from merc import room_index_hash, ROOM_VNUM_TEMPLE, WEAR_LIGHT, ITEM_LIGHT, AFF_PLAGUE, TO_AFFECTS, APPLY_STR, \
    DAM_DISEASE, TO_ROOM


class Location:
    def __init__(self):
        #Location
        super().__init__()
        self.in_room = None
        self.was_in_room = None
        self.on = None
        self.zone = None

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False

    def to_room(self, pRoomIndex):
        if not pRoomIndex:
            logger.error("Char_to_room: None. %s", self.name)
            self.to_room(room_index_hash[ROOM_VNUM_TEMPLE])
            return

        self.in_room = pRoomIndex
        pRoomIndex.people.append(self)

        if not self.is_npc():
            if self.in_room.area.empty:
                self.in_room.area.empty = False
                self.in_room.area.age = 0

            self.in_room.area.nplayer += 1

        obj = self.get_eq(WEAR_LIGHT)

        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0:
            self.in_room.light += 1

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

            for vch in self.in_room.people[:]:
                if not saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                        and not vch.is_immortal() and not vch.is_affected(AFF_PLAGUE) \
                        and random.randint(0, 5) == 0:
                    vch.send("You feel hot and feverish.\n\r")
                    handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                    vch.affect_join(plague)
        return
    # * Move a char out of a room.
    def from_room(self):
        if not self.in_room:
            logger.error("BUG: Char_from_room: None.")
            return

        if not self.is_npc():
            self.in_room.area.nplayer -= 1
        obj = self.get_eq(WEAR_LIGHT)
        if obj and obj.item_type == ITEM_LIGHT and obj.value[2] != 0 and self.in_room.light > 0:
            self.in_room.light -= 1

        if self not in self.in_room.people:
            logger.error("BUG: Char_from_room: ch not found.")
            return
        self.in_room.people.remove(self)
        self.in_room = None
        self.on = None  # sanity check! */
        return