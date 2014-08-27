import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks
import instance

#TODO: Known broken. Exit flags or locks are messed up.
def do_rstat(ch, argument):
    argument, arg = game_utils.read_word(argument)
    location = ch.in_room if not arg else game_utils.find_location(ch, arg)
    if not location:
        ch.send("No such location.\n")
        return

    if not ch.is_room_owner(location) and ch.in_room != location \
            and location.is_private() and not state_checks.IS_TRUSTED(ch, merc.MAX_LEVEL):
        ch.send("That room is private right now.\n")
        return
    ch.send("Name: '%s'\nArea: '%s'\n" % (location.name, location.area))
    ch.send("Vnum: %d  Sector: %d  Light: %d  Healing: %d  Mana: %d\n" % (
        location.vnum,
        location.sector_type,
        location.available_light,
        location.heal_rate,
        location.mana_rate))
    ch.send("Room flags: %d.\nDescription:\n%s" % (location.room_flags, location.description))
    if location.extra_descr:
        ch.send("Extra description keywords: '")
        [ch.send(ed.keyword + " ") for ed in location.extra_descr]
        ch.send("'.\n")

    ch.send("Characters:")
    for rch_id in location.people:
        rch = instance.characters[rch_id]
        if ch.can_see(rch):
            ch.send("%s " % rch.name if not rch.is_npc() else rch.short_descr)
    ch.send(".\nObjects:   ")
    for obj_id in location.inventory[:]:
        obj = instance.global_instances[obj_id]
        ch.send("'%s' " % obj.name)
    ch.send(".\n")
    for door, pexit in enumerate(location.exit):
        if pexit:
            ch.send("Door: %d.  To: %d.  Key: %d.  Exit flags: %d.\nKeyword: '%s'.  Description: %s" % (
                door,  # TODO:  come back and fix this
                -1 if pexit.to_room is None else instance.rooms[pexit.to_room].vnum,
                -1 if pexit.key is None else pexit.key,
                pexit.exit_info,
                pexit.keyword,
                pexit.description if pexit.description else "(none).\n" ))
    return


interp.register_command(interp.cmd_type('rstat', do_rstat, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
