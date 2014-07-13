import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_alias(ch, argument):
    if rch.is_npc():
        return

    argument, arg = game_utils.read_word(argument)
    if not arg:
        if not rch.alias:
            ch.send("You have no aliases defined.\n")
            return
        ch.send("Your current aliases are:\n")

        for alias, sub in rch.alias.iteritems():
            ch.send("    %s:  %s\n" % (alias, sub))
        return

    if "unalias" == arg or "alias" == arg:
        ch.send("Sorry, that word is reserved.\n")
        return

    if not argument:
        if arg not in rch.alias:
            ch.send("That alias is not defined.\n")
            return
        ch.send("%s aliases to '%s'.\n" % (arg, rch.alias[arg]))
        return

    if argument.startswith("delete") or argument.startswith("prefix"):
        ch.send("That shall not be done!\n")
        return

    if arg in rch.alias:
        rch.alias[arg] = argument
        ch.send("%s is now realiased to '%s'.\n" % (arg, argument))
        return
    elif len(rch.alias) > merc.MAX_ALIAS:
        ch.send("Sorry, you have reached the alias limit.\n")
        return
    rch.alias[arg] = argument
    ch.send("%s is now aliased to '%s'.\n" % (arg, argument))
    return


interp.register_command(interp.cmd_type('alias', do_alias, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
