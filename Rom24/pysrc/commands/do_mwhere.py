import logging

logger = logging.getLogger()

import handler_game
import merc
import interp
import nanny
import instance


def do_mwhere(ch, argument):
    count = 0
    if not argument:
        # show characters logged
        for d in merc.descriptor_list:
            if d.character and d.is_connected(nanny.con_playing) \
                    and d.character.in_room and ch.can_see(d.character) \
                    and ch.can_see_room(d.character.in_room.instance_id):
                victim = d.character
                count += 1
            if d.original:
                ch.send("%3d) %s (in the body of %s) is in %s [[%d]]\n" % (
                    count, d.original.name, victim.short_descr,
                    victim.in_room.name, victim.in_room.vnum))
            else:
                ch.send("%3d) %s is in %s [[%d]]\n" % (
                    count, victim.name, victim.in_room.name, victim.in_room.vnum))
        return
    found = False
    for victim in instance.characters.values():
        if victim.in_room and argument in victim.name:
            found = True
            count += 1
            ch.send("%3d) [[%5d]] %-28s [[%5d]] %s\n" % (
                count, 0 if not victim.is_npc() else victim.vnum,
                victim.short_descr if victim.is_npc() else victim.name,
                victim.in_room.vnum,
                victim.in_room.name ))
    if not found:
        handler_game.act("You didn't find any $T.", ch, None, argument, merc.TO_CHAR)


interp.register_command(interp.cmd_type('mwhere', do_mwhere, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1))
