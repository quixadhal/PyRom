__author__ = 'quixadhal'

import hashlib
import logging
logger = logging.getLogger()

import auth
import game_utils
import interp
import merc


def do_authenticator(ch, argument):
    if ch.is_npc():
        return

    argument, arg1 = game_utils.read_word(argument, False)
    argument, arg2 = game_utils.read_word(argument, False)

    if not arg1 or not arg2:
        ch.send('Authenticator %s.\n' % ('active' if ch.auth else 'disabled'))
        ch.send('Usage:  authenticator <on|off> <password> [token]\n')
        if ch.auth:
            import time
            import sys_utils
            trials = [ch.auth.time_code(time.time() + offset) for offset in (-30, 0, 30)]
            ch.send('DEBUG: %s - %s, %r\n' % (sys_utils.sysTimeStamp(time.time()), ch.auth.secret, trials))
        return

    arg1 = arg1.lower()
    if arg1 == 'on' or arg1 == 'activate' or arg1 == 'enable' or arg1 == 'add':
        if ch.auth:
            ch.send('Authentication is already active.\n')
            return
        else:
            pwd = hashlib.sha512(arg2.encode()).hexdigest()
            if pwd != ch.pwd:
                ch.send('Wrong password.  Operation cancelled.\n')
                return
            else:
                secret = auth.random_base32_token()
                ch.auth = auth.TwoFactorAuth(secret)
                ch.save()
                ch.send('Authentication is now active!\n')
                ch.send('You must now use Google Authenticator to log in.\n')
                ch.send('Please add a new time-based account to your authenticator, using %s as the code.\n' %
                        ch.auth.secret)
                ch.send('If you don\'t have a smartphone app, you can get a Windows version at https://winauth.com/\n')
                return

    if arg1 == 'off' or arg1 == 'deactivate' or arg1 == 'disable' or arg1 == 'remove':
        if not ch.auth:
            ch.send('Authentication is not active.\n')
            return
        else:
            pwd = hashlib.sha512(arg2.encode()).hexdigest()
            if pwd != ch.pwd:
                ch.send('Wrong password.  Operation cancelled.\n')
                return
            else:
                argument, arg3 = game_utils.read_word(argument, False)
                if not arg3:
                    ch.send('You must provide the current auth token to remove your authenticator.\n')
                    return
                elif not ch.auth.verify(arg3):
                    ch.send('Incorrect token.  Operation cancelled.\n')
                    return
                else:
                    ch.auth = None
                    ch.save()
                    ch.send('Authentication is now disabled.\n')
                    return


interp.register_command(interp.cmd_type('authenticator', do_authenticator, merc.POS_DEAD, 0, merc.LOG_NEVER, 1))
