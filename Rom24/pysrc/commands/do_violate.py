import logging

logger = logging.getLogger()

import merc
import interp
import fight
import game_utils
import handler_game


def do_violate(ch, argument):
    if not argument:
        ch.send("Goto where?\n")
        return
    location = game_utils.find_location(ch, argument)
    if not location:
        ch.send("No such location.\n")
        return
    if not location.is_private():
        ch.send("That room isn't private, use goto.\n")
        return
    if ch.fighting:
        fight.stop_fighting(ch, True)

    for rch in merc.rooms[ch.in_room].people:
        if rch.trust >= ch.invis_level:
            if ch.pcdata and ch.bamfout:
                handler_game.act("$t", ch, ch.bamfout, rch, merc.TO_VICT)
            else:
                handler_game.act("$n leaves in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.from_room()
    ch.to_room(location)

    for rch in merc.rooms[ch.in_room].people:
        if rch.trust >= ch.invis_level:
            if ch.pcdata and ch.bamfin:
                handler_game.act("$t", ch, ch.bamfin, rch, merc.TO_VICT)
            else:
                handler_game.act("$n appears in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.do_look("auto")
    return


interp.register_command(interp.cmd_type('violate', do_violate, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))
