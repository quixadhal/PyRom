import logging

logger = logging.getLogger()

import game_utils
import merc
import interp
import nanny
import state_checks
import handler_ch


def do_where(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Players near you:\n")
        found = False
        for d in merc.descriptor_list:
            victim = handler_ch.CH(d)
            if d.is_connected(nanny.con_playing) \
            and victim \
            and not victim.is_npc() \
            and victim.in_room \
            and not state_checks.IS_SET(merc.rooms[victim.in_room].room_flags, merc.ROOM_NOWHERE) \
            and (ch.is_room_owner(victim.in_room) or not merc.rooms[victim.in_room].is_private()) \
            and merc.rooms[victim.in_room].area == merc.rooms[ch.in_room].area \
            and ch.can_see(victim):
                found = True
                ch.send("%-28s %s\n" % (victim.name, merc.rooms[victim.in_room].name))
        if not found:
            ch.send("None\n")

    else:
        found = False
        for victim in merc.char_list[:]:
            if victim.in_room \
            and merc.rooms[victim.in_room].area == merc.rooms[ch.in_room].area \
            and not victim.is_affected( merc.AFF_HIDE) \
            and not victim.is_affected( merc.AFF_SNEAK) \
            and ch.can_see(victim) \
            and arg in victim.name.lower():
                found = True
                ch.send("%-28s %s\n" % (state_checks.PERS(victim, ch), merc.rooms[victim.in_room].name))
                break
        if not found:
            act("You didn't find any $T.", ch, None, arg, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('where', do_where, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
