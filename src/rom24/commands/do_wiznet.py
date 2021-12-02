import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import const
from rom24 import state_checks


def do_wiznet(ch, argument):
    if not argument:
        if state_checks.IS_SET(ch.wiznet, merc.WIZ_ON):
            ch.send("Signing off of Wiznet.\n")
            ch.wiznet = state_checks.REMOVE_BIT(ch.wiznet, merc.WIZ_ON)
        else:
            ch.send("Welcome to Wiznet!\n")
            ch.wiznet = state_checks.SET_BIT(ch.wiznet, merc.WIZ_ON)
        return

    if "on".startswith(argument):
        ch.send("Welcome to Wiznet!\n")
        ch.wiznet = state_checks.SET_BIT(ch.wiznet, merc.WIZ_ON)
        return
    if "off".startswith(argument):
        ch.send("Signing off of Wiznet.\n")
        ch.wiznet = state_checks.REMOVE_BIT(ch.wiznet, merc.WIZ_ON)
        return
    buf = ""
    # show wiznet status
    if "status".startswith(argument):
        if not state_checks.IS_SET(ch.wiznet, merc.WIZ_ON):
            buf += "off "
        for name, flag in const.wiznet_table.items():
            if state_checks.IS_SET(ch.wiznet, flag.bit):
                buf += name + " "
            ch.send("Wiznet status:\n%s\n" % buf)
            return
    if "show".startswith(argument):
        # list of all wiznet options
        buf = ""
        for name, flag in const.wiznet_table.items():
            if flag.level <= ch.trust:
                buf += name + " "
        ch.send("Wiznet options available to you are:\n%s\n" % buf)
        return
    flag = state_checks.prefix_lookup(const.wiznet_table, argument)
    if not flag or ch.trust < flag.level:
        ch.send("No such option.\n")
        return
    if state_checks.IS_SET(ch.wiznet, flag.bit):
        ch.send("You will no longer see %s on wiznet.\n" % flag.name)
        ch.wiznet = state_checks.REMOVE_BIT(ch.wiznet, flag.bit)
        return
    else:
        ch.send("You will now see %s on wiznet.\n" % flag.name)
        ch.wiznet = state_checks.SET_BIT(ch.wiznet, flag.bit)
        return


interp.register_command(
    interp.cmd_type("wiznet", do_wiznet, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)
)
