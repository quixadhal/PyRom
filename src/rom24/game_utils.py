__author__ = "syn"

import os
import re
import time
import collections
import random
import logging
from typing import *

logger = logging.getLogger(__name__)

from rom24 import settings
from rom24 import merc
from rom24 import instance


# def find_instance_file(
#     instance_id: int = None, from_char_dir: str = None, from_world: bool = False
# ):
#     if not instance_id:
#         return None
#     if from_char_dir:
#         pathname = os.path.join(
#             settings.PLAYER_DIR,
#             from_char_dir[0].capitalize(),
#             from_char_dir.capitalize(),
#         )
#         for start, directories, file in os.walk(pathname):
#             if str(instance_id) in file:
#                 return os.path.join(start, directories, file)
#         return None
#     if from_world:
#         pass


def read_forward(pstr, jump=1):
    return pstr[jump:]


def read_letter(pstr):
    pstr = pstr.lstrip()
    return pstr[1:], pstr[:1]


def old_read_word(pstr, lower=True):
    if not pstr:
        return "", ""
    pstr = pstr.lstrip()
    locate = len(pstr)
    unmatch = False
    if locate == 0:
        return "", ""
    if pstr[0] == "'":
        locate = pstr.find("'", 1) + 1
        if locate == 0:
            locate = len(pstr)
            unmatch = True
    elif pstr[0] == '"':
        locate = pstr.find('"', 1) + 1
        if locate == 0:
            locate = len(pstr)
            unmatch = True
    else:
        for i, c in enumerate(pstr):
            if c.isspace():
                locate = i
                break

    word = pstr[:locate]
    strip = len(word)
    if not word:
        return pstr, word
    if word[0] in ['"', "'"]:
        word = word[1:]
        if not unmatch:
            word = word[:-1]
    if lower:
        word = word.lower()

    return pstr.lstrip()[strip:], word.strip()


def read_word(pstr, to_lower=True):
    if not pstr:
        return "", ""

    start = None
    end = None
    if to_lower:
        pstr = pstr.lower()
    i = -1
    for c in pstr:
        i += 1
        if c == "'" and start is None:
            start = i + 1
            quote = pstr.find("'", i + 1)
            if quote > -1:
                end = quote
            else:
                end = len(pstr)
            return pstr[end + 1 :], pstr[start:end]
        elif c == '"' and start is None:
            start = i + 1
            quote = pstr.find('"', i + 1)
            if quote > -1:
                end = quote
            else:
                end = len(pstr)
            return pstr[end + 1 :], pstr[start:end]
        elif c.isspace():
            if start is not None:
                end = i
                break
        else:
            if start is None:
                start = i

    if not end:
        end = len(pstr)
    return pstr[end:], pstr[start:end]


def read_int(pstr):
    if not pstr:
        return None, None
    pstr = pstr.lstrip()
    number = ""
    negative = False
    for c in pstr:
        if c == "-":
            negative = True
        elif c.isdigit():
            number += c
        else:
            break

    pstr = pstr.lstrip()
    if not negative:
        pstr = pstr[len(number) :]
        return pstr, int(number)
    else:
        pstr = pstr[len(number) + 1 :]
        number = int(number) * -1
        return pstr, number


def read_string(pstr):
    if not pstr:
        return None, None
    end = pstr.find("~")
    word = pstr[0:end]
    pstr = pstr[end + 1 :]
    return pstr, word.strip()


def read_flags(pstr):
    if not pstr:
        return None, None
    pstr, w = read_word(pstr, False)
    if w == "0" or w == 0:
        return pstr, 0
    if w.isdigit():
        return pstr, int(w)
    flags = 0

    for c in w:
        flag = 0
        if "A" <= c <= "Z":
            flag = merc.A
            while c != "A":
                flag *= 2
                c = chr(ord(c) - 1)

        elif "a" <= c <= "z":
            flag = merc.aa
            while c != "a":
                flag *= 2
                c = chr(ord(c) - 1)

        flags += flag
    return pstr, flags


def read_equipment_flags(item, pstr):
    ret_set = {""}
    if not pstr:
        return None, None
    pstr, w = read_word(pstr, False)
    if w == "0" or w == 0:
        return pstr, ret_set
    if w.isdigit():
        return pstr, ret_set

    for l in w:
        if l.isupper():
            ret_set.add(merc.rom_wear_flag_map[l])
        else:
            l.upper()
            ret_set.add(merc.rom_wear_flag_map[l])

    x = [item.equips_to[str(location)] for location in ret_set if location]

    return pstr, ret_set


def item_bitvector_flag_str(bits: int, in_type="extra flags"):
    if not bits or not in_type:
        return None
    if bits == 0:
        return None
    if "wear flags" in in_type:
        if bits & merc.ITEM_TAKE:
            return "take"
        elif bits & merc.ITEM_WEAR_FINGER:
            return "left_finger, right_finger"
        elif bits & merc.ITEM_WEAR_NECK:
            return "neck, collar"
        elif bits & merc.ITEM_WEAR_BODY:
            return "body"
        elif bits & merc.ITEM_WEAR_HEAD:
            return "head"
        elif bits & merc.ITEM_WEAR_LEGS:
            return "legs"
        elif bits & merc.ITEM_WEAR_FEET:
            return "feet"
        elif bits & merc.ITEM_WEAR_HANDS:
            return "hands"
        elif bits & merc.ITEM_WEAR_ARMS:
            return "arms"
        elif bits & merc.ITEM_WEAR_SHIELD:
            return "off_hand"
        elif bits & merc.ITEM_WEAR_ABOUT:
            return "about_body"
        elif bits & merc.ITEM_WEAR_WAIST:
            return "waist"
        elif bits & merc.ITEM_WEAR_WRIST:
            return "left_wrist, right_wrist"
        elif bits & merc.ITEM_WIELD:
            return "main_hand"
        elif bits & merc.ITEM_HOLD:
            return "held"
        elif bits & merc.ITEM_NO_SAC:
            return "no_sac"
        elif bits & merc.ITEM_WEAR_FLOAT:
            return "float"
        else:
            return None
    if "extra flags" in in_type:
        if bits & merc.ITEM_GLOW:
            return "glow"
        elif bits & merc.ITEM_HUM:
            return "hum"
        elif bits & merc.ITEM_DARK:
            return "dark"
        elif bits & merc.ITEM_LOCK:
            return "lock"
        elif bits & merc.ITEM_EVIL:
            return "evil"
        elif bits & merc.ITEM_INVIS:
            return "invis"
        elif bits & merc.ITEM_MAGIC:
            return "magic"
        elif bits & merc.ITEM_NODROP:
            return "no_drop"
        elif bits & merc.ITEM_BLESS:
            return "bless"
        elif bits & merc.ITEM_ANTI_GOOD:
            return "anti_good"
        elif bits & merc.ITEM_ANTI_EVIL:
            return "anti_evil"
        elif bits & merc.ITEM_ANTI_NEUTRAL:
            return "anti_neutral"
        elif bits & merc.ITEM_NOREMOVE:
            return "no_remove"
        elif bits & merc.ITEM_INVENTORY:
            return "inventory"
        elif bits & merc.ITEM_NOPURGE:
            return "no_purge"
        elif bits & merc.ITEM_ROT_DEATH:
            return "rot_death"
        elif bits & merc.ITEM_VIS_DEATH:
            return "vis_death"
        elif bits & merc.ITEM_NONMETAL:
            return "non_metal"
        elif bits & merc.ITEM_NOLOCATE:
            return "no_locate"
        elif bits & merc.ITEM_MELT_DROP:
            return "melt_drop"
        elif bits & merc.ITEM_HAD_TIMER:
            return "had_timer"
        elif bits & merc.ITEM_SELL_EXTRACT:
            return "sell_extract"
        elif bits & merc.ITEM_BURN_PROOF:
            return "burn_proof"
        elif bits & merc.ITEM_NOUNCURSE:
            return "no_uncurse"
        else:
            return None
    if "weapon flags" in in_type:
        if bits & merc.WEAPON_FLAMING:
            return "flaming"
        elif bits & merc.WEAPON_FROST:
            return "frost"
        elif bits & merc.WEAPON_VAMPIRIC:
            return "vampiric"
        elif bits & merc.WEAPON_SHARP:
            return "sharp"
        elif bits & merc.WEAPON_VORPAL:
            return "vorpal"
        elif bits & merc.WEAPON_TWO_HANDS:
            return "two_handed"
        elif bits & merc.WEAPON_SHOCKING:
            return "shocking"
        elif bits & merc.WEAPON_POISON:
            return "poison"
        else:
            return None


def item_flags_from_bits(bits: int, out_data: Any, in_type="wear flags"):
    if not out_data or not bits or not in_type:
        return None
    if bits == 0:
        return None
    if "wear flags" in in_type:
        if bits & merc.ITEM_TAKE:
            out_data.attributes.update({"take"})
        if bits & merc.ITEM_WEAR_FINGER:
            out_data.slots.update({"left_finger", "right_finger"})
        if bits & merc.ITEM_WEAR_NECK:
            out_data.slots.update({"neck", "collar"})
        if bits & merc.ITEM_WEAR_BODY:
            out_data.slots.update({"body"})
        if bits & merc.ITEM_WEAR_HEAD:
            out_data.slots.update({"head"})
        if bits & merc.ITEM_WEAR_LEGS:
            out_data.slots.update({"legs"})
        if bits & merc.ITEM_WEAR_FEET:
            out_data.slots.update({"feet"})
        if bits & merc.ITEM_WEAR_HANDS:
            out_data.slots.update({"hands"})
        if bits & merc.ITEM_WEAR_ARMS:
            out_data.slots.update({"arms"})
        if bits & merc.ITEM_WEAR_SHIELD:
            out_data.slots.update({"off_hand"})
        if bits & merc.ITEM_WEAR_ABOUT:
            out_data.slots.update({"about_body"})
        if bits & merc.ITEM_WEAR_WAIST:
            out_data.slots.update({"waist"})
        if bits & merc.ITEM_WEAR_WRIST:
            out_data.slots.update({"left_wrist", "right_wrist"})
        if bits & merc.ITEM_WIELD:
            out_data.slots.update({"main_hand"})
        if bits & merc.ITEM_HOLD:
            out_data.slots.update({"held"})
        if bits & merc.ITEM_NO_SAC:
            out_data.restrictions.update({"no_sac"})
        if bits & merc.ITEM_WEAR_FLOAT:
            out_data.slots.update({"float"})
    if "extra flags" in in_type:
        if bits & merc.ITEM_GLOW:
            out_data.attributes.update({"glow"})
        if bits & merc.ITEM_HUM:
            out_data.attributes.update({"hum"})
        if bits & merc.ITEM_DARK:
            out_data.attributes.update({"dark"})
        if bits & merc.ITEM_LOCK:
            out_data.attributes.update({"lock"})
        if bits & merc.ITEM_EVIL:
            out_data.attributes.update({"evil"})
        if bits & merc.ITEM_INVIS:
            out_data.attributes.update({"invis"})
        if bits & merc.ITEM_MAGIC:
            out_data.attributes.update({"magic"})
        if bits & merc.ITEM_NODROP:
            out_data.restrictions.update({"no_drop"})
        if bits & merc.ITEM_BLESS:
            out_data.attributes.update({"bless"})
        if bits & merc.ITEM_ANTI_GOOD:
            out_data.restrictions.update({"anti_good"})
        if bits & merc.ITEM_ANTI_EVIL:
            out_data.restrictions.update({"anti_evil"})
        if bits & merc.ITEM_ANTI_NEUTRAL:
            out_data.restrictions.update({"anti_neutral"})
        if bits & merc.ITEM_NOREMOVE:
            out_data.restrictions.update({"no_remove"})
        if bits & merc.ITEM_INVENTORY:
            out_data.attributes.update({"inventory"})
        if bits & merc.ITEM_NOPURGE:
            out_data.restrictions.update({"no_purge"})
        if bits & merc.ITEM_ROT_DEATH:
            out_data.attributes.update({"rot_death"})
        if bits & merc.ITEM_VIS_DEATH:
            out_data.attributes.update({"vis_death"})
        if bits & merc.ITEM_NONMETAL:
            out_data.attributes.update({"non_metal"})
        if bits & merc.ITEM_NOLOCATE:
            out_data.restrictions.update({"no_locate"})
        if bits & merc.ITEM_MELT_DROP:
            out_data.attributes.update({"melt_drop"})
        if bits & merc.ITEM_HAD_TIMER:
            out_data.attributes.update({"had_timer"})
        if bits & merc.ITEM_SELL_EXTRACT:
            out_data.attributes.update({"sell_extract"})
        if bits & merc.ITEM_BURN_PROOF:
            out_data.attributes.update({"burn_proof"})
        if bits & merc.ITEM_NOUNCURSE:
            out_data.restrictions.update({"no_uncurse"})
    if "weapon flags" in in_type:
        if bits & merc.WEAPON_FLAMING:
            out_data.weapon.update({"flaming"})
        if bits & merc.WEAPON_FROST:
            out_data.weapon.update({"frost"})
        if bits & merc.WEAPON_VAMPIRIC:
            out_data.weapon.update({"vampiric"})
        if bits & merc.WEAPON_SHARP:
            out_data.weapon.update({"sharp"})
        if bits & merc.WEAPON_VORPAL:
            out_data.weapon.update({"vorpal"})
        if bits & merc.WEAPON_TWO_HANDS:
            out_data.weapon.update({"two_handed"})
        if bits & merc.WEAPON_SHOCKING:
            out_data.weapon.update({"shocking"})
        if bits & merc.WEAPON_POISON:
            out_data.weapon.update({"poison"})


def find_location(ch, arg):
    if arg.isdigit():
        vnum = int(arg)
        if vnum not in instance.room_templates.keys():
            return None
        else:
            room_instance = instance.instances_by_room[vnum][0]
            return instance.rooms[room_instance]
    victim = ch.get_char_world(arg)
    if victim:
        return victim.in_room
    item = ch.get_item_world(arg)
    if item:
        return item.in_room
    return None


def append_file(ch, fp, pstr):
    pstr = "[%5d] %s: %s" % (ch.in_room.vnum, ch.name, pstr)
    with open(fp, "a") as f:
        f.write(pstr + "\n")


def read_to_eol(pstr):
    locate = pstr.find("\n")
    if locate == -1:
        locate = len(pstr)
    return pstr[locate + 1 :], pstr[:locate]


def old_is_name(arg, name):
    name, tmp = read_word(name)
    if not arg:
        return False
    while tmp:
        if tmp.lower().startswith(arg):
            return True
        name, tmp = read_word(name)
    return False


_breakup = re.compile("(\".*?\"|'.*?'|[^\s]+)")


def is_name(arg, name):
    if not arg or not name:
        return False
    arg = arg.lower()
    name = name.lower()
    words = _breakup.findall(name)
    for word in words:
        if word[0] in ('"', "'"):
            word = word[1:-1]
        if word.startswith(arg):
            return True
    return False


def dice(number, size):
    return sum([random.randint(1, size) for x in range(number)])


def number_fuzzy(number):
    return random.randint(number - 1, number + 1)


def number_argument(argument):
    if not argument:
        return 1, ""
    if "." not in argument:
        return 1, argument
    dot = argument.find(".")
    number = argument[:dot]
    if number.isdigit():
        return int(number), argument[dot + 1 :]
    else:
        return 1, argument[dot + 1 :]


# * Simple linear interpolation.
def interpolate(level, value_00, value_32):
    return value_00 + level * (value_32 - value_00) // 32


def mass_replace(pstr, pdict):
    for k, v in pdict.items():
        if v:
            pstr = pstr.replace(k, v)
    return pstr


def set_title(ch, title):
    if ch.is_npc():
        return
    nospace = [".", ",", "!", "?"]
    if title[0] in nospace:
        ch.title = title
    else:
        ch.title = " " + title


def get_mob_id():
    return time.time()


# * Get an extra description from a list.
def get_extra_descr(name, edlist):
    if not edlist:
        return None
    for ed in edlist:
        if name.lower() in ed.keyword:
            return ed.description
    return None


def argument_parser(arg_string):
    if not arg_string:
        return None

    atype = None
    num_or_count = None
    arg_num = 1

    if "" is arg_string:
        return None, None, None, None

    arg_string = arg_string.lstrip()
    if "#" in arg_string:
        if arg_string[0] == "#":
            atype = "instance_id"
            target = arg_string.replace("#", "")
            return atype, num_or_count, arg_num, int(target)
        else:
            return None  # Funky id request

    elif "." in arg_string or "*" in arg_string:
        if "*" in arg_string:
            sep = arg_string.find("*")
            num_or_count = "count"
        else:
            sep = arg_string.find(".")
            num_or_count = "number"
        arg_num = arg_string[:sep]
        target = arg_string[sep + 1 :]
        if '"' in target or "'" in target:
            if num_or_count == "number":
                atype = "number_compound"
            else:
                atype = "count_compound"
            compound_set = set({})
            if '"' in target:
                target = target.replace('"', "")
            else:
                target = target.replace("'", "")
            compound, word = read_word(target, True)
            compound_set |= {word}
            while len(compound) > 0:
                compound, word = read_word(compound)
                compound_set |= {word}
            return atype, num_or_count, arg_num, compound_set
        elif " " in target and re.match("^[a-zA-Z ]*$", target):
            if num_or_count == "number":
                atype = "number_compound"
            else:
                atype = "count_compound"
            compound_set = set({})
            compound, word = read_word(target, True)
            compound_set |= {word}
            while len(compound) > 0:
                compound, word = read_word(compound)
                compound_set |= {word}
            return atype, num_or_count, arg_num, compound_set
        if not arg_num.isdigit():
            arg_num = 1
        if target.isdigit():
            if num_or_count == "number":
                atype = "number_vnum"
            else:
                atype = "count_vnum"
            return atype, num_or_count, arg_num, int(target)
        elif target.isalpha():
            if num_or_count == "number":
                atype = "number_word"
            else:
                atype = "count_word"
            return atype, num_or_count, arg_num, target
        else:
            return None, None, None, None

    elif arg_string.isdigit():
        atype = "vnum"
        return atype, None, arg_num, int(arg_string)

    elif arg_string.isalpha():
        atype = "word"
        return atype, None, arg_num, arg_string

    elif re.match("^[a-zA-Z ]*$", arg_string):
        compound_set = set({})
        compound, word = read_word(arg_string, True)
        compound_set |= {word}
        while len(compound) > 0:
            compound, word = read_word(compound)
            compound_set |= {word}
        atype = "compound"
        return atype, num_or_count, arg_num, compound_set

    elif not arg_string.isalnum():
        return None, None, None, None

    else:
        return None, None, None, None


def object_search(
    ch, template: bool = False, obj_type: str = None, target_package: tuple = None
):
    if not obj_type:
        try:
            return find_character(ch, template, target_package)
        except:
            try:
                return find_item(ch, template, target_package)
            except:
                try:
                    return find_room(ch, template, target_package)
                except:
                    return None

    if "character" in obj_type:
        return find_character(ch, template, target_package)
    elif "room" in obj_type:
        return find_room(ch, template, target_package)
    elif "item" in obj_type:
        return find_item(ch, template, target_package)


def find_character(ch, template, target_package):
    atype, num_or_count, arg_num, target = target_package
    if ch.in_room:
        room_inventory_list = [
            npc_id
            for npc_id in ch.in_room.people[:]
            if instance.characters[npc_id].vnum == target
        ]
        if room_inventory_list:
            try:
                return instance.characters[room_inventory_list[arg_num - 1]]
            except:
                room_inventory_list = None
        else:
            npc_id = instance.instances_by_npc[target][arg_num - 1]
            if npc_id:
                return instance.characters[npc_id]


def find_room(ch, template, target_package):
    atype, num_or_count, arg_num, target = target_package
    if isinstance(target, int):
        trash = ""
        try:
            room_id = instance.instances_by_room[target][arg_num - 1]
            return instance.rooms[room_id]
        except:
            trash = "onion bagels!"
        if trash:
            try:
                return instance.rooms[target]
            except:
                return None


def find_item(ch, template, target_package):
    # TODO change instance dicts to ordered dicts to support searches with predictable results.
    atype, num_or_count, arg_num, target = target_package
    bagels = ""
    sorted(
        sorted(instance.rooms.keys(), key=lambda x: instance.rooms[x].vnum),
        key=lambda x: instance.rooms[x].instance_id,
    )

    combined_inventory = ch.inventory + ch.in_room.items

    if "vnum" in atype:
        if combined_inventory:
            final_item = [
                instance.items[item_id]
                for item_id in combined_inventory
                if instance.items[item_id].vnum == target
            ][arg_num - 1]
            if final_item:
                return final_item
        elif ch.is_immortal():
            item_id = instance.instances_by_item[target][arg_num - 1]
            return instance.items.get(item_id, None)
        else:
            return None
    elif "instance" in atype:
        return instance.items.get(target, None)
    elif "number" in atype:
        pass
    else:
        if "vnum" in atype:
            if ch.is_immortal():
                try:
                    # temp
                    return instance.items[None]
                except:
                    return None


def to_integer(s: str):
    try:
        return int(s)
    except ValueError:
        return int(float(s))
