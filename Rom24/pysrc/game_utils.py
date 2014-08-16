import logging

logger = logging.getLogger()

import time
import collections

__author__ = 'syn'
import merc
import random


def read_forward(pstr, jump=1):
    return pstr[jump:]


def read_letter(pstr):
    pstr = pstr.lstrip()
    return pstr[1:], pstr[:1]


def read_word(pstr, lower=True):
    if not pstr:
        return "", ""
    pstr = pstr.lstrip()
    locate = len(pstr)
    if pstr[0] == "'":
        locate = pstr.find("'", 1)+1
        if locate == 0:
            locate = len(pstr)-1
    elif pstr[0] == '"':
        locate = pstr.find('"', 1)+1
        if locate == 0:
            locate = len(pstr)-1
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
        word = word[1:-1]
    if lower:
        word = word.lower()

    return pstr.lstrip()[strip:], word.strip()


def read_int(pstr):
    if not pstr:
        return None, None
    pstr = pstr.lstrip()
    number = ""
    negative = False
    for c in pstr:
        if c == '-':
            negative = True
        elif c.isdigit():
            number += c
        else:
            break

    pstr = pstr.lstrip()
    if not negative:
        pstr = pstr[len(number):]
        return pstr, int(number)
    else:
        pstr = pstr[len(number) + 1:]
        number = int(number) * -1
        return pstr, number


def read_string(pstr):
    if not pstr:
        return None, None
    end = pstr.find('~')
    word = pstr[0:end]
    pstr = pstr[end + 1:]
    return pstr, word.strip()


def read_flags(pstr):
    if not pstr:
        return None, None
    pstr, w = read_word(pstr, False)
    if w == '0' or w == 0:
        return pstr, 0
    if w.isdigit():
        return pstr, int(w)
    flags = 0

    for c in w:
        flag = 0
        if 'A' <= c <= 'Z':
            flag = merc.A
            while c != 'A':
                flag *= 2
                c = chr(ord(c) - 1)

        elif 'a' <= c <= 'z':
            flag = merc.aa
            while c != 'a':
                flag *= 2
                c = chr(ord(c) - 1)

        flags += flag
    return pstr, flags


def read_equipment_flags(item, pstr):
    ret_set = {''}
    if not pstr:
        return None, None
    pstr, w = read_word(pstr, False)
    if w == '0' or w == 0:
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


def item_bitvector_flag_str(bits: int, in_type='extra flags'):
    if not bits or in_type:
        return None
    if bits == 0:
        return None
    if 'wear flags' in in_type:
        if bits & merc.ITEM_TAKE:
            return 'take'
        elif bits & merc.ITEM_WEAR_FINGER:
            return 'left_finger, right_finger'
        elif bits & merc.ITEM_WEAR_NECK:
            return 'neck, collar'
        elif bits & merc.ITEM_WEAR_BODY:
            return 'body'
        elif bits & merc.ITEM_WEAR_HEAD:
            return 'head'
        elif bits & merc.ITEM_WEAR_LEGS:
            return 'legs'
        elif bits & merc.ITEM_WEAR_FEET:
            return 'feet'
        elif bits & merc.ITEM_WEAR_HANDS:
            return 'hands'
        elif bits & merc.ITEM_WEAR_ARMS:
            return 'arms'
        elif bits & merc.ITEM_WEAR_SHIELD:
            return 'off_hand'
        elif bits & merc.ITEM_WEAR_ABOUT:
            return 'about'
        elif bits & merc.ITEM_WEAR_WAIST:
            return 'waist'
        elif bits & merc.ITEM_WEAR_WRIST:
            return 'left_wrist, right_wrist'
        elif bits & merc.ITEM_WIELD:
            return 'main_hand'
        elif bits & merc.ITEM_HOLD:
            return 'held'
        elif bits & merc.ITEM_NO_SAC:
            return 'no_sac'
        elif bits & merc.ITEM_WEAR_FLOAT:
            return 'float'
        else:
            return None
    if 'extra flags' in in_type:
        if bits & merc.ITEM_GLOW:
            return 'glow'
        elif bits & merc.ITEM_HUM:
            return 'hum'
        elif bits & merc.ITEM_DARK:
            return 'dark'
        elif bits & merc.ITEM_LOCK:
            return 'lock'
        elif bits & merc.ITEM_EVIL:
            return 'evil'
        elif bits & merc.ITEM_INVIS:
            return 'invis'
        elif bits & merc.ITEM_MAGIC:
            return 'magic'
        elif bits & merc.ITEM_NODROP:
            return 'no_drop'
        elif bits & merc.ITEM_BLESS:
            return 'bless'
        elif bits & merc.ITEM_ANTI_GOOD:
            return 'anti_good'
        elif bits & merc.ITEM_ANTI_EVIL:
            return 'anti_evil'
        elif bits & merc.ITEM_ANTI_NEUTRAL:
            return 'anti_neutral'
        elif bits & merc.ITEM_NOREMOVE:
            return 'no_remove'
        elif bits & merc.ITEM_INVENTORY:
            return 'inventory'
        elif bits & merc.ITEM_NOPURGE:
            return 'no_purge'
        elif bits & merc.ITEM_ROT_DEATH:
            return 'rot_death'
        elif bits & merc.ITEM_VIS_DEATH:
            return 'vis_death'
        elif bits & merc.ITEM_NONMETAL:
            return 'non_metal'
        elif bits & merc.ITEM_NOLOCATE:
            return 'no_locate'
        elif bits & merc.ITEM_MELT_DROP:
            return 'melt_drop'
        elif bits & merc.ITEM_HAD_TIMER:
            return 'had_timer'
        elif bits & merc.ITEM_SELL_EXTRACT:
            return 'sell_extract'
        elif bits & merc.ITEM_BURN_PROOF:
            return 'burn_proof'
        elif bits & merc.ITEM_NOUNCURSE:
            return 'no_uncurse'
        else:
            return None
    if 'weapon flags' in in_type:
        if bits & merc.WEAPON_FLAMING:
            return 'flaming'
        elif bits & merc.WEAPON_FROST:
            return 'frost'
        elif bits & merc.WEAPON_VAMPIRIC:
            return 'vampiric'
        elif bits & merc.WEAPON_SHARP:
            return 'sharp'
        elif bits & merc.WEAPON_VORPAL:
            return 'vorpal'
        elif bits & merc.WEAPON_TWO_HANDS:
            return 'two_handed'
        elif bits & merc.WEAPON_SHOCKING:
            return 'shocking'
        elif bits & merc.WEAPON_POISON:
            return 'poison'
        else:
            return None


def item_flags_from_bits(bits: int, out_data: collections.namedtuple, in_type='wear flags'):
    if not out_data or not bits or not in_type:
        return None
    if bits == 0:
        return None
    if 'wear flags' in in_type:
        if bits & merc.ITEM_TAKE:
            out_data.attributes.update({'take'})
        if bits & merc.ITEM_WEAR_FINGER:
            out_data.slots.update({'left_finger', 'right_finger'})
        if bits & merc.ITEM_WEAR_NECK:
            out_data.slots.update({'neck', 'collar'})
        if bits & merc.ITEM_WEAR_BODY:
            out_data.slots.update({'body'})
        if bits & merc.ITEM_WEAR_HEAD:
            out_data.slots.update({'head'})
        if bits & merc.ITEM_WEAR_LEGS:
            out_data.slots.update({'legs'})
        if bits & merc.ITEM_WEAR_FEET:
            out_data.slots.update({'feet'})
        if bits & merc.ITEM_WEAR_HANDS:
            out_data.slots.update({'hands'})
        if bits & merc.ITEM_WEAR_ARMS:
            out_data.slots.update({'arms'})
        if bits & merc.ITEM_WEAR_SHIELD:
            out_data.slots.update({'off_hand'})
        if bits & merc.ITEM_WEAR_ABOUT:
            out_data.slots.update({'about'})
        if bits & merc.ITEM_WEAR_WAIST:
            out_data.slots.update({'waist'})
        if bits & merc.ITEM_WEAR_WRIST:
            out_data.slots.update({'left_wrist', 'right_wrist'})
        if bits & merc.ITEM_WIELD:
            out_data.slots.update({'main_hand'})
        if bits & merc.ITEM_HOLD:
            out_data.slots.update({'held'})
        if bits & merc.ITEM_NO_SAC:
            out_data.restrictions.update({'no_sac'})
        if bits & merc.ITEM_WEAR_FLOAT:
            out_data.slots.update({'float'})
    if 'extra flags' in in_type:
        if bits & merc.ITEM_GLOW:
            out_data.attributes.update({'glow'})
        if bits & merc.ITEM_HUM:
            out_data.attributes.update({'hum'})
        if bits & merc.ITEM_DARK:
            out_data.attributes.update({'dark'})
        if bits & merc.ITEM_LOCK:
            out_data.attributes.update({'lock'})
        if bits & merc.ITEM_EVIL:
            out_data.attributes.update({'evil'})
        if bits & merc.ITEM_INVIS:
            out_data.attributes.update({'invis'})
        if bits & merc.ITEM_MAGIC:
            out_data.attributes.update({'magic'})
        if bits & merc.ITEM_NODROP:
            out_data.restrictions.update({'no_drop'})
        if bits & merc.ITEM_BLESS:
            out_data.attributes.update({'bless'})
        if bits & merc.ITEM_ANTI_GOOD:
            out_data.restrictions.update({'anti_good'})
        if bits & merc.ITEM_ANTI_EVIL:
            out_data.restrictions.update({'anti_evil'})
        if bits & merc.ITEM_ANTI_NEUTRAL:
            out_data.restrictions.update({'anti_neutral'})
        if bits & merc.ITEM_NOREMOVE:
            out_data.restrictions.update({'no_remove'})
        if bits & merc.ITEM_INVENTORY:
            out_data.attributes.update({'inventory'})
        if bits & merc.ITEM_NOPURGE:
            out_data.restrictions.update({'no_purge'})
        if bits & merc.ITEM_ROT_DEATH:
            out_data.attributes.update({'rot_death'})
        if bits & merc.ITEM_VIS_DEATH:
            out_data.attributes.update({'vis_death'})
        if bits & merc.ITEM_NONMETAL:
            out_data.attributes.update({'non_metal'})
        if bits & merc.ITEM_NOLOCATE:
            out_data.restrictions.update({'no_locate'})
        if bits & merc.ITEM_MELT_DROP:
            out_data.attributes.update({'melt_drop'})
        if bits & merc.ITEM_HAD_TIMER:
            out_data.attributes.update({'had_timer'})
        if bits & merc.ITEM_SELL_EXTRACT:
            out_data.attributes.update({'sell_extract'})
        if bits & merc.ITEM_BURN_PROOF:
            out_data.attributes.update({'burn_proof'})
        if bits & merc.ITEM_NOUNCURSE:
            out_data.restrictions.update({'no_uncurse'})
    if 'weapon flags' in in_type:
        if bits & merc.WEAPON_FLAMING:
            out_data.weapon.update({'flaming'})
        if bits & merc.WEAPON_FROST:
            out_data.weapon.update({'frost'})
        if bits & merc.WEAPON_VAMPIRIC:
            out_data.weapon.update({'vampiric'})
        if bits & merc.WEAPON_SHARP:
            out_data.weapon.update({'sharp'})
        if bits & merc.WEAPON_VORPAL:
            out_data.weapon.update({'vorpal'})
        if bits & merc.WEAPON_TWO_HANDS:
            out_data.weapon.update({'two_handed'})
        if bits & merc.WEAPON_SHOCKING:
            out_data.weapon.update({'shocking'})
        if bits & merc.WEAPON_POISON:
            out_data.weapon.update({'poison'})

def find_location(ch, arg):
    if arg.isdigit():
        vnum = int(arg)
        if vnum not in merc.roomTemplate:
            return None
        else:
            room_instance = merc.instances_by_room[vnum][0]
            return merc.rooms[room_instance]
    victim = ch.get_char_world(arg)
    if victim:
        return victim.in_room
    item = ch.get_item_world(arg)
    if item:
        return item.in_room
    return None


def append_file(ch, fp, pstr):
    with open(fp, "a") as f:
        f.write(pstr + "\n")


def read_to_eol(pstr):
    locate = pstr.find('\n')
    if locate == -1:
        locate = len(pstr)
    return pstr[locate+1:], pstr[:locate]

def is_name(arg, name):
    name, tmp = read_word(name)
    if not arg:
        return False
    while tmp:
        if tmp.lower().startswith(arg):
            return True
        name, tmp = read_word(name)
    return False


def dice(number, size):
    return sum([random.randint(1, size) for x in range(number)])


def number_fuzzy(number):
    return random.randint(number - 1, number + 1)


def number_argument(argument):
    if not argument:
        return 0, ""
    if '.' not in argument:
        return 1, argument
    dot = argument.find('.')
    number = argument[:dot]
    if number.isdigit():
        return int(number), argument[dot + 1:]
    else:
        return 1, argument[dot + 1:]


# * Simple linear interpolation.
def interpolate(level, value_00, value_32):
    return value_00 + level * (value_32 - value_00) / 32


def mass_replace(pstr, pdict):
    for k, v in pdict.items():
        if v:
            pstr = pstr.replace(k, v)
    return pstr


def set_title(ch, title):
    if ch.is_npc():
        return
    nospace = ['.', ',', '!', '?']
    if title[0] in nospace:
        ch.title = title
    else:
        ch.title = ' ' + title


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


def argument_parser(string):
    if not string:
        return None

    atype = None
    num_or_count = None
    arg_num = 1

    string = string.lstrip()
    if '#' in string:
        if string[0] == '#':
            atype = 'instance_id'
            target = string.replace('#', '')
            return atype, num_or_count, arg_num, int(target)
        else:
            return None  # Funky id request

    if '.' in string or '*' in string:
        if '*' in string:
            sep = string.find('*')
            num_or_count = 'count'
        else:
            sep = string.find('.')
            num_or_count = 'number'
        arg_num = string[:sep]
        target = string[sep + 1:]
        if not target.isalnum():
            return None, None, None, None
        if '"' in target or "'" in target:
            if num_or_count == 'number':
                atype = 'number_compound'
            else:
                atype = 'count_compound'
            compound_list = []
            if '"' in target:
                target = target.replace('"', '')
            else:
                target = target.replace("'", "")
            compound, word = read_word(target, True)
            compound_list.append(word)
            while len(compound) > 0:
                compound, word = read_word(compound)
                compound_list.append(word)
            return atype, num_or_count, arg_num, compound_list
        if not arg_num.isdigit():
            arg_num = 1
        if target.isdigit():
            atype = 'vnum'
            return atype, num_or_count, arg_num, int(target)
        elif target.isalpha():
            atype = 'word'
            return atype, num_or_count, arg_num, target
        else:
            return None, None, None, None

    elif string.isdigit():
        atype = 'vnum'
        return atype, None, arg_num, int(string)

    elif string.isalpha():
        atype = 'word'
        return atype, None, arg_num, string

    elif not string.isalnum():
        return None, None, None, None

    else:
        compound_list = []
        compound, word = read_word(string, True)
        compound_list.append(word)
        while len(compound) > 0:
            compound, word = read_word(compound)
            compound_list.append(word)
        atype = 'compound'
        return atype, num_or_count, arg_num, compound_list


def object_search(ch, environment, template, obj_type, atype, num_or_count, arg_num, target):
    if not atype or not target:
        return None

    count = 0
    result_list = None
    contains_id_list = None
    contents_id_list = None

    if template is True:  # just in case we ever need to 'find' a template..
        if 'vnum' not in atype:
            return None
        if obj_type == 'item':
            return merc.itemTemplate[target]
        elif obj_type == 'npc':
            return merc.characterTemplate[target]
        elif obj_type == 'room':
            return merc.roomTemplate[target]
        else:
            return None

    if atype == 'vnum':
        if obj_type == 'item':
            if ch.inventory:
                contains_id_list = [item_id for item_id in ch.inventory if merc.items[item_id].vnum == target]
                if contains_id_list:
                    try:
                        return merc.items[contains_id_list[arg_num - 1]]
                    except:
                        contains_id_list = None
            elif merc.rooms[environment] and not contains_id_list:
                contents_id_list = [item_id for item_id in environment.inventory if merc.items[item_id].vnum == target]
                if contents_id_list:
                    try:
                        return merc.items[contents_id_list[arg_num - 1]]
                    except:
                        contents_id_list = None
            elif not contents_id_list:
                try:
                    return merc.instances_by_item[target][arg_num - 1]
                except:
                    return None
            else:
                return None
        elif obj_type == 'npc':
            try:
                item_id = merc.instances_by_item[target][0]
                return merc.items[item_id]
            except:
                return None
        elif obj_type == 'room':
            try:
                item_id = merc.instances_by_item[target][0]
                return merc.items[item_id]
            except:
                return None
        else:
            return None
    elif atype == 'instance_id':
        pass
    elif atype == 'compound' or atype == 'word' or atype == 'number_compound' or atype == 'count_compound':
        pass


def to_integer(s: str):
    try:
        return int(s)
    except ValueError:
        return int(float(s))
