import logging

logger = logging.getLogger()

import merc
import interp
import handler_game


def do_report(ch, argument):
    ch.send("You say 'I have %d/%d hp %d/%d mana %d/%d mv %d xp.'\n" % (
        ch.hit, ch.max_hit,
        ch.mana, ch.max_mana,
        ch.move, ch.max_move,
        ch.exp  ))
    buf = "$n says 'I have %d/%d hp %d/%d mana %d/%d mv %d xp.'" % (
        ch.hit, ch.max_hit,
        ch.mana, ch.max_mana,
        ch.move, ch.max_move,
        ch.exp  )
    handler_game.act(buf, ch, None, None, merc.TO_ROOM)
    return


interp.register_command(interp.cmd_type('report', do_report, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
