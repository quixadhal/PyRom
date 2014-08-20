import logging

logger = logging.getLogger()

import merc
import interp


def do_description(ch, argument):
    if argument:
        if argument[0] == '-':
            if not ch.description:
                ch.send("No lines left to remove.\n")
                return
            buf = ch.description.split('\n')
            buf.pop()
            ch.description = '\n'.join(buf)
            if len(buf) > 1:
                ch.send("Your description is:\n")
                ch.send(ch.description if ch.description else "(None).\n")
                return
            else:
                ch.description = ""
                ch.send("Description cleared.\n")
                return
        if argument[0] == '+':
            argument = argument[1:].lstrip()

            if len(argument) + len(ch.description) >= 1024:
                ch.send("Description too long.\n")
                return
            ch.description += argument + "\n"

    ch.send("Your description is:\n")
    ch.send(ch.description if ch.description else "(None).\n")
    return


interp.register_command(interp.cmd_type('description', do_description, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
