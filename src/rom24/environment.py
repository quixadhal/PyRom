import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import state_checks
from rom24 import game_utils
from rom24 import instance


class Environment:
    def __init__(self):
        """ """
        super().__init__()
        self._environment = None
        self.was_in_room = None
        # When we load into a game without persistent room instances, this will get us to logged room
        self._room_vnum = None
        self.on = None
        self.zone_template = ""
        self.zone = 0
        self.area = None
        self.available_light = 0

    @property
    def environment(self):
        return instance.global_instances.get(self._environment, None)

    @environment.setter
    def environment(self, input_value):
        if not input_value:
            self._environment = None
        elif type(input_value) is int:
            self._environment = input_value
        else:
            raise TypeError(
                "Environment trying to be set with non integer value %r"
                % type(input_value)
            )

    @property
    def in_area(self):
        current_step = self.environment
        while current_step:
            if current_step.is_area:
                return current_step
            current_step = current_step.environment
        return None

    @property
    def in_living(self):
        current_step = self.environment
        while current_step:
            if current_step.is_living:
                return current_step
            current_step = current_step.environment
        return None

    @property
    def in_room(self):
        current_step = self.environment
        while current_step:
            if current_step.is_room:
                return current_step
            current_step = current_step.environment
        return None

    @property
    def in_item(self):
        current_step = self.environment
        while current_step:
            if current_step.is_item:
                return current_step
            current_step = current_step.environment
        return None

    def spread_plague(self, plague_carrier):
        af = [af for af in plague_carrier.affected if af.type == "plague"]
        if not af:
            plague_carrier.affected_by.rem_bit(merc.AFF_PLAGUE)
            return
        af = af[0]
        if af.level == 1:
            return
        plague = handler_game.AFFECT_DATA()
        plague.where = merc.TO_AFFECTS
        plague.type = "plague"
        plague.level = af.level - 1
        plague.duration = random.randint(1, 2 * plague.level)
        plague.location = merc.APPLY_STR
        plague.modifier = -5
        plague.bitvector = merc.AFF_PLAGUE
        for vch_id in self.people[:]:
            vch = instance.characters[vch_id]
            if (
                not handler_magic.saves_spell(plague.level - 2, vch, merc.DAM_DISEASE)
                and not vch.is_immortal()
                and not vch.is_affected(merc.AFF_PLAGUE)
                and random.randint(0, 5) == 0
            ):
                vch.send("You feel hot and feverish.\n\r")
                handler_game.act(
                    "$n shivers and looks very ill.", vch, None, None, merc.TO_ROOM
                )
                vch.affect_join(plague)

    def is_room_owner(self, room):
        if not room.owner:
            return False
        return True if game_utils.is_name(self.name, room.owner) else False

    # * Move an instance from a location
    def get(self, instance_object):
        pass

    # * Give an obj to a char.
    def put(self, instance_object):
        pass

    def has_key(self, key):
        instance_id = [
            item_id
            for item_id in self.items
            if instance.items[item_id].vnum == key.vnum
        ]
        if instance_id:
            return True
        return False

    # * Return # of objects which an object counts as.
    # * Thanks to Tony Chamberlain for the correct recursive code here.
    def get_number(self):
        try:  # if self is an item.
            noweight = [
                merc.ITEM_CONTAINER,
                merc.ITEM_MONEY,
                merc.ITEM_GEM,
                merc.ITEM_JEWELRY,
            ]
            if self.item_type in noweight:
                number = 0
            else:
                number = 1
        except AttributeError:
            number = 1

        contents = self.inventory[:]
        counted = [self.instance_id]
        for content_id in contents:
            content = instance.items[content_id]
            number += 1
            if content.instance_id in counted:
                logger.debug(
                    "BUG: Objects contain eachother. %s(%d) - %s(%d)"
                    % (
                        self.short_descr,
                        self.instance_id,
                        content.short_descr,
                        content.instance_id,
                    )
                )
                break
            counted.append(content)
            contents.extend(content.inventory)

        return number

    #
    # * Return weight of an object, including weight of contents.
    def get_weight(item):
        weight = item.weight
        contents = item.inventory[:]
        counted = [item.instance_id]
        for content_id in contents:
            content = instance.items[content_id]
            if content.instance_id in counted:
                print(
                    "BUG: Objects contain eachother. %s(%d) - %s(%d)"
                    % (
                        item.short_descr,
                        item.instance_id,
                        content.short_descr,
                        content.instance_id,
                    )
                )
                break
            counted.append(content)
            contents.extend(content.inventory)
            try:  # For items in containers
                weight += content.weight * state_checks.WEIGHT_MULT(item) // 100
            except AttributeError:
                pass

        return weight

    def true_weight(item):
        weight = item.weight
        for content_id in item.inventory[:]:
            content = instance.items[content_id]
            weight += content.get_weight()
        return weight
