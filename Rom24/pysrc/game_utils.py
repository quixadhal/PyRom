import time

__author__ = 'venom'
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
    elif pstr[0] == '"':
        locate = pstr.find('"', 1)+1
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
            if ch.contains:
                contains_id_list = [item_id for item_id in ch.contains if merc.items[item_id].vnum == target]
                if contains_id_list:
                    try:
                        return merc.items[contains_id_list[arg_num - 1]]
                    except:
                        contains_id_list = None
            elif merc.rooms[environment] and not contains_id_list:
                contents_id_list = [item_id for item_id in environment.contents if merc.items[item_id].vnum == target]
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
