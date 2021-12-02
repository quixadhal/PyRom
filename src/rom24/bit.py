import json
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

from rom24 import game_utils
from rom24 import state_checks


class Bit:
    """
    The Bit() class is meant to be a drop-in replacement for the old
    DikuMUD style 'bitflag' variable.  Because DikuMUD was written on
    limited hardware, many techniques were used to try and fit as much
    data as possible into a small amount of memory.

    Rather than using distinct variables, 32 boolean values were
    crammed into a single integer, with each bit being assigned a
    use.  #define'd macros were created to make it somewhat eaasier
    to check, set, and clear them.  And, in Rom and later derivatives,
    functions were made to convert them to and from textual names, so
    they could be stored in area files without worrying about architecture
    changes screwing up the order.

    This class reimplements that concept, but in a more useful way.  You
    can directly use a set of names to set, clear, or check a bit.  You can
    use a list of names to do this for multiples at a time.  You can get back
    the name OR numerical value, and you can still use the numbers if you
    like.
    """

    def __init__(self, default: int = 0, flags: OrderedDict = None):
        """
        The constructor allows you to specify the default value, as
        well as providing an ordered dict which will be used for
        bit position/name to number mapping.

        :param default: An integer of the starting bit values, usually 0.
        :type default: int
        :param flags: An ordered dict holding the name/number mappings used.
        :type flags: OrderedDict
        :return:
        :rtype:
        """
        self.bits = default
        self._flags = flags

    def __add__(self, other):
        """
        This implements addition between integers and Bit() objects.
        It creates a new Bit() object containing the result.

        :param other: An integer value to be numerically added to self.bits.
        :type other: int
        :return: A new Bit() object with the value added.
        :rtype: Bit
        """
        return Bit(self.bits + self.from_name(other), self.flags)

    def __radd__(self, other):
        """
        This implements addition between integers and Bit() objects.
        It creates a new Bit() object containing the result.
        This version is for the reversed form, where the right-hand side is
        the Bit() object.

        :param other: An integer value to be numerically added to self.bits.
        :type other: int
        :return: A new Bit() object with the value added.
        :rtype: Bit
        """
        return Bit(self.from_name(other) + self.bits, self.flags)

    def __iadd__(self, other):
        """
        This adds the given integer value to the Bit() object and
        returns the Bit() object with the new value.

        :param other: An integer value to be numerically added to self.bits.
        :type other: int
        :return: A new Bit() object with the value added.
        :rtype: Bit
        """
        self.bits += self.from_name(other)
        return self

    def __sub__(self, other):
        return Bit(self.bits - self.from_name(other), self.flags)

    def __rsub__(self, other):
        return Bit(self.from_name(other) - self.bits, self.flags)

    def __isub__(self, other):
        self.bits -= self.from_name(other)
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            return Bit(self.bits * other, self.flags)
        raise TypeError(
            "You can only multiply a Bit() value by an integer, not a " + repr(other)
        )

    def __rmul__(self, other):
        if isinstance(other, int):
            return Bit(other * self.bits, self.flags)
        raise TypeError(
            "You can only multiply a Bit() value by an integer, not a " + repr(other)
        )

    def __imul__(self, other):
        if isinstance(other, int):
            self.bits *= other
            return self
        raise TypeError(
            "You can only multiply a Bit() value by an integer, not a " + repr(other)
        )

    def __truediv__(self, other):
        if isinstance(other, int):
            return Bit(self.bits // other, self.flags)
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __rtruediv__(self, other):
        if isinstance(other, int):
            return Bit(other // self.bits, self.flags)
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __itruediv__(self, other):
        if isinstance(other, int):
            self.bits //= other
            return self
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Bit(self.bits // other, self.flags)
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __rfloordiv__(self, other):
        if isinstance(other, int):
            return Bit(other // self.bits, self.flags)
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __ifloordiv__(self, other):
        if isinstance(other, int):
            self.bits //= other
            return self
        raise TypeError(
            "You can only divide a Bit() value by an integer, not a " + repr(other)
        )

    def __mod__(self, other):
        if isinstance(other, int):
            return Bit(self.bits % other, self.flags)
        raise TypeError(
            "You can only get the integer modulo of a Bit() value, not a " + repr(other)
        )

    def __rmod__(self, other):
        if isinstance(other, int):
            return Bit(other % self.bits, self.flags)
        raise TypeError(
            "You can only get the integer modulo of a Bit() value, not a " + repr(other)
        )

    def __imod__(self, other):
        if isinstance(other, int):
            self.bits %= other
            return self
        raise TypeError(
            "You can only get the integer modulo of a Bit() value, not a " + repr(other)
        )

    def __pow__(self, power, modulo=None):
        if isinstance(power, int):
            return Bit(self.bits ** power, self.flags)
        raise TypeError(
            "You can only raise a Bit() value to an integer power, not a " + repr(power)
        )

    def __rpow__(self, power, modulo=None):
        if isinstance(power, int):
            return Bit(power ** self.bits, self.flags)
        raise TypeError(
            "You can only raise a Bit() value to an integer power, not a " + repr(power)
        )

    def __ipow__(self, power, modulo=None):
        if isinstance(power, int):
            self.bits **= power
            return self
        raise TypeError(
            "You can only raise a Bit() value to an integer power, not a " + repr(power)
        )

    def __lshift__(self, other):
        if isinstance(other, int):
            return Bit(self.bits << other, self.flags)
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __rlshift__(self, other):
        if isinstance(other, int):
            return Bit(other << self.bits, self.flags)
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __ilshift__(self, other):
        if isinstance(other, int):
            self.bits <<= other
            return self
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __rshift__(self, other):
        if isinstance(other, int):
            return Bit(self.bits >> other, self.flags)
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __rrshift__(self, other):
        if isinstance(other, int):
            return Bit(other >> self.bits, self.flags)
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __irshift__(self, other):
        if isinstance(other, int):
            self.bits >>= other
            return self
        raise TypeError(
            "You can only shift a Bit() value by an integer, not a " + repr(other)
        )

    def __and__(self, other):
        return Bit(self.bits & self.from_name(other), self.flags)

    def __rand__(self, other):
        return Bit(self.from_name(other) & self.bits, self.flags)

    def __iand__(self, other):
        self.bits &= self.from_name(other)
        return self

    def __xor__(self, other):
        return Bit(self.bits ^ self.from_name(other), self.flags)

    def __rxor__(self, other):
        return Bit(self.from_name(other) ^ self.bits, self.flags)

    def __ixor__(self, other):
        self.bits ^= self.from_name(other)
        return self

    def __or__(self, other):
        return Bit(self.bits | self.from_name(other), self.flags)

    def __ror__(self, other):
        return Bit(self.from_name(other) | self.bits, self.flags)

    def __ior__(self, other):
        self.bits |= self.from_name(other)
        return self

    def __bool__(self):
        return True if self.bits else False

    def __neg__(self):
        return Bit(-self.bits, self.flags)

    def __pos__(self):
        return Bit(+self.bits, self.flags)

    def __abs__(self):
        return Bit(abs(self.bits), self.flags)

    def __int__(self):
        return self.bits

    def __getattr__(self, name):
        if not name.startswith("is_"):
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

    def clear_bit(self, bit):
        self.bits &= ~self.from_name(bit)

    def rem_bit(self, bit):
        self.bits &= ~self.from_name(bit)

    def is_set(self, bit):
        return self.bits & self.from_name(bit)

    def read_bits(self, area, default=0):
        area, bits = game_utils.read_flags(area)
        self.set_bit(bits)
        self.set_bit(default)
        return area

    # lets you chose the flag table. so act/plr flags will save correctly.
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
            bitstring = name.split(" ")
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

    def to_json(self, outer_encoder=None):
        """
        This method implements the serialization of a Bit() object
        for the JSON module to use.

        :param outer_encoder:
        :type outer_encoder:
        :return: JSON serialization
        :rtype: str
        """
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        cls_name = "__class__/" + __name__ + "." + self.__class__.__name__
        return {
            cls_name: {
                "bits": outer_encoder(self.bits),
                "flags": outer_encoder(self.flags),
            }
        }

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        """
        This class method implements turning a JSON serialization of the data
        from a Bit() class back into an actual Bit() object.

        :param data:
        :type data:
        :param outer_decoder:
        :type outer_decoder:
        :return: Bit() object or unrecognized data
        :rtype:
        """
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = "__class__/" + __name__ + "." + cls.__name__
        if cls_name in data:
            return cls(
                default=outer_decoder(data[cls_name]["bits"]),
                flags=outer_decoder(data[cls_name]["flags"]),
            )
        return data
