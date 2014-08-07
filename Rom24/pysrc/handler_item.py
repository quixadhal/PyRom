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
import container
from instance import Instancer

logger = logging.getLogger()

import physical
import location
import handler_game
import object_creator
import merc
import state_checks


# One object.
class Items(Instancer, location.Location, physical.Physical, container.Container):
    def __init__(self, template=None):
        super().__init__()
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
        self.extra_flags = 0
        self.wear_flags = 0
        self.wear_loc = 0
        self.cost = 0
        self.level = 0
        self.condition = 0
        self.timer = 0
        self.value = [0, 0, 0, 0, 0]

    def __del__(self):
        logger.trace("Freeing %s" % str(self))

    def __repr__(self):
        if not self.instance_id:
            return "<Item Template: %s : %d>" % (self.short_descr, self.vnum)
        else:
            return "<Item Instance: %s : ID %d>" % (self.short_descr, self.instance_id)

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

    def apply_ac(self, iWear, loc):
        if self.item_type != merc.ITEM_ARMOR:
            return 0

        multi = {merc.WEAR_BODY: 3, merc.WEAR_HEAD: 2, merc.WEAR_LEGS: 2, merc.WEAR_ABOUT: 2}
        if iWear in multi:
            return multi[iWear] * self.value[loc]
        else:
            return self.value[loc]



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
                state_checks.SET_BIT(self.extra_flags, paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    state_checks.SET_BIT(self.value[4], paf.bitvector)

    def affect_remove(self, paf):
        if not self.affected:
            print("BUG: Affect_remove_object: no affect.")
            return

        if self.in_living is not None and self.wear_loc != -1:
            merc.characters[self.in_living].affect_modify(paf, False)

        where = paf.where
        vector = paf.bitvector

        # remove flags from the object if needed */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                state_checks.REMOVE_BIT(self.extra_flags, paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if self.item_type == merc.ITEM_WEAPON:
                    state_checks.REMOVE_BIT(self.value[4], paf.bitvector)

        if paf not in self.affected:
            print("BUG: Affect_remove_object: cannot find paf.")
            return
        self.affected.remove(paf)
        del paf
        if self.in_living is not None and self.wear_loc != -1:
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
    if not state_checks.CAN_WEAR(item, merc.ITEM_TAKE):
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
        if this_container.vnum == merc.OBJ_VNUM_PIT \
                and not state_checks.CAN_WEAR(this_container, merc.ITEM_TAKE) \
                and not state_checks.is_item_stat(item, merc.ITEM_HAD_TIMER):
            item.timer = 0
            handler_game.act("You get $p from $P.", ch, item, this_container, merc.TO_CHAR)
            handler_game.act("$n gets $p from $P.", ch, item, this_container, merc.TO_ROOM)
            state_checks.REMOVE_BIT(item.extra_flags, merc.ITEM_HAD_TIMER)
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


def format_item_to_char(item_id, ch, use_short):
    buf = ''
    item = merc.items[item_id]
    if (use_short and not item.short_descr) or not item.description:
        return buf

    if state_checks.is_item_stat(item, merc.ITEM_INVIS):
        buf += "(Invis) "
    if ch.is_affected(merc.AFF_DETECT_EVIL) and state_checks.is_item_stat(item, merc.ITEM_EVIL):
        buf += "(Red Aura) "
    if ch.is_affected(merc.AFF_DETECT_GOOD) and state_checks.is_item_stat(item, merc.ITEM_BLESS):
        buf += "(Blue Aura) "
    if ch.is_affected(merc.AFF_DETECT_MAGIC) and state_checks.is_item_stat(item, merc.ITEM_MAGIC):
        buf += "(Magical) "
    if state_checks.is_item_stat(item, merc.ITEM_GLOW):
        buf += "(Glowing) "
    if state_checks.is_item_stat(item, merc.ITEM_HUM):
        buf += "(Humming) "

    if use_short:
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
    return len([item for item in contents if merc.items[item].vnum == itemInstance.vnum])


# for clone, to insure that cloning goes many levels deep
def recursive_clone(ch, item, clone):
    for c_item_id in item.contents:
        c_item = merc.items[c_item_id]
        if item_check(ch, c_item):
            t_obj = object_creator.create_item(merc.itemTemplate[c_item.vnum], 0)
            object_creator.clone_item(c_item, t_obj)
            t_obj.to_environment(clone)
            recursive_clone(ch, c_item, t_obj)
