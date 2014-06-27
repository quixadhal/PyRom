import logging

logger = logging.getLogger()

import merc
import interp
import nanny


def do_where(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Players near you:\n")
        found = False
        for d in merc.descriptor_list:
            victim = merc.CH(d)
            if d.is_connected(nanny.con_playing) \
                    and victim \
                    and not merc.IS_NPC(victim) \
                    and victim.in_room \
                    and not merc.IS_SET(victim.in_room.room_flags, merc.ROOM_NOWHERE) \
                    and (ch.is_room_owner(victim.in_room) or not victim.in_room.is_private()) \
                    and victim.in_room.area == ch.in_room.area \
                    and ch.can_see(victim):
                found = True
                ch.send("%-28s %s\n" % (victim.name, victim.in_room.name))
        if not found:
            ch.send("None\n")

    else:
        found = False
        for victim in merc.char_list[:]:
            if victim.in_room \
                    and victim.in_room.area == ch.in_room.area \
                    and not merc.IS_AFFECTED(victim, merc.AFF_HIDE) \
                    and not merc.IS_AFFECTED(victim, merc.AFF_SNEAK) \
                    and ch.can_see(victim) \
                    and arg in victim.name.lower():
                found = True
                ch.send("%-28s %s\n" % (merc.PERS(victim, ch), victim.in_room.name))
                break
        if not found:
            merc.act("You didn't find any $T.", ch, None, arg, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('where', do_where, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
