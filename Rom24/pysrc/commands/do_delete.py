import os
import merc
import interp
import settings
import fight

def do_delete(self, argument):
    ch=self
    if IS_NPC(ch):
        return

    if ch.pcdata.confirm_delete:
        if argument:
            ch.send("Delete status removed.\n")
            ch.pcdata.confirm_delete = False
            return
        else:
            pfile = os.path.join(settings.PLAYER_DIR, ch.name+'.json')
            merc.wiznet("$N turns $Mself into line noise.",ch,None,0,0,0)
            fight.stop_fighting(ch,True)
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
    merc.wiznet("$N is contemplating deletion.",ch,None,0,0,ch.get_trust())

interp.cmd_type('delete', do_delete, merc.POS_STANDING, 0, merc.LOG_ALWAYS, 1)