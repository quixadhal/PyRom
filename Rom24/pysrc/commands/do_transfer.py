import merc
import fight
import interp
import nanny


def do_transfer(ch, argument):
    argument, arg1  = merc.read_word(argument)
    argument, arg2  = merc.read_word(argument)
    if not arg1:
        ch.send("Transfer whom (and where)?\n")
        return
    if arg1 == "all" :
        for d in merc.descriptor_list:
            if d.is_connected(nanny.con_playing) \
            and d.character != ch \
            and d.character.in_room \
            and ch.can_see(d.character):
                 ch.do_transfer("%s %s" % d.character.name, arg2 )
        return
    # * Thanks to Grodyn for the optional location parameter.
    if not arg2:
        location = ch.in_room
    else:
        location = merc.find_location(ch, arg2)
        if not location:
            ch.send("No such location.\n")
            return
        if not ch.is_room_owner(location) and location.is_private() \
        and ch.get_trust() < merc.MAX_LEVEL:
            ch.send("That room is private right now.\n")
            return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.in_room == None:
        ch.send("They are in limbo.\n")
        return

    if victim.fighting:
        fight.stop_fighting(victim, True)
    merc.act("$n disappears in a mushroom cloud.", victim, None, None, merc.TO_ROOM)
    victim.from_room()
    victim.to_room(location)
    act("$n arrives from a puff of smoke.", victim, None, None, merc.TO_ROOM)
    if ch != victim:
        merc.act("$n has transferred you.", ch, None, victim, merc.TO_VICT)
    victim.do_look("auto")
    ch.send("Ok.\n")

interp.cmd_table['teleport'] = interp.cmd_type('teleport', do_transfer, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)
interp.cmd_table['transfer'] = interp.cmd_type('transfer', do_transfer, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)