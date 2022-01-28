import random

from rom24 import const
from rom24 import fight
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_heat_metal(sn, level, ch, victim, target):
    fail = True

    if not handler_magic.saves_spell(
        level + 2, victim, merc.DAM_FIRE
    ) and not state_checks.IS_SET(victim.imm_flags, merc.IMM_FIRE):
        total_items = set({})
        total_items.update([an_item for an_item in victim.equipped.values()])
        total_items.update(victim.contents)
        for item_id in total_items:
            item = instance.items[item_id]
            if (
                random.randint(1, 2 * level) > item.level
                and not handler_magic.saves_spell(level, victim, merc.DAM_FIRE)
                and not item.flags.no_n_metal
                and not item.flags.burn_proof
            ):
                if item.item_type == merc.ITEM_ARMOR:
                    if item.equipped_to:  # remove the item */
                        if (
                            victim.can_drop_item(item)
                            and (item.weight // 10)
                            < random.randint(1, 2 * victim.stat(merc.STAT_DEX))
                            and victim.unequip(item.equipped_to, True)
                        ):
                            handler_game.act(
                                "$n yelps and throws $p to the ground! ",
                                victim,
                                item,
                                None,
                                merc.TO_ROOM,
                            )
                            handler_game.act(
                                "You remove and drop $p before it burns you.",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level) // 3
                            victim.get(item)
                            victim.in_room.put(item)
                            fail = False
                        else:  # stuck on the body!  ouch!  */
                            handler_game.act(
                                "Your skin is seared by $p! ",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level)
                            fail = False
                    else:  # drop it if we can */
                        if victim.can_drop_item(item):
                            handler_game.act(
                                "$n yelps and throws $p to the ground! ",
                                victim,
                                item,
                                None,
                                merc.TO_ROOM,
                            )
                            handler_game.act(
                                "You and drop $p before it burns you.",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level) // 6
                            victim.get(item)
                            victim.in_room.put(item)
                            fail = False
                        else:  # can! drop */
                            handler_game.act(
                                "Your skin is seared by $p! ",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level) // 2
                            fail = False
                if item.item_type == merc.ITEM_WEAPON:
                    if item.equipped_to:  # try to drop it */
                        if item.flags.flaming:
                            continue
                        if victim.can_drop_item(item) and victim.unequip(
                            item.equipped_to, True
                        ):
                            handler_game.act(
                                "$n is burned by $p, and throws it to the ground.",
                                victim,
                                item,
                                None,
                                merc.TO_ROOM,
                            )
                            victim.send(
                                "You throw your red-hot weapon to the ground! \n"
                            )
                            dam += 1
                            victim.get(item)
                            victim.in_room.put(item)
                            fail = False
                        else:  # YOWCH!  */
                            victim.send("Your weapon sears your flesh! \n")
                            dam += random.randint(1, item.level)
                            fail = False
                    else:  # drop it if we can */
                        if victim.can_drop_item(item):
                            handler_game.act(
                                "$n throws a burning hot $p to the ground! ",
                                victim,
                                item,
                                None,
                                merc.TO_ROOM,
                            )
                            handler_game.act(
                                "You and drop $p before it burns you.",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level) // 6
                            victim.get(item)
                            victim.in_room.put(item)
                            fail = False
                        else:  # can! drop */
                            handler_game.act(
                                "Your skin is seared by $p! ",
                                victim,
                                item,
                                None,
                                merc.TO_CHAR,
                            )
                            dam += random.randint(1, item.level) // 2
                            fail = False
    if fail:
        ch.send("Your spell had no effect.\n")
        victim.send("You feel momentarily warmer.\n")
    else:  # damage!  */
        if handler_magic.saves_spell(level, victim, merc.DAM_FIRE):
            dam = 2 * dam // 3
        fight.damage(ch, victim, dam, sn, merc.DAM_FIRE, True)


const.register_spell(
    const.skill_type(
        "heat metal",
        {"mage": 53, "cleric": 16, "thief": 53, "warrior": 23},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_heat_metal,
        merc.TAR_CHAR_OFFENSIVE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(516),
        25,
        18,
        "spell",
        "!Heat Metal!",
        "",
    )
)
