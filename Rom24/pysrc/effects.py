"""
/***************************************************************************
 *  Original Diku Mud copyright (C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright (C) 1992, 1993 by Michael          *
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

/***************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/ 
 ************/
"""
import random

from merc import *
import merc
from update import gain_condition
import handler_game
import handler_magic
import state_checks
import const


def acid_effect(vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        for item_id in vo.inventory[:]:
            item = merc.items[item_id]
            acid_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_CHAR:  # do the effect on a victim */
        # let's toast some gear */
        for item_id in vo.inventory[:]:
            item = merc.items[item_id]
            acid_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_ITEM:  # toast an object */
        item = vo
        if item.flags.burn_proof or item.flags.no_purge or random.randint(0, 4) == 0:
            return
        chance = level / 4 + dam / 10
        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50

        if item.flags.bless:
            chance -= 5

        chance -= item.level * 2

        if item.item_type == ITEM_CONTAINER or item.item_type == ITEM_CORPSE_PC or item.item_type == ITEM_CORPSE_NPC:
            msg = "$p fumes and dissolves."
        elif item.item_type == ITEM_ARMOR:
            msg = "$p is pitted and etched."
        elif item.item_type == ITEM_CLOTHING:
            msg = "$p is corroded into scrap."
        elif item.item_type == ITEM_STAFF or item.item_type == ITEM_WAND:
            chance -= 10
            msg = "$p corrodes and breaks."
        elif item.item_type == ITEM_SCROLL:
            chance += 10
            msg = "$p is burned into waste."
        else:
            return

        chance = max(5, min(chance, 95))

        if random.randint(1, 99) > chance:
            return
        if item.in_living:
            handler_game.act(msg, item.in_living, item, None, TO_ALL)
        elif item.in_room and item.in_room.people is not None:
            handler_game.act(msg, item.in_room.people, item, None, TO_ALL)
        if item.item_type == ITEM_ARMOR:  # etch it */
            af_found = False
            item.affect_enchant()
            for paf in item.affected:
                if paf.location == APPLY_AC:
                    af_found = True
                    paf.type = -1
                    paf.modifier += 1
                    paf.level = max(paf.level, level)
                    break

            if not af_found:
                # needs a new affect */
                paf = handler_game.AFFECT_DATA()
                paf.type = -1
                paf.level = level
                paf.duration = -1
                paf.location = APPLY_AC
                paf.modifier = 1
                paf.bitvector = 0
                item.affected.append(paf)

            if item.in_living and item.equipped_to:
                for i in range(4):
                    item.in_living.armor[i] = [i + 1 for i in item.in_living.armor]
                return
        # get rid of the object */
        if item.inventory:  # dump contents */
            for t_item_id in item.inventory[:]:
                t_item = merc.items[t_item_id]
                item.get(t_item)
                if item.in_room:
                    item.in_room.put(t_item)
                elif item.in_living:
                    item.in_living.in_room.put(t_item)
                else:
                    t_item.extract()
                    continue
                acid_effect(t_item, level // 2, dam // 2, TARGET_ITEM)
            item.extract()


def cold_effect(vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        room = vo
        for item_id in room.inventory[:]:
            item = merc.items[item_id]
            cold_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_CHAR:  # whack a character */
        victim = vo
        # chill touch effect */
        if not handler_magic.saves_spell(level / 4 + dam / 20, victim, DAM_COLD):
            af = handler_game.AFFECT_DATA()
            handler_game.act("$n turns blue and shivers.", victim, None, None, TO_ROOM)
            handler_game.act("A chill sinks deep into your bones.", victim, None, None, TO_CHAR)
            af.where = TO_AFFECTS
            af.type = 'chill touch'
            af.level = level
            af.duration = 6
            af.location = APPLY_STR
            af.modifier = -1
            af.bitvector = 0
            victim.affect_join(af)

        # hunger! (warmth sucked out */
        if not victim.is_npc():
            gain_condition(victim, COND_HUNGER, dam / 20)

        # let's toast some gear */
        for item_id in victim.inventory[:]:
            item = merc.items[item_id]
            cold_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_ITEM:  # toast an object */
        item = vo
        if item.flags.burn_proof \
                or item.flags.no_purge \
                or random.randint(0, 4) == 0:
            return
        chance = level // 4 + dam // 10
        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50

        if item.flags.bless:
            chance -= 5

        chance -= item.level * 2
        if item.item_type == ITEM_POTION:
            msg = "$p freezes and shatters!"
            chance += 25
        elif item.item_type == ITEM_DRINK_CON:
            msg = "$p freezes and shatters!"
            chance += 5
        else:
            return

        chance = max(5, min(chance, 95))

        if random.randint(1, 99) > chance:
            return

        if item.in_living is not None:
            handler_game.act(msg, item.in_living, item, None, TO_ALL)
        elif item.in_room and item.in_room.people:
            handler_game.act(msg, item.in_room.people, item, None, TO_ALL)
        item.extract()
        return


def fire_effect(vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        room = vo
        for item_id in room.inventory[:]:
            item = merc.items[item_id]
            fire_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_CHAR:  # do the effect on a victim */
        victim = vo
        # chance of blindness */
        if not victim.is_affected(AFF_BLIND) and not handler_magic.saves_spell(level / 4 + dam / 20, victim, DAM_FIRE):
            handler_game.act("$n is blinded by smoke!", victim, None, None, TO_ROOM)
            handler_game.act("Your eyes tear up from smoke...you can't see a thing!", victim, None, None, TO_CHAR)
            af = handler_game.AFFECT_DATA()
            af.where = TO_AFFECTS
            af.type = 'fire breath'
            af.level = level
            af.duration = random.randint(0, level / 10)
            af.location = APPLY_HITROLL
            af.modifier = -4
            af.bitvector = AFF_BLIND
            victim.affect_add(af)
        # getting thirsty */
        if not victim.is_npc():
            gain_condition(victim, COND_THIRST, dam / 20)

        # let's toast some gear! */
        for item_id in victim.inventory[:]:
            item = merc.items[item_id]
            fire_effect(item, level, dam, TARGET_ITEM)

    if target == TARGET_ITEM:  # toast an object */
        item = vo

        if item.flags.burn_proof or item.flags.no_purge or random.randint(0, 4) == 0:
            return

        chance = level // 4 + dam // 10

        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50

        if item.flags.bless:
            chance -= 5
        chance -= item.level * 2

        if item.item_type == ITEM_CONTAINER:
            msg = "$p ignites and burns!"
        elif item.item_type == ITEM_POTION:
            chance += 25
            msg = "$p bubbles and boils!"
        elif item.item_type == ITEM_SCROLL:
            chance += 50
            msg = "$p crackles and burns!"
        elif item.item_type == ITEM_STAFF:
            chance += 10
            msg = "$p smokes and chars!"
        elif item.item_type == ITEM_WAND:
            msg = "$p sparks and sputters!"
        elif item.item_type == ITEM_FOOD:
            msg = "$p blackens and crisps!"
        elif item.item_type == ITEM_PILL:
            msg = "$p melts and drips!"
        else:
            return
        chance = max(5, min(chance, 95))

        if random.randint(1, 99) > chance:
            return

        if item.in_living:
            handler_game.act(msg, item.in_living, item, None, TO_ALL)
        elif item.in_room and item.in_room.people:
            handler_game.act(msg, item.in_room.people, item, None, TO_ALL)

        if item.inventory:
            # dump the contents */
            for t_item_id in item.inventory[:]:
                t_item = merc.items[t_item_id]
                item.get(t_item)
                if item.in_room:
                    item.in_room.put(t_item)
                elif item.in_living:
                    item.in_living.in_room.put(t_item)
                else:
                    t_item.extract()
                    continue
                fire_effect(t_item, level / 2, dam / 2, TARGET_ITEM)
        item.extract()
        return


def poison_effect(vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        room = vo
        for item_id in room.inventory[:]:
            item = merc.items[item_id]
            poison_effect(item, level, dam, TARGET_ITEM)
        return

    if target == TARGET_CHAR:  # do the effect on a victim */
        victim = vo
        # chance of poisoning */
        if not handler_magic.saves_spell(level // 4 + dam // 20, victim, DAM_POISON):
            af = handler_game.AFFECT_DATA()

            victim.send("You feel poison coursing through your veins.\n\r")
            handler_game.act("$n looks very ill.", victim, None, None, TO_ROOM)

            af.where = TO_AFFECTS
            af.type = 'poison'
            af.level = level
            af.duration = level // 2
            af.location = APPLY_STR
            af.modifier = -1
            af.bitvector = AFF_POISON
            victim.affect_join(af)
            # equipment */
        for item_id in victim.inventory[:]:
            item = merc.items[item_id]
            poison_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_ITEM:  # do some poisoning */
        item = vo
        if item.flags.burn_proof or item.flags.bless or random.randint(0, 4) == 0:
            return

        chance = level // 4 + dam // 10
        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50

        chance -= item.level * 2

        if item.item_type == ITEM_FOOD:
            pass
        if item.item_type == ITEM_DRINK_CON:
            if item.value[0] == item.value[1]:
                return
        else:
            return
        chance = max(5, min(chance, 95))

        if random.randint(1, 99) > chance:
            return

        item.value[3] = 1
        return


def shock_effect(vo, level, dam, target):
    if target == TARGET_ROOM:
        room = vo
        for item_id in room.inventory[:]:
            item = merc.items[item_id]
            shock_effect(item, level, dam, TARGET_ITEM)
        return

    if target == TARGET_CHAR:
        victim = vo
        # daze and confused? */
        if not handler_magic.saves_spell(level // 4 + dam // 20, victim, DAM_LIGHTNING):
            victim.send("Your muscles stop responding.\n\r")
            state_checks.DAZE_STATE(victim, max(12, level // 4 + dam / 20))
        # toast some gear */
        for item_id in victim.inventory[:]:
            item = merc.items[item_id]
            shock_effect(item, level, dam, TARGET_ITEM)
        return
    if target == TARGET_ITEM:
        item = vo
        if item.flags.burn_proof or item.flags.no_purge or random.randint(0, 4) == 0:
            return

        chance = level // 4 + dam // 10

        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50

        if item.flags.bless:
            chance -= 5

        chance -= item.level * 2

        if item.item_type == ITEM_WAND \
                or item.item_type == ITEM_STAFF:
            chance += 10
            msg = "$p overloads and explodes!"
        elif item.item_type == ITEM_JEWELRY:
            chance -= 10
            msg = "$p is fused into a worthless lump."
        else:
            return
        chance = max(5, min(chance, 95))

        if random.randint(1, 99) > chance:
            return

        if item.in_living:
            handler_game.act(msg, item.in_living, item, None, TO_ALL)
        elif item.in_room and item.in_room.people:
            handler_game.act(msg, item.in_room.people, item, None, TO_ALL)
        item.extract()
        return
