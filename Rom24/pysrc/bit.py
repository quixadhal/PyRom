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
from collections import OrderedDict
import game_utils
import state_checks
import tables


class Bit:
    def __init__(self, default=0, flags=None):
        self.bits = default
        self._flags = flags

    def __getattr__(self, name):
        if not name.startswith('is_'):
            raise AttributeError
        flags = self.flags
        flag = state_checks.name_lookup(flags, name[3:])
        if not flag:
            raise AttributeError
        return self.is_set(flags[flag].bit)

    @property
    def flags(self):
        flags = OrderedDict()
        if type(self._flags) == list:
            for d in self._flags:
                for k, v in d.items():
                    flags[k] = v
        else:
            flags = self._flags
        return flags

    def set_bit(self, bit):
        self.bits |= self.from_name(bit)

    def rem_bit(self, bit):
        self.bits &= ~self.from_name(bit)

    def is_set(self, bit):
        return self.bits & self.from_name(bit)

    def read_bits(self, area, default=0):
        area, bits = game_utils.read_flags(area)
        self.set_bit(bits)
        self.set_bit(default)
        return area

    #lets you chose the flag table. so act/plr flags will save correctly.
    def print_flags(self, flags):
        holder = self._flags
        self._flags = flags
        as_str = repr(self)
        self._flags = holder
        return as_str

    def from_name(self, name):
        if type(name) is int:
            return name
        elif type(name) is list or type(name) is tuple:
            bitstring = name
        elif isinstance(name, Bit):
            bitstring = repr(name)
        else:
            name = name.strip()
            bitstring = name.split(' ')
        bits = 0
        flags = self.flags
        for tok in flags.values():
            if tok.name in bitstring:
                bits += tok.bit
        return bits

    def __repr__(self):
        buf = ""
        if not self.flags:
            return buf
        flags = self.flags
        for k, fl in flags.items():
            if self.is_set(fl.bit):
                buf += " %s" % fl.name
        return buf


def to_json(b):
    """
    A Bit() object can be serialized to json data by
    js = json.dumps(b, default=bit.to_json)

    :param b:
    :return:
    """
    if isinstance(b, Bit):
        return {'__Bit__': True, 'flags': b.flags, 'bits': b.bits}
    raise TypeError(repr(b) + " is not JSON serializable")


def from_json(js):
    """
    A Bit() object can be reconstructed from json data by
    b = json.loads(js, object_pairs_hook=bit.from_json)

    :param js:
    :return:
    """
    ok = False
    for i in js:
        if i[0] == '__Bit__':
            ok = True
    if ok:
        d_bits = 0
        for i in js:
            if i[0] == '__Bit__':
                continue
            elif i[0] == 'bits':
                d_bits = i[1]
            elif i[0] == 'flags':
                d_flags = OrderedDict()
                for j in i[1]:
                    k = j[0]
                    v = j[1]
                    d_flags[k] = tables.flag_type._make(v)
                b = Bit(flags=d_flags)
                b.set_bit(d_bits)
                return b
            else:
                raise TypeError(repr(js) + " is not a valid Bit serialization")
    return js
