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
from merc import *

def acid_effect(vo, level, dam, target):
    if target == TARGET_ROOM: # nail objects on the floor */
        for obj in vo.contents[:]:
            acid_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_CHAR:  # do the effect on a victim */
        # let's toast some gear */
        for obj in vo.carrying[:]:
            acid_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_OBJ: # toast an object */
        obj = vo
        if IS_OBJ_STAT(obj,ITEM_BURN_PROOF) or IS_OBJ_STAT(obj,ITEM_NOPURGE) or random.randint(0,4) == 0:
            return
        chance = level / 4 + dam / 10
        if chance > 25:
            chance = (chance - 25) / 2 + 25
        if chance > 50:
            chance = (chance - 50) / 2 + 50

        if IS_OBJ_STAT(obj,ITEM_BLESS):
            chance -= 5

        chance -= obj.level * 2

        if obj.item_type == ITEM_CONTAINER \
        or obj.item_type == ITEM_CORPSE_PC \
        or obj.item_type == ITEM_CORPSE_NPC:
            msg = "$p fumes and dissolves."
        elif obj.item_type == ITEM_ARMOR:
            msg = "$p is pitted and etched."
        elif obj.item_type == ITEM_CLOTHING:
            msg = "$p is corroded into scrap."
        elif obj.item_type == ITEM_STAFF \
        or obj.item_type == ITEM_WAND:
            chance -= 10
            msg = "$p corrodes and breaks."
        elif obj.item_type == ITEM_SCROLL:
            chance += 10
            msg = "$p is burned into waste."
        else:
            return

        chance = min(5,max(chance,95))

        if random.randint(1,99) > chance:
            return
        if obj.carried_by != None:
            act(msg,obj.carried_by,obj,None,TO_ALL)
        elif obj.in_room and obj.in_room.people != None:
            act(msg,obj.in_room.people,obj,None,TO_ALL)
        if obj.item_type == ITEM_ARMOR:  # etch it */
            af_found = False
            obj.affect_enchant()
            for paf in obj.affected:
                if paf.location == APPLY_AC:
                    af_found = True
                    paf.type = -1
                    paf.modifier += 1
                    paf.level = max(paf.level,level)
                    break
     
            if not af_found:
                # needs a new affect */
                paf = AFFECT_DATA()
                paf.type = -1
                paf.level = level
                paf.duration = -1
                paf.location = APPLY_AC
                paf.modifier =  1
                paf.bitvector = 0
                obj.affected.append(paf)

            if obj.carried_by and obj.wear_loc != WEAR_NONE:
                obj.carried_by.armor[i] = [ i+1 for i in obj.carried_by.armor ]
                return
        # get rid of the object */
        if obj.contains:  # dump contents */
            for t_obj in obj.contains[:]:
                t_obj.from_obj()
                if obj.in_room :
                    t_obj.to_room(obj.in_room)
                elif obj.carried_by:
                    t_obj.to_room(obj.carried_by.in_room)
                else:
                    t_obj.extract()
                    continue
                acid_effect(t_obj,level/2,dam/2,TARGET_OBJ)
            obj.extract()


def cold_effect( vo, level, dam, target):
    if target == TARGET_ROOM: # nail objects on the floor */
        room = vo
        for obj in room.contents[:]:
            cold_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_CHAR: # whack a character */
        victim = vo
        # chill touch effect */
        if not saves_spell(level/4 + dam / 20, victim, DAM_COLD):
            af = AFFECT_DATA()
            act("$n turns blue and shivers.",victim,None,None,TO_ROOM)
            act("A chill sinks deep into your bones.",victim,None,None,TO_CHAR)
            af.where     = TO_AFFECTS
            af.type      = skill_table["chill touch"]
            af.level     = level
            af.duration  = 6
            af.location  = APPLY_STR
            af.modifier  = -1
            af.bitvector = 0
            victim.affect_join(af)

        # hunger! (warmth sucked out */
        if not IS_NPC(victim):
            gain_condition(victim,COND_HUNGER,dam/20)

        # let's toast some gear */
        for obj in victim.carrying[:]:
            cold_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_OBJ: # toast an object */
        obj = vo
        if IS_OBJ_STAT(obj,ITEM_BURN_PROOF) or IS_OBJ_STAT(obj,ITEM_NOPURGE) or random.randint(0,4) == 0:
            return
        chance = level / 4 + dam / 10
        if chance > 25:
            chance = (chance - 25) / 2 + 25
        if chance > 50:
            chance = (chance - 50) / 2 + 50

        if IS_OBJ_STAT(obj,ITEM_BLESS):
            chance -= 5

        chance -= obj.level * 2
        msg = ""
        if obj.item_type == ITEM_POTION:
            msg = "$p freezes and shatters!"
            chance += 25
        elif obj.item_type == ITEM_DRINK_CON:
            msg = "$p freezes and shatters!"
            chance += 5
        else:
            return

        chance = min(5,max(chance,95))

        if random.randint(1,99) > chance:
            return

        if obj.carried_by != None:
            act(msg,obj.carried_by,obj,None,TO_ALL)
        elif obj.in_room and obj.in_room.people:
            act(msg,obj.in_room.people,obj,None,TO_ALL)
        obj.extract()
        return

def fire_effect(vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        room = vo
        for obj in room.contents[:]:
            fire_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_CHAR:   # do the effect on a victim */
        victim = vo
        # chance of blindness */
        if not IS_AFFECTED(victim,AFF_BLIND) and not saves_spell(level / 4 + dam / 20, victim,DAM_FIRE):
            act("$n is blinded by smoke!",victim,None,None,TO_ROOM)
            act("Your eyes tear up from smoke...you can't see a thing!", victim,None,None,TO_CHAR)
            af = AFFECT_DATA()
            af.where        = TO_AFFECTS
            af.type         = skill_table["fire breath"]
            af.level        = level
            af.duration     = random.randint(0,level/10)
            af.location     = APPLY_HITROLL
            af.modifier     = -4
            af.bitvector    = AFF_BLIND
            victim.affect_add(af)
        # getting thirsty */
        if not IS_NPC(victim):
            gain_condition(victim,COND_THIRST,dam/20)

        # let's toast some gear! */
        for obj in victim.carrying[:]:
            fire_effect(obj,level,dam,TARGET_OBJ)
        return
    
    if target == TARGET_OBJ:  # toast an object */
        obj = vo

        if IS_OBJ_STAT(obj,ITEM_BURN_PROOF) or IS_OBJ_STAT(obj,ITEM_NOPURGE) or random.randint(0,4) == 0:
            return
 
        chance = level / 4 + dam / 10
 
        if chance > 25:
            chance = (chance - 25) / 2 + 25
        if chance > 50:
            chance = (chance - 50) / 2 + 50

        if IS_OBJ_STAT(obj,ITEM_BLESS):
            chance -= 5
        chance -= obj.level * 2

        if obj.item_type == ITEM_CONTAINER:
            msg = "$p ignites and burns!"
        elif obj.item_type == ITEM_POTION:
            chance += 25
            msg = "$p bubbles and boils!"
        elif obj.item_type == ITEM_SCROLL:
            chance += 50
            msg = "$p crackles and burns!"
        elif obj.item_type == ITEM_STAFF:
            chance += 10
            msg = "$p smokes and chars!"
        elif obj.item_type == ITEM_WAND:
            msg = "$p sparks and sputters!"
        elif obj.item_type == ITEM_FOOD:
            msg = "$p blackens and crisps!"
        elif obj.item_type == ITEM_PILL:
            msg = "$p melts and drips!"
        else:
            return
        chance = min(5,max(chance,95))

        if random.randint(1,99) > chance:
            return
 
        if obj.carried_by:
            act( msg, obj.carried_by, obj, None, TO_ALL )
        elif obj.in_room and obj.in_room.people:
            act(msg,obj.in_room.people,obj,None,TO_ALL)

        if obj.contains:
            # dump the contents */
            for t_obj in obj.contains[:]:
                t_obj.from_obj()
                if obj.in_room:
                    t_obj.to_room(obj.in_room)
                elif obj.carried_by:
                    t_obj.to_room(obj.carried_by.in_room)
                else:
                    t_obj.extract()
                    continue
                fire_effect(t_obj,level/2,dam/2,TARGET_OBJ)

        obj.extract()
        return

def poison_effect( vo, level, dam, target):
    if target == TARGET_ROOM:  # nail objects on the floor */
        room = vo
        for obj in room.contents[:]:
            poison_effect(obj,level,dam,TARGET_OBJ)
        return

    if target == TARGET_CHAR:   # do the effect on a victim */
        victim = vo
        # chance of poisoning */
        if not saves_spell(level / 4 + dam / 20,victim,DAM_POISON):
            af = AFFECT_DATA()

            victim.send("You feel poison coursing through your veins.\n\r")
            act("$n looks very ill.",victim,None,None,TO_ROOM)

            af.where     = TO_AFFECTS
            af.type      = gsn_poison
            af.level     = level
            af.duration  = level / 2
            af.location  = APPLY_STR
            af.modifier  = -1
            af.bitvector = AFF_POISON
            victim.affect_join(af)
    # equipment */
        for obj in victim.carrying[:]:
            poison_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_OBJ:  # do some poisoning */
        obj = vo
        if IS_OBJ_STAT(obj,ITEM_BURN_PROOF) or IS_OBJ_STAT(obj,ITEM_BLESS) or random.randint(0,4) == 0:
            return

        chance = level / 4 + dam / 10
        if chance > 25:
            chance = (chance - 25) / 2 + 25
        if chance > 50:
            chance = (chance - 50) / 2 + 50

        chance -= obj.level * 2


        if obj.item_type ==  ITEM_FOOD:
            pass
        if obj.item_type == ITEM_DRINK_CON:
            if obj.value[0] == obj.value[1]:
                return
        else:
            return
        chance = min(5,max(chance,95))

        if random.randint(1,99) > chance:
            return

        obj.value[3] = 1
        return

def shock_effect( vo, level, dam, target):
    if target == TARGET_ROOM:
        room = vo
        for obj in room.contents[:]:
            shock_effect(obj,level,dam,TARGET_OBJ)
        return

    if target == TARGET_CHAR:
        victim = vo
        # daze and confused? */
        if not saves_spell(level/4 + dam/20,victim,DAM_LIGHTNING):
            victim.send("Your muscles stop responding.\n\r")
            DAZE_STATE(victim,max(12,level/4 + dam/20))
        # toast some gear */
        for obj in victim.carrying[:]:
            shock_effect(obj,level,dam,TARGET_OBJ)
        return
    if target == TARGET_OBJ:
        obj = vo
        if IS_OBJ_STAT(obj,ITEM_BURN_PROOF) or IS_OBJ_STAT(obj,ITEM_NOPURGE) or random.randint(0,4) == 0:
            return

        chance = level / 4 + dam / 10

        if chance > 25:
            chance = (chance - 25) / 2 + 25
        if chance > 50:
            chance = (chance - 50) /2 + 50

        if IS_OBJ_STAT(obj,ITEM_BLESS):
            chance -= 5

        chance -= obj.level * 2

        if obj.item_type == ITEM_WAND \
        or obj.item_type == ITEM_STAFF:
            chance += 10
            msg = "$p overloads and explodes!"
        elif obj.item_type == ITEM_JEWELRY:
            chance -= 10
            msg = "$p is fused into a worthless lump."
        else:
            return
        chance = min(5,max(chance,95))

        if random.randint(1,99) > chance:
            return

        if obj.carried_by:
            act(msg,obj.carried_by,obj,None,TO_ALL)
        elif obj.in_room and obj.in_room.people:
            act(msg,obj.in_room.people,obj,None,TO_ALL)

        obj.extract()
        return
