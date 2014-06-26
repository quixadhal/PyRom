import merc
import interp
import fight


def do_goto(ch, argument):
    if not argument:
        ch.send("Goto where?\n")
        return
    location = merc.find_location(ch, argument)
    if not location:
        ch.send("No such location.\n")
        return
    count = len(location.people)
    if not ch.is_room_owner(location) and location.is_private() \
    and (count > 1 or ch.get_trust() < merc.MAX_LEVEL):
        ch.send("That room is private right now.\n")
        return
    if ch.fighting:
        fight.stop_fighting(ch, True)
    for rch in ch.in_room.people:
        if rch.get_trust() >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfout:
                merc.act("$t", ch, ch.pcdata.bamfout, rch, merc.TO_VICT)
            else:
                merc.act("$n leaves in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.from_room()
    ch.to_room(location)

    for rch in ch.in_room.people:
        if rch.get_trust() >= ch.invis_level:
            if ch.pcdata and ch.pcdata.bamfin:
                merc.act("$t", ch, ch.pcdata.bamfin, rch, merc.TO_VICT)
            else:
                merc.act("$n appears in a swirling mist.", ch, None, rch, merc.TO_VICT)
    ch.do_look("auto" )
    return

interp.cmd_type('goto', do_goto, merc.POS_DEAD, merc.L8, merc.LOG_NORMAL, 1)