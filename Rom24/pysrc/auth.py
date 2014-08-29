"""
The code in this module is NOT subject to the DikuMUD, Merc, or ROM licenses.
It is, instead, released under the MIT License, as follows.

Copyright (c) 2014 Chris Meshkin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
__author__ = 'quixadhal'

import time
import struct
import hmac
import hashlib
import base64
import random
import json
import logging

logger = logging.getLogger()

import instance


class TwoFactorAuth:
    """
    This class implements the basic functionality of the Google Authenticator.

    To use this, add a property to your login object to hold a unique secret
    key, which will be used to drive the 2-factor authentication algorithm.

    The user should add this key to their Google authenticator, so it should
    be printed to the user when they enable this feature (during creation, or
    later).

    The secret key itself must be a 16-character long base32-encoded chunk of
    data.  It can be generated from any source, including a random number, or
    it can be something meaningful.  As long as the encoded result is 16
    characters, and can be decoded as base32, it will work fine.

    The user should use a time-based authentication (TOTP) when adding their
    account to the Google authenticator.

    Once this is done, this module can be used.  When a new instance of this
    class is initialized, it is passed that secret key.  If no secret is
    passed, a default one is used.

    When the user is prompted to enter their time-based token, they should
    enter a 6 digit number, zero-padded.  This number can then be passed
    to the verify() method, which will return True or False.
    """
    def __init__(self, s: str='ABCDEFGHIJKLMNOP'):
        """
        Initializes the class with a secret key, using an application-wide
        default if none is provided.

        :param s: Expected to be a base32-encoded string, 16 characters long.
        :type s: str
        :return:
        :rtype:
        """
        if '-' in s:
            s = s.replace('-', '')
        self._raw_secret = s.upper().rjust(16, 'A')[0:16]
        self._secret = base64.b32decode(self._raw_secret.encode())

    def time_code(self, moment: int=None):
        """
        Returns a string indicating the current valid token which will be
        generated, and which should be matched to authenticate the user.

        :param moment: A time value, defaulting to now.
        :type moment: int
        :return: A 6-digit authentication token
        :rtype: str
        """
        if moment is None:
            moment = time.time()
        moment = int(moment // 30)
        time_bytes = struct.pack('>q', moment)
        hash_digest = hmac.HMAC(self._secret, time_bytes, hashlib.sha1).digest()
        offset = hash_digest[-1] & 0x0F
        truncated_digest = hash_digest[offset:offset + 4]
        code = struct.unpack('>L', truncated_digest)[0]
        code &= 0x7FFFFFFF
        code %= 1000000
        return '%06d' % code

    def verify(self, token):
        """
        This method validates the token passed in against the currently generated
        token.  Because of clock skew between the user's device and the application
        server's device, we actually calculate the previous and next tokens and compare
        the one passed to all three.  If any of them match, it is considered a success.

        This allows the user's clock to be up to 30 seconds offset from the server's clock
        with a reasonable expectation of success.

        :param token: user-supplied token to be validated
        :type token: str or int
        :return: True or False
        :rtype: bool
        """
        if isinstance(token, int):
            token = '%06d' % token
        trials = [self.time_code(time.time() + offset) for offset in (-30, 0, 30)]
        if token in trials:
            return True
        return False

    @property
    def secret(self):
        """
        This property just provides a clean way to get the user's secret key in its
        base32 encoded format.  This should be used to present that key to the user
        so they can add it to their Google Authentication device.

        The token is "prettied-up" to make it easier to type in.

        :return: Secret key token
        :rtype: str
        """
        token = self._raw_secret.lower()
        return '-'.join((token[0:4], token[4:8], token[8:12], token[12:16]))

    @secret.setter
    def secret(self, s: str):
        """
        Reset the class with a new secret key.

        :param s: Expected to be a base32-encoded string, 16 characters long.
        :type s: str
        :return:
        :rtype:
        """
        if '-' in s:
            s = s.replace('-', '')
        self._raw_secret = s.upper().rjust(16, 'A')[0:16]
        self._secret = base64.b32decode(self._raw_secret.encode())

    def __repr__(self):
        """
        A printable format of the object's initial value, for use in saving and restoring.

        :return: Secret key token, as set.
        :rtype: str
        """
        return json.dumps(self, default=instance.to_json, indent=4, sort_keys=True)

    def to_json(self, outer_encoder=None):
        """
        This method implements the serialization of a TwoFactorAuth() object
        for the JSON module to use.

        :param outer_encoder:
        :type outer_encoder:
        :return: JSON serialization
        :rtype: str
        """
        if outer_encoder is None:
            outer_encoder = json.JSONEncoder.default

        cls_name = '__class__/' + __name__ + '.' + self.__class__.__name__
        return {
            cls_name: {
                'secret': outer_encoder(self._raw_secret),
            }
        }

    @classmethod
    def from_json(cls, data, outer_decoder=None):
        """
        This class method implements turning a JSON serialization of the data
        from a TwoFactorAuth() class back into an actual TwoFactorAuth() object.

        :param data:
        :type data:
        :param outer_decoder:
        :type outer_decoder:
        :return: TwoFactorAuth() object or unrecognized data
        :rtype:
        """
        if outer_decoder is None:
            outer_decoder = json.JSONDecoder.decode

        cls_name = '__class__/' + __name__ + '.' + cls.__name__
        if cls_name in data:
            return cls(s=outer_decoder(data[cls_name]['secret']))
        return data


def random_base32_token(length: int=16, rng=random.SystemRandom(),
                        charset='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'):
    """
    This method just provides a quick way to obtain a proper key to
    use for a 2-factor authentication secret key.

    :param length: Normally 16
    :type length: int
    :param rng: Normally, the system RNG
    :type rng: method
    :param charset: The base32 character set
    :type charset: str
    :return: A 16-character base32 encoded token
    :rtype: str
    """
    token = ''.join(rng.choice(charset) for i in range(length))
    return '-'.join((token[0:4], token[4:8], token[8:12], token[12:16]))
