import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


def do_alias(ch, argument):
    if ch.is_npc():
        return

    argument, arg = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg:
        if not ch.alias:
            ch.send("You have no aliases defined.\n")
            return
        ch.send("Your current aliases are:\n")

        for alias, sub in ch.alias.iteritems():
            ch.send("    %s:  %s\n" % (alias, sub))
        return

    if "unalias" == arg or "alias" == arg:
        ch.send("Sorry, that word is reserved.\n")
        return

    if not arg2:
        if arg not in ch.alias:
            ch.send("That alias is not defined.\n")
            return
        ch.send("%s aliases to '%s'.\n" % (arg, ch.alias[arg]))
        return

    if arg2.startswith("delete") or arg2.startswith("prefix"):
        ch.send("That shall not be done!\n")
        return

    if arg2 in ch.alias:
        ch.alias[arg] = arg2
        ch.send("%s is now realiased to '%s'.\n" % (arg, arg2))
        return
    elif len(ch.alias) > merc.MAX_ALIAS:
        ch.send("Sorry, you have reached the alias limit.\n")
        return
    ch.alias[arg] = arg2
    ch.send("%s is now aliased to '%s'.\n" % (arg, arg2))
    return

def do_alia(ch, argument):
    ch.send("I'm sorry, alias must be entered in full.\n")
    return

interp.register_command(interp.cmd_type('alias', do_alias, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('alia', do_alia, merc.POS_DEAD, 0, merc.LOG_NORMAL, 0))

