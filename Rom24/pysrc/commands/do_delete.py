import logging

logger = logging.getLogger()

import os

import handler_game
import state_checks
import merc
import interp
import settings
import fight

def do_delete(ch, argument):
    if ch.is_npc():
        return

    if ch.pcdata.confirm_delete:
        if argument:
            ch.send("Delete status removed.\n")
            ch.pcdata.confirm_delete = False
            return
        else:
            pfile = os.path.join(settings.PLAYER_DIR, ch.name + '.json')
            handler_game.wiznet("$N turns $Mself into line noise.", ch, None, 0, 0, 0)
            fight.stop_fighting(ch, True)
            ch.do_quit("")
            os.remove(pfile)
            return
    if argument:
        ch.send("Just type delete. No argument.\n")
        return

    ch.send("Type delete again to confirm this command.\n")
    ch.send("WARNING: this command is irreversible.\n")
    ch.send("Typing delete with an argument will undo delete status.\n")
    ch.pcdata.confirm_delete = True
    handler_game.wiznet("$N is contemplating deletion.", ch, None, 0, 0, ch.trust)


interp.register_command(interp.cmd_type('delete', do_delete, merc.POS_STANDING, 0, merc.LOG_ALWAYS, 1))
