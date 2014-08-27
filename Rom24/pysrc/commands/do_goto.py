import logging

logger = logging.getLogger()

import handler_game
import merc
import interp
import fight
import game_utils
import instance


def do_goto(ch, argument):
    if not argument:
        ch.send("Goto where?\n")
        return
    location = game_utils.find_location(ch, argument)
    if not location:
        ch.send("No such location.\n")
        return
    count = len(location.people)
    if not ch.is_room_owner(location) and location.is_private() \
            and (count > 1 or ch.trust < merc.MAX_LEVEL):
        ch.send("That room is private right now.\n")
        return
    if ch.fighting:
        fight.stop_fighting(ch, True)
    for rch_id in ch.in_room.people[:]:
        rch = instance.characters[rch_id]
        if rch.trust >= ch.invis_level:
            if ch.is_npc() and ch.bamfout:
                handler_game.act("$t", ch, ch.bamfout, rch, merc.TO_VICT)
            else:
                handler_game.act("$n leaves in a swirling mist.", ch, None, rch, merc.TO_VICT)
    location.put(ch.in_room.get(ch))

    for rch_id in ch.in_room.people[:]:
        rch = instance.characters[rch_id]
        if rch.trust >= ch.invis_level:
            if ch.is_npc() and ch.bamfin:
                handler_game.act("$t", ch, ch.bamfin, rch, merc.TO_VICT)
            else:
                handler_game.act("$n appears in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.do_look("auto")
    return


interp.register_command(interp.cmd_type('goto', do_goto, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1))
