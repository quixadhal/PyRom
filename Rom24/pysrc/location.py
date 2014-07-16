import logging

import merc
import state_checks


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
        self.in_environment = None
        self.was_in_template = 0
        self.was_in_room = None

        self.on_template = 0
        self.on = None
        self.zone_template = ""
        self.zone = 0
        self.area = None
        self.light = 0
    @property
    def in_living(self):
        from living import Living
        in_environment = merc.global_instances.get(self.in_environment, None)
        while in_environment:
            if isinstance(in_environment, Living):
                return in_environment.instance_id
            in_environment = merc.global_instances.get(in_environment.in_environment, None)
        return None

    @property
    def in_room(self):
        from handler_room import Room
        in_environment = merc.global_instances.get(self.in_environment, None)
        while in_environment:
            if isinstance(in_environment, Room):
                return in_environment.instance_id
            in_environment = merc.global_instances.get(in_environment.in_environment, None)
        return None

    @property
    def in_item(self):
        from handler_item import Items
        in_environment = merc.global_instances.get(self.in_environment, None)
        while in_environment:
            if isinstance(in_environment, Items):
                return in_environment.instance_id
            in_environment = merc.global_instances.get(in_environment.in_environment, None)
        return None

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False



    # * Move an instance from a location
    def from_environment(self):
        if self.in_environment not in merc.global_instances:
            logger.error("BUG: form_environment: %s No instance %d.", self.name, self.in_environemnt)
            return
        instance = merc.global_instances[self.in_environment]
        try:  # For characters only
            if not self.is_npc() and instance.area in areaTemplate:
                areaTemplate[instance.area].nplayer -= 1
            item = merc.items.get(self.get_eq(WEAR_LIGHT), None)

        except AttributeError:
            item = instance

        try:  # see if item is a light.
            if item and item.item_type == ITEM_LIGHT and item.value[2] != 0 and room.light > 0:
                instance.light -= 1
            if self.wear_loc != merc.WEAR_NONE:
                instance.unequip(self.instance_id)
            instance.carry_number -= self.get_number()
            instance.carry_weight -= self.get_weight()
        except AttributeError:
            pass

        if self.instance_id not in instance.contents:
            logger.error("BUG: from_environment: %s ch not found in instance %d.", self.name, room.instance_id)
            return
        instance.contents.remove(self.instance_id)

        while instance:
            if instance.in_living:
                merc.characters[instance.in_living].carry_number -= self.get_number()
                merc.characters[instance.in_living].carry_weight -= self.get_weight() * \
                                                                      state_checks.WEIGHT_MULT(instance) // 100
            instance = merc.global_instances.get(instance.in_environment, None)

        self.in_environment = None
        self.room_template = 0
        self.on = None  # sanity check!
        return


    # * Give an obj to a char.
    def to_environment(self, instance):
        if type(instance) is int:
            instance = merc.global_instances.get(instance, None)
        if not instance:
            logger.error(In)
            return

        instance.contents.append(self.instance_id)
        self.in_environment = instance.instance_id
        instance.carry_number += self.get_number()
        instance.carry_weight += self.get_weight()
        try: # if a player leaves a room.
            if not self.is_npc():
                #TODO change to area instances
                if areaTemplate[instance.area].empty:
                    areaTemplate[instance.area].empty = False
                    areaTemplate[instance.area].age = 0

                areaTemplate[instance.area].nplayer += 1

            item = merc.items.get(self.get_eq(WEAR_LIGHT), None)

            if item and item.item_type == ITEM_LIGHT and item.value[2] != 0:
                instance.light += 1

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

                for vch_id in instance.people[:]:
                    vch = merc.characters[vch_id]
                    if not saves_spell(plague.level - 2, vch, DAM_DISEASE) \
                            and not vch.is_immortal() and not vch.is_affected(AFF_PLAGUE) \
                            and random.randint(0, 5) == 0:
                        vch.send("You feel hot and feverish.\n\r")
                        handler_game.act("$n shivers and looks very ill.", vch, None, None, TO_ROOM)
                        vch.affect_join(plague)
        except AttributeError:
            pass

        try:  # if instance is an item
            if instance.vnum == merc.OBJ_VNUM_PIT:
                self.cost = 0

            while instance:
                if instance.in_living:
                    merc.characters[instance.in_living].carry_number += self.get_number()
                    merc.characters[instance.in_living].carry_weight += \
                        self.get_weight() * state_checks.WEIGHT_MULT(instance) // 100
                instance = instance.in_environment
        except:
            pass
        return



    def has_key(self, key):
        instance_id = [item_id for item_id in self.items if merc.items[item_id].vnum == key.vnum]
        if instance_id:
            return True
        return False

    # * Return # of objects which an object counts as.
    # * Thanks to Tony Chamberlain for the correct recursive code here.
    def get_number(self):
        try:  # if self is an item.
            noweight = [merc.ITEM_CONTAINER, merc.ITEM_MONEY, merc.ITEM_GEM, merc.ITEM_JEWELRY]
            if self.item_type in noweight:
                number = 0
            else:
                number = 1
        except AttributeError:
            number = 1

        contents = self.contents[:]
        counted = [self.instance_id]
        for content_id in contents:
            content = merc.items[content_id]
            number += 1
            if content.instance_id in counted:
                logger.debug("BUG: Objects contain eachother. %s(%d) - %s(%d)" %
                             (self.short_descr, self.instance_id, content.short_descr, content.instance_id))
                break
            counted.append(content)
            contents.extend(content.contents)

        return number

    #
    # * Return weight of an object, including weight of contents.
    def get_weight(item):
        weight = item.weight
        contents = item.contents[:]
        counted = [item.instance_id]
        for content_id in contents:
            content = merc.items[content_id]
            if content.instance_id in counted:
                print("BUG: Objects contain eachother. %s(%d) - %s(%d)" %
                      (item.short_descr, item.instance_id, content.short_descr, content.instance_id))
                break
            counted.append(content)
            contents.extend(content.contents)
            try:  # For items in containers
                weight += content.weight * state_checks.WEIGHT_MULT(item) // 100
            except AttributeError:
                pass

        return weight

    def true_weight(item):
        weight = item.weight
        for content_id in item.contents:
            content = merc.items[content_id]
            weight += content.get_weight()
        return weight

