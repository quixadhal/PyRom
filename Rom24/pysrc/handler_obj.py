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
import const
import handler_game
import merc
import state_checks


class OBJ_INDEX_DATA:
    def __init__(self):
        self.extra_descr = []
        self.affected = []
        self.new_format = True
        self.name = ""
        self.short_descr = ""
        self.description = ""
        self.vnum = 0
        self.reset_num = 0
        self.material = ""
        self.item_type = 0
        self.extra_flags = 0
        self.wear_flags = 0
        self.level = 0
        self.condition = 0
        self.count = 0
        self.weight = 0
        self.cost = 0
        self.value = [0, 0, 0, 0, 0]

    def __repr__(self):
        return "<ObjIndex: %s:%d>" % (self.short_descr, self.vnum)

# * One object.


class OBJ_DATA:
    def __init__(self):
        self.contains = []
        self.in_obj = None
        self.on = None
        self.carried_by = None
        self.extra_descr = []
        self.affected = []
        self.pIndexData = None
        self.in_room = None
        self.valid = False
        self.enchanted = False
        self.owner = ""
        self.name = ""
        self.short_descr =""
        self.description =""
        self.item_type = 0
        self.extra_flags = 0
        self.wear_flags = 0
        self.wear_loc = 0
        self.weight = 0
        self.cost = 0
        self.level = 0
        self.condition = 0
        self.material = ""
        self.timer = 0
        self.value = [0 for x in range(5)]


   # * Remove an object.
def remove_obj(ch, iWear, fReplace):
    obj = ch.get_eq(iWear)
    if not obj:
        return True
    if not fReplace:
        return False
    if state_checks.IS_SET(obj.extra_flags, merc.ITEM_NOREMOVE):
        handler_game.act("You can't remove $p.", ch, obj, None, merc.TO_CHAR)
        return False
    ch.unequip(obj)
    handler_game.act("$n stops using $p.", ch, obj, None, merc.TO_ROOM)
    handler_game.act("You stop using $p.", ch, obj, None, merc.TO_CHAR)
    return True

    #
# * Wear one object.
# * Optional replacement of existing objects.
# * Big repetitive code, ick.
def wear_obj( ch, obj, fReplace ):
    if ch.level < obj.level:
        ch.send("You must be level %d to use this object.\n" % obj.level)
        handler_game.act( "$n tries to use $p, but is too inexperienced.", ch, obj, None, merc.TO_ROOM)
        return
    if obj.item_type == merc.ITEM_LIGHT:
        if not remove_obj( ch, merc.WEAR_LIGHT, fReplace ):
            return
        handler_game.act( "$n lights $p and holds it.", ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You light $p and hold it.",  ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_LIGHT)
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_FINGER):
        if ch.get_eq(merc.WEAR_FINGER_L) and ch.get_eq(merc.WEAR_FINGER_R) \
                and not remove_obj(ch, merc.WEAR_FINGER_L, fReplace) \
                and not remove_obj(ch, merc.WEAR_FINGER_R, fReplace):
            return
        if not ch.get_eq(merc.WEAR_FINGER_L):
            handler_game.act( "$n wears $p on $s left finger.",    ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p on your left finger.",  ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_FINGER_L)
            return
        if not ch.get_eq(merc.WEAR_FINGER_R):
            handler_game.act( "$n wears $p on $s right finger.",   ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p on your right finger.", ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_FINGER_R)
            return
        print ("BUG: Wear_obj: no free finger.")
        ch.send("You already wear two rings.\n")
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_NECK):
        if ch.get_eq(merc.WEAR_NECK_1) and ch.get_eq(merc.WEAR_NECK_2) \
                and not remove_obj(ch, merc.WEAR_NECK_1, fReplace) \
                and not remove_obj(ch, merc.WEAR_NECK_2, fReplace):
            return
        if not ch.get_eq(merc.WEAR_NECK_1):
            handler_game.act( "$n wears $p around $s neck.",   ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p around your neck.", ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_NECK_1)
            return
        if not ch.get_eq(merc.WEAR_NECK_2):
            handler_game.act( "$n wears $p around $s neck.",   ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p around your neck.", ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_NECK_2)
            return
        print ("BUG: Wear_obj: no free neck.")
        ch.send("You already wear two neck items.\n")
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_BODY):
        if not remove_obj( ch, merc.WEAR_BODY, fReplace ):
            return
        handler_game.act( "$n wears $p on $s torso.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your torso.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_BODY)
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_HEAD):
        if not remove_obj(ch, merc.WEAR_HEAD, fReplace):
            return
        handler_game.act( "$n wears $p on $s head.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your head.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_HEAD)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WEAR_LEGS):
        if not remove_obj( ch, merc.WEAR_LEGS, fReplace):
            return
        handler_game.act( "$n wears $p on $s legs.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your legs.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_LEGS)
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_FEET):
        if not remove_obj( ch, merc.WEAR_FEET, fReplace ):
            return
        handler_game.act( "$n wears $p on $s feet.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your feet.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_FEET)
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_HANDS):
        if not remove_obj( ch, merc.WEAR_HANDS, fReplace ):
            return
        handler_game.act( "$n wears $p on $s hands.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your hands.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_HANDS)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WEAR_ARMS):
        if not remove_obj( ch, merc.WEAR_ARMS, fReplace ):
            return
        handler_game.act( "$n wears $p on $s arms.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p on your arms.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_ARMS)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WEAR_ABOUT):
        if not remove_obj( ch, merc.WEAR_ABOUT, fReplace ):
            return
        handler_game.act( "$n wears $p about $s torso.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p about your torso.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_ABOUT)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WEAR_WAIST):
        if not remove_obj( ch, merc.WEAR_WAIST, fReplace ):
            return
        handler_game.act( "$n wears $p about $s waist.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p about your waist.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_WAIST)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WEAR_WRIST):
        if ch.get_eq(merc.WEAR_WRIST_L) and ch.get_eq(merc.WEAR_WRIST_R) \
        and not remove_obj(ch, merc.WEAR_WRIST_L, fReplace) and not remove_obj( ch, merc.WEAR_WRIST_R, fReplace ):
            return
        if not ch.get_eq(merc.WEAR_WRIST_L):
            handler_game.act( "$n wears $p around $s left wrist.",ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p around your left wrist.",ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_WRIST_L)
            return
        if not ch.get_eq(merc.WEAR_WRIST_R):
            handler_game.act( "$n wears $p around $s right wrist.",ch, obj, None, merc.TO_ROOM)
            handler_game.act( "You wear $p around your right wrist.",ch, obj, None, merc.TO_CHAR)
            ch.equip(obj, merc.WEAR_WRIST_R)
            return

        print ("BUG: Wear_obj: no free wrist.")
        ch.send("You already wear two wrist items.\n")
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_SHIELD):
        if not remove_obj(ch, merc.WEAR_SHIELD, fReplace):
            return
        weapon = ch.get_eq(merc.WEAR_WIELD)
        if weapon and ch.size < merc.SIZE_LARGE and state_checks.IS_WEAPON_STAT(weapon, merc.WEAPON_TWO_HANDS):
            ch.send("Your hands are tied up with your weapon!\n")
            return
        handler_game.act( "$n wears $p as a shield.", ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wear $p as a shield.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_SHIELD)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_WIELD):
        if not remove_obj( ch, merc.WEAR_WIELD, fReplace ):
            return
        if not state_checks.IS_NPC(ch) and obj.get_weight() > (const.str_app[ch.get_curr_stat(merc.STAT_STR)].wield * 10):
            ch.send("It is too heavy for you to wield.\n")
            return
        if not state_checks.IS_NPC(ch) and ch.size < merc.SIZE_LARGE \
                and state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_TWO_HANDS) \
                and ch.get_eq(merc.WEAR_SHIELD) is not None:
            ch.send("You need two hands free for that weapon.\n")
            return
        handler_game.act( "$n wields $p.", ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You wield $p.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_WIELD)

        sn = ch.get_weapon_sn()

        if sn == "hand to hand":
            return

        skill = ch.get_weapon_skill(sn)
        if skill >= 100: handler_game.act("$p feels like a part of you!",ch,obj,None, merc.TO_CHAR)
        elif skill > 85: handler_game.act("You feel quite confident with $p.",ch,obj,None, merc.TO_CHAR)
        elif skill > 70: handler_game.act("You are skilled with $p.",ch,obj,None, merc.TO_CHAR)
        elif skill > 50: handler_game.act("Your skill with $p is adequate.",ch,obj,None, merc.TO_CHAR)
        elif skill > 25: handler_game.act("$p feels a little clumsy in your hands.",ch,obj,None, merc.TO_CHAR)
        elif skill > 1: handler_game.act("You fumble and almost drop $p.",ch,obj,None, merc.TO_CHAR)
        else: handler_game.act("You don't even know which end is up on $p.",ch,obj,None, merc.TO_CHAR)
        return
    if state_checks.CAN_WEAR( obj, merc.ITEM_HOLD):
        if not remove_obj( ch, merc.WEAR_HOLD, fReplace ):
            return
        handler_game.act( "$n holds $p in $s hand.",   ch, obj, None, merc.TO_ROOM)
        handler_game.act( "You hold $p in your hand.", ch, obj, None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_HOLD)
        return
    if state_checks.CAN_WEAR(obj, merc.ITEM_WEAR_FLOAT):
        if not remove_obj(ch, merc.WEAR_FLOAT, fReplace):
            return
        handler_game.act("$n releases $p to float next to $m.",ch,obj,None, merc.TO_ROOM)
        handler_game.act("You release $p and it floats next to you.",ch,obj,None, merc.TO_CHAR)
        ch.equip(obj, merc.WEAR_FLOAT)
        return
    if fReplace:
        ch.send("You can't wear, wield, or hold that.\n")
    return



def get_obj(ch, obj, container):
    # variables for AUTOSPLIT */
    if not state_checks.CAN_WEAR(obj, merc.ITEM_TAKE):
        ch.send("You can't take that.\n")
        return
    if ch.carry_number + obj.get_number() > ch.can_carry_n():
        handler_game.act( "$d: you can't carry that many items.", ch, None, obj.name, merc.TO_CHAR)
        return
    if ( not obj.in_obj or obj.in_obj.carried_by != ch) \
    and (state_checks.get_carry_weight(ch) + obj.get_weight() > ch.can_carry_w()):
        handler_game.act( "$d: you can't carry that much weight.", ch, None, obj.name, merc.TO_CHAR)
        return
    if not ch.can_loot(obj):
        handler_game.act("Corpse looting is not permitted.",ch,None,None, merc.TO_CHAR)
        return
    if obj.in_room is not None:
        for gch in obj.in_room.people:
            if gch.on == obj:
                handler_game.act("$N appears to be using $p.", ch,obj,gch, merc.TO_CHAR)
                return
    if container:
        if container.pIndexData.vnum == merc.OBJ_VNUM_PIT and ch.get_trust() < obj.level:
            ch.send("You are not powerful enough to use it.\n")
            return
    if container.pIndexData.vnum == merc.OBJ_VNUM_PIT \
            and not state_checks.CAN_WEAR(container, merc.ITEM_TAKE) \
    and not state_checks.IS_OBJ_STAT(obj, merc.ITEM_HAD_TIMER):
        obj.timer = 0
        handler_game.act( "You get $p from $P.", ch, obj, container, merc.TO_CHAR)
        handler_game.act( "$n gets $p from $P.", ch, obj, container, merc.TO_ROOM)
        state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_HAD_TIMER)
        obj.from_obj()
    else:
        handler_game.act( "You get $p.", ch, obj, container, merc.TO_CHAR)
        handler_game.act( "$n gets $p.", ch, obj, container, merc.TO_ROOM)
        obj.from_room()
    if obj.item_type == merc.ITEM_MONEY:
        ch.silver += obj.value[0]
        ch.gold += obj.value[1]
        if state_checks.IS_SET(ch.act, merc.PLR_AUTOSPLIT):
            # AUTOSPLIT code */
            members = len([gch for gch in ch.in_room.people if not state_checks.IS_AFFECTED(gch, merc.AFF_CHARM) and gch.is_same_group(ch)])
            if members > 1 and (obj.value[0] > 1 or obj.value[1]):
                ch.do_split("%d %d" % (obj.value[0],obj.value[1]))
        obj.extract()
    else:
        obj.to_char(ch)
    return

# trust levels for load and clone */
def obj_check (ch, obj):
    if state_checks.IS_TRUSTED(ch,GOD) \
    or (state_checks.IS_TRUSTED(ch,IMMORTAL) and obj.level <= 20 and obj.cost <= 1000) \
    or (state_checks.IS_TRUSTED(ch,DEMI)     and obj.level <= 10 and obj.cost <= 500) \
    or (state_checks.IS_TRUSTED(ch,ANGEL)    and obj.level <=  5 and obj.cost <= 250) \
    or (state_checks.IS_TRUSTED(ch,AVATAR)   and obj.level ==  0 and obj.cost <= 100):
        return True
    else:
        return False

def format_obj_to_char(obj, ch, fShort):
    buf = ''
    if (fShort and not obj.short_descr) or not obj.description:
        return buf

    if state_checks.IS_OBJ_STAT(obj, merc.ITEM_INVIS):
        buf += "(Invis) "
    if state_checks.IS_AFFECTED(ch, merc.AFF_DETECT_EVIL) and state_checks.IS_OBJ_STAT(obj, merc.ITEM_EVIL):
        buf += "(Red Aura) "
    if state_checks.IS_AFFECTED(ch, merc.AFF_DETECT_GOOD) and  state_checks.IS_OBJ_STAT(obj, merc.ITEM_BLESS):
        buf += "(Blue Aura) "
    if state_checks.IS_AFFECTED(ch, merc.AFF_DETECT_MAGIC) and state_checks.IS_OBJ_STAT(obj, merc.ITEM_MAGIC):
        buf += "(Magical) "
    if state_checks.IS_OBJ_STAT(obj, merc.ITEM_GLOW):
        buf += "(Glowing) "
    if state_checks.IS_OBJ_STAT(obj, merc.ITEM_HUM):
        buf += "(Humming) "

    if fShort:
        if obj.short_descr:
            buf += obj.short_descr
    else:
        if obj.description:
            buf += obj.description
    if state_checks.IS_SET(ch.act, merc.PLR_OMNI):
        buf += "(%d)" % obj.pIndexData.vnum
    return buf

# * Find some object with a given index data.
# * Used by area-reset 'P' command.
def get_obj_type(pObjIndex):
    search = [obj for obj in merc.object_list if obj.pIndexData == pObjIndex][:1]
    return search[0] if search else None

# * Count occurrences of an obj in a list.
def count_obj_list(pObjIndex, contents):
    return len([obj for obj in contents if obj.pIndexData == pObjIndex])

# for clone, to insure that cloning goes many levels deep */
def recursive_clone(ch, obj, clone):
    import db
    for c_obj in obj.contains:
        if obj_check(ch,c_obj):
            t_obj = db.create_object(c_obj.pIndexData,0)
            db.clone_object(c_obj,t_obj)
            t_obj.to_obj(clone)
            recursive_clone(ch,c_obj,t_obj)

class handler_obj:
    # * Find the ac value of an obj, including position effect.
    def apply_ac(obj, iWear, loc):
        if obj.item_type != merc.ITEM_ARMOR:
            return 0

        multi = {merc.WEAR_BODY:3, merc.WEAR_HEAD:2, merc.WEAR_LEGS:2, merc.WEAR_ABOUT:2}
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
        noweight = [merc.ITEM_CONTAINER, merc.ITEM_MONEY, merc.ITEM_GEM, merc.ITEM_JEWELRY]
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

            weight += tobj.weight * state_checks.WEIGHT_MULT(obj) / 100
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
                af_new = handler_game.AFFECT_DATA()
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
        paf_new = handler_game.AFFECT_DATA()
        obj.affected.append(paf_new)
        # apply any affect vectors to the object's extra_flags */
        if paf.bitvector:
            if paf.where == merc.TO_OBJECT:
                state_checks.SET_BIT(obj.extra_flags,paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if obj.item_type == merc.ITEM_WEAPON:
                    state_checks.SET_BIT(obj.value[4],paf.bitvector)

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
            if paf.where == merc.TO_OBJECT:
                state_checks.REMOVE_BIT(obj.extra_flags,paf.bitvector)
            elif paf.where == merc.TO_WEAPON:
                if obj.item_type == merc.ITEM_WEAPON:
                    state_checks.REMOVE_BIT(obj.value[4],paf.bitvector)

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
        if obj_to.pIndexData.vnum == merc.OBJ_VNUM_PIT:
            obj.cost = 0 

        while obj_to:
            if obj_to.carried_by:
                obj_to.carried_by.carry_number += obj.get_number()
                obj_to.carried_by.carry_weight += obj.get_weight() * state_checks.WEIGHT_MULT(obj_to) / 100
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
                obj_from.carried_by.carry_weight -= obj.get_weight() * state_checks.WEIGHT_MULT(obj_from) / 100
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

        if obj not in merc.object_list:
            print ("Extract_obj: obj %d not found." % obj.pIndexData.vnum)
            return
        merc.object_list.remove(obj)

    # * Take an obj from its character.
    def from_char(obj):
        ch = obj.carried_by
        if not ch:
            print ("BUG: Obj_from_char: null ch.")
            return
        
        if obj.wear_loc != merc.WEAR_NONE:
            ch.unequip(obj)

        ch.carrying.remove(obj)

        obj.carried_by = None
        ch.carry_number -= obj.get_number()
        ch.carry_weight -= obj.get_weight()
        return

    # Return the number of players "on" an object.
    def count_users(obj):
        total = 0
        if obj.in_room:
            for person in obj.in_room.people:
                if person.on == obj:
                    total += 1
        return total

methods = {d:f for d,f in handler_obj.__dict__.items() if not d.startswith('__')}
for m,f in methods.items():
    setattr(OBJ_DATA, m, f)
