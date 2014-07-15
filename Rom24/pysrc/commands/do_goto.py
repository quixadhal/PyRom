import logging

logger = logging.getLogger()

import merc
import interp
import fight
import game_utils


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
    for rch in merc.rooms[ch.in_room].people:
        if rch.trust >= ch.invis_level:
            if ch.pcdata and ch.bamfout:
                act("$t", ch, ch.bamfout, rch, merc.TO_VICT)
            else:
                act("$n leaves in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.from_environment()
    ch.to_environment(location)

    for rch in merc.rooms[ch.in_room].people:
        if rch.trust >= ch.invis_level:
            if ch.pcdata and ch.bamfin:
                act("$t", ch, ch.bamfin, rch, merc.TO_VICT)
            else:
                act("$n appears in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.do_look("auto")
    return


interp.register_command(interp.cmd_type('goto', do_goto, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1))
