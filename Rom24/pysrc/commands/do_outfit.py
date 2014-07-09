import logging

logger = logging.getLogger()

import merc
import db
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
        obj = db.create_object(merc.obj_templates[merc.OBJ_VNUM_SCHOOL_BANNER], 0)
        obj.cost = 0
        obj.to_char(ch)
        ch.equip(obj, merc.WEAR_LIGHT)

    obj = ch.get_eq(merc.WEAR_BODY)
    if not obj:
        obj = db.create_object(merc.obj_templates[merc.OBJ_VNUM_SCHOOL_VEST], 0)
        obj.cost = 0
        obj.to_char(ch)
        ch.equip(obj, merc.WEAR_BODY)

    # do the weapon thing
    obj = ch.get_eq(merc.WEAR_WIELD)
    if not obj:
        sn = 'dagger'
        vnum = merc.OBJ_VNUM_SCHOOL_SWORD  # just in case!
        for k, weapon in const.weapon_table.items():
            if sn not in ch.pcdata.learned or (
                    weapon.gsn in ch.pcdata.learned and ch.pcdata.learned[sn] < ch.pcdata.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum
        obj = db.create_object(merc.obj_templates[vnum], 0)
        obj.to_char(ch)
        ch.equip(obj, merc.WEAR_WIELD)

    obj = ch.get_eq(merc.WEAR_WIELD)
    shield = ch.get_eq(merc.WEAR_SHIELD)
    if (not obj or not state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_TWO_HANDS)) and not shield:
        obj = db.create_object(merc.obj_templates[merc.OBJ_VNUM_SCHOOL_SHIELD], 0)
        obj.cost = 0
        obj.to_char(ch)
        ch.equip(obj, merc.WEAR_SHIELD)

    ch.send("You have been equipped by Mota.\n")


interp.register_command(interp.cmd_type('outfit', do_outfit, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
