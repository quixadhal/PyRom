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
from merc import *

class handler_obj:
    # * Find the ac value of an obj, including position effect.
    def apply_ac(obj, iWear, loc):
        if obj.item_type != ITEM_ARMOR:
            return 0

        multi = {WEAR_BODY:3, WEAR_HEAD:2, WEAR_LEGS:2, WEAR_ABOUT:2}
        if iWear in multi:
            return multi[iWear] * obj.value[loc]
        else:
            return obj.value[loc]

    # * Give an obj to a char.
    def to_char(obj, ch):
        ch.carrying.append(obj)
        obj.carried_by = ch
        obj.in_room = None
        obj.in_obj = None
        ch.carry_number += obj.get_number()
        ch.carry_weight += obj.get_weight()

    # * Return # of objects which an object counts as.
    # * Thanks to Tony Chamberlain for the correct recursive code here.
    def get_number(obj):
        noweight = [ITEM_CONTAINER, ITEM_MONEY, ITEM_GEM, ITEM_JEWELRY]
        if obj.item_type in noweight:
            number = 0
        else:
            number = 1
        contents = obj.contains[:]
        counted = [obj]
        for o in contents:
            number += 1
            if o in counted:
                print ("BUG: Objects contain eachother. %s(%d) - %s(%d)" % (obj.short_descr, obj.pIndexData.vnum, o.short_descr, o.pIndexData.vnum))
                break
            counted.append(o)
            contents.extend(o.contains)
     
        return number
    #
    #* Return weight of an object, including weight of contents.
    def get_weight(obj):
        weight = obj.weight
        contents = obj.contains[:]
        counted = [obj]
        for tobj in contents:
            if tobj in counted:
                print("BUG: Objects contain eachother. %s(%d) - %s(%d)" % (obj.short_descr, obj.pIndexData.vnum, tobj.short_descr, tobj.pIndexData.vnum))
                break
            counted.append(tobj)

            weight += tobj.weight * WEIGHT_MULT(obj) / 100
            contents.extend(tobj.contains)
        return weight

    def true_weight(obj):
        weight = obj.weight
        for o in obj.contains:
            weight += o.get_weight()
        return weight

    # enchanted stuff for eq */
    def affect_enchant(obj):
        # okay, move all the old flags into new vectors if we have to */
        if not obj.enchanted:
            obj.enchanted = True
            for paf in obj.pIndexData.affected:
                af_new = AFFECT_DATA()
                obj.affected.append(af_new)

                af_new.where = paf.where
                af_new.type = max(0,paf.type)
                af_new.level = paf.level
                af_new.duration = paf.duration
                af_new.location = paf.location
                af_new.modifier = paf.modifier
                af_new.bitvector = paf.bitvector
    # give an affect to an object */
    def affect_add(obj, paf):
        paf_new = AFFECT_DATA()
        obj.affected.append(paf_new)
        # apply any affect vectors to the object's extra_flags */
        if paf.bitvector:
            if paf.where == TO_OBJECT:
                SET_BIT(obj.extra_flags,paf.bitvector)
            elif paf.where == TO_WEAPON:
                if obj.item_type == ITEM_WEAPON:
                    SET_BIT(obj.value[4],paf.bitvector)                

    def affect_remove(obj, paf):
        if not obj.affected:
            print ("BUG: Affect_remove_object: no affect.")
            return

        if obj.carried_by != None and obj.wear_loc != -1:
            obj.carried_by.affect_modify(paf, False)

        where = paf.where
        vector = paf.bitvector

        # remove flags from the object if needed */
        if paf.bitvector:
            if paf.where == TO_OBJECT:
                REMOVE_BIT(obj.extra_flags,paf.bitvector)
            elif paf.where == TO_WEAPON:
                if obj.item_type == ITEM_WEAPON:
                    REMOVE_BIT(obj.value[4],paf.bitvector)

        if paf not in obj.affected:
            print ("BUG: Affect_remove_object: cannot find paf.")
            return
        obj.affected.remove(paf)
        del paf
        if obj.carried_by != None and obj.wear_loc != -1:
            obj.carried_by.affect_check(where, vector)
        return

    # * Move an obj out of a room.
    def from_room(obj):
        if not obj.in_room:
            print ("Bug: obj_from_room: None.")
            return
        in_room = obj.in_room
        for ch in in_room.people:
            if ch.on == obj:
                ch.on = None

        if obj not in in_room.contents:
            print ("Bug: Obj_from_room: obj not found.")
            return

        obj.in_room = None
        in_room.contents.remove(obj)
        return

    # * Move an obj into a room.
    def to_room(obj, pRoomIndex):
        pRoomIndex.contents.append(obj)
        obj.in_room = pRoomIndex
        obj.carried_by = None
        obj.in_obj = None
        return

    # * Move an object into an object.
    def to_obj(obj, obj_to):
        obj_to.contains.append(obj)
        obj.in_obj = obj_to
        obj.in_room = None
        obj.carried_by = None
        if obj_to.pIndexData.vnum == OBJ_VNUM_PIT:
            obj.cost = 0 

        while obj_to:
            if obj_to.carried_by:
                obj_to.carried_by.carry_number += obj.get_number()
                obj_to.carried_by.carry_weight += obj.get_weight() * WEIGHT_MULT(obj_to) / 100
            obj_to = obj_to.in_obj            
        return

    # * Move an object out of an object.
    def from_obj(obj):
        if not obj.in_obj:
            print ("Bug: Obj_from_obj: null obj_from.")
            return
        obj_from = obj.in_obj

        if obj not in obj_from.contents:
            print ("BUG: Obj_from_obj: obj not found.")
            return
        obj_from.contents.remove(obj)
        obj.in_obj       = None

        while obj_from:
            if obj_from.carried_by:
                obj_from.carried_by.carry_number -= obj.get_number()
                obj_from.carried_by.carry_weight -= obj.get_weight() * WEIGHT_MULT(obj_from) / 100
            obj_from = obj_from.in_obj
        return

    # * Extract an obj from the world.
    def extract(obj):
        if obj.in_room:
            obj.from_room()
        elif obj.carried_by:
            obj.from_char()
        elif obj.in_obj:
            obj.from_obj()

        for obj_content in obj.contains[:]:
            obj_content.extract()

        if obj not in object_list:
            print ("Extract_obj: obj %d not found." % obj.pIndexData.vnum)
            return
        object_list.remove(obj)

    # * Take an obj from its character.
    def from_char(obj):
        ch = obj.carried_by
        if not ch:
            print ("BUG: Obj_from_char: null ch.")
            return
        
        if obj.wear_loc != WEAR_NONE:
            ch.unequip(obj)

        ch.carrying.remove(obj)

        obj.carried_by = None
        ch.carry_number -= obj.get_number()
        ch.carry_weight -= obj.get_weight()
        return

methods = {d:f for d,f in handler_obj.__dict__.items() if not d.startswith('__')}
for m,f in methods.items():
    setattr(OBJ_DATA, m, f)