import logging

logger = logging.getLogger()

import handler_log
import merc
import interp
import save
import comm
import handler_ch
import handler_game
import state_checks


@handler_log.logged("Debug")
def do_quit(ch, argument):
    if ch.is_npc():
        return
    if ch.position == merc.POS_FIGHTING:
        ch.send("No way! You are fighting.\n")
        return
    if ch.position < merc.POS_STUNNED:
        ch.send("You're not DEAD yet.\n")
        return
    ch.send("Alas, all good things must come to an end.\n")
    handler_game.act("$n has left the game.", ch, None, None, merc.TO_ROOM)
    logger.info("%s has quit.", ch.name)
    handler_game.wiznet("$N rejoins the real world.", ch, None, merc.WIZ_LOGINS, 0, ch.trust)
    # After extract_char the ch is no longer valid!
    save.save_char_obj(ch)
    id = ch.id
    d = ch.desc
    ch.extract(True)
    if d is not None:
        comm.close_socket(d)

    # toast evil cheating bastards
    for d in merc.descriptor_list[:]:
        tch = handler_ch.CH(d)
        if tch and tch.id == id:
            tch.extract(True)
            comm.close_socket(d)
    return


interp.register_command(interp.cmd_type('quit', do_quit, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
