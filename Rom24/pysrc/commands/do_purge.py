import logging

logger = logging.getLogger()

import merc
import comm
import interp
import save
import game_utils
import handler_game
import state_checks

def do_purge(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        for victim_id in merc.rooms[ch.in_room].people[:]:
            victim = merc.characters[victim_id]
            if victim.is_npc() and not state_checks.IS_SET(victim.act,
                                                                       merc.ACT_NOPURGE) and victim != ch:  # safety precaution
                victim.extract(True)
        for item_id in merc.rooms[ch.in_room].contents[:]:
            item = merc.items[item_id]
            if not state_checks.IS_OBJ_STAT(item, merc.ITEM_NOPURGE):
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
        if ch.trust <= victim.get_trust():
            ch.send("Maybe that wasn't a good idea...\n")
            victim.send("%s tried to purge you!\n" % ch.name)
            return
        handler_game.act("$n disintegrates $N.", ch, 0, victim, merc.TO_NOTVICT)

        if victim.level > 1:
            save.save_char_obj(victim)
        d = victim.desc
        victim.extract(True)
        if d:
            comm.close_socket(d)
        return
    handler_game.act("$n purges $N.", ch, None, victim, merc.TO_NOTVICT)
    victim.extract(True)
    return


interp.register_command(interp.cmd_type('purge', do_purge, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
