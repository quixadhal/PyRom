"""All item handlers we could ever need."""

import json
import os
import copy
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

from rom24 import instance
from rom24 import settings
from rom24 import equipment
from rom24 import game_utils
from rom24 import type_bypass
from rom24 import inventory
from rom24 import physical
from rom24 import environment
from rom24 import handler_game
from rom24 import object_creator
from rom24 import merc
from rom24 import state_checks
from rom24 import item_flags

# Equip "Flags":
# Keyword: internal identifier
# Value: String Representation

equips_to_strings = {
    "left_finger": "Left Finger",
    "right_finger": "Right Finger",
    "neck": "Neck",
    "collar": "Collar",
    "body": "Body",
    "head": "Head",
    "legs": "Legs",
    "feet": "Feet",
    "hands": "Hands",
    "arms": "Arms",
    "about_body": "About Body",
    "left_wrist": "Left Wrist",
    "right_wrist": "Right Wrist",
    "waist": "Waist",
    "main_hand": "Main Hand",
    "off_hand": "Off Hand",
    "held": "Held",
    "float": "Float",
    "light": "Light",
}

item_restriction_strings = {
    "no_drop": "No Drop",
    "no_sac": "No Sacrifice",
    "no_remove": "No Remove",
    "no_uncurse": "No Uncurse",
    "no_purge": "No Purge",
    "anti_good": "Anti-Good",
    "anti_evil": "Anti-Evil",
    "anti_neutral": "Anti-Neutral",
    "no_locate": "No Locate",
}

item_attribute_strings = {
    "magic": "Magic",
    "glow": "Glowing",
    "hum": "Humming",
    "dark": "Dark",
    "lock": "Lock",
    "evil": "Evil",
    "invis": "Invisible",
    "bless": "Bless",
    "non_metal": "Non Metal",
    "had_timer": "Had Timer",
    "burn_proof": "Burn Proof",
    "melt_drop": "Melt Drop",
    "rot_death": "Rot Death",
    "vis_death": "Vis Death",
    "inventory": "Inventory",
    "sell_extract": "Sell Extract",
    "take": "Take",
}

weapon_attribute_strings = {
    "flaming": "Flaming",
    "frost": "Frost",
    "vampiric": "Vampiric",
    "sharp": "Sharp",
    "vorpal": "Vorpal",
    "two_handed": "Two-Handed",
    "shocking": "Shocking",
    "poison": "Poison",
}


class Items(
    instance.Instancer,
    environment.Environment,
    physical.Physical,
    inventory.Inventory,
    equipment.Equipment,
    type_bypass.ObjectType,
):
    template_count = 0
    instance_count = 0

    def __init__(self, template=None, **kwargs):
        super().__init__()
        self.is_item = True
        self.vnum = 0
        self.instance_id = None
        self.count = 0
        self.reset_num = 0
        self.extra_descr = []
        self.affected = []
        self.valid = False
        self.enchanted = False
        self.new_format = True
        self.owner = ""
        self.item_type = 0
        self.cost = 0
        self.level = 0
        self.condition = 0
        self.timer = 0
        self.value = [0] * 5
        self.flags = item_flags.ItemFlags()
        if kwargs:
            [setattr(self, k, copy.deepcopy(v)) for k, v in kwargs.items()]
        if template:
            [setattr(self, k, copy.deepcopy(v)) for k, v in template.__dict__.items()]
            self.instancer()
        if self.instance_id:
            self.instance_setup()
            Items.instance_count += 1
        else:
            Items.template_count += 1
        self._last_saved = None
        self._md5 = None

    def __del__(self):
        try:
            logger.trace("Freeing %s" % str(self))
            if self.instance_id:
                Items.instance_count -= 1
                if instance.items.get(self.instance_id, None):
                    self.instance_destructor()
            else:
                Items.template_count -= 1
        except:
            return

    def __repr__(self):
        if not self.instance_id:
            return "<Item Template: %s : %d>" % (self.short_descr, self.vnum)
        else:
            return "<Item Instance: %s : ID %d VNUM %d>" % (
                self.short_descr,
                self.instance_id,
                self.vnum,
            )

    # Equipped/Equips To
    @property
    def equipped_to(self):
        """
        Find the slot this item is equipped to on a character and return str name, or return None

        :return: :rtype: str or None
        """
        if self.in_living:
            for k, v in self.in_living.equipped.items():
                if v == self.instance_id:
                    return k
        else:
            return None

    @property
    def equips_to_names(self):
        """
        return equips_to flags as string

        :param check_occupied:
        :return: :rtype: str
        """
        check_occupied: bool = False
        things = set({})
        used = self.equipped_to if check_occupied else None
        for name in self.equips_to:
            if used == name:
                continue
            things.add(equips_to_strings[name])
        return ", ".join(name for name in things)

    @property
    def equips_to(self):
        """
        Equips To getter

        :return: equips_to set, current slot list it can equip to
        :rtype: set
        """
        if self.is_item:
            return self.flags._equips_to
        else:
            return None

    @equips_to.setter
    # Default of the equippable flag is True, because the
    # caller will either want to set or clear that status.
    def equips_to(self, slots):
        """
        Clear, and re-set wear slot(s)

        :param slots: iterable
        """
        if self.flags._equips_to:
            self.flags._equips_to.clear()
        self.flags._equips_to |= set(slots)

    # Item Attributes
    @property
    def item_attribute_names(self):
        """
        return item_attributes flags as string

        :return: :rtype: str
        """
        attributes = set({})
        for astring in self.item_attributes:
            attributes.add(item_attribute_strings[astring])
        return ", ".join(name for name in attributes)

    @property
    def item_attributes(self):
        # Item Attribute getter
        """
        return the item_attributes set

        :return: :rtype: set
        """
        return self.flags._item_attributes

    @item_attributes.setter
    def item_attributes(self, attr_set):
        """
        Clear and re-set the attribute set.

        :param attr_set:
        :raise TypeError:
        """
        if self.flags._item_attributes:
            self.flags._item_attributes.clear()
        self.flags._item_attributes |= set(attr_set)

    # Restrictions
    @property
    def item_restriction_names(self):
        """
        return restriction flags as string

        :return: :rtype: str
        """
        restrictions = set({})
        for rstring in self.item_restrictions:
            restrictions.add(item_restriction_strings[rstring])
        return ", ".join(name for name in restrictions)

    @property
    def item_restrictions(self):
        # Item Restrictions getter
        """
        return item_restriction flags as set

        :return: :rtype: set
        """
        return self.flags._item_restrictions

    @item_restrictions.setter
    def item_restrictions(self, restrictions):
        """
        clear and re-set the restriction set

        :param restrictions: input flags
        """
        if self.flags._item_restrictions:
            self.flags._item_restrictions.clear()
        self.flags._item_restrictions |= set(restrictions)

    # Weapons
    @property
    def weapon_attribute_names(self):
        """
        return weapon_attribute flags as str

        :return: :rtype: str
        """
        attributes = set({})
        for wstring in self.item_restrictions:
            attributes.add(weapon_attribute_strings[wstring])
        return ", ".join(name for name in attributes)

    @property
    def weapon_attributes(self):
        """
        return weapon_attributes flags as set

        :return: :rtype: set
        """
        return self.flags._weapon_attributes

    @weapon_attributes.setter
    def weapon_attributes(self, weap_attr):
        """
        Clear and re-set weapon_attribute flags

        :param weap_attr: input data
        """
        if self.flags._weapon_attributes:
            self.flags._weapon_attributes.clear()
        self.flags._weapon_attributes |= set(weap_attr)

    def get(self, instance_object):
        if instance_object.is_item and instance_object.instance_id in self.inventory:
            self.inventory.remove(instance_object.instance_id)
            self.carry_number -= instance_object.get_number()
            self.carry_weight -= (
                instance_object.get_weight() * state_checks.WEIGHT_MULT(self) // 100
            )
            instance_object.environment = None
            return instance_object
        else:
            raise KeyError(
                "Item to be removed from Item, not in inventory %d"
                % instance_object.instance_id
            )

    def put(self, instance_object):
        if (
            instance_object.is_item
            and instance_object.instance_id not in self.inventory
        ):
            self.inventory += [instance_object.instance_id]
            self.carry_weight += (
                instance_object.get_weight() * state_checks.WEIGHT_MULT(self) // 100
            )
            self.carry_number += instance_object.get_number()
            instance_object.environment = self.instance_id
            return instance_object
        else:
            raise KeyError(
                "Item to be added to Item, already in inventory or wrong type "
                "%d, %r" % (instance_object.instance_id, type(instance_object))
            )

    def instance_setup(self):
        instance.items[self.instance_id] = self
        instance.global_instances[self.instance_id] = self
        if self.vnum not in instance.instances_by_item.keys():
            instance.instances_by_item[self.vnum] = [self.instance_id]
        else:
            instance.instances_by_item[self.vnum] += [self.instance_id]

    def instance_destructor(self):
        instance.instances_by_item[self.vnum].remove(self.instance_id)
        del instance.items[self.instance_id]
        del instance.global_instances[self.instance_id]
        # Remove an object.

    def apply_ac(self, ac_position):
        if self.item_type != merc.ITEM_ARMOR:
            return 0
        multi = {"body": 3, "head": 2, "legs": 2, "about": 2}
        for worn_on in self.equipped_to:
            if worn_on in multi.keys():
                return multi[worn_on] * self.value[ac_position]
        else:
            return self.value[ac_position]

    # enchanted stuff for eq */
    def affect_enchant(self):
        # okay, move all the old flags into new vectors if we have to
        if not self.enchanted:
            self.enchanted = True
            for paf in instance.item_templates[self.vnum].affected:
                af_new = handler_game.AFFECT_DATA()
                self.affected.append(af_new)

                af_new.where = paf.where
                af_new.type = max(0, paf.type)
                af_new.level = paf.level
                af_new.duration = paf.duration
                af_new.location = paf.location
                af_new.modifier = paf.modifier
                af_new.bitvector = paf.bitvector

    # give an affect to an object */

    def affect_add(self, paf):
        paf_new = handler_game.AFFECT_DATA()
        self.affected.append(paf_new)
        # apply any affect vectors to the object's extra_flags
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                ret_str = game_utils.item_bitvector_flag_str(
                    paf.bitvector, "extra flags"
                )
                if self.item_attribute_names.intersection(ret_str):
                    self.item_attributes |= {ret_str}
                elif self.item_restriction_names.intersection(ret_str):
                    self.item_restrictions |= {ret_str}
                else:
                    raise ValueError(
                        "paf set attempt failed, unable to find flag %s" % ret_str
                    )
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    ret_str = game_utils.item_bitvector_flag_str(
                        paf.bitvector, "weapon flags"
                    )
                    if self.weapon_attribute_names.intersection(ret_str):
                        self.weapon_attributes |= {ret_str}
                    else:
                        raise ValueError(
                            "paf set attempt failed, unable to find flag %s" % ret_str
                        )

    def affect_remove(self, paf):
        if not self.affected:
            print("BUG: Affect_remove_object: no affect.")
            return

        if self.in_living is not None and self.equipped_to:
            instance.characters[self.in_living].affect_modify(paf, False)

        where = paf.where
        vector = paf.bitvector

        # remove flags from the object if needed */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                ret_str = game_utils.item_bitvector_flag_str(
                    paf.bitvector, "extra flags"
                )
                if self.item_attribute_names.intersection(ret_str):
                    self.item_attributes -= {ret_str}
                elif self.item_restriction_names.intersection(ret_str):
                    self.item_restrictions -= {ret_str}
                else:
                    raise ValueError(
                        "paf removal attempt failed, unable to find flag %s" % ret_str
                    )
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    ret_str = game_utils.item_bitvector_flag_str(
                        paf.bitvector, "weapon flags"
                    )
                    if self.weapon_attribute_names.intersection(ret_str):
                        self.weapon_attributes -= {ret_str}
                    else:
                        raise ValueError(
                            "paf removal attempt failed, unable to find flag %s"
                            % ret_str
                        )

        if paf not in self.affected:
            print("BUG: Affect_remove_object: cannot find paf.")
            return
        self.affected.remove(paf)
        del paf
        if self.in_living is not None and self.equipped_to:
            instance.characters[self.in_living].affect_check(where, vector)
        return

    # Extract an obj from the world.
    def extract(self):
        if self.environment:
            if self.equipped_to:
                self.in_living.raw_unequip(self)
            self.environment.get(self)
            for item_id in self.inventory[:]:
                if self.instance_id not in instance.items:
                    logger.error(
                        "Extract_obj: obj %d not found in obj_instance dict."
                        % self.instance_id
                    )
                    return
                tmp = instance.items[item_id]
                self.get(tmp)
                tmp.extract()
        self.instance_destructor()

    # Return the number of players "on" an object.
    def count_users(self):
        total = 0
        if self.in_room:
            for person_id in self.in_room.people[:]:
                person = instance.characters[person_id]
                if person.on == self.instance_id:
                    total += 1
        return total

        # Serialization

    def to_json(self, outer_encoder=None):
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        tmp_dict = {}
        for k, v in self.__dict__.items():
            if str(type(v)) in ("<class 'function'>", "<class 'method'>"):
                continue
            elif str(k) in ("_last_saved", "_md5"):
                continue
            else:
                tmp_dict[k] = v

        cls_name = "__class__/" + __name__ + "." + self.__class__.__name__
        return {cls_name: outer_encoder(tmp_dict)}

    @classmethod
    def from_json(cls, data, outer_decoder=None, player_name=None):
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = "__class__/" + __name__ + "." + cls.__name__
        if cls_name in data:
            tmp_data = outer_decoder(data[cls_name])
            return cls(**tmp_data)
        return data

    def save(
        self,
        is_equipped: bool = False,
        in_inventory: bool = False,
        player_name: str = None,
        force: bool = False,
    ):
        if self._last_saved is None:
            self._last_saved = time.time() - settings.SAVE_LIMITER - 2
        if not force and time.time() < self._last_saved + settings.SAVE_LIMITER:
            return

        if player_name is None:
            if self.instance_id:
                top_dir = settings.INSTANCE_DIR
                number = self.instance_id
            else:
                top_dir = settings.AREA_DIR
                number = self.vnum
            if self.in_area.instance_id:
                area_number = self.in_area.instance_id
            else:
                area_number = self.in_area.index
            pathname = os.path.join(
                top_dir, "%d-%s" % (area_number, self.in_area.name), "items"
            )
        else:
            top_dir = os.path.join(
                settings.PLAYER_DIR, player_name[0].lower(), player_name.capitalize()
            )
            number = self.instance_id
            if is_equipped and in_inventory:
                raise ValueError(
                    "A player item cannot be BOTH equipped AND in their inventory!"
                )
            if is_equipped:
                pathname = os.path.join(top_dir, "equipment")
            elif in_inventory:
                pathname = os.path.join(top_dir, "inventory")
            else:
                raise ValueError(
                    "Player items must specify if they are equipped or in their inventory!"
                )

        os.makedirs(pathname, 0o755, True)
        filename = os.path.join(pathname, "%d-item.json" % number)
        # logger.info('Saving %s', filename)
        js = json.dumps(self, default=instance.to_json, indent=4, sort_keys=True)
        md5 = hashlib.md5(js.encode("utf-8")).hexdigest()
        if self._md5 != md5:
            self._md5 = md5
            with open(filename, "w") as fp:
                fp.write(js)

        if self.inventory:
            for item_id in self.inventory[:]:
                if item_id not in instance.global_instances:
                    # logger.error('Item %d is in Item %d\'s inventory, but does not exist?', item_id, self.instance_id)
                    continue
                item = instance.global_instances[item_id]
                item.save(
                    is_equipped=is_equipped,
                    in_inventory=in_inventory,
                    player_name=player_name,
                    force=force,
                )

    @classmethod
    def load(cls, instance_id: int = None, vnum: int = None, player_name: str = None):
        if not vnum and not instance_id:
            raise ValueError("You must provide either a vnum or an instance_id!")
        if vnum and instance_id:
            raise ValueError(
                "You must provide either a vnum or an instance_id, not BOTH!"
            )
        if instance_id and instance_id in instance.items:
            logger.warn("Instance %d of item already loaded!", instance_id)
            return

        if player_name:
            pathname = os.path.join(
                settings.PLAYER_DIR, player_name[0].lower(), player_name.capitalize()
            )
            number = instance_id
        elif instance_id:
            pathname = settings.INSTANCE_DIR
            number = instance_id
        else:
            pathname = settings.AREA_DIR
            number = vnum

        target_file = f"{number}-item.json"
        filename = None
        for a_path, a_directory, i_files in os.walk(pathname):
            if target_file in i_files:
                filename = os.path.join(a_path, target_file)
                break
        if not filename:
            raise ValueError("Cannot find %s" % target_file)

        with open(filename) as fp:
            obj = json.load(fp, object_hook=instance.from_json)
        if not isinstance(obj, Items):
            raise TypeError("Could not load instance %r!" % number)
        if obj.inventory:
            obj.load_inventory(player_name)
        if obj.environment:
            if (
                obj.environment.is_room
                and obj.instance_id not in obj.environment.inventory
            ):
                obj.environment.put(obj)
        return obj

    def load_inventory(self, player_name: str = None):
        for number in self.inventory[:]:
            if self.instance_id:
                obj = Items.load(instance_id=number, player_name=player_name)
            else:
                obj = Items.load(vnum=number, player_name=player_name)
            if not isinstance(obj, Items):
                raise TypeError("Could not load instance %r!" % number)


def get_item(ch, item, this_container):
    # variables for AUTOSPLIT
    if not item.flags.take:
        ch.send("You can't take that.\n")
        return
    if ch.carry_number + item.get_number() > ch.can_carry_n():
        handler_game.act(
            "$d: you can't carry that many items.", ch, None, item.name, merc.TO_CHAR
        )
        return
    if not ch.can_loot(item):
        handler_game.act(
            "Corpse looting is not permitted.", ch, None, None, merc.TO_CHAR
        )
        return
    if item.in_living:
        if (not item.in_item or (item.in_living.instance_id != ch.instance_id)) and (
            state_checks.get_carry_weight(ch) + item.get_weight() > ch.can_carry_w()
        ):
            handler_game.act(
                "$d: you can't carry that much weight.",
                ch,
                None,
                item.name,
                merc.TO_CHAR,
            )
            return

    # Make sure nobody is using the item before we allow someone to get it.
    if item.in_room:
        for gch_id in item.in_room.people[:]:
            gch = instance.characters[gch_id]
            if gch.on:
                on_item = instance.items[gch.on]
                if on_item.instance_id in item.in_room.items:
                    handler_game.act(
                        "$N appears to be using $p.", ch, item, gch, merc.TO_CHAR
                    )
                    return
    # Get things from a container.
    if this_container:
        if this_container.vnum == merc.OBJ_VNUM_PIT and ch.trust < item.level:
            ch.send("You are not powerful enough to use it.\n")
            return
        elif (
            this_container.vnum == merc.OBJ_VNUM_PIT
            and item.flags.take
            and item.flags.had_timer
        ):
            item.timer = 0
        handler_game.act("You get $p from $P.", ch, item, this_container, merc.TO_CHAR)
        handler_game.act("$n gets $p from $P.", ch, item, this_container, merc.TO_ROOM)
        item.flags.had_timer = False
        this_container.get(item)
    # Get a normal thing.
    else:
        handler_game.act("You get $p.", ch, item, this_container, merc.TO_CHAR)
        handler_game.act("$n gets $p.", ch, item, this_container, merc.TO_ROOM)
        ch.in_room.get(item)

    if item.item_type == merc.ITEM_MONEY:
        ch.silver += item.value[0]
        ch.gold += item.value[1]
        if ch.act.is_set(merc.PLR_AUTOSPLIT):
            # AUTOSPLIT code
            members = len(
                [
                    gch
                    for gch in ch.in_room.people[:]
                    if not instance.characters[gch].is_affected(merc.AFF_CHARM)
                    and instance.characters[gch].is_same_group(ch)
                ]
            )
            if members > 1 and (item.value[0] > 1 or item.value[1]):
                ch.do_split("%d %d" % (item.value[0], item.value[1]))
        ch.get(item)
        item.extract()
    else:
        ch.put(item)
    return


# trust levels for load and clone
def item_check(ch, obj):
    # TODO add real values, just guessed for now
    if (
        state_checks.IS_TRUSTED(ch, 60)
        or (state_checks.IS_TRUSTED(ch, 55) and obj.level <= 20 and obj.cost <= 1000)
        or (state_checks.IS_TRUSTED(ch, 53) and obj.level <= 10 and obj.cost <= 500)
        or (state_checks.IS_TRUSTED(ch, 52) and obj.level <= 5 and obj.cost <= 250)
        or (state_checks.IS_TRUSTED(ch, 51) and obj.level == 0 and obj.cost <= 100)
    ):
        return True
    else:
        return False


def format_item_to_char(item, ch, fShort):
    if type(item) == int:
        item = instance.items[item]
    buf = ""
    if (fShort and not item.short_descr) or not item.description:
        return buf

    if item.flags.invis:
        buf += "(Invis) "
    if ch.is_affected(merc.AFF_DETECT_EVIL) and item.evil:
        buf += "(Red Aura) "
    if ch.is_affected(merc.AFF_DETECT_GOOD) and item.bless:
        buf += "(Blue Aura) "
    if ch.is_affected(merc.AFF_DETECT_MAGIC) and item.magic:
        buf += "(Magical) "
    if item.flags.glow:
        buf += "(Glowing) "
    if item.flags.hum:
        buf += "(Humming) "

    if fShort:
        if item.short_descr:
            buf += item.short_descr
    else:
        if item.description:
            buf += item.description
    if ch.act.is_set(merc.PLR_OMNI):
        buf += "(%d)" % item.instance_id
    return buf


# Count occurrences of an obj in a list.
def count_obj_list(itemInstance, contents):
    count = 0
    for item_id in contents:
        if item_id:
            if instance.items[item_id].name == itemInstance.name:
                count += 1
    return count


# for clone, to insure that cloning goes many levels deep
def recursive_clone(ch, item, clone):
    for c_item_id in item.inventory[:]:
        c_item = instance.items[c_item_id]
        if item_check(ch, c_item):
            t_obj = object_creator.create_item(instance.item_templates[c_item.vnum], 0)
            object_creator.clone_item(c_item, t_obj)
            clone.put(t_obj)
            recursive_clone(ch, c_item, t_obj)
