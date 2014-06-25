import merc
import interp
import save


def do_save(ch, argument):
    if merc.IS_NPC(ch):
        return
    save.save_char_obj( ch )
    ch.send("Saving. Remember that ROM has automatic saving now.\n")
    merc.WAIT_STATE(ch, 4 * merc.PULSE_VIOLENCE)
    return

interp.cmd_table['save'] = interp.cmd_type('save', do_save, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)