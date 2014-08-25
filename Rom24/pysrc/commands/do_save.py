import logging

logger = logging.getLogger()

import merc
import interp
import state_checks


def do_save(ch, argument):
    if ch.is_npc():
        return
    ch.save()
    #save.legacy_save_char_obj(ch)
    ch.send("Saving. Remember that ROM has automatic saving now.\n")
    state_checks.WAIT_STATE(ch, 4 * merc.PULSE_VIOLENCE)
    return


interp.cmd_table['save'] = interp.cmd_type('save', do_save, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)
