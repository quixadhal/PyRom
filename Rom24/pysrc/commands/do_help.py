import logging

logger = logging.getLogger()

import merc
import interp
import nanny


def do_help(ch, argument):
    if not argument:
        argument = "summary"

    found = [h for h in merc.help_list if h.level <= ch.trust and argument.lower() in h.keyword.lower()]

    for pHelp in found:
        if ch.desc.is_connected(nanny.con_playing):
            ch.send("\n============================================================\n")
            ch.send(pHelp.keyword)
            ch.send("\n")
        text = pHelp.text
        if pHelp.text[0] == '.':
            text = pHelp.text[1:]
        ch.send(text + "\n")
        # small hack :)
        if ch.desc and ch.desc.connected != nanny.con_playing and ch.desc.connected != nanny.con_gen_groups:
            break

    if not found:
        ch.send("No help on that word.\n")


interp.register_command(interp.cmd_type('help', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('motd', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1, 'motd'))
interp.register_command(interp.cmd_type('imotd', do_help, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1, 'imotd'))
interp.register_command(interp.cmd_type('rules', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1, 'rules'))
interp.register_command(interp.cmd_type('story', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1, 'story'))
interp.register_command(interp.cmd_type('wizlist', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1, 'wizlist'))
interp.register_command(interp.cmd_type('credits', do_help, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1, 'credits'))
