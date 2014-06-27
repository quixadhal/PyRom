import logging

logger = logging.getLogger()

import random
import merc
import interp
import fight
import skills


def do_cast(ch, argument):
    # Switched NPC's can cast spells, but others can't.
    if merc.IS_NPC(ch) and not ch.desc:
        return

    merc.target_name, arg1 = merc.read_word(argument)
    holder, arg2 = merc.read_word(merc.target_name)

    if not arg1:
        ch.send("Cast which what where?\n")
        return
    sn = merc.find_spell(ch, arg1)
    if not sn or sn.spell_fun == None \
            or (not merc.IS_NPC(ch)
                and (ch.level < sn.skill_level[ch.guild.name]
                     or ch.pcdata.learned[sn.name] == 0)):
        ch.send("You don't know any spells of that name.\n")
        return
    if ch.position < sn.minimum_position:
        ch.send("You can't concentrate enough.\n")
        return
    if ch.level + 2 == sn.skill_level[ch.guild.name]:
        mana = 50
    else:
        mana = max(sn.min_mana, 100 // (2 + ch.level - sn.skill_level[ch.guild.name]))
    # Locate targets.
    victim = None
    obj = None
    vo = None
    target = merc.TARGET_NONE
    if sn.target == merc.TAR_IGNORE:
        pass
    elif sn.target == merc.TAR_CHAR_OFFENSIVE:
        if not arg2:
            victim = ch.fighting
            if not victim:
                ch.send("Cast the spell on whom?\n")
                return
        else:
            victim = ch.get_char_room(merc.target_name)
            if not victim:
                ch.send("They aren't here.\n")
                return
            # if ch == victim:
            # ch.send("You can't do that to yourself.\n")
            # return
            if not merc.IS_NPC(ch):
                if fight.is_safe(ch, victim) and victim != ch:
                    ch.send("Not on that target.\n")
                    return

                fight.check_killer(ch, victim)

            if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
                ch.send("You can't do that on your own follower.\n")
                return
            vo = victim
            target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_CHAR_DEFENSIVE:
        if not arg2:
            victim = ch
        else:
            victim = ch.get_char_room(merc.target_name)
        if not victim:
            ch.send("They aren't here.\n")
            return
        vo = victim
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_CHAR_SELF:
        if arg2 and merc.target_name not in ch.name.lower():
            ch.send("You can! cast this spell on a!her.\n")
            return

        vo = ch
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_OBJ_INV:
        if not arg2:
            ch.send("What should the spell be cast upon?\n")
            return
        obj = ch.get_obj_carry(merc.target_name, ch)
        if not obj:
            ch.send("You are not carrying that.\n")
            return
        vo = obj
        target = merc.TARGET_OBJ
    elif sn.target == merc.TAR_OBJ_CHAR_OFF:
        if not arg2:
            victim = ch.fighting
            if not victim:
                ch.send("Cast the spell on whom or what?\n")
                return
            target = merc.TARGET_CHAR
        else:
            victim = ch.get_char_room(merc.target_name)
            obj = ch.get_obj_here(merc.target_name)
            if victim:
                target = merc.TARGET_CHAR
                # check the sanity of the attack
                if fight.is_safe_spell(ch, victim, False) and victim != ch:
                    ch.send("Not on that target.\n")
                    return
                if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
                    ch.send("You can't do that on your own follower.\n")
                    return
                if not IS_NPC(ch):
                    fight.check_killer(ch, victim)
                vo = victim
            elif obj:
                vo = obj
                target = merc.TARGET_OBJ
            else:
                ch.send("You don't see that here.\n")
                return
    elif sn.target == merc.TAR_OBJ_CHAR_DEF:
        if not arg2:
            vo = ch
            target = merc.TARGET_CHAR
        else:
            victim = ch.get_char_room(merc.target_name)
            obj = ch.get_obj_carry(merc.target_name, ch)
            if not victim:
                vo = victim
                target = merc.TARGET_CHAR
            elif not obj:
                vo = obj
                target = merc.TARGET_OBJ
            else:
                ch.send("You don't see that here.\n")
                return
    else:
        logging.error("BUG: Do_cast: bad target for sn %s.", sn)
        return

    if not merc.IS_NPC(ch) and ch.mana < mana:
        ch.send("You don't have enough mana.\n")
        return

    if sn.name != "ventriloquate":
        merc.say_spell(ch, sn)
    merc.WAIT_STATE(ch, sn.beats)

    if random.randint(1, 99) > ch.get_skill(sn.name):
        ch.send("You lost your concentration.\n")
        skills.check_improve(ch, sn, False, 1)
        ch.mana -= mana // 2
    else:
        ch.mana -= mana
        if merc.IS_NPC(ch) or ch.guild.fMana:
            # class has spells
            sn.spell_fun(sn, ch.level, ch, vo, target)
        else:
            sn.spell_fun(sn, 3 * ch.level // 4, ch, vo, target)
            skills.check_improve(ch, sn, True, 1)

    if (sn.target == merc.TAR_CHAR_OFFENSIVE or (sn.target == merc.TAR_OBJ_CHAR_OFF and target == merc.TARGET_CHAR)) \
            and victim != ch and victim.master != ch:
        for vch in ch.in_room.people[:]:
            if victim == vch and not victim.fighting:
                fight.check_killer(victim, ch)
                fight.multi_hit(victim, ch, merc.TYPE_UNDEFINED)
                break
    return


interp.register_command(interp.cmd_type('cast', do_cast, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1))
