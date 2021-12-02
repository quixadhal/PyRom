import random
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import handler_magic
from rom24 import state_checks
from rom24 import merc
from rom24 import interp
from rom24 import fight
from rom24 import instance


def do_cast(ch, argument):
    # Switched NPC's can cast spells, but others can't.
    if ch.is_npc() and not ch.desc:
        return

    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    handler_magic.target_name = arg2

    if not arg1:
        ch.send("Cast which what where?\n")
        return
    sn = handler_magic.find_spell(ch, arg1)
    if (
        not sn
        or sn.spell_fun is None
        or (
            not ch.is_npc()
            and (
                ch.level < sn.skill_level[ch.guild.name]
                or ch.learned.get(sn.name, 0) == 0
            )
        )
    ):
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
            victim = ch.get_char_room(arg2)
            if not victim:
                ch.send("They aren't here.\n")
                return
            # if ch == victim:
            # ch.send("You can't do that to yourself.\n")
            # return
        if not ch.is_npc():
            if fight.is_safe(ch, victim) and victim != ch:
                ch.send("Not on that target.\n")
                return

            fight.check_killer(ch, victim)

        if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
            ch.send("You can't do that on your own follower.\n")
            return
        vo = victim
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_CHAR_DEFENSIVE:
        if not arg2:
            victim = ch
        else:
            victim = ch.get_char_room(handler_magic.target_name)
        if not victim:
            ch.send("They aren't here.\n")
            return
        vo = victim
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_CHAR_SELF:
        if arg2 and handler_magic.target_name not in ch.name.lower():
            ch.send("You can't cast this spell on another.\n")
            return

        vo = ch
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_OBJ_INV:
        if not arg2:
            ch.send("What should the spell be cast upon?\n")
            return
        obj = ch.get_item_carry(handler_magic.target_name, ch)
        if not obj:
            ch.send("You are not carrying that.\n")
            return
        vo = obj
        target = merc.TARGET_ITEM
    elif sn.target == merc.TAR_OBJ_CHAR_OFF:
        if not arg2:
            victim = ch.fighting
            if not victim:
                ch.send("Cast the spell on whom or what?\n")
                return
            target = merc.TARGET_CHAR
        else:
            victim = ch.get_char_room(handler_magic.target_name)
            obj = ch.get_item_here(handler_magic.target_name)
            if victim:
                target = merc.TARGET_CHAR
                # check the sanity of the attack
                if fight.is_safe_spell(ch, victim, False) and victim != ch:
                    ch.send("Not on that target.\n")
                    return
                if ch.is_affected(merc.AFF_CHARM) and ch.master == victim:
                    ch.send("You can't do that on your own follower.\n")
                    return
                if not ch.is_npc():
                    fight.check_killer(ch, victim)
                vo = victim
            elif obj:
                vo = obj
                target = merc.TARGET_ITEM
            else:
                ch.send("You don't see that here.\n")
                return
    elif sn.target == merc.TAR_OBJ_CHAR_DEF:
        if not arg2:
            vo = ch
            target = merc.TARGET_CHAR
        else:
            victim = ch.get_char_room(handler_magic.target_name)
            obj = ch.get_item_carry(handler_magic.target_name, ch)
            if not victim:
                vo = victim
                target = merc.TARGET_CHAR
            elif not obj:
                vo = obj
                target = merc.TARGET_ITEM
            else:
                ch.send("You don't see that here.\n")
                return
    else:
        logging.error("BUG: Do_cast: bad target for sn %s.", sn)
        return

    if not ch.is_npc() and ch.mana < mana:
        ch.send("You don't have enough mana.\n")
        return

    if sn.name != "ventriloquate":
        handler_magic.say_spell(ch, sn)
    state_checks.WAIT_STATE(ch, sn.beats)

    if random.randint(1, 99) > ch.get_skill(sn.name):
        ch.send("You lost your concentration.\n")
        if ch.is_pc:
            ch.check_improve(sn, False, 1)
        ch.mana -= mana // 2
    else:
        ch.mana -= mana
        if ch.is_npc() or ch.guild.fMana:
            # class has spells
            sn.spell_fun(sn, ch.level, ch, vo, target)
        else:
            sn.spell_fun(sn, 3 * ch.level // 4, ch, vo, target)
            if ch.is_pc:
                ch.check_improve(sn, True, 1)

    if (
        (
            sn.target == merc.TAR_CHAR_OFFENSIVE
            or (sn.target == merc.TAR_OBJ_CHAR_OFF and target == merc.TARGET_CHAR)
        )
        and victim != ch
        and victim.master != ch
    ):
        for vch_id in ch.in_room.people[:]:
            vch = instance.characters[vch_id]
            if victim == vch and not victim.fighting:
                fight.check_killer(victim, ch)
                fight.multi_hit(victim, ch, merc.TYPE_UNDEFINED)
                break
    return


interp.register_command(
    interp.cmd_type("cast", do_cast, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1)
)
