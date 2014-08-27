#Thanks to this post http://stackoverflow.com/questions/5597836/how-can-i-embedcreate-an-interactive-python-shell-in-my-python-program
# I'm setting up a small environment for testing.

import code
import logging

logger = logging.getLogger()

import db

db.boot_db()


def send(txt):
    print(txt)

vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()
