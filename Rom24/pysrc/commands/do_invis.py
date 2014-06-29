import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game

# New routines by Dionysos.
def do_invis(ch, argument):
    # RT code for taking a level argument
    argument, arg = game_utils.read_word(argument)
    if not arg:
        # take the default path
        if ch.invis_level:
            ch.invis_level = 0
            handler_game.act("$n slowly fades into existence.", ch, None, None, merc.TO_ROOM)
            ch.send("You slowly fade back into existence.\n")
        else:
            ch.invis_level = ch.trust
            handler_game.act("$n slowly fades into thin air.", ch, None, None, merc.TO_ROOM)
            ch.send("You slowly vanish into thin air.\n")
    else:
        # do the level thing
        level = int(arg) if arg.isdigit() else -1
        if level < 2 or level > ch.trust:
            ch.send("Invis level must be between 2 and your level.\n")
            return
        else:
            ch.reply = None
            ch.invis_level = level
            handler_game.act("$n slowly fades into thin air.", ch, None, None, merc.TO_ROOM)
            ch.send("You slowly vanish into thin air.\n")
            return


interp.register_command(interp.cmd_type('invis', do_invis, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 0))
interp.register_command(interp.cmd_type('wizinvis', do_invis, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
