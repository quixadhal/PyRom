from collections import OrderedDict
import state_checks


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
            return
        flags = self.flags
        for k, fl in flags.items():
            if self.is_set(fl.bit):
                buf += " %s" % fl.name
        return buf
