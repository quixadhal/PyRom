import merc
import interp


def do_alias(ch, argument):
    if not ch.desc:
        rch = ch
    else:
        rch = ch.desc.original if ch.desc.original else ch

    if merc.IS_NPC(rch):
        return

    argument, arg = merc.read_word(argument)
    if not arg:
        if not rch.pcdata.alias:
            ch.send("You have no aliases defined.\n\r")
            return
        ch.send("Your current aliases are:\n\r")

        for alias,sub in rch.pcdata.alias.iteritems():
            ch.send("    %s:  %s\n\r" % (alias, sub) )
        return

    if "unalias" ==  arg or "alias" == arg:
        ch.send("Sorry, that word is reserved.\n\r")
        return

    if not argument:
        if arg not in rch.pcdata.alias:
            ch.send("That alias is not defined.\n\r")
            return
        ch.send("%s aliases to '%s'.\n\r" % (arg, rch.pcdata.alias[arg]) )
        return

    if argument.startswith("delete") or argument.startswith("prefix"):
        ch.send("That shall not be done!\n\r")
        return

    if arg in rch.pcdata.alias:
        rch.pcdata.alias[arg] = argument
        ch.send("%s is now realiased to '%s'.\n\r" % (arg,argument) )
        return
    elif len(rch.pcdata.alias) > merc.MAX_ALIAS:
        ch.send("Sorry, you have reached the alias limit.\r\n")
        return
    rch.pcdata.alias[arg] = argument
    ch.send("%s is now aliased to '%s'.\n\r" % (arg,argument) )
    return

interp.cmd_type('alias', do_alias, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)