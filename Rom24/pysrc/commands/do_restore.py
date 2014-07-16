import logging

logger = logging.getLogger()

import merc
import interp
import fight
import game_utils
import handler_game


def do_restore(ch, argument):
    junky, arg = game_utils.read_word(argument)
    if not arg or arg == "room":
        # cure room
        for vch in ch.in_room.people:
            vch.affect_strip("plague")
            vch.affect_strip("poison")
            vch.affect_strip("blindness")
            vch.affect_strip("sleep")
            vch.affect_strip("curse")
            vch.hit = vch.max_hit
            vch.mana = vch.max_mana
            vch.move = vch.max_move
            fight.update_pos(vch)
            act("$n has restored you.", ch, None, vch, merc.TO_VICT)
        handler_game.wiznet("$N restored room %d." % ch.in_room.vnum, ch, None, merc.WIZ_RESTORE, merc.WIZ_SECURE,
                    ch.trust)
        ch.send("Room restored.\n")
        return
    if ch.trust >= merc.MAX_LEVEL - 1 and arg == "all":
        # cure all
        for d in merc.descriptor_list:
            victim = d.character
            if victim is None or victim.is_npc():
                continue
            victim.affect_strip("plague")
            victim.affect_strip("poison")
            victim.affect_strip("blindness")
            victim.affect_strip("sleep")
            victim.affect_strip("curse")
            victim.hit = victim.max_hit
            victim.mana = victim.max_mana
            victim.move = victim.max_move
            fight.update_pos(victim)
            if victim.in_room:
                act("$n has restored you.", ch, None, victim, merc.TO_VICT)
        ch.send("All active players restored.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    victim.affect_strip("plague")
    victim.affect_strip("poison")
    victim.affect_strip("blindness")
    victim.affect_strip("sleep")
    victim.affect_strip("curse")
    victim.hit = victim.max_hit
    victim.mana = victim.max_mana
    victim.move = victim.max_move
    fight.update_pos(victim)
    act("$n has restored you.", ch, None, victim, merc.TO_VICT)
    buf = "$N restored %s", (victim.short_descr if victim.is_npc() else victim.name)
    handler_game.wiznet(buf, ch, None, merc.WIZ_RESTORE, merc.WIZ_SECURE, ch.trust)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('restore', do_restore, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
