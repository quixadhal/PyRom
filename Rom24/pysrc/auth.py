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
        trials = [self.time_code(time.time() + offset) for offset in range(-30, 31, 30)]
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
        return json.dumps(self, default=to_json)


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

def to_json(self: TwoFactorAuth):
    """
    A TwoFactorAuth object can be serialized to JSON by
    js = json.dumps(obj, default=auth.to_json)

    :param self: The object to be serialized
    :type self: TwoFactorAuth
    :return: A dictionary of the object's data
    :rtype: dict
    """
    if isinstance(self, TwoFactorAuth):
        return {'__TwoFactorAuth__': True, 'secret': self._raw_secret}
    raise TypeError(repr(self) + " is not JSON serializable")

def from_json(self: str):
    """
    A TwoFactorAuth() object can be reconstructed from JSON data by
    obj = json.loads(js, object_pairs_hook=auth.from_json)

    :param self: JSON data
    :type self: str
    :return: A TwoFactorAuth object
    :rtype: TwoFactorAuth
    """
    ok = False
    for i in self:
        if i[0] == '__TwoFactorAuth__':
            ok = True
    if ok:
        for i in self:
            if i[0] == '__TwoFactorAuth__':
                continue
            elif i[0] == 'secret':
                obj = TwoFactorAuth(i[1])
                return obj
            else:
                raise TypeError(repr(self) + " is not a valid TwoFactorAuth serialization")
    return self
