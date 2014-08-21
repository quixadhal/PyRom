import logging

logger = logging.getLogger()

import merc
import interp
import state_checks

# RT code to display channel status
def do_channels(ch, argument):
    # lists all channels and their status
    ch.send("   channel     status\n")
    ch.send("---------------------\n")
    ch.send("gossip         ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOGOSSIP):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("auction        ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOAUCTION):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("music          ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOMUSIC):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("Q/A            ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOQUESTION):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("Quote          ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOQUOTE):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("grats          ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_NOGRATS):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    if ch.is_immortal():
        ch.send("god channel    ")
        if not state_checks.IS_SET(ch.comm, merc.COMM_NOWIZ):
            ch.send("ON\n")
        else:
            ch.send("OFF\n")
    ch.send("shouts         ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_SHOUTSOFF):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("tells          ")
    if not state_checks.IS_SET(ch.comm, merc.COMM_DEAF):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("quiet mode     ")
    if state_checks.IS_SET(ch.comm, merc.COMM_QUIET):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    if state_checks.IS_SET(ch.comm, merc.COMM_AFK):
        ch.send("You are AFK.\n")
    if state_checks.IS_SET(ch.comm, merc.COMM_SNOOP_PROOF):
        ch.send("You are immune to snooping.\n")
    if ch.lines != merc.PAGELEN:
        if ch.lines:
            ch.send("You display %d lines of scroll.\n" % ch.lines + 2)
        else:
            ch.send("Scroll buffering is off.\n")
    if ch.prompt:
        ch.send("Your current prompt is: %s\n" % ch.prompt)
    if state_checks.IS_SET(ch.comm, merc.COMM_NOSHOUT):
        ch.send("You cannot shout.\n")
    if state_checks.IS_SET(ch.comm, merc.COMM_NOTELL):
        ch.send("You cannot use tell.\n")
    if state_checks.IS_SET(ch.comm, merc.COMM_NOCHANNELS):
        ch.send("You cannot use channels.\n")
    if state_checks.IS_SET(ch.comm, merc.COMM_NOEMOTE):
        ch.send("You cannot show emotions.\n")


interp.register_command(interp.cmd_type('channels', do_channels, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
