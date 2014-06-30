import random
import const
import fight
import handler_game
import handler_magic
import handler_obj
import merc
import state_checks


def spell_heat_metal(sn, level, ch, victim, target):
    fail = True

    if not handler_magic.saves_spell(level + 2, victim, merc.DAM_FIRE) and not state_checks.IS_SET(victim.imm_flags,
                                                                                                   merc.IMM_FIRE):
        for obj_lose in victim.contents[:]:
            if random.randint(1, 2 * level) > obj_lose.level \
                    and not handler_magic.saves_spell(level, victim, merc.DAM_FIRE) \
                    and not state_checks.IS_OBJ_STAT(obj_lose, merc.ITEM_NONMETAL) \
                    and not state_checks.IS_OBJ_STAT(obj_lose, merc.ITEM_BURN_PROOF):
                if obj_lose.item_type == merc.ITEM_ARMOR:
                    if obj_lose.wear_loc != -1:  # remove the item */
                        if victim.can_drop_obj(obj_lose) \
                                and (obj_lose.weight // 10) < random.randint(1, 2 * victim.stat(merc.STAT_DEX)) \
                                and handler_obj.remove_obj(victim, obj_lose.wear_loc, True):
                            handler_game.act("$n yelps and throws $p to the ground! ", victim, obj_lose, None,
                                             merc.TO_ROOM)
                            handler_game.act("You remove and drop $p before it burns you.", victim, obj_lose, None,
                                             merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 3)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # stuck on the body!  ouch!  */
                            handler_game.act("Your skin is seared by $p! ",
                                victim, obj_lose, None, merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level))
                            fail = False
                    else:  # drop it if we can */
                        if victim.can_drop_obj(obj_lose):
                            handler_game.act("$n yelps and throws $p to the ground! ", victim, obj_lose, None,
                                             merc.TO_ROOM)
                            handler_game.act("You and drop $p before it burns you.", victim, obj_lose, None,
                                             merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 6)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # can! drop */
                            handler_game.act("Your skin is seared by $p! ", victim, obj_lose, None, merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 2)
                            fail = False
                if obj_lose.item_type == merc.ITEM_WEAPON:
                    if obj_lose.wear_loc != -1:  # try to drop it */
                        if state_checks.IS_WEAPON_STAT(obj_lose, merc.WEAPON_FLAMING):
                            continue
                        if victim.can_drop_obj(obj_lose) and handler_obj.remove_obj(victim, obj_lose.wear_loc, True):
                            handler_game.act("$n is burned by $p, and throws it to the ground.", victim, obj_lose, None,
                                             merc.TO_ROOM)
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
                            handler_game.act("$n throws a burning hot $p to the ground! ", victim, obj_lose, None,
                                             merc.TO_ROOM)
                            handler_game.act("You and drop $p before it burns you.", victim, obj_lose, None,
                                             merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 6)
                            obj_lose.from_char()
                            obj_lose.to_room(victim.in_room)
                            fail = False
                        else:  # can! drop */
                            handler_game.act("Your skin is seared by $p! ", victim, obj_lose, None, merc.TO_CHAR)
                            dam += (random.randint(1, obj_lose.level) // 2)
                            fail = False
    if fail:
        ch.send("Your spell had no effect.\n")
        victim.send("You feel momentarily warmer.\n")
    else:  # damage!  */
        if handler_magic.saves_spell(level, victim, merc.DAM_FIRE):
            dam = 2 * dam // 3
        fight.damage(ch, victim, dam, sn, merc.DAM_FIRE, True)


const.register_spell(const.skill_type("heat metal",
                          {'mage': 53, 'cleric': 16, 'thief': 53, 'warrior': 23},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_heat_metal, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(516), 25, 18, "spell", "!Heat Metal!", ""))
