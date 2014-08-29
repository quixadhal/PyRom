import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


def do_freeze(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Freeze whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    if victim.trust >= ch.trust:
        ch.send("You failed.\n")
        return
    if victim.act.is_set(merc.PLR_FREEZE):
        victim.act.rem_bit(merc.PLR_FREEZE)
        victim.send("You can play again.\n")
        ch.send("FREEZE removed.\n")
        handler_game.wiznet("$N thaws %s." % victim.name, ch, None, merc.WIZ_PENALTIES, merc.WIZ_SECURE, 0)
    else:
        state_checks.SET_BIT(victim.act, merc.PLR_FREEZE)
        victim.send("You can't do ANYthing!\n")
        ch.send("FREEZE set.\n")
        handler_game.wiznet("$N puts %s in the deep freeze." % victim.name, ch, None, merc.WIZ_PENALTIES,
                            merc.WIZ_SECURE, 0)

    victim.save(force=True)
    return


interp.register_command(interp.cmd_type('freeze', do_freeze, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
