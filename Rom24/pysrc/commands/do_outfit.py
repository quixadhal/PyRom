import logging

logger = logging.getLogger()

import merc
import interp
import const
import object_creator

# equips a character
def do_outfit(ch, argument):
    if ch.level > 5 or ch.is_npc():
        ch.send("Find it yourself!\n")
        return

    logger.debug('In outfit..')

    item = ch.slots.light
    if not item:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_BANNER], 0)
        item.cost = 0
        ch.put(item)
        ch.equip(item, True, False)

    item = ch.slots.body
    if not item:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_VEST], 0)
        item.cost = 0
        ch.put(item)
        ch.equip(item, True, False)

    # do the weapon thing
    item = ch.slots.main_hand
    if not item:
        sn = 'dagger'
        vnum = merc.OBJ_VNUM_SCHOOL_SWORD  # just in case!
        for k, weapon in const.weapon_table.items():
            if sn not in ch.learned or (
                    weapon.gsn in ch.learned and ch.learned[sn] < ch.learned[weapon.gsn]):
                sn = weapon.gsn
                vnum = weapon.vnum
        item = object_creator.create_item(merc.itemTemplate[vnum], 0)
        ch.put(item)
        ch.equip(item, True, False)

    item = ch.slots.main_hand
    shield = ch.slots.off_hand
    if (not item or not item.flags.two_handed) and not shield:
        item = object_creator.create_item(merc.itemTemplate[merc.OBJ_VNUM_SCHOOL_SHIELD], 0)
        item.cost = 0
        ch.put(item)
        ch.equip(item, True, False)

    ch.send("You have been equipped by Mota.\n")


interp.register_command(interp.cmd_type('outfit', do_outfit, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
