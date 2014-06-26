import merc
import interp


def do_rstat(ch, argument):
    argument, arg = merc.read_word(argument)
    location = ch.in_room if not arg else merc.find_location(ch, arg)
    if not location:
        ch.send("No such location.\n")
        return

    if not ch.is_room_owner(location) and ch.in_room != location \
    and location.is_private() and not merc.IS_TRUSTED(ch, merc.MAX_LEVEL):
        ch.send("That room is private right now.\n")
        return
    ch.send("Name: '%s'\nArea: '%s'\n" % (location.name, location.area.name))
    ch.send("Vnum: %d  Sector: %d  Light: %d  Healing: %d  Mana: %d\n" % (
              location.vnum,
              location.sector_type,
              location.light,
              location.heal_rate,
              location.mana_rate))
    ch.send("Room flags: %d.\nDescription:\n%s" % (location.room_flags, location.description))
    if location.extra_descr:
        ch.send("Extra description keywords: '")
        [ch.send(ed.keyword + " ") for ed in location.extra_descr]
        ch.send("'.\n")

    ch.send("Characters:")
    for rch in location.people:
        if ch.can_see(rch):
            ch.send("%s " % rch.name if not merc.IS_NPC(rch) else rch.short_descr)
    ch.send(".\nObjects:   ")
    for obj in location.contents:
        ch.send("'%s' " % obj.name )
    ch.send(".\n")
    for pexit in location.exit:
        if pexit:
            ch.send("Door: %d.  To: %d.  Key: %d.  Exit flags: %d.\nKeyword: '%s'.  Description: %s" % (
            door,
            -1 if pexit.to_room == None else pexit.to_room.vnum,
            pexit.key,
            pexit.exit_info,
            pexit.keyword,
            pexit.description if pexit.description else "(none).\n" ) )
    return

interp.cmd_type('rstat', do_rstat, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)