__author__ = "syn"

import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import state_checks
from rom24 import game_utils
from rom24 import instance

# Magic functions
def say_spell(ch, spell):
    syl_dict = {
        "ar": "abra",
        "au": "kada",
        "bless": "fido",
        "blind": "nose",
        "bur": "mosa",
        "cu": "judi",
        "de": "oculo",
        "en": "unso",
        "light": "dies",
        "lo": "hi",
        "mor": "zak",
        "move": "sido",
        "ness": "lacri",
        "ning": "illa",
        "per": "duda",
        "ra": "gru",
        "fresh": "ima",
        "re": "candus",
        "son": "sabru",
        "tect": "infra",
        "tri": "cula",
        "ven": "nofo",
        "a": "a",
        "b": "b",
        "c": "q",
        "d": "e",
        "e": "z",
        "f": "y",
        "g": "o",
        "h": "p",
        "i": "u",
        "j": "y",
        "k": "t",
        "l": "r",
        "m": "w",
        "n": "i",
        "o": "a",
        "p": "s",
        "q": "d",
        "r": "f",
        "s": "g",
        "t": "h",
        "u": "j",
        "v": "z",
        "w": "x",
        "x": "n",
        "y": "l",
        "z": "k",
    }
    incantation = game_utils.mass_replace(spell.name, syl_dict)

    buf = "$n utters the words, '%s'." % incantation
    buf2 = "$n utters the words, '%s'." % spell.name

    for rch_id in ch.in_room.people[:]:
        rch = instance.characters[rch_id]
        send = buf2 if ch.guild == rch.guild else buf
        handler_game.act(send, ch, None, rch, merc.TO_VICT)


def saves_spell(level, victim, dam_type):
    save = 50 + (victim.level - level) * 5 - victim.saving_throw * 2
    if victim.is_affected(merc.AFF_BERSERK):
        save += victim.level // 2

    immunity = victim.check_immune(dam_type)
    if immunity == merc.IS_IMMUNE:
        return True
    elif immunity == merc.IS_RESISTANT:
        save += 2
    elif immunity == merc.IS_VULNERABLE:
        save -= 2

    if not victim.is_npc() and victim.guild.fMana:
        save = 9 * save // 10
    save = max(5, min(save, 95))

    return random.randint(1, 99) < save


def saves_dispel(dis_level, spell_level, duration):
    if duration == -1:
        spell_level += 5
        # very hard to dispel permanent effects */

    save = 50 + (spell_level - dis_level) * 5
    save = max(5, min(save, 95))
    return random.randint(1, 99) < save


def check_dispel(dis_level, victim, skill):
    from rom24.const import skill_table

    if state_checks.is_affected(victim, skill):
        for af in victim.affected[:]:
            if af.type == skill:
                if not saves_dispel(dis_level, af.level, af.duration):
                    victim.affect_strip(skill)
                    if skill.msg_off:
                        victim.send(skill_table[skill.name].msg_off + "\n")
                    return True
                else:
                    af.level -= 1
    return False


target_name = ""
fLogAll = False

# for finding mana costs -- temporary version */
def mana_cost(ch, min_mana, level):
    if ch.level + 2 == level:
        return 1000
    return max(min_mana, (100 // (2 + ch.level - level)))


def find_spell(ch, name):
    # * finds a spell the character can cast if possible */
    from rom24.const import skill_table

    found = None
    if ch.is_npc():
        return state_checks.prefix_lookup(skill_table, name)
    for key, sn in skill_table.items():
        if key.startswith(name.lower()):
            if found == None:
                found = sn
            if ch.level >= sn.skill_level[ch.guild.name] and key in ch.learned:
                return sn
    return found


# Cast spells at targets using a magical object.
def obj_cast_spell(sn, level, ch, victim, obj):
    from rom24 import const
    from rom24 import fight

    target = merc.TARGET_NONE
    vo = None
    if not sn:
        return
    if sn not in const.skill_table or not const.skill_table[sn].spell_fun:
        print("BUG: Obj_cast_spell: bad sn %d." % sn)
        return
    sn = const.skill_table[sn]
    if sn.target == merc.TAR_IGNORE:
        vo = None
    elif sn.target == merc.TAR_CHAR_OFFENSIVE:
        if not victim:
            victim = ch.fighting
        if not victim:
            ch.send("You can't do that.\n")
            return
        if fight.is_safe(ch, victim) and ch != victim:
            ch.send("Something isn't right...\n")
            return
        vo = victim
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_CHAR_DEFENSIVE or sn.target == merc.TAR_CHAR_SELF:
        if not victim:
            victim = ch
        vo = victim
        target = merc.TARGET_CHAR
    elif sn.target == merc.TAR_OBJ_INV:
        if not obj:
            ch.send("You can't do that.\n")
            return
        vo = obj
        target = merc.TARGET_ITEM
    elif sn.target == merc.TAR_OBJ_CHAR_OFF:
        if not victim and not obj:
            if ch.fighting:
                victim = ch.fighting
            else:
                ch.send("You can't do that.\n")
                return
        if victim:
            if fight.is_safe_spell(ch, victim, False) and ch != victim:
                ch.send("Somehting isn't right...\n")
                return
            vo = victim
            target = merc.TARGET_CHAR
        else:
            vo = obj
            target = merc.TARGET_ITEM
    elif sn.target == merc.TAR_OBJ_CHAR_DEF:
        if not victim and not obj:
            vo = ch
            target = merc.TARGET_CHAR
        elif victim:
            vo = victim
            target = merc.TARGET_CHAR
        else:
            vo = obj
            target = merc.TARGET_ITEM
    else:
        print("BUG: Obj_cast_spell: bad target for sn %s." % sn.name)
        return
    target_name = ""
    sn.spell_fun(sn, level, ch, vo, target)
    if (
        (
            sn.target == merc.TAR_CHAR_OFFENSIVE
            or (sn.target == merc.TAR_OBJ_CHAR_OFF and target == merc.TARGET_CHAR)
        )
        and victim != ch
        and victim.master != ch
    ):
        for vch in ch.in_room.people[:]:
            if victim == vch and not victim.fighting:
                fight.check_killer(victim, ch)
                fight.multi_hit(victim, ch, merc.TYPE_UNDEFINED)
