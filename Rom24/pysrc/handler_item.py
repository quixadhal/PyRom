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

import const
import handler_game
import handler
import object_creator
import merc
import state_checks

# * One object.


class Items(handler.Instancer):
    def __init__(self, template=None):
        super().__init__()
        self.vnum = 0
        if template:
            [setattr(self, k, v) for k, v in template.__dict__.items()]
            self.instancer()
            self.instance_setup()
        else:
            self.template = True
            self.instance_id = None
            self.count = 0
            self.in_room = None
            self.in_item = None
            self.on = None
            self.carried_by = None
            self.reset_num = 0
            self.contains = []
            self.extra_descr = []
            self.affected = []
            self.valid = False
            self.enchanted = False
            self.new_format = True
            self.owner = ""
            self.name = ""
            self.short_descr = ""
            self.description = ""
            self.item_type = 0
            self.extra_flags = 0
            self.wear_flags = 0
            self.wear_loc = 0
            self._weight = 0
            self.cost = 0
            self.level = 0
            self.condition = 0
            self.material = ""
            self.timer = 0
            self.value = [0, 0, 0, 0, 0]

    def __del__(self):
        if self.instance_id:
            self.instance_destructor()

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
            # * Remove an object.


def remove_item(ch, iWear, fReplace):
    item = merc.items.get(ch.get_eq(iWear), None)
    if not item:
        return True
    if not fReplace:
        return False
    if state_checks.IS_SET(item.extra_flags, merc.ITEM_NOREMOVE):
        handler_game.act("You can't remove $p.", ch, item, None, merc.TO_CHAR)
        return False
    ch.unequip(item)
    handler_game.act("$n stops using $p.", ch, item, None, merc.TO_ROOM)
    handler_game.act("You stop using $p.", ch, item, None, merc.TO_CHAR)
    return True

    #


# * Wear one object.
# * Optional replacement of existing objects.
# * Big repetitive code, ick.
def wear_item(ch, item, fReplace):
    if ch.level < item.level:
        ch.send("You must be level %d to use this object.\n" % item.level)
        handler_game.act("$n tries to use $p, but is too inexperienced.", ch, item, None, merc.TO_ROOM)
        return
    if item.item_type == merc.ITEM_LIGHT:
        if not remove_item(ch, merc.WEAR_LIGHT, fReplace):
            return
        handler_game.act("$n lights $p and holds it.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You light $p and hold it.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_LIGHT)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FINGER):
        if merc.items.get(ch.get_eq(merc.WEAR_FINGER_L), None) and merc.items.get(ch.get_eq(merc.WEAR_FINGER_R), None) \
                and not remove_item(ch, merc.WEAR_FINGER_L, fReplace) \
                and not remove_item(ch, merc.WEAR_FINGER_R, fReplace):
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_FINGER_L), None):
            handler_game.act("$n wears $p on $s left finger.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your left finger.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_FINGER_L)
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_FINGER_R), None):
            handler_game.act("$n wears $p on $s right finger.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p on your right finger.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_FINGER_R)
            return
        print("BUG: Wear_obj: no free finger.")
        ch.send("You already wear two rings.\n")
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_NECK):
        if merc.items.get(ch.get_eq(merc.WEAR_NECK_1), None) and merc.items.get(ch.get_eq(merc.WEAR_NECK_2), None) \
                and not remove_item(ch, merc.WEAR_NECK_1, fReplace) \
                and not remove_item(ch, merc.WEAR_NECK_2, fReplace):
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_NECK_1), None):
            handler_game.act("$n wears $p around $s neck.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p around your neck.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_NECK_1)
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_NECK_2), None):
            handler_game.act("$n wears $p around $s neck.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p around your neck.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_NECK_2)
            return
        print("BUG: Wear_obj: no free neck.")
        ch.send("You already wear two neck items.\n")
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_BODY):
        if not remove_item(ch, merc.WEAR_BODY, fReplace):
            return
        handler_game.act("$n wears $p on $s torso.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your torso.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_BODY)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_HEAD):
        if not remove_item(ch, merc.WEAR_HEAD, fReplace):
            return
        handler_game.act("$n wears $p on $s head.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your head.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_HEAD)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_LEGS):
        if not remove_item(ch, merc.WEAR_LEGS, fReplace):
            return
        handler_game.act("$n wears $p on $s legs.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your legs.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_LEGS)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FEET):
        if not remove_item(ch, merc.WEAR_FEET, fReplace):
            return
        handler_game.act("$n wears $p on $s feet.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your feet.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_FEET)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_HANDS):
        if not remove_item(ch, merc.WEAR_HANDS, fReplace):
            return
        handler_game.act("$n wears $p on $s hands.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your hands.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_HANDS)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_ARMS):
        if not remove_item(ch, merc.WEAR_ARMS, fReplace):
            return
        handler_game.act("$n wears $p on $s arms.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p on your arms.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_ARMS)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_ABOUT):
        if not remove_item(ch, merc.WEAR_ABOUT, fReplace):
            return
        handler_game.act("$n wears $p about $s torso.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p about your torso.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_ABOUT)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_WAIST):
        if not remove_item(ch, merc.WEAR_WAIST, fReplace):
            return
        handler_game.act("$n wears $p about $s waist.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p about your waist.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_WAIST)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_WRIST):
        if merc.items.get(ch.get_eq(merc.WEAR_WRIST_L), None) and merc.items.get(ch.get_eq(merc.WEAR_WRIST_R), None) \
                and not remove_item(ch, merc.WEAR_WRIST_L, fReplace) and not remove_item(ch, merc.WEAR_WRIST_R, fReplace):
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_WRIST_L), None):
            handler_game.act("$n wears $p around $s left wrist.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p around your left wrist.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_WRIST_L)
            return
        if not merc.items.get(ch.get_eq(merc.WEAR_WRIST_R), None):
            handler_game.act("$n wears $p around $s right wrist.", ch, item, None, merc.TO_ROOM)
            handler_game.act("You wear $p around your right wrist.", ch, item, None, merc.TO_CHAR)
            ch.equip(item, merc.WEAR_WRIST_R)
            return

        print("BUG: Wear_obj: no free wrist.")
        ch.send("You already wear two wrist items.\n")
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_SHIELD):
        if not remove_item(ch, merc.WEAR_SHIELD, fReplace):
            return
        weapon = merc.items.get(ch.get_eq(merc.WEAR_WIELD), None)
        if weapon and ch.size < merc.SIZE_LARGE and state_checks.IS_WEAPON_STAT(weapon, merc.WEAPON_TWO_HANDS):
            ch.send("Your hands are tied up with your weapon!\n")
            return
        handler_game.act("$n wears $p as a shield.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wear $p as a shield.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_SHIELD)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WIELD):
        if not remove_item(ch, merc.WEAR_WIELD, fReplace):
            return
        if not ch.is_npc() and item.get_weight() > (const.str_app[ch.stat(merc.STAT_STR)].wield * 10):
            ch.send("It is too heavy for you to wield.\n")
            return
        if not ch.is_npc() and ch.size < merc.SIZE_LARGE \
                and state_checks.IS_WEAPON_STAT(item, merc.WEAPON_TWO_HANDS) \
                and merc.items.get(ch.get_eq(merc.WEAR_SHIELD), None) is not None:
            ch.send("You need two hands free for that weapon.\n")
            return
        handler_game.act("$n wields $p.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You wield $p.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_WIELD)

        sn = ch.get_weapon_sn()

        if sn == "hand to hand":
            return

        skill = ch.get_weapon_skill(sn)
        if skill >= 100:
            handler_game.act("$p feels like a part of you!", ch, item, None, merc.TO_CHAR)
        elif skill > 85:
            handler_game.act("You feel quite confident with $p.", ch, item, None, merc.TO_CHAR)
        elif skill > 70:
            handler_game.act("You are skilled with $p.", ch, item, None, merc.TO_CHAR)
        elif skill > 50:
            handler_game.act("Your skill with $p is adequate.", ch, item, None, merc.TO_CHAR)
        elif skill > 25:
            handler_game.act("$p feels a little clumsy in your hands.", ch, item, None, merc.TO_CHAR)
        elif skill > 1:
            handler_game.act("You fumble and almost drop $p.", ch, item, None, merc.TO_CHAR)
        else:
            handler_game.act("You don't even know which end is up on $p.", ch, item, None, merc.TO_CHAR)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_HOLD):
        if not remove_item(ch, merc.WEAR_HOLD, fReplace):
            return
        handler_game.act("$n holds $p in $s hand.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You hold $p in your hand.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_HOLD)
        return
    if state_checks.CAN_WEAR(item, merc.ITEM_WEAR_FLOAT):
        if not remove_item(ch, merc.WEAR_FLOAT, fReplace):
            return
        handler_game.act("$n releases $p to float next to $m.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You release $p and it floats next to you.", ch, item, None, merc.TO_CHAR)
        ch.equip(item, merc.WEAR_FLOAT)
        return
    if fReplace:
        ch.send("You can't wear, wield, or hold that.\n")
    return


def get_item(ch, item, container):
    # variables for AUTOSPLIT */
    if not state_checks.CAN_WEAR(item, merc.ITEM_TAKE):
        ch.send("You can't take that.\n")
        return
    if ch.carry_number + item.get_number() > ch.can_carry_n():
        handler_game.act("$d: you can't carry that many items.", ch, None, item.name, merc.TO_CHAR)
        return
    if (not item.in_item or merc.items[item.in_item].carried_by != ch.instance_id) \
            and (state_checks.get_carry_weight(ch) + item.get_weight() > ch.can_carry_w()):
        handler_game.act("$d: you can't carry that much weight.", ch, None, item.name, merc.TO_CHAR)
        return
    if not ch.can_loot(item):
        handler_game.act("Corpse looting is not permitted.", ch, None, None, merc.TO_CHAR)
        return
    if item.in_room:
        for gch_id in merc.rooms[item.in_room].people:
            gch = merc.characters[gch_id]
            if gch.on:
                if merc.items[gch.on] == item.instance_id:
                    handler_game.act("$N appears to be using $p.", ch, item, gch, merc.TO_CHAR)
                    return
    if container:
        if container.vnum == merc.OBJ_VNUM_PIT and ch.trust < item.level:
            ch.send("You are not powerful enough to use it.\n")
            return
        if container.vnum == merc.OBJ_VNUM_PIT \
                and not state_checks.CAN_WEAR(container, merc.ITEM_TAKE) \
                and not state_checks.is_item_stat(item, merc.ITEM_HAD_TIMER):
            item.timer = 0
            handler_game.act("You get $p from $P.", ch, item, container, merc.TO_CHAR)
            handler_game.act("$n gets $p from $P.", ch, item, container, merc.TO_ROOM)
            state_checks.REMOVE_BIT(item.extra_flags, merc.ITEM_HAD_TIMER)
            item.from_item()
    else:
        handler_game.act("You get $p.", ch, item, container, merc.TO_CHAR)
        handler_game.act("$n gets $p.", ch, item, container, merc.TO_ROOM)
        item.from_room()
    if item.item_type == merc.ITEM_MONEY:
        ch.silver += item.value[0]
        ch.gold += item.value[1]
        if ch.act.is_set(merc.PLR_AUTOSPLIT):
            # AUTOSPLIT code */
            members = len([gch for gch in merc.rooms[ch.in_room].people
                           if not state_checks.IS_AFFECTED(merc.characters[gch], merc.AFF_CHARM)
                           and merc.characters[gch].is_same_group(ch)])
            if members > 1 and (item.value[0] > 1 or item.value[1]):
                ch.do_split("%d %d" % (item.value[0], item.value[1]))
        item.extract()
    else:
        item.to_char(ch)
    return


# trust levels for load and clone */
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


def format_item_to_char(item_id, ch, fShort):
    buf = ''
    item = merc.items[item_id]
    if (fShort and not item.short_descr) or not item.description:
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

    if fShort:
        if item.short_descr:
            buf += item.short_descr
    else:
        if item.description:
            buf += item.description
    if ch.act.is_set(merc.PLR_OMNI):
        buf += "(%d)" % item.instance_id
    return buf


# * Count occurrences of an obj in a list.
def count_obj_list(itemInstance, contents):
    return len([item_id for item_id in contents if merc.items[item_id].name == itemInstance.name])


# for clone, to insure that cloning goes many levels deep */
def recursive_clone(ch, item, clone):
    for c_item_id in item.contains:
        c_item = merc.items[c_item_id]
        if item_check(ch, c_item):
            t_obj = object_creator.create_item(merc.itemTemplate[c_item.vnum], 0)
            object_creator.clone_item(c_item, t_obj)
            t_obj.to_item(clone)
            recursive_clone(ch, c_item, t_obj)


class handler_item:
    # * Find the ac value of an obj, including position effect.
    def apply_ac(item, iWear, loc):
        if item.item_type != merc.ITEM_ARMOR:
            return 0

        multi = {merc.WEAR_BODY: 3, merc.WEAR_HEAD: 2, merc.WEAR_LEGS: 2, merc.WEAR_ABOUT: 2}
        if iWear in multi:
            return multi[iWear] * item.value[loc]
        else:
            return item.value[loc]

    # * Give an obj to a char.
    def to_char(item, ch):
        ch.contents.append(item.instance_id)
        item.carried_by = ch.instance_id
        item.in_room = None
        item.in_item = None
        ch.carry_number += item.get_number()
        ch.carry_weight += item.get_weight()

    # * Return # of objects which an object counts as.
    # * Thanks to Tony Chamberlain for the correct recursive code here.
    def get_number(item):
        noweight = [merc.ITEM_CONTAINER, merc.ITEM_MONEY, merc.ITEM_GEM, merc.ITEM_JEWELRY]
        if item.item_type in noweight:
            number = 0
        else:
            number = 1
        contents = item.contains[:]
        counted = [item.instance_id]
        for content_id in contents:
            content = merc.items[content_id]
            number += 1
            if content.instance_id in counted:
                logger.debug("BUG: Objects contain eachother. %s(%d) - %s(%d)" %
                             (item.short_descr, item.instance_id, content.short_descr, content.instance_id))
                break
            counted.append(content)
            contents.extend(content.contains)

        return number

    #
    # * Return weight of an object, including weight of contents.
    def get_weight(item):
        weight = item.weight
        contents = item.contains[:]
        counted = [item.instance_id]
        for content_id in contents:
            content = merc.items[content_id]
            if content.instance_id in counted:
                print("BUG: Objects contain eachother. %s(%d) - %s(%d)" %
                      (item.short_descr, item.instance_id, content.short_descr, content.instance_id))
                break
            counted.append(content)

            weight += content.weight * state_checks.WEIGHT_MULT(item) / 100
            contents.extend(content.contains)
        return weight

    def true_weight(item):
        weight = item.weight
        for content_id in item.contains:
            content = merc.items[content_id]
            weight += content.get_weight()
        return weight

    # enchanted stuff for eq */
    def affect_enchant(item):
        # okay, move all the old flags into new vectors if we have to */
        if not item.enchanted:
            item.enchanted = True
            for paf in merc.itemTemplate[item.vnum].affected:
                af_new = handler_game.AFFECT_DATA()
                item.affected.append(af_new)

                af_new.where = paf.where
                af_new.type = max(0, paf.type)
                af_new.level = paf.level
                af_new.duration = paf.duration
                af_new.location = paf.location
                af_new.modifier = paf.modifier
                af_new.bitvector = paf.bitvector

    # give an affect to an object */

    def affect_add(item, paf):
        paf_new = handler_game.AFFECT_DATA()
        item.affected.append(paf_new)
        # apply any affect vectors to the object's extra_flags */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                state_checks.SET_BIT(item.extra_flags, paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if item.item_type == merc.ITEM_WEAPON:
                    state_checks.SET_BIT(item.value[4], paf.bitvector)

    def affect_remove(item, paf):
        if not item.affected:
            print("BUG: Affect_remove_object: no affect.")
            return

        if item.carried_by is not None and item.wear_loc != -1:
            merc.characters[item.carried_by].affect_modify(paf, False)

        where = paf.where
        vector = paf.bitvector

        # remove flags from the object if needed */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                state_checks.REMOVE_BIT(item.extra_flags, paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if item.item_type == merc.ITEM_WEAPON:
                    state_checks.REMOVE_BIT(item.value[4], paf.bitvector)

        if paf not in item.affected:
            print("BUG: Affect_remove_object: cannot find paf.")
            return
        item.affected.remove(paf)
        del paf
        if item.carried_by != 0 and item.wear_loc != -1:
            merc.characters[item.carried_by].affect_check(where, vector)
        return

    # * Move an obj out of a room.
    def from_room(item):
        if not item.in_room:
            print("Bug: obj_from_room: None.")
            return
        room = merc.rooms[item.in_room]
        for ids in room.people:
            ch = merc.characters[ids]
            if ch.on:
                if merc.items[ch.on] == item.instance_id:
                    merc.items[ch.on] = None

        if item.instance_id not in room.contents:
            print("Bug: Obj_from_room: obj not found.")
            return

        item.in_room = None
        room.contents.remove(item.instance_id)
        return

    # * Move an obj into a room.
    def to_room(item, room_instance):
        room = merc.rooms[room_instance]
        room.contents.append(item.instance_id)
        item.in_room = room.instance_id
        item.carried_by = None
        item.in_item = None
        return

    # * Move an object into an object.
    def to_item(item, obj_to):
        obj_to.contains.append(item.instance_id)
        item.in_item = obj_to.instance_id
        item.in_room = None
        item.carried_by = None
        if obj_to.vnum == merc.OBJ_VNUM_PIT:
            item.cost = 0

        while obj_to:
            if obj_to.carried_by:
                merc.characters[obj_to.carried_by].carry_number += item.get_number()
                merc.characters[obj_to.carried_by].carry_weight += \
                    item.get_weight() * state_checks.WEIGHT_MULT(obj_to) / 100
            obj_to = obj_to.in_item
        return

    # * Move an object out of an object.
    def from_item(item):
        if not merc.items[item.in_item]:
            print("Bug: Obj_from_obj: null obj_from.")
            return
        item_from = merc.items[item.in_item]

        if item.instance_id not in item_from.contents:
            print("BUG: Obj_from_obj: obj not found.")
            return
        item_from.contents.remove(item.instance_id)
        item.in_item = None

        while item_from:
            if item_from.carried_by:
                merc.characters[item_from.carried_by].carry_number -= item.get_number()
                merc.characters[item_from.carried_by].carry_weight -= item.get_weight() * \
                                                                      state_checks.WEIGHT_MULT(item_from) / 100
            item_from = merc.items[item_from.in_item]
        return

    # * Extract an obj from the world.
    def extract(item):
        if item.in_room:
            item.from_room()
        elif item.carried_by:
            item.from_char()
        elif item.in_item:
            item.from_item()

        for item_id in item.contains[:]:
            if item.instance_id not in merc.items:
                print("Extract_obj: obj %d not found in obj_instance dict." % item.instance_id)
                return
            item = merc.items[item_id]
            item.extract()

    # * Take an obj from its character.
    def from_char(item):
        ch = merc.characters[item.carried_by]
        if not ch:
            print("BUG: Obj_from_char: null ch.")
            return

        if item.wear_loc != merc.WEAR_NONE:
            ch.unequip(item.instance_id)

        ch.contents.remove(item.instance_id)

        item.carried_by = None
        ch.carry_number -= item.get_number()
        ch.carry_weight -= item.get_weight()
        return

    # Return the number of players "on" an object.
    def count_users(item):
        total = 0
        if item.in_room:
            for person_id in merc.rooms[item.in_room].people:
                person = merc.characters[person_id]
                if person.on == item.instance_id:
                    total += 1
        return total


methods = {d: f for d, f in handler_item.__dict__.items() if not d.startswith('__')}
for m, f in methods.items():
    setattr(Items, m, f)
