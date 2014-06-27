import logging

logger = logging.getLogger()

import merc
import interp
import const


def do_wiznet(ch, argument):
    if not argument:
        if merc.IS_SET(ch.wiznet, merc.WIZ_ON):
            ch.send("Signing off of Wiznet.\n")
            ch.wiznet = merc.REMOVE_BIT(ch.wiznet, merc.WIZ_ON)
        else:
            ch.send("Welcome to Wiznet!\n")
            ch.wiznet = merc.SET_BIT(ch.wiznet, merc.WIZ_ON)
        return

    if "on".startswith(argument):
        ch.send("Welcome to Wiznet!\n")
        ch.wiznet = merc.SET_BIT(ch.wiznet, merc.WIZ_ON)
        return
    if "off".startswith(argument):
        ch.send("Signing off of Wiznet.\n")
        ch.wiznet = merc.REMOVE_BIT(ch.wiznet, merc.WIZ_ON)
        return
    buf = ''
    # show wiznet status
    if "status".startswith(argument):
        if not merc.IS_SET(ch.wiznet, merc.WIZ_ON):
            buf += "off "
        for name, flag in const.wiznet_table.items():
            if merc.IS_SET(ch.wiznet, flag.flag):
                buf += name + " "
            ch.send("Wiznet status:\n%s\n" % buf)
            return
    if "show".startswith(argument):
        # list of all wiznet options
        buf = ''
        for name, flag in const.wiznet_table.items():
            if flag.level <= ch.get_trust():
                buf += name + " "
        ch.send("Wiznet options available to you are:\n%s\n" % buf)
        return
    flag = merc.prefix_lookup(const.wiznet_table, argument)
    if not flag or ch.get_trust() < flag.level:
        ch.send("No such option.\n")
        return
    if merc.IS_SET(ch.wiznet, flag.flag):
        ch.send("You will no longer see %s on wiznet.\n" % flag.name)
        ch.wiznet = merc.REMOVE_BIT(ch.wiznet, flag.flag)
        return
    else:
        ch.send("You will now see %s on wiznet.\n" % flag.name)
        ch.wiznet = merc.SET_BIT(ch.wiznet, flag.flag)
        return


interp.register_command(interp.cmd_type('wiznet', do_wiznet, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
