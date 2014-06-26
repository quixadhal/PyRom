import merc
import interp


def do_snoop(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Snoop whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if not victim.desc:
        ch.send("No descriptor to snoop.\n")
        return
    if victim == ch:
        ch.send("Cancelling all snoops.\n")
        merc.wiznet("$N stops being such a snoop.", ch,None, merc.WIZ_SNOOPS, merc.WIZ_SECURE, ch.get_trust())
        for d in merc.descriptor_list:
            if d.snoop_by == ch.desc:
                d.snoop_by = None
        return
    if victim.desc.snoop_by:
        ch.send("Busy already.\n")
        return
    if not ch.is_room_owner(victim.in_room) and ch.in_room != victim.in_room \
    and victim.in_room.is_private() and not merc.IS_TRUSTED(ch,merc.MAX_LEVEL):
        ch.send("That character is in a private room.\n")
        return
    if victim.get_trust() >= ch.get_trust() or merc.IS_SET(merc.victim.comm, merc.COMM_SNOOP_PROOF):
        ch.send("You failed.\n")
        return
    if ch.desc:
        d = ch.desc.snoop_by
        while d:
            if d.character == victim or d.original == victim:
                ch.send("No snoop loops.\n")
                return
            d = d.snoop_by
    victim.desc.snoop_by = ch.desc
    buf = "$N starts snooping on %s" % (victim.short_descr if merc.IS_NPC(ch) else victim.name)
    merc.wiznet(buf, ch, None, merc.WIZ_SNOOPS, merc.WIZ_SECURE, ch.get_trust())
    ch.send("Ok.\n")
    return

interp.cmd_type('snoop', do_snoop, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)