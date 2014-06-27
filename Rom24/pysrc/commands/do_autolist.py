import logging

logger = logging.getLogger()

import merc
import interp

# RT this following section holds all the auto commands from ROM, as well as
# replacements for config
def do_autolist(ch, argument):
    # lists most player flags
    if merc.IS_NPC(ch):
        return
    ch.send("   action     status\n")
    ch.send("---------------------\n")
    ch.send("autoassist     ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOASSIST):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("autoexit       ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOEXIT):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("autogold       ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOGOLD):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("autoloot       ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOLOOT):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("autosac        ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOSAC):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("autosplit      ")
    if merc.IS_SET(ch.act, merc.PLR_AUTOSPLIT):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("compact mode   ")
    if merc.IS_SET(ch.comm, merc.COMM_COMPACT):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("prompt         ")
    if merc.IS_SET(ch.comm, merc.COMM_PROMPT):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    ch.send("combine items  ")
    if merc.IS_SET(ch.comm, merc.COMM_COMBINE):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    if not merc.IS_SET(ch.act, merc.PLR_CANLOOT):
        ch.send("Your corpse is safe from thieves.\n")
    else:
        ch.send("Your corpse may be looted.\n")
    if merc.IS_SET(ch.act, merc.PLR_NOSUMMON):
        ch.send("You cannot be summoned.\n")
    else:
        ch.send("You can be summoned.\n")
    if merc.IS_SET(ch.act, merc.PLR_NOFOLLOW):
        ch.send("You do not welcome followers.\n")
    else:
        ch.send("You accept followers.\n")


interp.register_command(interp.cmd_type('autolist', do_autolist, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
