import time

__author__ = 'venom'
from merc import *

import random
import state_checks


def read_forward(pstr, jump=1):
    return pstr[jump:]


def read_letter(pstr):
    pstr = pstr.lstrip()
    return pstr[1:], pstr[:1]


def read_word(pstr, lower=True):
    if not pstr:
        return "", ""
    pstr = pstr.lstrip()
    word = pstr.split()[0]
    if word[0] == "'":
        word = pstr[:pstr.find("'", 1) + 1]
    if lower:
        word = word.lower()
    pstr = pstr.lstrip()
    pstr = pstr[len(word)+1:]
    word = word.replace("'", '')
    return pstr, word.strip()


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
            flag = A
            while c != 'A':
                flag *= 2
                c = chr(ord(c) - 1)

        elif 'a' <= c <= 'z':
            flag = aa
            while c != 'a':
                flag *= 2
                c = chr(ord(c) - 1)

        flags += flag
    return pstr, flags

def find_location( ch, arg ):
    if arg.isdigit():
        vnum = int(arg)
        if vnum not in room_index_hash:
            return None
        else:
            return room_index_hash[vnum]
    victim = ch.get_char_world(arg)
    if victim:
        return victim.in_room
    obj = ch.get_obj_world(arg)
    if obj:
        return obj.in_room
    return None

def append_file(ch, fp, str):
    with open(fp, "a") as f:
        f.write(str + "\n")

def read_to_eol(pstr):
    pstr = pstr.split('\n')
    line = pstr.pop(0)
    pstr = "\n".join(pstr)
    return pstr, line


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
    if '.' not in argument:
        return 1, argument

    dot = argument.find('.')
    number = argument[:dot]
    if number.isdigit():
        return int(number), argument[dot + 1:]
    return 1, argument


# * Simple linear interpolation.
def interpolate(level, value_00, value_32):
    return value_00 + level * (value_32 - value_00) / 32


def mass_replace(str, dict):
    for k,v in dict.items():
        if v:
            str = str.replace(k,v)
    return str


def set_title(ch, title):
    if ch.is_npc():
        return
    nospace = ['.', ',', '!', '?']
    if title[0] in nospace:
        ch.pcdata.title = title
    else:
        ch.pcdata.title = ' ' + title


def get_mob_id():
    return time.time()


# * Get an extra description from a list.
def get_extra_descr(name, edlist):
    if not edlist: return None
    for ed in edlist:
        if name.lower() in ed.keyword:
            return ed.description
    return None
