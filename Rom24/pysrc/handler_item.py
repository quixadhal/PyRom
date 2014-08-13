"""
 #**************************************************************************
 *  Original Diku Mud copyright(C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright(C) 1992, 1993 by Michael           *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                            *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
import logging

logger = logging.getLogger()

import instance
import game_utils
import type_bypass
import container
import physical
import location
import handler_game
import object_creator
import merc
import state_checks
import item_flags

# * One object.

'''Equip "Flags":
Keyword: internal identifier
Value: String Representation'''
equips_to_strings = {'left_finger': 'Left Finger',
                     'right_finger': 'Right Finger',
                     'neck': 'Neck',
                     'collar': 'Collar',
                     'body': 'Body',
                     'head': 'Head',
                     'legs': 'Legs',
                     'feet': 'Feet',
                     'hands': 'Hands',
                     'arms': 'Arms',
                     'about': 'About Body',
                     'left_wrist': 'Left Wrist',
                     'right_wrist': 'Right Wrist',
                     'waist': 'Waist',
                     'main_hand': 'Main Hand',
                     'off_hand': 'Off Hand',
                     'held': 'Held',
                     'float': 'Float',
                     'light': 'Light'}

item_restriction_strings = {'no_drop': 'No Drop',
                            'no_remove': 'No Remove',
                            'no_uncurse': 'No Uncurse',
                            'no_purge': 'No Purge',
                            'anti_good': 'Anti-Good',
                            'anti_evil': 'Anti-Evil',
                            'anti_neutral': 'Anti-Neutral',
                            'no_locate': 'No Locate'}

item_attribute_strings = {'magic': 'Magic',
                          'glow': 'Glowing',
                          'hum': 'Humming',
                          'dark': 'Dark',
                          'lock': 'Lock',
                          'evil': 'Evil',
                          'invis': 'Invisible',
                          'bless': 'Bless',
                          'non_metal': 'Non Metal',
                          'had_timer': 'Had Timer',
                          'burn_proof': 'Burn Proof',
                          'melt_drop': 'Melt Drop',
                          'rot_death': 'Rot Death',
                          'vis_death': 'Vis Death',
                          'inventory': 'Inventory',
                          'sell_extract': 'Sell Extract',
                          'take': 'Take'}

weapon_attribute_strings = {'flaming': 'Flaming',
                            'frost': 'Frost',
                            'vampiric': 'Vampiric',
                            'sharp': 'Sharp',
                            'vorpal': 'Vorpal',
                            'two_handed': 'Two-Handed',
                            'shocking': 'Shocking',
                            'poison': 'Poison'}


class Items(instance.Instancer, location.Location, physical.Physical, container.Container,
            item_flags.ItemFlags, type_bypass.ObjectType):
    def __init__(self, template=None):
        super().__init__()
        self.is_item = True
        self.vnum = 0
        self.template = True
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
        self._equips_to = set({})
        self._item_attributes = set({})
        self._item_restrictions = set({})
        self._weapon_attributes = set({})
        self._equips_to_names = equips_to_strings
        self._restriction_names = item_restriction_strings
        self._item_attribute_names = item_attribute_strings
        self._weapon_attribute_names = weapon_attribute_strings

    def __del__(self):
        logger.trace("Freeing %s" % str(self))

    def __repr__(self):
        if not self.instance_id:
            return "<Item Template: %s : %d>" % (self.short_descr, self.vnum)
        else:
            return "<Item Instance: %s : ID %d>" % (self.short_descr, self.instance_id)

    #Equipped/Equips To
    @property
    def equipped_to(self):
        """
        Find the slot this item is equipped to on a character and return str name, or return None

        :return: :rtype: str or None
        """
        if self.in_living:
            character = merc.characters[self.in_living]
            for k, v in character.equipped.items():
                if v == self.instance_id:
                    return k
        else:
            return None

    @property
    def equips_to_names(self, check_occupied=False):
        """
        return equips_to flags as string

        :param check_occupied:
        :return: :rtype: str
        """
        things = set({})
        used = self.equipped_to if check_occupied else None
        for name in self.equips_to:
            if used == name:
                continue
            things.add(self._equips_to_names[name])
        return ', '.join(name for name in things)

    @property
    def equips_to(self):
        """
        Equips To getter

        :return: equips_to set, current slot list it can equip to
        :rtype: set
        """
        if self.is_item:
            return self._equips_to
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
        if self._equips_to:
            self._equips_to.clear()
        self._equips_to |= set(slots)

    #Item Attributes
    @property
    def item_attribute_names(self):
        """
        return item_attributes flags as string

        :return: :rtype: str
        """
        attributes = set({})
        for astring in self.item_attributes:
            attributes.add(self._restriction_names[astring])
        return ', '.join(name for name in attributes)

    @property
    def item_attributes(self):
        #Item Attribute getter
        """
        return the item_attributes set

        :return: :rtype: set
        """
        return self._item_attributes

    @item_attributes.setter
    def item_attributes(self, attr_set):
        """
        Clear and re-set the attribute set.

        :param attr_set:
        :raise TypeError:
        """
        if self._item_attributes:
            self._item_attributes.clear()
        self._item_attributes |= set(attr_set)

    #Restrictions
    @property
    def restriction_names(self):
        """
        return restriction flags as string

        :return: :rtype: str
        """
        restrictions = set({})
        for rstring in self.item_restrictions:
            restrictions.add(self._restriction_names[rstring])
        return ', '.join(name for name in restrictions)

    @property
    def item_restrictions(self):
        #Item Restrictions getter
        """
        return item_restriction flags as set

        :return: :rtype: set
        """
        return self._item_restrictions

    @item_restrictions.setter
    def item_restrictions(self, restrictions):
        """
        clear and re-set the restriction set

        :param restrictions: input flags
        """
        if self._item_restrictions:
            self._item_restrictions.clear()
        self._item_restrictions |= set(restrictions)

    #Weapons
    @property
    def weapon_attribute_names(self):
        """
        return weapon_attribute flags as str

        :return: :rtype: str
        """
        attributes = set({})
        for wstring in self.item_restrictions:
            attributes.add(self._restriction_names[wstring])
        return ', '.join(name for name in attributes)

    @property
    def weapon_attributes(self):
        """
        return weapon_attributes flags as set

        :return: :rtype: set
        """
        return self._weapon_attributes

    @weapon_attributes.setter
    def weapon_attributes(self, weap_attr):
        """
        Clear and re-set weapon_attribute flags

        :param weap_attr: input data
        """
        if self._weapon_attributes:
            self._weapon_attributes.clear()
        self._weapon_attributes |= set(weap_attr)

    def instance_setup(self):
        merc.global_instances[self.instance_id] = self
        merc.items[self.instance_id] = merc.global_instances[self.instance_id]
        if self.vnum not in merc.instances_by_item.keys():
            merc.instances_by_item[self.vnum] = [self.instance_id]
        else:
            merc.instances_by_item[self.vnum].append(self.instance_id)

    def instance_destructor(self):
        merc.instances_by_item[self.vnum].remove(self.instance_id)
        del merc.items[self.instance_id]
        del merc.global_instances[self.instance_id]
        # Remove an object.

    def apply_ac(self, ac_position):
        if self.item_type != merc.ITEM_ARMOR:
            return 0
        multi = {'body': 3, 'head': 2, 'legs': 2, 'about': 2}
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
            for paf in merc.itemTemplate[self.vnum].affected:
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
                ret_str = game_utils.item_bitvector_flag_str(paf.bitvector, 'extra flags')
                if self.item_attribute_names.intersection(ret_str):
                    self.item_attributes |= {ret_str}
                elif self.restriction_names.intersection(ret_str):
                    self.item_restrictions |= {ret_str}
                else:
                    raise ValueError('paf set attempt failed, unable to find flag %s' % ret_str)
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    ret_str = game_utils.item_bitvector_flag_str(paf.bitvector, 'weapon flags')
                    if self.weapon_attribute_names.intersection(ret_str):
                        self.weapon_attributes |= {ret_str}
                    else:
                        raise ValueError('paf set attempt failed, unable to find flag %s' % ret_str)

    def affect_remove(self, paf):
        if not self.affected:
            print("BUG: Affect_remove_object: no affect.")
            return

        if self.in_living is not None and self.equipped_to:
            merc.characters[self.in_living].affect_modify(paf, False)

        where = paf.where
        vector = paf.bitvector

        # remove flags from the object if needed */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                ret_str = game_utils.item_bitvector_flag_str(paf.bitvector, 'extra flags')
                if self.item_attribute_names.intersection(ret_str):
                    self.item_attributes -= {ret_str}
                elif self.restriction_names.intersection(ret_str):
                    self.item_restrictions -= {ret_str}
                else:
                    raise ValueError('paf removal attempt failed, unable to find flag %s' % ret_str)
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    ret_str = game_utils.item_bitvector_flag_str(paf.bitvector, 'weapon flags')
                    if self.weapon_attribute_names.intersection(ret_str):
                        self.weapon_attributes -= {ret_str}
                    else:
                        raise ValueError('paf removal attempt failed, unable to find flag %s' % ret_str)

        if paf not in self.affected:
            print("BUG: Affect_remove_object: cannot find paf.")
            return
        self.affected.remove(paf)
        del paf
        if self.in_living is not None and self.equipped_to:
            merc.characters[self.in_living].affect_check(where, vector)
        return

    # Extract an obj from the world.
    def extract(self):
        if self.in_environment:
            self.from_environment()

        for item_id in self.contents[:]:
            if self.instance_id not in merc.items:
                logger.error("Extract_obj: obj %d not found in obj_instance dict." % self.instance_id)
                return
            tmp = merc.items[item_id]
            tmp.extract()
        self.instance_destructor()

    # Return the number of players "on" an object.
    def count_users(self):
        total = 0
        if self.in_room:
            for person_id in self.in_room.people:
                person = merc.characters[person_id]
                if person.on == self.instance_id:
                    total += 1
        return total


def get_item(ch, item, this_container):
    # variables for AUTOSPLIT
    if not item.take:
        ch.send("You can't take that.\n")
        return
    if ch.carry_number + item.get_number() > ch.can_carry_n():
        handler_game.act("$d: you can't carry that many items.", ch, None, item.name, merc.TO_CHAR)
        return
    if (not item.in_item or merc.items[item.in_item].in_living != ch.instance_id) \
            and (state_checks.get_carry_weight(ch) + item.get_weight() > ch.can_carry_w()):
        handler_game.act("$d: you can't carry that much weight.", ch, None, item.name, merc.TO_CHAR)
        return
    if not ch.can_loot(item):
        handler_game.act("Corpse looting is not permitted.", ch, None, None, merc.TO_CHAR)
        return
    if item.in_room:
        for gch_id in item.in_room.people:
            gch = merc.characters[gch_id]
            if gch.on:
                if merc.items[gch.on] == item.instance_id:
                    handler_game.act("$N appears to be using $p.", ch, item, gch, merc.TO_CHAR)
                    return
    if this_container:
        if this_container.vnum == merc.OBJ_VNUM_PIT and ch.trust < item.level:
            ch.send("You are not powerful enough to use it.\n")
            return
        if this_container.vnum == merc.OBJ_VNUM_PIT and not item.take and not item.had_timer:
            item.timer = 0
            handler_game.act("You get $p from $P.", ch, item, this_container, merc.TO_CHAR)
            handler_game.act("$n gets $p from $P.", ch, item, this_container, merc.TO_ROOM)
            item.had_timer = False
            item.from_environment()
    else:
        handler_game.act("You get $p.", ch, item, this_container, merc.TO_CHAR)
        handler_game.act("$n gets $p.", ch, item, this_container, merc.TO_ROOM)
        item.from_environment()
    if item.item_type == merc.ITEM_MONEY:
        ch.silver += item.value[0]
        ch.gold += item.value[1]
        if ch.act.is_set(merc.PLR_AUTOSPLIT):
            # AUTOSPLIT code
            members = len([gch for gch in ch.in_room.people
                           if not state_checks.IS_AFFECTED(merc.characters[gch], merc.AFF_CHARM)
                           and merc.characters[gch].is_same_group(ch)])
            if members > 1 and (item.value[0] > 1 or item.value[1]):
                ch.do_split("%d %d" % (item.value[0], item.value[1]))
        item.extract()
    else:
        item.to_environment(ch)
    return


# trust levels for load and clone
def item_check(ch, obj):
    #TODO add real values, just guessed for now
    if state_checks.IS_TRUSTED(ch, 60) \
            or (state_checks.IS_TRUSTED(ch, 55) and obj.level <= 20 and obj.cost <= 1000) \
            or (state_checks.IS_TRUSTED(ch, 53) and obj.level <= 10 and obj.cost <= 500) \
            or (state_checks.IS_TRUSTED(ch, 52) and obj.level <= 5 and obj.cost <= 250) \
            or (state_checks.IS_TRUSTED(ch, 51) and obj.level == 0 and obj.cost <= 100):
        return True
    else:
        return False


def format_item_to_char(item, ch, fShort):
    if type(item) == int:
        item = merc.items[item]
    buf = ''
    if (fShort and not item.short_descr) or not item.description:
        return buf

    if item.invis:
        buf += "(Invis) "
    if ch.is_affected(merc.AFF_DETECT_EVIL) and item.evil:
        buf += "(Red Aura) "
    if ch.is_affected(merc.AFF_DETECT_GOOD) and item.bless:
        buf += "(Blue Aura) "
    if ch.is_affected(merc.AFF_DETECT_MAGIC) and item.magic:
        buf += "(Magical) "
    if item.glow:
        buf += "(Glowing) "
    if item.hum:
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
    return len([item_id for item_id in contents if merc.items[item_id].name == itemInstance.name])


# for clone, to insure that cloning goes many levels deep
def recursive_clone(ch, item, clone):
    for c_item_id in item.contents:
        c_item = merc.items[c_item_id]
        if item_check(ch, c_item):
            t_obj = object_creator.create_item(merc.itemTemplate[c_item.vnum], 0)
            object_creator.clone_item(c_item, t_obj)
            t_obj.to_environment(clone)
            recursive_clone(ch, c_item, t_obj)
