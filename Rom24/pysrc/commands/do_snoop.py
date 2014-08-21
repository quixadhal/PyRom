import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


def do_snoop(ch, argument):
    argument, arg = game_utils.read_word(argument)
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
        handler_game.wiznet("$N stops being such a snoop.", ch, None, merc.WIZ_SNOOPS, merc.WIZ_SECURE, ch.trust)
        for d in merc.descriptor_list:
            if d.snoop_by == ch.desc:
                d.snoop_by = None
        return
    if victim.desc.snoop_by:
        ch.send("Busy already.\n")
        return
    if not ch.is_room_owner(victim.in_room) and ch.in_room != victim.in_room \
            and victim.in_room.is_private() and not state_checks.IS_TRUSTED(ch, merc.MAX_LEVEL):
        ch.send("That character is in a private room.\n")
        return
    if victim.trust >= ch.trust or victim.comm.is_set(merc.COMM_SNOOP_PROOF):
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
    buf = "$N starts snooping on %s" % (victim.short_descr if ch.is_npc() else victim.name)
    handler_game.wiznet(buf, ch, None, merc.WIZ_SNOOPS, merc.WIZ_SECURE, ch.trust)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('snoop', do_snoop, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
