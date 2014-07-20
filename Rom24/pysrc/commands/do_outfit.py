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

    item = ch.get_eq(merc.WEAR_LIGHT)
    if not item:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_BANNER], 0)
        item.cost = 0
        item.to_environment(ch)
        ch.equip(item, merc.WEAR_LIGHT)

    item = ch.get_eq(merc.WEAR_BODY)
    if not item:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_VEST], 0)
        item.cost = 0
        item.to_environment(ch)
        ch.equip(item, merc.WEAR_BODY)

    # do the weapon thing
    item = ch.get_eq(merc.WEAR_WIELD)
    if not item:
        sn = 'dagger'
        vnum = merc.OBJ_VNUM_SCHOOL_SWORD  # just in case!
        for k, weapon in const.weapon_table.items():
            if sn not in ch.learned or (
                    weapon.gsn in ch.learned and ch.learned[sn] < ch.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum
        item = object_creator.create_item(merc.itemTemplate[vnum], 0)
        item.to_environment(ch)
        ch.equip(item, merc.WEAR_WIELD)

    item = ch.get_eq(merc.WEAR_WIELD)
    shield = ch.get_eq(merc.WEAR_SHIELD)
    if (not item or not state_checks.IS_WEAPON_STAT(item, merc.WEAPON_TWO_HANDS)) and not shield:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_SHIELD], 0)
        item.cost = 0
        item.to_environment(ch)
        ch.equip(item, merc.WEAR_SHIELD)

    ch.send("You have been equipped by Mota.\n")


interp.register_command(interp.cmd_type('outfit', do_outfit, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
