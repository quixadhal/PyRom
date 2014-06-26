import merc
import interp
import nanny

def do_help(self, argument):
    ch = self
    if not argument:
        argument = "summary"

    found = [h for h in merc.help_list if h.level <= self.get_trust() and argument.lower() in h.keyword.lower()]

    for pHelp in found:
        if ch.desc.is_connected(nanny.con_playing):
            self.send("\n============================================================\n")
            ch.send(pHelp.keyword)
            ch.send("\n")
        text = pHelp.text
        if pHelp.text[0] == '.':
            text = pHelp.text[1:]
        ch.send(text + "\n")
        # small hack :) */
        if ch.desc and ch.desc.connected != nanny.con_playing and ch.desc.connected != nanny.con_gen_groups:
            break

    if not found:
        self.send("No help on that word.\n")

POS_DEAD = merc.POS_DEAD
LOG_NORMAL  = merc.LOG_NORMAL
IM = merc.IM

interp.cmd_type('help', do_help, POS_DEAD, 0, LOG_NORMAL, 1)
interp.cmd_type('motd', do_help, POS_DEAD, 0, LOG_NORMAL, 1, 'motd')
interp.cmd_type('imotd', do_help, POS_DEAD, IM, LOG_NORMAL, 1, 'imotd')
interp.cmd_type('rules', do_help, POS_DEAD, 0, LOG_NORMAL, 1, 'rules')
interp.cmd_type('story', do_help, POS_DEAD, 0, LOG_NORMAL, 1, 'story')
interp.cmd_type('wizlist', do_help, POS_DEAD, 0, LOG_NORMAL, 1, 'wizlist')
interp.cmd_type('credits', do_help, POS_DEAD, 0, LOG_NORMAL, 1, 'credits')