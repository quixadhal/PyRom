import logging

logger = logging.getLogger(__name__)

from rom24 import handler_game
from rom24 import merc
from rom24 import comm
from rom24 import interp
from rom24 import game_utils
from rom24 import state_checks
from rom24 import instance


def do_purge(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        for victim_id in ch.in_room.people:
            victim = instance.characters[victim_id]
            if (
                victim.is_npc()
                and not state_checks.IS_SET(victim.act, merc.ACT_NOPURGE)
                and victim != ch
            ):  # safety precaution
                victim.in_room.get(victim)
                victim.extract(True)
        for item_id in ch.in_room.items:
            item = instance.items[item_id]
            if not item.flags.no_purge:
                ch.in_room.get(item)
                item.extract()
        handler_game.act("$n purges the room!", ch, None, None, merc.TO_ROOM)
        ch.send("Ok.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if not victim.is_npc():
        if ch == victim:
            ch.send("Ho ho ho.\n")
            return
        if ch.trust <= victim.trust:
            ch.send("Maybe that wasn't a good idea...\n")
            victim.send("%s tried to purge you!\n" % ch.name)
            return
        handler_game.act("$n disintegrates $N.", ch, 0, victim, merc.TO_NOTVICT)

        if victim.level > 1:
            victim.save(logout=True, force=True)
        d = victim.desc
        victim.in_room.get(victim)
        victim.extract(True)
        if d:
            comm.close_socket(d)
        return
    handler_game.act("$n purges $N.", ch, None, victim, merc.TO_NOTVICT)
    victim.extract(True)
    return


interp.register_command(
    interp.cmd_type("purge", do_purge, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1)
)
