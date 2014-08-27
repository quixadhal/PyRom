import hashlib
import logging

logger = logging.getLogger()

import game_utils
import state_checks
import merc
import interp
import settings


def do_password(ch, argument):
    if ch.is_npc():
        return

    # Can't use read_word here because it smashes case.
    # So we just steal all its code.  Bleagh.
    # -- It actually doesn't now because it loads areas too. Davion.
    argument, arg1 = game_utils.read_word(argument, False)
    argument, arg2 = game_utils.read_word(argument, False)

    if not arg1 or not arg2:
        ch.send("Syntax: password <old> <new>.\n")
        return

    if settings.ENCRYPT_PASSWORD:
        # Had to add .encode() for unicode text input.
        arg1 = hashlib.sha512(arg1.encode()).hexdigest()
        arg2 = hashlib.sha512(arg2.encode()).hexdigest()

    if arg1 != ch.pwd:
        state_checks.WAIT_STATE(ch, 40)
        ch.send("Wrong password.  Wait 10 seconds.\n")
        return
    if len(arg2) < 5:
        ch.send("New password must be at least five characters long.\n")
        return

        # No tilde allowed because of player file format.
        # Also now not true. Davion

    ch.pwd = arg2
    ch.save()
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('password', do_password, merc.POS_DEAD, 0, merc.LOG_NEVER, 1))
