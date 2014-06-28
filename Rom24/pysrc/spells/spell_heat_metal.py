import random

from const import SLOT, skill_type, register_spell
from fight import damage
from merc import saves_spell, DAM_FIRE, IS_SET, IMM_FIRE, IS_OBJ_STAT, ITEM_NONMETAL, ITEM_BURN_PROOF, ITEM_ARMOR, \
    STAT_DEX, remove_obj, act, TO_ROOM, TO_CHAR, ITEM_WEAPON, IS_WEAPON_STAT, WEAPON_FLAMING, TAR_CHAR_OFFENSIVE, \
    POS_FIGHTING


def spell_heat_metal(sn, level, ch, victim, target):
    fail = True

    if not saves_spell(level + 2, victim, DAM_FIRE) and not IS_SET(victim.imm_flags, IMM_FIRE):
        for obj_lose in victim.carrying[:]:
            if random.randint(1, 2 * level) > obj_lose.level \
                    and not saves_spell(level, victim, DAM_FIRE) \
                    and not IS_OBJ_STAT(obj_lose, ITEM_NONMETAL) \
                    and not IS_OBJ_STAT(obj_lose, ITEM_BURN_PROOF):
                if obj_lose.item_type == ITEM_ARMOR:
                    if obj_lose.wear_loc != -1:  # remove the item */
                        if victim.can_drop_obj(obj_lose) \
                                and (obj_lose.weight // 10) < random.randint(1, 2 * victim.get_curr_stat(STAT_DEX)) \
                                and remove_obj(victim, obj_lose.wear_loc, True):
                            act("$n yelps and throws $p to the ground! ", victim, obj_lose, None, TO_ROOM)
                            act("You remove and drop $p before it burns you.", victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 3)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # stuck on the body!  ouch!  */
                            act("Your skin is seared by $p! ",
                                victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level))
                            fail = False
                    else:  # drop it if we can */
                        if victim.can_drop_obj(obj_lose):
                            act("$n yelps and throws $p to the ground! ", victim, obj_lose, None, TO_ROOM)
                            act("You and drop $p before it burns you.", victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 6)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # can! drop */
                            act("Your skin is seared by $p! ", victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 2)
                            fail = False
                if obj_lose.item_type == ITEM_WEAPON:
                    if obj_lose.wear_loc != -1:  # try to drop it */
                        if IS_WEAPON_STAT(obj_lose, WEAPON_FLAMING):
                            continue
                        if victim.can_drop_obj(obj_lose) and remove_obj(victim, obj_lose.wear_loc, True):
                            act("$n is burned by $p, and throws it to the ground.", victim, obj_lose, None, TO_ROOM)
                            victim.send("You throw your red-hot weapon to the ground! \n")
                            dam += 1
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # YOWCH!  */
                            victim.send("Your weapon sears your flesh! \n")
                            dam += random.randint(1, obj_lose.level)
                            fail = False
                    else:  # drop it if we can */
                        if victim.can_drop_obj(obj_lose):
                            act("$n throws a burning hot $p to the ground! ", victim, obj_lose, None, TO_ROOM)
                            act("You and drop $p before it burns you.", victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 6)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # can! drop */
                            act("Your skin is seared by $p! ", victim, obj_lose, None, TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 2)
                            fail = False
    if fail:
        ch.send("Your spell had no effect.\n")
        victim.send("You feel momentarily warmer.\n")
    else:  # damage!  */
        if saves_spell(level, victim, DAM_FIRE):
            dam = 2 * dam // 3
        damage(ch, victim, dam, sn, DAM_FIRE, True)


register_spell(skill_type("heat metal",
                          {'mage': 53, 'cleric': 16, 'thief': 53, 'warrior': 23},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_heat_metal, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(516), 25, 18, "spell", "!Heat Metal!", ""))