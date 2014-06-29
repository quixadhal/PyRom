from collections import OrderedDict


class Bit:
    def __init__(self, default=0,  flags=None):
        self.bits = default
        self.flags = flags

    def set_bit(self, bit):
        self.bits = self.bits | self.from_name(bit)

    def rem_bit(self, bit):
        self.bits = self.bits & ~self.from_name(bit)

    def is_set(self, bit):
        return self.bits & self.from_name(bit)

    def from_name(self, name):
        if type(name) == int:
            return name
        name = name.strip()
        bitstring = name.split(' ')
        bits = 0
        flags = OrderedDict()
        if type(self.flags) == list:
            for d in self.flags:
                for k, v in d.items():
                    flags[k] = v
        else:
            flags = self.flags

        for tok in flags.values():
            if tok.name in bitstring:
                bits += tok.bit
        return bits
    def __repr__(self):
        buf = ""
        if not self.flags:
            return
        flags = OrderedDict()
        if type(self.flags) == list:
            for d in self.flags:
                for k, v in d.items():
                    flags[k] = v
        else:
            flags = self.flags

        for k,fl in flags.items():
            if self.is_set(fl.bit):
                buf += " %s" % fl.name
        return buf