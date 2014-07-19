import logging
import object_creator

logger = logging.getLogger()

import merc
import interp
import const
import state_checks


# equips a character
def do_outfit(ch, argument):
    if ch.level > 5 or ch.is_npc():
        ch.send("Find it yourself!\n")
        return

    obj = ch.get_eq(merc.WEAR_LIGHT)
    if not obj:
        obj = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_BANNER], 0)
        obj.cost = 0
        obj.to_environment(ch)
        ch.equip(obj, merc.WEAR_LIGHT)

    obj = ch.get_eq(merc.WEAR_BODY)
    if not obj:
        obj = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_VEST], 0)
        obj.cost = 0
        obj.to_environment(ch)
        ch.equip(obj, merc.WEAR_BODY)

    # do the weapon thing
    obj = ch.get_eq(merc.WEAR_WIELD)
    if not obj:
        sn = 'dagger'
        vnum = merc.OBJ_VNUM_SCHOOL_SWORD  # just in case!
        for k, weapon in const.weapon_table.items():
            if sn not in ch.learned or (
                    weapon.gsn in ch.learned and ch.learned[sn] < ch.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum
        obj = object_creator.create_item(merc.itemTemplate[vnum], 0)
        obj.to_environment(ch)
        ch.equip(obj, merc.WEAR_WIELD)

    obj = merc.items.get(ch.get_eq(merc.WEAR_WIELD), None)
    shield = merc.items.get(ch.get_eq(merc.WEAR_SHIELD), None)
    if (not obj or not state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_TWO_HANDS)) and not shield:
        obj = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_SHIELD], 0)
        obj.cost = 0
        obj.to_environment(ch)
        ch.equip(obj, merc.WEAR_SHIELD)

    ch.send("You have been equipped by Mota.\n")


interp.register_command(interp.cmd_type('outfit', do_outfit, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
